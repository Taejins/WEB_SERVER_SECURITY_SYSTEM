import requests
from bs4 import BeautifulSoup as bs

import Server_info
import dir_indexing
import default_admin
import pred_location
import file_download
import options_method

## 웹 페이지 정보 호출

# url = 'http://192.168.56.101/bWAPP/portal.php'
# url = 'http://192.168.153.134/login.php'
# url = 'https://bwapp.hakhub.net/login.php'
url = 'http://192.168.153.134/filedown.php'
# url = 'https://codeup.kr/rival.php'

split_url = url.split('/')
ori_url = f"{split_url[0]}//{split_url[2]}"

with requests.Session() as s: # 쿠키가 안맞아서 요청 url과 적은 url이 다를 경우 조건을 취하는 코드가 필요
    cookie = {
        'security_level':'0',
        'PHPSESSID':'l80nqpv9a8sgn84q5rjr8lplg1'
    }

    req = s.get(url, cookies=cookie)
    header = req.headers
    html = req.text

    # soup = bs(html, "html.parser")

    # 서버 정보 탐색
    print("< 헤더를 이용한 서버 정보 >\n ",Server_info.use_header(url, cookie))
    print("< 오류페이지를 이용한 서버 정보 >\n ", Server_info.use_errer_page(ori_url))
    # 불필요한 메소드 확인
    print("< 불필요한 메소드 확인 > \n", options_method.unnecessary_method(url))
    # 디렉토리 인덱싱 여부 확인
    print("< 디렉토리 인덱싱 여부 확인 >\n ",dir_indexing.dir_indexing(split_url, cookie))
    # 관리자 페이지 노출 확인
    print("< 관리자 페이지 노출 확인 >\n ",default_admin.default_admin(split_url, cookie))
    # 위치 노출
    print("< 위치 노출 취약점 확인 >"); pred_location.pred_location(split_url)
    # 파일 다운로드
    print("< 파일 다운로드 취약점 확인 >"); file_download.file_download(url, ori_url, cookie)