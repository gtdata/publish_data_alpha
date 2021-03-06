from django.conf.urls import url
from django.contrib.auth.decorators import login_required

import datasets.views as v


urlpatterns = [
    url(r'^new$',
        login_required(v.new_dataset),
        name='new_dataset'),

    url(r'^edit/(?P<dataset_name>[\w-]+)$',
        login_required(v.edit_full_dataset),
        name='edit_full_dataset'),

    # url(r'^(?P<dataset_name>[\w-]+)/organisation$',
    #     login_required(v.edit_organisation),
    #     name='edit_dataset_organisation'),

    url(r'^(?P<dataset_name>[\w-]+)/licence$',
        login_required(v.edit_licence),
        name='edit_dataset_licence'),

    url(r'^(?P<dataset_name>[\w-]+)/location$',
        login_required(v.edit_location),
        name='edit_dataset_location'),

    url(r'^(?P<dataset_name>[\w-]+)/frequency$',
        login_required(v.edit_frequency),
        name='edit_dataset_frequency'),

    # Data file URLs
    url(r'^(?P<dataset_name>[\w-]+)/addfile/(?P<datafile_id>[a-z\d-]+)?$',
        login_required(v.edit_addfile),
        name='edit_dataset_addfile'),

    url(r'^(?P<dataset_name>[\w-]+)/addfile_weekly/(?P<datafile_id>[a-z\d-]+)?$',
        login_required(v.edit_addfile_weekly),
        name='edit_dataset_addfile_weekly'),

    url(r'^(?P<dataset_name>[\w-]+)/addfile_monthly/(?P<datafile_id>[a-z\d-]+)?$',
        login_required(v.edit_addfile_monthly),
        name='edit_dataset_addfile_monthly'),

    url(r'^(?P<dataset_name>[\w-]+)/addfile_quarterly/(?P<datafile_id>[a-z\d-]+)?$',
        login_required(v.edit_addfile_quarterly),
        name='edit_dataset_addfile_quarterly'),

    url(r'^(?P<dataset_name>[\w-]+)/addfile_annually/(?P<datafile_id>[a-z\d-]+)?$',
        login_required(v.edit_addfile_annually),
        name='edit_dataset_addfile_annually'),

    url(r'^(?P<dataset_name>[\w-]+)/deletefile/(?P<datafile_id>[a-z\d-]+)$',
        login_required(v.edit_deletefile),
        name='edit_dataset_deletefile'),

    url(r'^(?P<dataset_name>[\w-]+)/confirmdeletefile/(?P<datafile_id>[a-z\d-]+)$',
        login_required(v.edit_confirmdeletefile),
        name='edit_dataset_confirmdeletefile'),

    url(r'^(?P<dataset_name>[\w-]+)/files$',
        login_required(v.edit_files),
        name='edit_dataset_files'),

    # Documentation URLs
    url(r'^(?P<dataset_name>[\w-]+)/adddoc/(?P<datafile_id>[a-z\d-]+)?$$',
        login_required(v.edit_add_doc),
        name='edit_dataset_adddoc'),

    url(r'^(?P<dataset_name>[\w-]+)/documents$',
        login_required(v.edit_documents),
        name='edit_dataset_documents'),

    url(r'^(?P<dataset_name>[\w-]+)/publish$',
        login_required(v.publish_dataset),
        name='publish_dataset'),

    url(r'^(?P<dataset_name>[\w-]+)/edit$',
        login_required(v.edit_dataset_details),
        name='edit_dataset'),

    url(r'^(?P<dataset_name>[\w-]+)/confirmdelete$',
        login_required(v.confirm_delete_dataset),
        name='confirm_delete_dataset'),

    url(r'^(?P<dataset_name>[\w-]+)/delete$',
        login_required(v.delete_dataset),
        name='delete_dataset'),
]
