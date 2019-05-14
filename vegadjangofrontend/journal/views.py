
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

	# groq query for issues information
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

	# groq query for single issue information
	issue_qs = '''*[_type == "issue" && _id == "%(issue_id)s"]{
		...,
		coverImage{
		  asset->{url}
		},
		content
	  }''' % {'issue_id':issue_id}
	issue = saga_handle.groq_query(issue_qs).get('result',[None])[0]

	# loop through sections, retrieve articles
	for section in issue.get('content',[]):

		# get article ids
		article_ids = [article.get('_ref', None) for article in section.get('articles',[]) if
                       article.get('_ref', None) is not None]
		logger.debug(article_ids)

		# groq query for article
		article_qs = '''*[_type == 'article' && _id in %(article_ids)s]{
          _id,
          title,
          _createdAt,
          authors[]{
            name,
          },
            mainImage{
            asset->{url}
          }
        }''' % {'article_ids':article_ids}
		section_articles = saga_handle.groq_query(article_qs).get('result',[None])

		# append to sections
		section['articles_ref'] = section_articles


	# return
	return render(request, 'issue.html', {
			'issue':issue,
			'page_title':'Issue'
		})



def article(request, issue_id, article_id):

	logger.debug('retrieving article id: %s' % article_id)

	# groq query for article content
	article_qs = '''*[_id == "%(article_id)s"]{
        ...,
        authors[]{
          name,
          profileImage{
            ...,
            asset->{url}
          }
        },
        content[]{
          ...,
          asset->{url}
        },
        mainImage{
          asset->{url}
        }
    }''' % {'article_id':article_id}
	article = saga_handle.groq_query(article_qs).get('result',[])[0]

	# return
	return render(request, 'article.html', {
			'article':article,
			'page_title':'Article'
		})











