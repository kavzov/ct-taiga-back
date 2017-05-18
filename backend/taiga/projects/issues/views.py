from django.shortcuts import render
from .models import Issue
from taiga.users.models import User
from taiga.timelogs.models import Timelog
from .forms import AddIssueForm
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def issues_list(request):
    issues_page_data = {}
    iss_list = Issue.objects.all()
    add_issue_form = AddIssueForm
    issues_page_data['title'] = "Issues"
    issues_page_data['issues_list'] = iss_list
    issues_page_data['add_issue_form'] = add_issue_form
    return render(request, "issues/issues_list.html", issues_page_data)


def issue_details(request, issue_id):
    args = {}

    users = User.objects.all()
    iss_details = Issue.objects.get(id=issue_id)

    args['title'] = 'Issue "' + iss_details.subject + '"'
    args['users'] = users
    args['issue_details'] = iss_details

    return render(request, "issues/issue_details.html", args)


def add_issue(request):
    pass


def timelogs_report(request, issue_id):
    user_id = request.GET.get('user_id')
    from_date = request.GET.get('from')
    till_date = request.GET.get('till')
    pass
