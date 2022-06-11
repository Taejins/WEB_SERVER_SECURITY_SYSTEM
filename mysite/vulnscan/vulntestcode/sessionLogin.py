import sys
import requests
from bs4 import BeautifulSoup as bs


def access_check(url):
    req = requests.get(url)
    if not req.ok:
        return "invalid_url"

    if url == req.url:
        return "ok"
    else : 
        return session_data(req.url)

def session_data(login_url):
    data = {}
    data_no_val = {}

    req = requests.get(login_url)
    html = req.text
    soup = bs(html, "html.parser")
    find_form = soup.find_all("form")

    for form in find_form:
        
        if form.find("input",{"type":"password"}) : 
            act_url = form["action"]        
            for input in form.find_all("input"):
                try :
                    if input.get('type') == 'submit':
                        continue
                    if input.get('value'):
                        data[input['name']] = input['value']
                    else : 
                        data_no_val[input['name']] = ""
                except:
                    pass
            for btn in form.find_all("button",{"type":"submit"}):
                if btn.get('value'): data[btn['name']] = btn['value']

    return {'data': data , 'data_no_val':data_no_val, 'act_url':act_url}

def session_check(url, act_url, data):
    
    if not "http" in act_url :
        split_url = url.split('/')
        ori_url = f"{split_url[0]}//{split_url[2]}"
        act_url = ori_url+"/"+act_url

    with requests.Session() as s:    
        log_req = s.post(act_url, data=data)
        req = s.get(url)
        if url == req.url : 
            return True
        else:
            return False
    
