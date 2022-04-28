import requests

def unnecessary_method(req):
    options_check_list = ['Allow', 'Access-Control-Allow-Methods','Public']
    headers = req.headers
    for i in options_check_list:
        if i in headers:
            return headers[i]
    

    
if __name__ == "__main__":
    # url = "http://172.30.1.31"/
    # url = "http://httpbin.org"
    url = "http://172.30.1.19/bWAPP/login.php"
    r = requests.options(url)
    