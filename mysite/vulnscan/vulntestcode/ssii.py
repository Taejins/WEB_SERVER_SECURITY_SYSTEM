from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import requests
from vulnscan.vulntestcode.parse_form import parse_form
        
def SSI_Injection(s, url):
    ssi_payload = []
    header = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}
    payload = '<!--#echo var="HTTP_USER_AGENT" -->'
    for form_details in parse_form(s, url):
        target_url = urljoin(url, form_details["action"])
        inputs = form_details["inputs"]
        submit = form_details["submit"]
        data = {}
    
        for input in inputs:
            data[input["name"]] = input["value"]
            
        data_key = list(data.keys())
        temp = data.copy()    
           
        if form_details["method"] == "post":
            for pl_key in data_key:
                reflect_data = data.copy()
                reflect_data[pl_key] = temp[pl_key] + payload
                if submit: reflect_data[submit["name"]] = submit["value"]
                res_q = s.post(target_url, data=reflect_data, headers = header)
                if "shtml" in res_q.url:
                    if header["User-Agent"] in res_q.text:
                        ssi_payload.append(reflect_data)
                    
        elif form_details["method"] == "get":
            for pl_key in data_key:
                reflect_data = data.copy()
                reflect_data[pl_key] = temp[pl_key] + payload
                if submit: reflect_data[submit["name"]] = submit["value"]
                res_g = s.get(target_url, data=reflect_data, headers = header)
                if "shtml" in res_g.url:
                    if header["User-Agent"] in res_g.text:
                        ssi_payload.append(reflect_data)

    return ssi_payload

    
if __name__ == "__main__":
    url = 'http://192.168.153.136/ssii.php'
    cookie = {"PHPSESSID":"2qcmbjkgstht0hlvjhp80rall2","security_level":"0"}
    print(SSI_Injection(url, cookie))
    # check(url,cookie)