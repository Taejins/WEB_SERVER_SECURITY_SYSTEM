import requests

def unnecessary_method(url):
    options_check_list = ['Allow', 'Access-Control-Allow-Methods','Public']
    vuln_method = ["OPTIONS", "PUT", "DELETE", "TRACE"]
    req = requests.options(url)
    headers = req.headers
    detect_method = []
    for i in options_check_list:
        if i in headers:
            for j in vuln_method:
                if j in headers[i] :
                    detect_method.append(j)
            break
    return detect_method
    
            
        
    

    
if __name__ == "__main__":
    # url = "http://172.30.1.31"/
    # url = "http://httpbin.org"
    url = "http://172.30.1.19/bWAPP/login.php"
    
    