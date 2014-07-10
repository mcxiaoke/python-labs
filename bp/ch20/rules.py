# -*- coding: UTF-8 -*-
__author__ = 'mcxiaoke'


class Rule:
    def __init__(self):
        pass

    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block)
        handler.end(self.type)
        return True

    def condition(self, block):
        return False


class HeadingRule(Rule):
    """
    heading is a line < 70 chars, not end with :
    """
    type = 'heading'

    @classmethod
    def condition2(cls, block):
        return not '\n' in block \
               and len(block) < 70 \
               and not block[-1] == ':'

    def condition(self, block):
        return not '\n' in block and len(block) <= 70 and not block[-1] == ':'


class TitleRule(Rule):
    """
    title is the first block
    """
    type = 'title'
    first = True

    def condition(self, block):
        if not self.first:
            return False
        self.first = False
        return HeadingRule.condition2(block)


class ListItemRule(Rule):
    """
    list item start with '-', and - will be deleted
    """
    type = 'listitem'

    @classmethod
    def condition2(cls, block):
        return block[0] == '-'

    def condition(self, block):
        return block[0] == '-'

    def action(self, block, handler):
        handler.start(self.type)
        handler.feed(block[1:].strip())
        handler.end(self.type)
        return True


class ListRule(Rule):
    """
    list, continuous list items
    """
    type = 'list'
    inside = False

    def condition(self, block):
        return True

    def action(self, block, handler):
        if not self.inside and ListItemRule.condition2(block):
            handler.start(self.type)
            self.inside = True
        elif self.inside and not ListItemRule.condition2(block):
            handler.end(self.type)
            self.inside = False
        return False


class ParagraphRule(Rule):
    """
    paragraph is default
    """
    type = 'paragraph'

    def condition(self, block):
        return True