import requests,json,os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64encode
def w_log(text):
    global mark
    import time
    now_localtime = time.strftime("%H:%M:%S", time.localtime())
    print(now_localtime + ' ⬛ By.mude' + ' | ' + str(mark) + ' | ' + str(text))
# 🟡 U+1F7E1 — 黄色方块
# 🟠 U+1F7E0 — 橙色方块
# 🟣 U+1F7E3 — 紫色方块
# 🟤 U+1F7E4 — 棕色方块
# 🟧 U+1F7E7 — 橙色圈
# 🟨 U+1F7E8 — 黄色圈
# 🟩 U+1F7E9 — 绿色圈
# 🟦 U+1F7E6 — 蓝色圈
# 🟥 U+1F7E5 — 红色方块
# ⬛ U+2B1B — 黑色方块
# ⬜ U+2B1C — 白色方块
# 🔄 U+1F504 — 旋转箭头（表示刷新或循环）
def pushnotie(token,content):
    import requests,json,time
    try:
        title= f'{content}打卡失败'
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
                w_log("🟩账号打卡推送推送通知成功！")
                break
            else:
                w_log("🔄尝试再次推送")
                time.sleep(5)
                pushre = requests.post(url,data=body,headers=headers)
                x=x+1
                if x == 3:
                    break
    except:
        w_log("🟠推送部分有问题")

