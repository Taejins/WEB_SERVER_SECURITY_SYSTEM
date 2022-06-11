import socket
import requests

## 디폴트 관리자 페이지
def default_admin(s, url):
    split_url = url.split('/')

    admin_payloads = [
        '/admin', '/manager', '/master', '/system', '/adm', '/cms',
        '/admin/main.asp', '/admin/menu.html',
        # WAS Default admin page
        '/manager/html', '/admin/login.jsp', # TOMCAT
        '/webadmin', 
    ]
    admin_payloads_with_port = [
        # WAS Default admin page
        ':8080/manager/html', # TOMCAT
        ':7001/console', # WebLogic
        ':7090/admin', ':9090/admin', ':9043/admin', #Websphere
        ':8080/resin', ':8080/resin-admin', # Resin
        ':9744/webadmin' #JEUS
    ]
    check_url = f"{split_url[0]}//{split_url[2]}"
    # check_url_to_ip = f"{split_url[0]}//{socket.gethostbyname(split_url[2])}"
    admin_urls = []

    for payload in admin_payloads:
    
        req = s.get(check_url+payload)
        if req.status_code == 200 :
            admin_urls.append(req.url)

    # for payload in admin_payloads_with_port:
    
    #     try:
    #         req = s.get(check_url_to_ip+payload)
    #         if req.status_code == 200 :
    #             admin_urls.append(req.url)
    #     except:
    #         pass
        
    return admin_urls
