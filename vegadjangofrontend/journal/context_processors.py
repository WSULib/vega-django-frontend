from django.conf import settings
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

def venue_info(request):
    """
    Get venue information for each request
    """

    # groq query for venue information
    venue_qs = """*[_type == "venue"]{
        ...,
        frontPageImage{
            asset->{url}
        },
        logo{
            asset->{url}
        }
    }"""
    venue = saga_handle.groq_query(venue_qs).get('result', [None])[0]

    return {
        'VENUE': venue
    }