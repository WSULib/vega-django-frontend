
from django.http import HttpResponse
from django.shortcuts import render
import logging

# import Saga Client
from journal.saga import SagaClient

# Get an instance of a logger
logger = logging.getLogger(__name__)

# instantiate saga handle
saga_handle = SagaClient(host='127.0.0.1', port=4000, dataset='tronic--pub')


def index(request):

	# groq query for venue information
	venue_qs = '''*[_type == "venue"]{
		...,
		frontPageImage{
			asset->{url}
		},
		logo{
			asset->{url}
		}
	}'''
	venue = saga_handle.groq_query(venue_qs)
	venue = venue['result'][0]
	logger.debug(venue)

	# return
	return render(request, 'index.html', {
			'venue':venue
		})