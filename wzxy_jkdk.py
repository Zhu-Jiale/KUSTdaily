import requests

def check(username,password):
    headers = {
    "authority": "gw.wozaixiaoyuan.com",
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
    "cache-control": "no-cache",
    "pragma": "no-cache",
    "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Microsoft Edge\";v=\"114\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "none",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.82"
    }
    url = "https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username"
    params = {
        "username": username,
        "password": password
    }
    response = session.get(url, headers=headers, params=params, timeout=3)
    if response.status_code == 200:
        result = response.json()
        if result["code"] == 0:
            jwsession = response.headers.get("Set-Cookie")
            import re
            # 定义正则表达式模式来匹配Set-Cookie中的SESSION值
            pattern = r'JWSESSION=([a-f0-9]+);'
            # 在返回中查找匹配的值
            cookie_header = jwsession
            # 使用findall来找到匹配的SESSION值
            matches = re.findall(pattern, cookie_header)
            # 输出匹配的SESSION值
            # for match in matches:
            #     print(match)
            jwsession = matches[0]
            print("JW:" + jwsession)
            print("账号未失效，开始重置密码...")
            return 1,jwsession
        else:
            print("❌ 账号已失效，将使用JWSESSION重置密码...")
            return 2,0
    else:
        print("❌ 请求失败")
        return 3,0


def passwordchange(password,jwsession):
    url = f"https://gw.wozaixiaoyuan.com/basicinfo/mobile/my/changePassword?oldPassword={password}&newPassword={password}"
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Cookie": "JWSESSION=1ed2d1bda1fe4975a4a128acd837b787",
        "Content-Type": "application/json;charset=UTF-8",
        "Referer": "https://gw.wozaixiaoyuan.com/h5/mobile/basicinfo/index/my/changePassword",
        "Host": "gw.wozaixiaoyuan.com",
        "User-Agent": "Mozilla/5.0 (iPad; CPU OS 15_5 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 MicroMessenger/8.0.23(0x1800172f) NetType/WIFI Language/zh_CN miniProgram/wxce6d08f781975d91",
        "Connection": "keep-alive",
        "Accept-Language": "zh-CN,zh-Hans;q=0.9",
        "JWSESSION":jwsession
    }
    data = ''
    response = session.get(url, headers=headers, data=data, timeout=3)
    if response.status_code == 200:
        result = response.json()
        if result["code"] == 0:
            print("✅ 密码重置成功")
            return 6
        else:
            print("❌ jwsession已失效")
            return 4
    else:
        print("❌ 请求失败")
        return 5

def timein(start_time,end_time): 
    import datetime   
    def is_time_within_range(current_time, start_time, end_time):
            return start_time <= current_time <= end_time
    current_time = datetime.datetime.now().time()
    if is_time_within_range(current_time, start_time, end_time):
        return 1
    else:
        return 0


