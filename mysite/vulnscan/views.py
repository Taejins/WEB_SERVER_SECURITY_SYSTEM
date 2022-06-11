from asyncio import base_tasks
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from vulnscan.vulntestcode import sessionLogin
from .tasks import vuln_scan
from django_celery_results.models import TaskResult
import json
import base64

# Create your views here.
def index(request):
    latest_question_list = "HI"
    context = {'latest_question_list': latest_question_list}
    return render(request, 'vulnscan/index.html', context)


def scan_start(request):
    return render(request, 'vulnscan/scan_start.html')

def scan_work(request):

    input = base64.b64decode(request.POST['content'])
    in_to_json = json.loads(input)

    task = vuln_scan.delay(in_to_json)
    return render(request, 'vulnscan/scan_work.html', {'task_id': task.task_id})

def scan_end(request, task_id):
    info = TaskResult.objects.get(task_id=task_id)
    print(info.result)
    return render(request, 'vulnscan/scan_end.html', {"info": info.result, })

def vuln_info(request):
    return render(request, 'vulnscan/vuln_info.html')

# jsonResponse

def url_access(request):
    result = sessionLogin.access_check(request.POST['url'])
    return JsonResponse({"status":result}, status=200) 

def session_test(request):
    input_data = request.POST['content']
    json_dic = json.loads(input_data)
    result = sessionLogin.session_check(json_dic['url'],json_dic['act_url'],json_dic['data'])
    return JsonResponse({"status":result}, status=200)