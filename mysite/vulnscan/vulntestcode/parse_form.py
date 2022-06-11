from bs4 import BeautifulSoup as bs

def parse_form(s, url):
    form_list=[]
    req = s.get(url)
    forms = bs(req.text,'html.parser').find_all('form')
    for form in forms:
        
        details = {}
        inputs = []
        submit = {}
        action = form.attrs.get("action") # form의 이동할 action url
        method = form.attrs.get("method", "get").lower() # form method (GET, POST, etc...)
        
        for select_tag in form.find_all("select"):
            select_name = select_tag.attrs.get("name")
            inputs.append(
                {"type": "select", "name": select_name, "value": " "})
            
        for input_tag in form.find_all("input"):
            input_type = input_tag.attrs.get("type")
            input_name = input_tag.attrs.get("name")

            if input_type == "radio":
                for input in inputs:
                    if input["name"] == input_name:
                        break
                else :
                    inputs.append({"type":input_type, "name" : input_name, "value": ' '})
            else:
                inputs.append({"type":input_type, "name" : input_name, "value": ' 'if input_tag.attrs.get("value") == None else input_tag.attrs.get("value")})

        for submit_tag in form.find_all("button"):
            if "submit" == submit_tag.attrs.get("type") and submit_tag.attrs.get("value") != None:
                submit_name = submit_tag.attrs.get("name")
                submit_value = submit_tag.attrs.get("value")
                submit = {"name":submit_name, "value": submit_value}
        
        details["action"] = action
        details["method"] = method
        details["inputs"] = inputs
        details["submit"] = submit
        
        if len(details["inputs"]) > 0:
            form_list.append(details)

    return form_list