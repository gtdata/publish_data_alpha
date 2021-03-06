from datetime import datetime

from django.contrib import messages
from django.http import (HttpResponseForbidden,
                         HttpResponseRedirect)
from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.utils.translation import ugettext as _
from django.conf import settings


import datasets.forms as f
from datasets.auth import user_can_edit_dataset, user_can_edit_datafile
from datasets.logic import organisations_for_user, publish
from datasets.models import Dataset, Datafile
from datasets.search import delete_dataset as unindex_dataset
from runtime_config.audit import audit_log


def _set_flow_state(request):
    ''' If the query string contains a 'state' string then
    we will set the current state, otherwise we will leave
    it unchanged '''
    return_to = request.GET.get('state')
    if return_to == 'edit':
        request.session['flow-state'] = 'editing'
    elif return_to == 'check':
        request.session['flow-state'] = 'checking'


def new_dataset(request):
    # Reset the flow state
    request.session['flow-state'] = None

    form = f.DatasetForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            try:
                user_org = organisations_for_user(request.user)[0]
            except:
                user_org = None
            obj = Dataset.objects.create(
                title=form.cleaned_data['title'],
                description=form.cleaned_data['description'],
                summary=form.cleaned_data['summary'],
                creator=request.user,
                owner=request.user,  # Initial owner = creator
                organisation=user_org
            )

            audit_log(
                'new-dataset',
                '{} created a new dataset "{}"'.format(request.user.username,
                                                       obj.title),
                data={
                    'dataset_name': obj.name,
                    'dataset_title': obj.title,
                    'user': request.user.username
                },
                external_key=obj.name
            )

            return HttpResponseRedirect(
                reverse('edit_dataset_licence', args=[obj.name])
            )

    return render(request, "datasets/edit_title.html", {
        "form": form,
        "dataset": {},
    })


