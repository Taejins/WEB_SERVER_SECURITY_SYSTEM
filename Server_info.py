import requests
## 서버 정보 탐색

# 헤더 이용
def use_header(url, cookie):
    req = requests.get(url, cookies=cookie)
    header = req.headers
    ret = {}
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
        ret['Server'] = ret_S
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
        ret['X_Powerd-By'] = ret_X
    return ret

# 오류 페이지 이용
def use_errer_page(ori_url):
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
    raise_err_url = ori_url+"/asdfasdfasd"
    req = requests.get(raise_err_url)
    header = req.headers
    html = req.text
    status = req.status_code
    if status != 200 : 
        for server_sig in server_info.keys():
            if html.lower().find(server_sig) != -1:
                return f'ERROR PAGE Server Detected : {server_info[server_sig]}'
                break








# 

