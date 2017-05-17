from django.shortcuts import render
from .models import Issue
from taiga.timelogs.models import Timelog
from .forms import AddIssueForm
from django.views.decorators.csrf import csrf_protect


@csrf_protect
def issues_list(request):
    issues_page_data = {}
    iss_list = Issue.objects.all()
    add_issue_form = AddIssueForm
    issues_page_data['title'] = "Issues list"
    issues_page_data['issues_list'] = iss_list
    issues_page_data['add_issue_form'] = add_issue_form
    return render(request, "issues/issues_list.html", issues_page_data)


def issue_details(request, issue_id):
    issue_page_data = {}

    iss_details = Issue.objects.get(id=issue_id)
    issue_page_data['issue_details'] = iss_details

    issue_page_data['title'] = 'Issue "' + iss_details.subject + '"'

    return render(request, "issues/issue_details.html", issue_page_data)


def add_issue(request):
    pass


def timelogs_report(request, issue_id):
    user_id = request.GET.get('user_id')
    from_date = request.GET.get('from')
    till_date = request.GET.get('till')
    pass