def main_loop(username,password,location,school,mark,key):
    
    def encrypt(t, e):
        key = e.encode('utf-8')
        cipher = AES.new(key, AES.MODE_ECB)
        padded_text = pad(t.encode('utf-8'), AES.block_size)
        encrypted_text = cipher.encrypt(padded_text)
        return b64encode(encrypted_text).decode('utf-8')
    encrypted_text = encrypt(password, key)

    session = requests.Session()

    headers00 = {
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/119.0.0.0"}
    url00 = "https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/getSchoolList"
    response00 = session.get(url00, headers=headers00)
    school_data = json.loads(response00.text)['data']
    def find_school_id(school_name, data):
        for school in data:
            if school['name'] == school_name:
                return school['id']
        return None

    school_id = find_school_id(school, school_data)

    headers0 = {
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/119.0.0.0"}
    url0 = "https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username"
    params0 = {
        "schoolId": school_id,
        "username": username,
        "password": encrypted_text
    }
    data0 = {}
    data0 = json.dumps(data0, separators=(',', ':'))
    response0 = session.post(url0, headers=headers0, params=params0, data=data0)
    cookie0 = response0.headers['Set-Cookie'].split(';')[0].split('=')[1]
    headers1 = {
        "accept": "application/json, text/plain, */*",
        "jwsession": cookie0,
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/119.0.0.0"
    }
    url = "https://gw.wozaixiaoyuan.com/health/mobile/health/getBatch"
    response1 = session.get(url, headers=headers1)
    dakaid = json.loads(response1.text)["data"]["list"][0]["id"]

    def get_location(location):
        longitude,latitude= location.split(',')
        url = f"https://apis.map.qq.com/ws/geocoder/v1/?key=A3YBZ-NC5RU-MFYVV-BOHND-RO3OT-ABFCR&location={latitude},{longitude}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data['status'] == 0:
                result = data.get('result', {})
                if result.get('address_component', {}).get('nation') == '中国':
                    town = result.get('address_reference', {}).get('town', {})
                    town_title = town.get('title', '')
                    town_id = town.get('id', '')

                    location_data = {
                        'address': result.get('address', ''),
                        'country': result['address_component']['nation'],
                        'province': result['ad_info']['province'],
                        'city': result['ad_info']['city'],
                        'district': result['ad_info']['district'],
                        'street': result['address_component']['street'],
                        'streetNumber': result['address_component']['street_number'],
                        'town': town_title,
                        'townCode': town_id,
                        'nationCode': result['ad_info']['nation_code'],
                        'adCode': result['ad_info']['adcode'],
                        'cityCode': result['ad_info']['city_code'],
                        'location': result.get('location', {})
                    }
                    return {'code': data['status'], 'data': location_data}
                else:
                    location_data = {
                        'address': result.get('address', ''),
                        'country': result['address_component']['nation'],
                        'province': result['address_component']['ad_level_1'],
                        'city': result['address_component']['ad_level_2'],
                        'nationCode': result['ad_info']['nation_code'],
                        'location': result.get('location', {}),
                        'district': '',
                        'street': '',
                        'streetNumber': '',
                        'town': '',
                        'townCode': '',
                        'adCode': '',
                        'cityCode': ''
                    }
                    return {'code': data['status'], 'data': location_data}
            else:
                return {'code': data.get('status', 1), 'message': data.get('message', '获取位置失败')}
        except Exception as e:
            return {'code': 1, 'message': f"获取位置异常[{str(e)}]"}
    original_data = get_location(location=location)
    sign_data = {
        'type': 0,
        'locationMode': 0,
        'location': f"{original_data['data']['country']}/{original_data['data']['province']}/{original_data['data']['city']}/{original_data['data']['district']}/{original_data['data']['town']}/{original_data['data']['street']}/{original_data['data']['nationCode']}/{original_data['data']['adCode']}/{original_data['data']['cityCode']}/{original_data['data']['townCode']}/{original_data['data']['location']['lat']}/{original_data['data']['location']['lng']}",
        'locationType': 0
    }

    url3 = f"https://gw.wozaixiaoyuan.com/health/mobile/health/save?batch={dakaid}"
    headers3 = {
        "Accept": "application/json, text/plain, */*",
        "JWSESSION": cookie0,
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/115.0.0.0",
        "Cookie": f"JWSESSION={cookie0}; JWSESSION={cookie0}"
    }
    data3 = json.dumps(sign_data)
    response3 = session.post(url=url3, headers=headers3, data=data3, timeout=3)
    # w_log(f"🔵账号- {mark} -打卡结果：{json.loads(response3.text)['message']}")
    return json.loads(response3.text)['code']
mark = ''
if __name__ == '__main__':
    code = 0
    for i in range(20):
            import requests,json,os
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from base64 import b64encode
def w_log(text):
    global mark
    import time
    now_localtime = time.strftime("%H:%M:%S", time.localtime())
    print(now_localtime + ' ⬛ By.mude' + ' | ' + str(mark) + ' | ' + str(text))
# 🟡 U+1F7E1 — 黄色方块
# 🟠 U+1F7E0 — 橙色方块
# 🟣 U+1F7E3 — 紫色方块
# 🟤 U+1F7E4 — 棕色方块
# 🟧 U+1F7E7 — 橙色圈
# 🟨 U+1F7E8 — 黄色圈
# 🟩 U+1F7E9 — 绿色圈
# 🟦 U+1F7E6 — 蓝色圈
# 🟥 U+1F7E5 — 红色方块
# ⬛ U+2B1B — 黑色方块
# ⬜ U+2B1C — 白色方块
# 🔄 U+1F504 — 旋转箭头（表示刷新或循环）
def pushnotie(token,content):
    import requests,json,time
    try:
        title= f'{content}打卡失败'
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
                w_log("🟩账号打卡推送推送通知成功！")
                break
            else:
                w_log("🔄尝试再次推送")
                time.sleep(5)
                pushre = requests.post(url,data=body,headers=headers)
                x=x+1
                if x == 3:
                    break
    except:
        w_log("🟠推送部分有问题")

def main_loop(username,password,location,school,mark,key):
    
    def encrypt(t, e):
        key = e.encode('utf-8')
        cipher = AES.new(key, AES.MODE_ECB)
        padded_text = pad(t.encode('utf-8'), AES.block_size)
        encrypted_text = cipher.encrypt(padded_text)
        return b64encode(encrypted_text).decode('utf-8')
    encrypted_text = encrypt(password, key)

    session = requests.Session()

    headers00 = {
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/119.0.0.0"}
    url00 = "https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/getSchoolList"
    response00 = session.get(url00, headers=headers00)
    school_data = json.loads(response00.text)['data']
    def find_school_id(school_name, data):
        for school in data:
            if school['name'] == school_name:
                return school['id']
        return None

    school_id = find_school_id(school, school_data)

    headers0 = {
        "accept": "application/json, text/plain, */*",
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/119.0.0.0"}
    url0 = "https://gw.wozaixiaoyuan.com/basicinfo/mobile/login/username"
    params0 = {
        "schoolId": school_id,
        "username": username,
        "password": encrypted_text
    }
    data0 = {}
    data0 = json.dumps(data0, separators=(',', ':'))
    response0 = session.post(url0, headers=headers0, params=params0, data=data0)
    cookie0 = response0.headers['Set-Cookie'].split(';')[0].split('=')[1]
    headers1 = {
        "accept": "application/json, text/plain, */*",
        "jwsession": cookie0,
        "user-agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1 Edg/119.0.0.0"
    }
    url = "https://gw.wozaixiaoyuan.com/health/mobile/health/getBatch"
    response1 = session.get(url, headers=headers1)
    dakaid = json.loads(response1.text)["data"]["list"][0]["id"]

    def get_location(location):
        longitude,latitude= location.split(',')
        url = f"https://apis.map.qq.com/ws/geocoder/v1/?key=A3YBZ-NC5RU-MFYVV-BOHND-RO3OT-ABFCR&location={latitude},{longitude}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            if data['status'] == 0:
                result = data.get('result', {})
                if result.get('address_component', {}).get('nation') == '中国':
                    town = result.get('address_reference', {}).get('town', {})
                    town_title = town.get('title', '')
                    town_id = town.get('id', '')

                    location_data = {
                        'address': result.get('address', ''),
                        'country': result['address_component']['nation'],
                        'province': result['ad_info']['province'],
                        'city': result['ad_info']['city'],
                        'district': result['ad_info']['district'],
                        'street': result['address_component']['street'],
                        'streetNumber': result['address_component']['street_number'],
                        'town': town_title,
                        'townCode': town_id,
                        'nationCode': result['ad_info']['nation_code'],
                        'adCode': result['ad_info']['adcode'],
                        'cityCode': result['ad_info']['city_code'],
                        'location': result.get('location', {})
                    }
                    return {'code': data['status'], 'data': location_data}
                else:
                    location_data = {
                        'address': result.get('address', ''),
                        'country': result['address_component']['nation'],
                        'province': result['address_component']['ad_level_1'],
                        'city': result['address_component']['ad_level_2'],
                        'nationCode': result['ad_info']['nation_code'],
                        'location': result.get('location', {}),
                        'district': '',
                        'street': '',
                        'streetNumber': '',
                        'town': '',
                        'townCode': '',
                        'adCode': '',
                        'cityCode': ''
                    }
                    return {'code': data['status'], 'data': location_data}
            else:
                return {'code': data.get('status', 1), 'message': data.get('message', '获取位置失败')}
        except Exception as e:
            return {'code': 1, 'message': f"获取位置异常[{str(e)}]"}
    original_data = get_location(location=location)
    sign_data = {
        'type': 0,
        'locationMode': 0,
        'location': f"{original_data['data']['country']}/{original_data['data']['province']}/{original_data['data']['city']}/{original_data['data']['district']}/{original_data['data']['town']}/{original_data['data']['street']}/{original_data['data']['nationCode']}/{original_data['data']['adCode']}/{original_data['data']['cityCode']}/{original_data['data']['townCode']}/{original_data['data']['location']['lat']}/{original_data['data']['location']['lng']}",
        'locationType': 0
    }

    url3 = f"https://gw.wozaixiaoyuan.com/health/mobile/health/save?batch={dakaid}"
    headers3 = {
        "Accept": "application/json, text/plain, */*",
        "JWSESSION": cookie0,
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1 Edg/115.0.0.0",
        "Cookie": f"JWSESSION={cookie0}; JWSESSION={cookie0}"
    }
    data3 = json.dumps(sign_data)
    response3 = session.post(url=url3, headers=headers3, data=data3, timeout=3)
    # w_log(f"🔵账号- {mark} -打卡结果：{json.loads(response3.text)['message']}")
    return json.loads(response3.text)['code']
mark = ''
if __name__ == '__main__':
    code = 0
    for i in range(20):
            # os.environ['wzxy0'] = '{"username": "15","password":"88","jkdk_location": "11.2872,22.75","mark": "木德","pushtk":"0801b4044865062d8415f","school":"大学"}'
            try:
                try:
                    configs = os.environ['wzxy'+str(i)]
                except:
                    continue
                configs = json.loads(configs)
                username = configs['username']
                password = configs['password']
                pushtoken = configs['pushtk']
                location = configs['jkdk_location']
                school = configs['school']
                mark = configs['mark']
                key = (username + "0000000000000000")[:16]
            except:
                w_log("🟠账号密码等数据出现问题")
                continue
            max_attempts = 3
            w_log(f"🔄账号- {mark} -开始打卡")
            for attempt in range(1, max_attempts + 1):
                try:
                    code = main_loop(username,password,location,school,mark,key)
                except:
                    w_log("🟠登录打卡部分出现问题")
                if code == 0:
                    w_log(f"🟩账号- {mark} -打卡成功")
                    break
                elif code ==1:
                    w_log("🔵打卡时间未到")
                else:
                    w_log(f"🔄账号- {mark} -尝试重新打卡")
                    remaining_attempts = max_attempts - attempt
                    if remaining_attempts == 0:
                        w_log(f"🟥账号- {mark} -尝试重新打卡三次失败")
                        # pushnotie(pushtoken,mark)
                        break


            try:
                try:
                    configs = os.environ['wzxy'+str(i)]
                except:
                    continue
                configs = json.loads(configs)
                username = configs['username']
                password = configs['password']
                pushtoken = configs['pushtk']
                location = configs['jkdk_location']
                school = configs['school']
                mark = configs['mark']
                key = (username + "0000000000000000")[:16]
            except:
                w_log("🟠账号密码等数据出现问题")
                continue
            max_attempts = 3
            w_log(f"🔄账号- {mark} -开始打卡")
            for attempt in range(1, max_attempts + 1):
                try:
                    code = main_loop(username,password,location,school,mark,key)
                except:
                    w_log("🟠登录打卡部分出现问题")
                if code == 0:
                    w_log(f"🟩账号- {mark} -打卡成功")
                    break
                elif code ==1:
                    w_log("🔵打卡时间未到")
                else:
                    w_log(f"🔄账号- {mark} -尝试重新打卡")
                    remaining_attempts = max_attempts - attempt
                    if remaining_attempts == 0:
                        w_log(f"🟥账号- {mark} -尝试重新打卡三次失败")
                        # pushnotie(pushtoken,mark)
                        break

