import json
import requests
## 서버 정보 탐색

# 헤더 이용
def use_header(s, url):
    req = s.get(url)
    header = req.headers
    ret = []
    if 'Server' in header:
        h_Server = header['Server']
        h_Server_list = h_Server.split(' ')
        ret_S = []
        tmp = ""
        for i in range(len(h_Server_list)):
            if '/' in h_Server_list[i]:
                tmp = h_Server_list[i]
            else : 
                tmp +=" "+h_Server_list[i]
            if i+1 >= len(h_Server_list) or '/' in h_Server_list[i+1] :
                ret_S.append(tmp)
        ret.append(f'[Server] : {ret_S}')

    if 'X-Powered-By' in header:
        h_X_powered_by = header['X-Powered-By']
        h_X_powered_by_list = h_X_powered_by.split(' ')

        ret_X = []
        tmp = ""
        for i in range(len(h_X_powered_by_list)):
            if '/' in h_X_powered_by_list[i]:
                tmp = h_X_powered_by_list[i]
            else : 
                tmp +=" "+h_X_powered_by_list[i]
            if i+1 >= len(h_X_powered_by_list) or '/' in h_X_powered_by_list[i+1] :
                ret_X.append(tmp)
        ret.append(f'["X-Powered-By"] : {ret_X}')
    
    if ret: return ret
    else : return []

# 오류 페이지 이용
def use_errer_page(s, url):
    split_url = url.split('/')
    ori_url = f"{split_url[0]}//{split_url[2]}"

    server_info = {
    'tomcat':'Tomcat',
    'apache':'Apache',
    'nginx':'NginX',
    'ISS':'ISS',
    'webtb':'WebTob',
    'jboss web':'jboss',
    'RFC2068':'Weblogic',
    'srve':'WebSphere',
    'jsfg':'WebSphere'
    }
    raise_err_url = ori_url+"/asdferrorfasd"
    req = s.get(raise_err_url)
    html = req.text
    status = req.status_code
    if status != 200 : 
        for server_sig in server_info.keys():
            if html.lower().find(server_sig) != -1:
                return [f'{server_info[server_sig]}']
    return []








# 

