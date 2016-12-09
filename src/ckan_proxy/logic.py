from memoize import memoize, delete_memoized
from ckanapi import NotFound

from .util import ckan_connection_for_admin, ckan_connection_for_user


def organization_list():
    """ Returns a list of all of the publishing organisation's names """
    conn = ckan_connection_for_admin()
    return conn.action.organization_list()

@memoize(timeout=60)
def organization_list_for_user(user):
    """ Returns a list of organization objects where this user
        has permissions """
    conn = ckan_connection_for_user(user.apikey)
    return conn.action.organization_list_for_user()

@memoize(timeout=60)
def datasets_for_user(user, search_term="*:*", limit=10, offset=0):
    orgs = organization_list_for_user(user)
    if orgs == []:
        return None

    fq_string = " OR ".join(
        ["organization:" + org.get('name') for org in orgs]
    )
    conn = ckan_connection_for_user(user.apikey)
    return conn.action.package_search(
        q=search_term,
        fq="({})".format(fq_string),
        facet="false",
        rows=limit,
        start=offset,
        sort="metadata_modified desc"
    )

def show_dataset(name):
    # TODO: Use user not admin
    conn = ckan_connection_for_admin()
    try:
        return conn.action.package_show(id=name)
    except NotFound:
        pass
    return None

def clear_cache():
    """ Removes all memoization, we don't necessarily want to clear
        the whole cache, but clearing the dataset cache is a little
        complex
    """
    delete_memoized(organization_list_for_user)
    delete_memoized(datasets_for_user)
