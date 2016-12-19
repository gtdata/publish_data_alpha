import math
import pytz

from dateutil.parser import parse as parse_date
from django.utils.translation import ugettext as _

from drafts.models import Dataset
from ckan_proxy.logic import datasets_for_user

utc = pytz.UTC


def dataset_list(user, page=1, filter_query=None):
    """
    For the given user returns a tuple containing total number of datasets
    both draft and published, and the 20 most recent.
    """
    per_page = 20
    max_fetch = per_page * page

    # TODO: This should be organisation specific

    # Find relevant datasets from the drafts database
    count = Dataset.objects.count()

    drafts = Dataset.objects
    if filter_query:
        drafts = drafts.filter(title__icontains=filter_query)
    drafts = drafts.all().order_by("-last_edit_date")[0:max_fetch]

    for d in drafts:
        d.last_edit_date = d.last_edit_date.replace(tzinfo=utc)
        d.status = _("draft")

    # Find relevant datasets from CKAN
    results = datasets_for_user(
        user,
        search_term=filter_query or "*:*",
        offset=0,
        limit=max_fetch
    )

    datasets = []
    for dataset in results['results']:
        dataset['metadata_modified'] = \
            parse_date(dataset['metadata_modified']).replace(tzinfo=utc)
        dataset['status'] = _('published')
        datasets.append(dataset)

    def get_key(obj):
        if isinstance(obj, dict):
            return obj['metadata_modified']
        return obj.last_edit_date

    resultset = sorted(list(drafts) + datasets, key=get_key, reverse=True)

    total = results['count'] + count
    page_count = math.ceil(float(total) / per_page)

    offset = (page * per_page) - per_page
    return (total, page_count, resultset[offset:offset+per_page],)