def confirm_delete_dataset(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    if dataset.published and not request.user.is_staff:
        return HttpResponseForbidden()

    return _edit_publish_dataset(
        request,
        dataset,
        'editing',
        deleting=True
    )


def delete_dataset(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    if dataset.published and not request.user.is_staff:
        return HttpResponseForbidden()

    audit_log(
        'delete-dataset',
        '{} deleted "{}"'.format(request.user.username, dataset.title),
        data={
            'dataset_name': dataset.name,
            'dataset_title': dataset.title,
            'user': request.user.username
        },
        external_key=dataset.name
    )

    unindex_dataset(dataset)
    dataset.delete()

    msg = '<h1 class="heading-medium">' + \
          (_('The dataset ‘%(title)s’ has been deleted') %
           {'title': dataset.title}) + '</h1>'

    messages.add_message(
        request,
        messages.INFO,
        msg,
        extra_tags='confirm-delete-box'
    )

    return HttpResponseRedirect(
        reverse('manage_my_data')
    )


def edit_dataset_details(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    _set_flow_state(request)

    form = f.EditDatasetForm(request.POST or None, instance=dataset)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            return _redirect_to(request, 'edit_dataset_licence', [obj.name])

    return render(request, 'datasets/edit_title.html', {
        'form': form,
        'dataset': dataset,
    })


# def edit_organisation(request, dataset_name):
#     dataset = get_object_or_404(Dataset, name=dataset_name)

#     if not user_can_edit_dataset(request.user, dataset):
#         return HttpResponseForbidden()

#     _set_flow_state(request)

#     organisations = organisations_for_user(request.user)
#     if len(organisations) == 1:
#         dataset.organisation = organisations[0]
#         dataset.save()
#         return _redirect_to(request, 'edit_dataset_licence', [dataset.name])

#     form = f.OrganisationForm(request.POST or None, instance=dataset)
#     form.fields["organisation"].queryset = organisations_for_user(request.user)

#     if request.method == 'POST':
#         if form.is_valid():
#             obj = form.save()
#             return _redirect_to(request, 'edit_dataset_licence', [obj.name])

#     return render(request, "datasets/edit_organisation.html", {
#         'form': form,
#         'dataset': dataset,
#         'organisations': organisations,
#     })


def edit_licence(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    _set_flow_state(request)

    form = f.LicenceForm(request.POST or None, instance=dataset)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            return _redirect_to(request, 'edit_dataset_location', [obj.name])

    return render(request, "datasets/edit_licence.html", {
        'form': form,
        'dataset': dataset,
    })


def edit_location(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    _set_flow_state(request)

    form = f.LocationForm(request.POST or None, instance=dataset)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            return _redirect_to(request, 'edit_dataset_frequency', [obj.name])

    return render(request, "datasets/edit_location.html", {
        'form': form,
        'dataset': dataset,
    })


def edit_frequency(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    _set_flow_state(request)

    form = f.FrequencyForm(request.POST or None, instance=dataset)
    if request.method == 'POST':
        if form.is_valid():
            obj = form.save()
            url = _frequency_addfile_viewname(obj)
            return _redirect_to(request, url, [obj.name])

    return render(request, "datasets/edit_frequency.html", {
        'form': form,
        'dataset': dataset,
    })


def _file_already_added(dataset, name, url):
    for file in dataset.files.all():
        if file.url == url and file.name == name:
            return True


def edit_addfile(request, dataset_name, datafile_id=None):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    datafile = get_object_or_404(Datafile, id=datafile_id) \
        if datafile_id else None
    form = f.FileForm(request.POST or None, instance=datafile)

    _set_flow_state(request)

    if request.method == 'POST':
        if form.is_valid():
            data = dict(**form.cleaned_data)
            if datafile:
                form.save()
            else:
                if not _file_already_added(dataset, data['name'], data['url']):
                    data['dataset'] = dataset
                    if 'size' in data:
                        data['size'] = data['size']
                    obj = Datafile.objects.create(**data)
                    obj.save()

            return HttpResponseRedirect(
                reverse('edit_dataset_files', args=[dataset_name])
            )

    return render(request, 'datasets/edit_addfile.html', {
        'is_first_file': len(dataset.files.filter(is_documentation=True)) == 0,
        'form': form,
        'dataset': dataset,
        'datafile_id': datafile_id or '',
    })


def edit_deletefile(request, dataset_name, datafile_id):
    datafile = get_object_or_404(Datafile, id=datafile_id)
    next_view = 'edit_dataset_documents' if datafile.is_documentation \
        else 'edit_dataset_files'

    if not user_can_edit_datafile(request.user, datafile):
        return HttpResponseForbidden()

    datafile.delete()

    msg = _('Your link ‘{}’ has been deleted'.format(datafile.name))
    messages.add_message(
        request,
        messages.INFO,
        msg,
        extra_tags='confirm-delete-box'
    )

    return HttpResponseRedirect(
        reverse(next_view, args=[dataset_name])
    )


def edit_confirmdeletefile(request, dataset_name, datafile_id):
    dataset = get_object_or_404(Dataset, name=dataset_name)
    datafile = get_object_or_404(Datafile, id=datafile_id) \
        if datafile_id else None
    url = _frequency_addfile_viewname(dataset)
    template = 'datasets/show_docs.html' if datafile.is_documentation \
        else 'datasets/show_files.html'

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    _set_flow_state(request)

    files = [f for f in dataset.files.all() if not f.is_documentation]

    return render(request, template, {
        'addfile_viewname': url,
        'dataset': dataset,
        'files': files,
        'file_to_delete_id': datafile_id,
        'file_to_delete_title': datafile.name,
    })


def _addfile(request, dataset_name, form_class, template, datafile_id=None):
    ''' Handler function for all of the 'period' datafile additions
    that vary only by template and form class '''

    dataset = get_object_or_404(Dataset, name=dataset_name)

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    datafile = get_object_or_404(Datafile, id=datafile_id) \
        if datafile_id else None

    form = form_class(request.POST or None, instance=datafile)
    _set_flow_state(request)

    if request.method == 'POST':
        if form.is_valid():
            data = dict(**form.cleaned_data)
            if datafile:
                data['dataset'] = dataset
                for k, v in data.items():
                    setattr(datafile, k, v)
                datafile.save()
            else:
                if not _file_already_added(dataset, data['name'], data['url']):
                    data['dataset'] = dataset
                    obj = Datafile.objects.create(**data)
                    obj.save()

            return HttpResponseRedirect(
                reverse('edit_dataset_files', args=[dataset.name])
            )

    return render(request, "datasets/edit_addfile_{}.html".format(template), {
        'is_first_file': len(dataset.files.all()) == 0,
        'form': form,
        'dataset': dataset,
        'datafile_id': datafile.id if datafile else '',
    })


def edit_addfile_weekly(request, dataset_name, datafile_id=None):
    return _addfile(
        request, dataset_name, f.WeeklyFileForm, 'week', datafile_id
    )


def edit_addfile_monthly(request, dataset_name, datafile_id=None):
    return _addfile(
        request, dataset_name, f.MonthlyFileForm, 'month', datafile_id
    )


def edit_addfile_quarterly(request, dataset_name, datafile_id=None):
    return _addfile(
        request, dataset_name, f.QuarterlyFileForm, 'quarter', datafile_id
    )


def edit_addfile_annually(request, dataset_name, datafile_id=None):
    return _addfile(
        request, dataset_name, f.AnnuallyFileForm, 'year', datafile_id
    )


def edit_files(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)
    url = _frequency_addfile_viewname(dataset)

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    _set_flow_state(request)

    files = [f for f in dataset.files.all() if not f.is_documentation]

    return render(request, "datasets/show_files.html", {
        'addfile_viewname': url,
        'dataset': dataset,
        'files': files
    })


def edit_add_doc(request, dataset_name, datafile_id=None):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    datafile = get_object_or_404(Datafile, id=datafile_id) \
        if datafile_id else None
    form = f.FileForm(request.POST or None, instance=datafile)

    _set_flow_state(request)

    if request.method == 'POST':
        if form.is_valid():
            data = dict(**form.cleaned_data)
            if datafile:
                form.save()
            else:
                if not _file_already_added(dataset, data['name'], data['url']):
                    data['dataset'] = dataset
                    data['is_documentation'] = True
                    obj = Datafile.objects.create(**data)
                    obj.save()

            return HttpResponseRedirect(
                reverse('edit_dataset_documents', args=[dataset_name])
            )

    return render(request, "datasets/edit_adddoc.html", {
        'is_first_file': len(dataset.files.filter(is_documentation=True)) == 0,
        'form': form,
        'dataset': dataset,
        'datafile_id': datafile_id or '',
    })


def edit_documents(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    _set_flow_state(request)

    files = [f for f in dataset.files.all() if f.is_documentation]

    return render(request, "datasets/show_docs.html", {
        'dataset': dataset,
        'files': files,
    })


def _edit_publish_dataset(request, dataset, state, deleting=False):
    ''' Handles the editing or publishing of a dataset, where
    the primary difference is just the state that we handle '''

    organisations = organisations_for_user(request.user)

    if request.session.get('flow-state') is None:
        request.session['flow-state'] = state

    new_state = request.session['flow-state']

    organisation = dataset.organisation
    single_organisation = len(organisations) == 1

    if request.method == 'POST':
        from django.forms.models import model_to_dict
        data = model_to_dict(dataset)

        datafile_count = dataset.files.filter(is_documentation=False).count()
        form = f.PublishForm(datafile_count=datafile_count, data=data)
        if form.is_valid():
            if state == 'checking':
                dataset.published = True
                dataset.published_date = datetime.now()

            dataset.save()

            # Determine event message based on state
            msg = '{} edited "{}"'.format(request.user.username, dataset.title)
            if new_state == 'checking':
                msg = '{} published "{}"'.format(
                    request.user.username, dataset.title
                )

            audit_log(
                'edit-dataset' if new_state == 'editing' else 'publish-dataset',
                msg,
                data={
                    'dataset_name': dataset.name,
                    'dataset_title': dataset.title,
                    'user': request.user.username
                },
                external_key=dataset.name
            )

            # Re-publish if we are editing a published dataset
            publish(dataset, request.user)

            result = 'edited' if new_state == 'editing' else 'created'

            if result == 'edited':
                msg = '<h1 class="bold-large">' + \
                      _('Your dataset has been edited') + \
                      '</h1>'
            else:
                msg = '<h1 class="bold-large">' + \
                      _('Your dataset has been published') + \
                      '</h1>'

            msg += '<h2><a href="' + settings.FIND_URL + '/dataset/' + \
                   dataset.name+'">' + _('View it') + '</a></h2>'

            messages.add_message(
                request,
                messages.INFO,
                msg,
                extra_tags='govuk-box-highlight',
            )

            request.session['flow-state'] = None

            return HttpResponseRedirect(
                reverse('manage_my_data')
            )
    else:
        form = f.PublishForm()

    all_files = dataset.files.all()
    datafiles = filter(lambda x: not x.is_documentation, all_files)
    docfiles = filter(lambda x: x.is_documentation, all_files)
    return render(request, "datasets/publish_dataset.html", {
        'deleting': deleting,
        'addfile_viewname': _frequency_addfile_viewname(dataset),
        "dataset": dataset,
        'organisation': organisation,
        'single_organisation': single_organisation,
        'docfiles': list(docfiles),
        'datafiles': list(datafiles),
        'form': form
    })


def edit_full_dataset(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    return _edit_publish_dataset(
        request,
        dataset,
        'editing',
    )


def publish_dataset(request, dataset_name):
    dataset = get_object_or_404(Dataset, name=dataset_name)

    if not user_can_edit_dataset(request.user, dataset):
        return HttpResponseForbidden()

    return _edit_publish_dataset(
        request,
        dataset,
        'checking',
    )


def _frequency_addfile_viewname(dataset):
    frequency = dataset.frequency

    if frequency in ['never', 'daily']:
        url = 'edit_dataset_addfile'
    elif frequency in ['weekly']:
        url = 'edit_dataset_addfile_weekly'
    elif frequency in ['quarterly']:
        url = 'edit_dataset_addfile_quarterly'
    elif frequency in ['monthly']:
        url = 'edit_dataset_addfile_monthly'
    elif frequency in ['annually', 'financial-year']:
        url = 'edit_dataset_addfile_annually'
    else:
        url = 'edit_dataset_addfile'

    return url


def _redirect_to(request, default_url_name, args):
    flow = request.session.get('flow-state', '')
    if flow == 'checking':
        next = 'publish_dataset'
    elif flow == 'editing':
        next = 'edit_full_dataset'
    else:
        next = default_url_name

    return HttpResponseRedirect(
        reverse(next, args=args)
    )
