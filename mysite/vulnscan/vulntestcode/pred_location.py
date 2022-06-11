import requests

## 위치 공개
def pred_location(s, url):
    split_url = url.split('/')
    result = []
    check_url = f"{split_url[0]}//{split_url[2]}"
    req = s.get(check_url+'/index.html')
    if req.ok:    
        html = req.text
        if html.find("Welcome to nginx!") != -1:
            result.append(f'{req.url} [nginx]')
        elif html.find("default home page") != -1:
            result.append(f'{req.url} [IIS]')
        elif html.find("It works!") != -1:
            result.append(f'{req.url} [Apache]')

    req = s.get(check_url+'/phpinfo.php')
    if req.ok:    
        html = req.text
        if html.find("PHP Version") != -1:
            result.append(f'{req.url} [phpinfo.php]')

    req = s.get(check_url+'/phpmyadmin')
    if req.ok:    
        html = req.text
        if html.find("phpMyAdmin") != -1:
            result.append(f'{req.url} [phpMyAdmin]')
    return result
