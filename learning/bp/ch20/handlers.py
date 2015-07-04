# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'


class Handler:
    def __init__(self):
        pass

    def callback(self, prefix, name, *args):
        method = getattr(self, prefix + name, None)
        if hasattr(method, '__call__'):
            return method(*args)

    def start(self, name):
        # sys.stderr.write('start_' + name + '\n')
        self.callback('start_', name)

    def end(self, name):
        # sys.stderr.write('end_' + name + '\n')
        self.callback('end_', name)

    def feed(self, data):
        pass

    def sub(self, name):
        def substitution(match):
            result = self.callback('sub_', name, match)
            if result is None:
                match.group(0)
            return result

        return substitution


class HTMLRender(Handler):
    """
    render to html
    """

    def start_document(self):
        print '<html><head><title>...</title><head><body>'

    def end_document(self):
        print '</body></html>'

    def start_paragraph(self):
        print '<p>'

    def end_paragraph(self):
        print '</p>'

    def start_heading(self):
        print '<h2>'

    def end_heading(self):
        print '</h2>'

    def start_list(self):
        print '<ul>'

    def end_list(self):
        print '</ul>'

    def start_listitem(self):
        print '<li>'

    def end_listitem(self):
        print '</li>'

    def start_title(self):
        print '<h1>'

    def end_title(self):
        print '</h1>'

    def sub_emphasis(self, match):
        return '<em>%s</em>' % match.group(1)

    def sub_code(self, match):
        return '<code>%s</code>' % match.group(1)

    def sub_heading(self, match):
        hx = str(len(match.group(1)))
        text = match.group(2)
        return '<h%s>%s</h%s>' % (hx, text, hx)

    def sub_url(self, match):
        return '<a href="%s">%s</a>' % (match.group(1), match.group(1))

    def sub_mail(self, match):
        return '<a href="mailto:%s>%s</a>"' % (match.group(1), match.group(1))

    def feed(self, data):
        print data























