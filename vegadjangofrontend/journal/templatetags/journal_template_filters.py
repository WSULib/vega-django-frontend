
import logging
from django import template
from django.conf import settings

register = template.Library()

# Get an instance of a logger
logger = logging.getLogger(__name__)


@register.filter(name='get')
def get(d, k):

	'''
	Provide dictionary like filter
	'''

	return d.get(k, None)