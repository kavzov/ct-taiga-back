from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Wiki
from .forms import WikiForm
from taiga.utils import valid_id, send_err_msg, user_project_perms, project_permission_required
from taiga.projects.models import Project
from markdownx.utils import markdownify


@valid_id
def wiki_details(request, wiki_id):
    """
    Wiki details
    """
    template = 'wiki/wiki_details.html'
    wiki = Wiki.objects.get(pk=wiki_id)
    wiki_content = markdownify(wiki.content)
    project = Project.objects.get(pk=wiki.project_id)
    user_perms = user_project_perms(request.user.id, project.id)

    args = {
        'title': 'Wiki: ' + wiki.title,
        'wiki': wiki,
        'wiki_content': wiki_content,
        'user_perms': user_perms,
    }

    return render(request, template, args)


def wiki_list(request, project_id):
    pass


@valid_id
@project_permission_required('wiki.add_wiki', '/wiki/')
def add_wiki(request, project_id=None):
    template = 'wiki/edit_wiki.html'
    form = WikiForm

    if request.POST:
        form = WikiForm(request.POST)
        if form.is_valid():
            wiki = Wiki(title=request.POST.get('title'), content=request.POST.get('text'), project_id=request.POST.get('project_id'))
            wiki.save()
            messages.success(request, 'Wiki added')
            return redirect('/projects/' + str(project_id))
        else:
            send_err_msg(request, form)
            return render(request, template, {'form': form})

    args = {
        'form': form,
        'project_id': project_id,
    }

    return render(request, template, args)


# TODO error with update "null value in column "created_date" violates not-null constraint"
@valid_id
@project_permission_required('wiki.change_wiki', '/wikis/')
def edit_wiki(request, wiki_id):
    template = 'wiki/edit_wiki.html'
    wiki = Wiki.objects.get(pk=wiki_id)
    project = Project.objects.get(pk=wiki.project_id)

    if request.POST:
        form = WikiForm(request.POST)
        if form.is_valid():
            wiki = Wiki(id=wiki_id, title=request.POST.get('title'), content=request.POST.get('text'), project_id=request.POST.get('project_id'))
            wiki.save()
            messages.success(request, 'Wiki added')
            return redirect('/projects/' + str(project.id))
        else:
            send_err_msg(request, form)
            return render(request, template, {'form': form})

    args = {
        'wiki': wiki,
        'form': WikiForm(initial={
            'title': wiki.title,
            'text': wiki.content,
        }),
        'project_id': project.id,
    }

    return render(request, template, args)


def delete_wiki(request, wiki_id):
    pass
