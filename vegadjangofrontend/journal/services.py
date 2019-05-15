
from django.conf import settings
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)



class Blocks2HTML(object):

    """Class to handle rendering of block content in Saga in HTML"""


    def __init__(self, blocks):

        self.blocks = blocks
        self.rendered_blocks = []


    def render(self):

        # loop through blocks
        for block in self.blocks:

            rendered_block = self.render_block(block)

            if rendered_block is not None:
                self.rendered_blocks.append(rendered_block)

        # return
        return self.rendered_blocks


    def render_block(self, block):

        inner_html = []

        # loop through children
        for child in block.get('children',[]):

            # get text
            text = child.get('text', None)

            # convert
            text = text.replace('\n', '<br>')

            # check for stylings
            marks = child.get('marks',[None])
            if len(marks) > 0:
                style = marks[0]
                if style in ['strong','em','code']:
                    text = '<%s>%s</%s>' % (style,text,style)

            # append to html
            inner_html.append(text)

        # close tag
        html = '<p>%s</p>' % ''.join(inner_html)

        # return
        return html






