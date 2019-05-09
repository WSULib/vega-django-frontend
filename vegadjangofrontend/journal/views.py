
from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
import logging

# import Saga Client
from journal.saga import SagaClient

# Get an instance of a logger
logger = logging.getLogger(__name__)

# instantiate saga handle
saga_handle = SagaClient(
	host=settings.SAGA_HOST,
	port=settings.SAGA_PORT,
	dataset=settings.SAGA_DATASET)


def index(request):

	'''
	Route for Venue/Journal
	'''

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
	venue = saga_handle.groq_query(venue_qs).get('result',[None])[0]

	# return
	return render(request, 'index.html', {
			'venue':venue,
			'page_title':'Home'
		})


def issues(request):

	# groq query for venue information
	issues_qs = '''*[_type == "issue"]{
		...,
		coverImage{
		  asset->{url}
		}
	  }'''
	issues = saga_handle.groq_query(issues_qs).get('result',[])

	# return
	return render(request, 'issues.html', {
			'issues':issues,
			'page_title':'Issues'
		})


def issue(request, issue_id):

	logger.debug('retrieving issue id: %s' % issue_id)

	# groq query for venue information
	issue_qs = '''*[_type == "issue" && _id == "%(issue_id)s"]{
		...,
		coverImage{
		  asset->{url}
		},
		content
	  }''' % {'issue_id':issue_id}
	issue = saga_handle.groq_query(issue_qs).get('result',[None])[0]

	# return
	return render(request, 'issue.html', {
			'issue':issue,
			'page_title':'Issues'
		})