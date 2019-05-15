
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

                # handle known type
                if style in ['strong','em','code']:
                    text = '<%s>%s</%s>' % (style,text,style)

                # elif string, assume key
                elif type(style) == str:

                    # retrieve key
                    for markDef in block.get('markDefs',[]):
                        if style == markDef.get('_key',''):

                            # handle hrefs
                            if 'href' in markDef.keys():
                                text = '<a href="%s">%s</a>' % (markDef.get('href'), text)

            # append to html
            inner_html.append(text)

        # close tag
        html = '<p>%s</p>' % ''.join(inner_html)

        # return
        return html






