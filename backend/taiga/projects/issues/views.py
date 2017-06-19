from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Issue
from .forms import IssueForm
from taiga.users.models import User
from taiga.timelogs.models import Timelog
from taiga.projects.models import Project
from taiga.utils import valid_id, send_err_msg, user_project_perms, project_permission_required


def issues_list(request):
    template = 'issues/issues_list.html'
    iss_list = Issue.objects.all()
    args = {
        'title': 'Issues',
        'issues_list': iss_list,
    }

    return render(request, template, args)


@valid_id
def issue_details(request, issue_id):
    template = "issues/issue_details.html"
    args = {}

    # queryset of users who tracked at this issue
    users = User.objects.filter(
        pk__in=[
            timelog.user for timelog in Timelog.objects.filter(issue_id=issue_id).distinct('user')
        ]
    )

    # issue
    issue = Issue.objects.get(id=issue_id)

    # total time duration on this issue
    timelogs = Timelog.objects.all().filter(issue_id=issue_id)
    duration = sum([v['duration'] for v in list(timelogs.values())])

    # users and its durations
    users_durations = {}
    for user in users:
        user_timelogs = timelogs.filter(user=user)
        users_durations[user] = sum([v['duration'] for v in list(user_timelogs.values())])

    args['user_perms'] = user_project_perms(request.user.id, issue.project.id)
    args['title'] = 'Issue "' + issue.subject + '"'
    args['users'] = users
    args['issue_details'] = issue
    args['total_time'] = duration
    args['users_durations'] = users_durations

    return render(request, template, args)


@project_permission_required('issues.add_issue')
def add_issue(request, project_id):
    """
    Create new issue at the project
    """
    template = 'issues/edit_issue.html'
    issue_form = IssueForm

    args = {
        'issue_form': issue_form,
        'project': Project.objects.get(pk=project_id),
        'editing': True,
    }

    if request.POST:
        issue_form = IssueForm(request.POST)
        if issue_form.is_valid():
            i = issue_form.save()
            issue_id = str(i.id)
        else:
            send_err_msg(request, issue_form)
            return render(request, template, args)

        msg = 'Issue &#35;' + issue_id + \
              ': &laquo;' + request.POST.get('subject') + \
              '&raquo; successfully added to project "' + args['project'].name + '"'
        messages.success(request, msg)

        return redirect('/projects/'+project_id)

    return render(request, template, args)


@valid_id
@project_permission_required('issues.change_issue', '/issues/')
def edit_issue(request, issue_id):
    """
    Edit issue
    """
    template = 'issues/edit_issue.html'

    # get issue
    issue = Issue.objects.get(pk=issue_id)

    args = {
        'issue': issue,
        'project': issue.project,
        'editing': True,
        'issue_form': IssueForm(initial={
            'subject': issue.subject,
            'description': issue.description,
            'assigned_to': issue.assigned_to,
            'status': issue.status,
        }),
    }

    if request.POST:
        issue_form = IssueForm(request.POST)
        if issue_form.is_valid():
            issue_form = IssueForm(request.POST, instance=issue)
            issue_form.save()
        else:
            send_err_msg(request, issue_form)
            return render(request, template, args)

        msg = 'Issue &#35;' + issue_id + \
              ': &laquo;' + request.POST.get('subject') + \
              '&raquo; successfully updated'
        messages.success(request, msg)

        return redirect('/issues/'+issue_id)

    return render(request, template, args)


@valid_id
@project_permission_required('issues.delete_issue', '/issues/')
def delete_issue(request, issue_id):
    """
    Delete issue
    """
    issue = Issue.objects.get(pk=issue_id)
    # issue.delete()

    # set success message
    msg = 'Issue &#35;' + issue_id + ': &laquo;' + issue.subject + '&raquo; successfully deleted'

    # send the message
    messages.success(request, msg)

    # go to the project page
    return redirect('/projects/' + str(issue.project.id))