def save_data_to_json(username, jwsession):
    import os
    import json
    def ensure_directory_exists(directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
    try:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        cache_directory = os.path.join(script_directory, ".cache")
        ensure_directory_exists(cache_directory)
        file_name = f"{username}.json"
        file_path = os.path.join(cache_directory, file_name)
        with open(file_path, 'w') as file:
            json.dump(jwsession, file, indent=None)
        print("JW成功保存:", file_name)
        return True
    except Exception as e:
        print("JW保存出错:", e)
        return False

def load_data_from_json(username):
    import json
    import os
    try:
        script_directory = os.path.dirname(os.path.abspath(__file__))
        cache_directory = os.path.join(script_directory, ".cache")
        file_name = f"{username}.json"
        file_path = os.path.join(cache_directory, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as file:
                data = json.load(file)
                print("读取到JW：")
            return True, data
        else:
            print("文件未创建！")
            return False, None
    except Exception as e:
        print("JW读取出错", e)
        return False, None

def PunchIn(jwsession, max_retries=3):
    import requests
    import time
    import json
    def handle_exception_and_callback(error_message, retries):
        print("异常处理及回调函数执行:", error_message)
        time.sleep(5)
        if retries > 0:
            print(f"尝试重新获取打卡列表，剩余重试次数: {retries}")
            PunchIn(jwsession, retries - 1)  # 重新调用PunchIn函数
        else:
            print("已达到最大重试次数，不再回调")
            return 4
    try:
        url = "https://gw.wozaixiaoyuan.com/health/mobile/health/getBatch"
        headers = {
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "Content-Type": "application/json;charset=UTF-8",
            "JWSESSION": jwsession,
            "Pragma": "no-cache",
            "Referer": "https://gw.wozaixiaoyuan.com/h5/mobile/health/index/health",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "same-origin",
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/115.0.0.0"
        }
        cookies = {
            "JWSESSION": jwsession,
            "WZXYSESSION":jwsession,
            "JWSESSION": jwsession
        }
        data = ''
        response = requests.get(url=url, headers=headers, cookies=cookies, data=data, timeout=3)
        resp = response.text
        respp = json.loads(resp)
        id_value = respp["data"]["list"][0]["id"]
        try:
            if response.status_code == 200:
                result = response.json()
                
                if result["code"] == -10:
                    print("jwsession 无效，尝试账号密码登录...")
                    time.sleep(2)
                    return 0,0
                if result["code"] == 0:
                    print("获取成功，开始打卡")
                    return  1,id_value
                if result["code"] != 0 and result["code"] != -10:
                    handle_exception_and_callback(f"❌ 获取失败，原因：{result['message']}", max_retries)
                    return 2,0
            else:
                handle_exception_and_callback("❌ 请求失败", max_retries)
                return 3,0
        except:
            handle_exception_and_callback("ccc", max_retries)
            return 4,0
    except:
        handle_exception_and_callback("获取打卡列表部分出问题！", max_retries)
        return 4,0
    

def doPunchIn(jwsession,id):
    import json
    try:
        url = f"https://gw.wozaixiaoyuan.com/health/mobile/health/save?batch={id}"
        headers = {
            "Host": "gw.wozaixiaoyuan.com",
            "Connection": "keep-alive",
            "Content-Length": "168",
            "Pragma": "no-cache",
            "Cache-Control": "no-cache",
            "Accept": "application/json, text/plain, */*",
            "JWSESSION": jwsession,
            "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/115.0.0.0",
            "Content-Type": "application/json;charset=UTF-8",
            "Origin": "https://gw.wozaixiaoyuan.com",
            "Sec-Fetch-Site": "same-origin",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://gw.wozaixiaoyuan.com/h5/mobile/health/index/health/detail?id=6700006",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "Cookie": f"JWSESSION={jwsession}; JWSESSION={jwsession}"
        }

        # 请求体数据
        data = json.dumps(sign_data)
        response = session.post(url=url, headers=headers, data=data, timeout=3)
        if response.status_code == 200:
            result = response.json()
            if result["code"] == 0:
                print("✅ 打卡成功")
                return 1
            elif result["code"] == 1 and result['message'] == "打卡时间未开始":
                print("❌ 打卡失败，打卡时间未开始")
                return 8
            elif result["code"] == 1 and result["message"] == "打卡时间已结束":
                print("❌ 打卡失败，当前不在打卡时间段内")
                return 2
            elif result["message"] == "请填写完整信息":
                print("请填写完整信息")
                return 3
            elif result['code'] == -10 and result["message"] == "未登录":
                print("未登录")
                return 4
            elif result['code'] == 103 and result["message"] == "未登录,请重新登录":
                print("未登录,请重新登录")
                return 5
            else:
                print(f"❌ 打卡失败，原因：{data}")
                return 6
        else:
            print("❌ 请求失败")
            return 7
    except:
        print("打卡部分有问题")

def adress_hq(location):
    import requests
    import json
    global sign_data
    longitude, latitude = location.split(',')
    new_location = f'{float(latitude):.4f},{float(longitude):.3f}'
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/115.0.0.0"
    }
    url = "https://apis.map.qq.com/ws/geocoder/v1/"
    params = {
        "key": "A3YBZ-NC5RU-MFYVV-BOHND-RO3OT-ABFCR",
        "output": "jsonp",
        "callback": "jsonCallBack",
        "location": new_location
    }
    response = requests.get(url, headers=headers, params=params)
    res = response.text
    import re
    json_data_match = re.search(r'jsonCallBack&&jsonCallBack\((.*)\)', res, re.DOTALL)
    if json_data_match:
        json_data = json_data_match.group(1)
        resp = json.loads(json_data)
    else:
        print("No JSON data found in the response.")
    # print(res)
    # resp = json.loads(res.split('(')[-1].split(')')[0])
    respp = resp['result']
    locat = respp["address_component"]["nation"] + '/' + respp["address_component"]["province"] + '/' + respp["address_component"]["city"] + '/' + respp["address_component"]["district"]  + '/' + respp["address_reference"]["town"]['title']
    locat = locat + '/' + respp["address_component"]["street"] + '/' + respp["ad_info"]["nation_code"] + '/' + respp["ad_info"]["adcode"] + '/' + respp["ad_info"]["city_code"] + '/' + respp["address_reference"]["town"]['id'] + '/' + latitude + '/' + longitude  
    sign_data = {"type":0,"locationMode":0,"location":locat,"locationType":0} 
    # print(sign_data)

def pushnotie(token,content):
    import requests,json,time
    try:
        title= f'{content}打卡失败' #改成你要的标题内容
        url = 'http://www.pushplus.plus/send'
        data = {
            "token":token,
            "title":title,
            "content":content
        }
        body=json.dumps(data).encode(encoding='utf-8')
        headers = {'Content-Type':'application/json'}
        pushre = requests.post(url,data=body,headers=headers)
        x=1
        while (x):
            if pushre.status_code == 200:
                print("推送通知成功！")
                break
            else:
                print("尝试再次推送。。。")
                time.sleep(5)
                pushre = requests.post(url,data=body,headers=headers)
                x=x+1
                if x == 3:
                    break
    except:
        print("推送部分有问题。。。")

if __name__ == '__main__':
    import datetime,time,json,os
#####################################
    start_time = datetime.time(17, 0)#
    end_time = datetime.time(23, 0)#
######################################
    for i in range(20):
        try:

            print('~~~~~~~~~~~~~~~~')
            configs = os.environ['wzxy'+str(i)]
            configs = json.loads(configs)
            U = configs['username']
            P = configs['password']
            token = configs['pushtk']
            location = configs['jkdk_location']
            mark = configs['mark']
            time_in_not = timein(start_time,end_time)
            session = requests.Session()
            if time_in_not == 1:
                print(f"打卡时间，账号- {mark} -开始打卡...")
                adress_hq(location)
                J = load_data_from_json(U)
                pushn = 1
                while(1):
                    chaxunlt = 100
                    time.sleep(2)
                    Puncode = PunchIn(J[1])
                    if Puncode[0] == 3:
                        break
                    elif Puncode[0] == 0:
                        check(U,P)
                    elif Puncode[0] == 1:
                        doif = doPunchIn(J[1],Puncode[1])
                        if doif == 1:
                            pushn = 0
                            break
                        elif doif == 2:
                            break
                        elif doif == 3:
                            break
                        elif doif == 4:
                            check(U,P)
                            continue
                        elif doif == 5:
                            check(U,P)
                            continue
                        elif doif == 6:
                            break
                        elif doif == 7:
                            continue
                        elif doif == 8:
                            break
                    elif Puncode[0] == 2:
                        break
                    elif Puncode[0] == 4:
                        break
                if pushn == 1:
                    pushnotie(token,mark)
                    # pass
            elif time_in_not == 0:
                print(f"非打卡时间，账号- {mark} -进行密码修改更新JW...")
                for i in range(3):
                    try:
                        Y,J = check(U,P)
                        while Y==3:
                            Y,J = check(U,P)
                        if Y!=3:
                            if Y==1:
                                passwordchange(P,J)
                                save_data_to_json(U,J)
                                break
                            if Y==2:
                                load_data_from_json(U)
                                passwordchange(P,J)
                                save_data_to_json(U,J)
                                break
                    except:
                        continue
        except:
            print(f'账号{i}信息有问题')
            continue
