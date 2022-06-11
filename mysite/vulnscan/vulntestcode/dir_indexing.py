import requests

## 디렉토리 인덱싱 진단
def dir_indexing(s, url):
    split_url = url.split('/')

    indexing_payloads = [
    '/', '/icons/', '/images/', '/pr/', '/adm', '/files',
    '/download', '/config' '/files/attach/images', '/data/',
    '/documents', '/doc', '/files/', '/%3f.jsp', '/%23.jsp']
    
    check_url = f"{split_url[0]}/"
    index_urls = []
    for url_shard in split_url[2:-1]:
        check_url+="/"+url_shard
        for payload in indexing_payloads:
            req = s.get(check_url+payload)
            if req.status_code == 200 :
                if req.text.lower().find('index of') != -1:
                    index_urls.append(req.url)
    return index_urls


