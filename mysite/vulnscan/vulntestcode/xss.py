from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin
import requests,os
from vulnscan.vulntestcode.parse_form import parse_form

def reflected_scan_xss(s, url):
    report_xss_reflected = []
    
    for form_details in parse_form(s, url):
        with open(os.path.dirname(os.path.realpath(__file__))+'/payloads/xss_payloads_list.txt', "r", encoding="utf-8") as vector_file:
            payload = vector_file.read().split('\n')
      
        target_url = urljoin(url, form_details["action"])
        inputs = form_details["inputs"]
        data = {}
        
        for input in inputs:
            data[input["name"]] = input["value"]
        data_key = list(data.keys())
        temp = data.copy()      
        if form_details["method"] == "post":
            for pl_key in data_key:
                reflect_data = data.copy()
                for reflect_pl in payload:
                    reflect_data[pl_key] = temp[pl_key]+reflect_pl
                    res_p = s.post(target_url, data=reflect_data).content.decode()
                    if reflect_pl in res_p:
                        report_xss_reflected.append(str(reflect_data))
                        
        elif form_details["method"] == "get":
                for pl_key in data_key:
                    reflect_data = data.copy()
                    for reflect_pl in payload:
                        reflect_data[pl_key] = temp[pl_key]+reflect_pl
                        res_g = s.get(target_url, params=reflect_data).content.decode()
                        if reflect_pl in res_g:
                            report_xss_reflected.append(str(reflect_data))
                        
    return report_xss_reflected
            


if __name__ == "__main__":
    url = 'http://192.168.153.134/xss_get.php'
    cookie = {"PHPSESSID":"of198hbvc7eb9fes39fri8tlr4","security_level":"0"}
    print('\n '.join(reflected_scan_xss(url,cookie)))