from sre_constants import SUCCESS
from celery import shared_task
from celery_progress.backend import ProgressRecorder
from click import option
import requests
from .vulntestcode import options_method, default_admin, dir_indexing, pred_location, Server_info, file_download, sqli, xss, ssii
from time import sleep, time
import json, base64

@shared_task(bind=True)
def vuln_scan(self, content):
    progress_recorder = ProgressRecorder(self)
    url = content['url']
    split_url = url.split('/')
    base_url = f"{split_url[0]}//{split_url[2]}"
    act_url = url
    data = {}

    if "act_url" in content:
        act_url = content['act_url']
        data = content['data']
    
        if not "http" in act_url :
            act_url = base_url+"/"+act_url
    total = {}
    global open_cnt
    global input_cnt
    open_cnt, input_cnt= 0,0
    time_taken = time()

    with requests.Session() as s:    
        s.post(act_url, data=data)

        total['method'] = method_format("불필요한 메소드 점검", options_method.unnecessary_method, url, s, progress_recorder, 5, "open")
        total['indexing'] = method_format("디렉토리 인덱싱 기능 점검",dir_indexing.dir_indexing, url, s, progress_recorder, 10, "open")
        total['admin'] = method_format("기본 관리자 위치 점검",default_admin.default_admin, url, s, progress_recorder, 15, "open")
        total['pred_loc'] = method_format("예측가능한 위치 점검",pred_location.pred_location, url, s, progress_recorder, 20, "open")
        total['server_header'] = method_format("서버 정보 노출 점검(헤더)", Server_info.use_header, url, s, progress_recorder, 25, "open")
        total['server_error'] = method_format("서버 정보 노출 점검(오류 페이지)",Server_info.use_errer_page, url, s, progress_recorder, 30, "open")
        total['file_download'] = method_format("파일 다운로드 취약점 점검",file_download.file_download, url, s, progress_recorder, 40, "open")
        total['sqli'] = method_format_secure("SQL Injection 취약점 점검", sqli.sqli_scan, url, s, progress_recorder, 60, "input")
        total['xss'] = method_format_secure("Cross Site Script 취약점 점검",xss.reflected_scan_xss, url, s, progress_recorder, 70, "input")
        total['ssii'] = method_format_secure("SSI Injection 취약점 점검", ssii.SSI_Injection, url, s, progress_recorder, 85, "input")

        total['open_cnt']=open_cnt
        total['input_cnt']=input_cnt
        total['url'] = url
        total['time_taken'] = int(time()-time_taken)
        sleep(2)
        
    return total

def method_format(name, func, url, s, pr, pr_n, type):
    global open_cnt, input_cnt
    result = func(s,url)
    status = "탐지" if result else "미탐지"
    prog_json = json.dumps({"name":name, "status":status, "content":f"{result}"})
    pr.set_progress(pr_n, 100, prog_json)
    if result :
        sleep(2) 
        if type == "open": open_cnt+=1
        else : input_cnt+=1
    else :
        sleep(1)
    return result
    # 기존 코드 반복을 함수로 모듈화(아래는 예시)
    # result = options_method.unnecessary_method(s, url)
    # total['method'] = result
    # progress_recorder.set_progress(3, 10, f'{result}')

def method_format_secure(name, func, url, s, pr, pr_n, type):
    global open_cnt, input_cnt
    result = func(s,url)
    status = "탐지" if result else "미탐지"
    prog_json = json.dumps({"name":name, "status":status, "content":f"{result}"})
    pr.set_progress(pr_n, 100, prog_json)
    sec_result = base64.b64encode(str(result).encode('utf-8'))
    if result :
        sleep(2)
        if type == "open": open_cnt+=1
        else : input_cnt+=1
        return sec_result.decode('utf-8')
    else :
        sleep(1)
        return result