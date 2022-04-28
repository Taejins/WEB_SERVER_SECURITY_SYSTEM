import requests

## 위치 공개
def pred_location(split_url):
    check_url = f"{split_url[0]}//{split_url[2]}"
    req = requests.get(check_url+'/index.html')
    if req.ok:    
        html = req.text
        if html.find("Welcome to nginx!") != -1:
            print(f'Server index page Detected : nginx')
        elif html.find("default home page") != -1:
            print(f'Server index page Detected : IIS')
        elif html.find("It works!") != -1:
            print(f'Server index page Detected : Apache')

    req = requests.get(check_url+'/phpinfo.php')
    if req.ok:    
        html = req.text
        if html.find("PHP Version") != -1:
            print(f'Server [phpinfo.php] Detected')

    req = requests.get(check_url+'/phpmyadmin')
    if req.ok:    
        html = req.text
        if html.find("phpMyAdmin") != -1:
            print(f'Server [phpMyAdmin] Detected')
