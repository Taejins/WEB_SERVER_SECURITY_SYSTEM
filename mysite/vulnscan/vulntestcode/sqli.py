import json
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlencode
import requests,os,re
from vulnscan.vulntestcode.parse_form import parse_form
import json
import base64

def check_sqli_vuln(res, err):
    for error in err:
        if re.search(error, res):
            return True
    return False

def sqli_scan(s, url):
    with open(os.path.dirname(os.path.realpath(__file__))+'/payloads/sql_payload.txt', 'r', encoding='utf8') as f:
        payload = f.read().split('\n')
    with open(os.path.dirname(os.path.realpath(__file__))+'/payloads/sqli_boolean.txt', 'r', encoding='utf8') as f:
        bool = f.read().split('\n')
    with open(os.path.dirname(os.path.realpath(__file__))+'/payloads/spl_error.txt', 'r', encoding='utf8') as f:
        err = f.read().split('\n')
    
    report_all = []
    
    for forms in parse_form(s, url):
        target_url = urljoin(url, forms["action"])
        joined_url = ""
        inputs = forms["inputs"]
        data = {}

        for input in inputs:
            data[input["name"]] = input["value"]
            try:
                data_key = list(data.keys())
                temp = data.copy()
                if forms["method"] == "get":
                    for pl_key in data_key:
                        # error based sqli
                        error_data = data.copy()
                        for error_pl in payload:
                            error_data[pl_key] = temp[pl_key]+error_pl
                            joined_url = target_url + "?" + urlencode(error_data)
                            response = s.get(
                                joined_url, params=error_data).content.decode()
                            if check_sqli_vuln(response, err):
                                report_all.append(f'(error based) : {joined_url}')
                        #boolean based sqli
                        bool_data = data.copy()
                        for bool_pl in bool:
                            true_pl, false_pl = bool_pl.split("\t")
                            bool_data[pl_key] = temp[pl_key]+true_pl
                            joined_url1 = target_url + "?" + urlencode(bool_data)
                            t_res = s.get(
                                joined_url1, params=bool_data).content.decode()
                            bool_data[pl_key] = temp[pl_key]+false_pl
                            joined_url2 = target_url + "?" + urlencode(bool_data)
                            f_res = s.get(
                                joined_url2, params=bool_data).content.decode()
                            if len(t_res) != len(f_res):
                                report_all.append(f"(boolean based) : True[{joined_url1}] False[{joined_url2}]")

                elif forms["method"] == "post":
                    for pl_key in data_key:
                        # error based sqli
                        error_data = data.copy()
                        for error_pl in payload:
                            error_data[pl_key] = temp[pl_key]+error_pl
                            response = s.post(
                                target_url, data=error_data).content.decode()
                            if check_sqli_vuln(response, err):
                                report_all.append(f"(error based) : {pl_key}:{error_pl}")
                        #boolean based sqli
                        bool_data = data.copy()
                        for bool_pl in bool:
                            true_pl, false_pl = bool_pl.split("\t")
                            bool_data[pl_key] = temp[pl_key]+true_pl
                            t_res = s.get(
                                target_url, data=bool_data)
                            bool_data[pl_key] = temp[pl_key]+false_pl
                            f_res = s.get(
                                target_url, data=bool_data)
                            if len(str(bs(t_res.text, "html.parser"))) != len(str(bs(t_res.text, "html.parser"))):
                                report_all.append(f"(boolean based) : {pl_key}: True[{true_pl}] False[{false_pl}]")
            except Exception as e:
                print("Exception Error: ", e)

    return report_all
    
    

if __name__ == "__main__":
    url = 'http://192.168.153.134/login.php'
    cookie = {"security_level":"0", "PHPSESSID":"4lhi800mp7h6b34751j360nff5"}

    print(sqli_scan(url, cookie))
