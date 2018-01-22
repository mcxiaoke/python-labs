from __future__ import unicode_literals
import os

def sanitize_filename(s, restricted=False, is_id=False):
    """Sanitizes a string so it could be used as part of a filename.
    If restricted is set, use a stricter subset of allowed characters.
    Set is_id if this is not an arbitrary string, but an ID that should be kept
    if possible.
    """
    def replace_insane(char):
        if restricted and char in ACCENT_CHARS:
            return ACCENT_CHARS[char]
        if char == '?' or ord(char) < 32 or ord(char) == 127:
            return ''
        elif char == '"':
            return '' if restricted else '\''
        elif char == ':':
            return '_-' if restricted else ' -'
        elif char in '\\/|*<>':
            return '_'
        if restricted and (char in '!&\'()[]{}$;`^,#' or char.isspace()):
            return '_'
        if restricted and ord(char) > 127:
            return '_'
        return char

    # Handle timestamps
    s = re.sub(r'[0-9]+(?::[0-9]+)+', lambda m: m.group(0).replace(':', '_'), s)
    result = ''.join(map(replace_insane, s))
    if not is_id:
        while '__' in result:
            result = result.replace('__', '_')
        result = result.strip('_')
        # Common case of "Foreign band name - English song title"
        if restricted and result.startswith('-_'):
            result = result[2:]
        if result.startswith('-'):
            result = '_' + result[len('-'):]
        result = result.lstrip('.')
        if not result:
            result = '_'
    return result


def sanitize_path(s):
    """Sanitizes and normalizes path on Windows"""
    if sys.platform != 'win32':
        return s
    drive_or_unc, _ = os.path.splitdrive(s)
    if sys.version_info < (2, 7) and not drive_or_unc:
        drive_or_unc, _ = os.path.splitunc(s)
    norm_path = os.path.normpath(remove_start(s, drive_or_unc)).split(os.path.sep)
    if drive_or_unc:
        norm_path.pop(0)
    sanitized_path = [
        path_part if path_part in ['.', '..'] else re.sub(r'(?:[/<>:"\|\\?\*]|[\s.]$)', '#', path_part)
        for path_part in norm_path]
    if drive_or_unc:
        sanitized_path.insert(0, drive_or_unc + os.path.sep)
    return os.path.join(*sanitized_path)

def get_subprocess_encoding():
    if sys.platform == 'win32' and sys.getwindowsversion()[0] >= 5:
        # For subprocess calls, encode with locale encoding
        # Refer to http://stackoverflow.com/a/9951851/35070
        encoding = preferredencoding()
    else:
        encoding = sys.getfilesystemencoding()
    if encoding is None:
        encoding = 'utf-8'
    return encoding