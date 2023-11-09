
#####运行前请确保有安装足够库####
#  pip install beautifulsoup4 #
#  pip install requests #
##############################
def write_cj_a(str1, user):
    'str1成绩-str2课程-user用户名'
    # 打开文件以追加模式，并指定编码为UTF-8
    file_name = f"CJ_{user}.txt"
    try:
        with open(file_name, "a", encoding="utf-8") as file:
            # 将两个字符串写入同一行并在之间添加换行符
            file.write(str1 + "|")
        #print(f"文件 '{file_name}' 追加内容成功！")
    except Exception as e:
        print(f"追加成绩到文件 '{file_name}' 时出现错误：{e}")

def write_cj_b(user):
    file1_name = f"CJ_{user}.txt"
    file2_name = f"A_{file1_name}"
    try:
        # 打开txt文件1以读取模式
        with open(file1_name, "r", encoding="utf-8") as file1:
            # 读取txt文件1的内容
            content = file1.read()

        # 打开txt文件2以写入模式（覆盖模式），并指定编码为UTF-8
        with open(file2_name, "w", encoding="utf-8") as file2:
            # 将txt文件1的内容写入txt文件2（会覆盖文件2的内容）
            file2.write(content)

        print(f"成功将 '{file1_name}' 的内容覆盖到 '{file2_name}'")
    except Exception as e:
        print(f"写入文件时出现错误：{e}")

def compare_and_print_diff(user,token):
    file1_name = f"CJ_{user}.txt"
    file2_name = f"A_{file1_name}"
    lines_not_found_in_file2 = []
    
    try:
        file_in = os.path.exists(file2_name)
        # print(file_in)
        # 打开文本文件2以附加和读取模式 "a+"，并指定编码为UTF-8
        with open(file2_name, "a+", encoding="utf-8") as file2:
            # 将文件指针移到文件开头，以便读取内容
            file2.seek(0)
            
            # 读取文本文件2的内容并按 "|" 分割
            text2 = file2.read().strip().split("|")

        # 打印读取的内容
        #print(text2)
    except Exception as e:
        print(f"处理文件时出现错误：{e}")
    try:


        # 打开文本文件1以读取模式，并指定编码为UTF-8
        with open(file1_name, "r", encoding="utf-8") as file1:
            # 读取文本文件1的内容并按 "|" 分割
            text1 = file1.read().strip().split("|")

        # 遍历文本文件1的每个元素，查找是否在文本文件2中
        for element1 in text1:
            if element1 not in text2:
                lines_not_found_in_file2.append(element1)

        if lines_not_found_in_file2:
            print("新成绩：")
            for element in lines_not_found_in_file2:
                print(element)
                if file_in == False:
                    pass
                elif file_in == True and len(element)>0:
                    pushnotie(token,element)
            return 1
        else:
            print("没有新成绩")
            return 0
    except Exception as e:
        print(f"查找新成绩失败：{e}")
        return 0


def pushnotie(token,content):
    import requests,json,time
    try:
        title= '新成绩' #改成你要的标题内容
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

def login_1():
    url = "https://cas.kmust.edu.cn/lyuapServer/login?service=http://i.kust.edu.cn/c/portal/login?redirect=/&p_l_id=249011"
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "max-age=0",
        "Connection": "keep-alive",
        "Host": "cas.kmust.edu.cn",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
        "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Microsoft Edge\";v=\"114\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    response = session.get(url, headers=headers,allow_redirects=False)
    html_content = response.text
    html_header = response.headers
    html_code = response.status_code
    soup = BeautifulSoup(html_content, 'html.parser')
    elements_lt = soup.select("html > body > div:nth-of-type(1) > div:nth-of-type(3) > div:nth-of-type(3) > div:nth-of-type(2) > div:nth-of-type(3) > form > div:nth-of-type(4) > input:nth-of-type(1)")
    elements_execution = soup.select("html > body > div:nth-of-type(1) > div:nth-of-type(3) > div:nth-of-type(3) > div:nth-of-type(2) > div:nth-of-type(3) > form > div:nth-of-type(4) > input:nth-of-type(2)")
    elements_eventid = soup.select("html > body > div:nth-of-type(1) > div:nth-of-type(3) > div:nth-of-type(3) > div:nth-of-type(2) > div:nth-of-type(3) > form > div:nth-of-type(4) > input:nth-of-type(3)")
    value_lt = elements_lt[0]['value']
    value_execution = elements_execution[0]['value']
    value_eventid = elements_eventid[0]['value']
    header_cookie = html_header['Set-Cookie'].split(";")[0]
    return value_lt,value_execution,value_eventid,header_cookie,html_code

def login_2(cookie,lt,exe,eve,usern,passw):
    ck = cookie.split('=')[1]
    url = f"https://cas.kmust.edu.cn/lyuapServer/login;jsessionid={ck}?service=http://i.kust.edu.cn/c/portal/login?redirect=%2F&p_l_id=249011"
    data = {
        "username" : usern,
        "password" : passw,
        "captcha" : "",
        "warn" : "true",
        "lt" : lt,
        "execution" : exe,
        "_eventId" : eve
    }
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "Content-Length": "399",
        "Content-Type": "application/x-www-form-urlencoded",
        "Cookie": cookie,
        "Host": "cas.kmust.edu.cn",
        "Origin": "https://cas.kmust.edu.cn",
        "Pragma": "no-cache",
        "Referer": "https://cas.kmust.edu.cn/lyuapServer/login?service=http%3A%2F%2Fi.kust.edu.cn%2Fc%2Fportal%2Flogin%3Fredirect%3D%252F%26p_l_id%3D249011",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-User": "?1",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36 Edg/114.0.1823.67",
        "sec-ch-ua": "\"Not.A/Brand\";v=\"8\", \"Chromium\";v=\"114\", \"Microsoft Edge\";v=\"114\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\""
    }
    response = session.post(url=url, headers=headers,data=data,allow_redirects=False)
    html_cookie = response.headers["Set-Cookie"]#.split(";")[4].split(",")[1].split(" ")[1]
    html_code = response.status_code
    return html_cookie,html_code

def login_3(cookie,cookie2):
    ck = cookie.split('=')[1]
    ck2=cookie2.split(";")
    ck3=ck2[0]+";"+ck2[2].split(",")[1]+";"+ck2[4].split(",")[1]
    url = f"https://cas.kmust.edu.cn/lyuapServer/login;jsessionid={ck}?service=http://i.kust.edu.cn/c/portal/login?redirect=%2F&p_l_id=249011"
    headers = {
        "Host": "cas.kmust.edu.cn",
        "Connection": "keep-alive",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "sec-ch-ua": '"Not_A Brand";v="99", "Microsoft Edge";v="109", "Chromium";v="109"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Referer": "https://cas.kmust.edu.cn/lyuapServer/login?service=http%3A%2F%2Fi.kust.edu.cn%2Fc%2Fportal%2Flogin%3Fredirect%3D%252F%26p_l_id%3D249011",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cookie": ck3
        }
    response = session.get(url, headers=headers,allow_redirects=False)
    html_code = response.status_code
    html_cookie = response.headers
    return html_cookie,html_code

def login_6():
    url = "http://jwctsp.kmust.edu.cn/integration/kcas-sso/login"
    headers = {
        "Host": "jwctsp.kmust.edu.cn",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Referer": "http://i.kust.edu.cn/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6"
    }
    rsp = session.get(url,headers=headers,allow_redirects=False)
    html_cookies=rsp.headers
    html_code=rsp.status_code
    return html_cookies,html_code

def login_7(cookie2):
    ck2=cookie2.split(";")
    ck3=ck2[0]+";"+ck2[2].split(",")[1]+";"+ck2[4].split(",")[1]
    url = "https://cas.kmust.edu.cn/lyuapServer/"
    params = {
        "service": "http%3A%2F%2Fjwctsp.kmust.edu.cn%2Fintegration%2Fkcas-sso%2Flogin"
    }
    headers = {
        "Host": "cas.kmust.edu.cn",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "sec-ch-ua": '"Not_A Brand";v="99", "Microsoft Edge";v="109", "Chromium";v="109"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Referer": "http://i.kust.edu.cn/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cookie": ck3
    }
    resp = session.get(url, params=params, headers=headers, allow_redirects=False)
    ck = resp.headers
    code = resp.status_code
    return ck,code

def login_8(cookie2):
    ck2=cookie2.split(";")
    ck3=ck2[0]+";"+ck2[2].split(",")[1]+";"+ck2[4].split(",")[1]
    url = "https://cas.kmust.edu.cn/lyuapServer/login?service=http%3A%2F%2Fjwctsp.kmust.edu.cn%2Fintegration%2Fkcas-sso%2Flogin"
    headers = {
        "Host": "cas.kmust.edu.cn",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-User": "?1",
        "Sec-Fetch-Dest": "document",
        "sec-ch-ua": '"Not_A Brand";v="99", "Microsoft Edge";v="109", "Chromium";v="109"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": '"Windows"',
        "Referer": "http://i.kust.edu.cn/",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cookie": ck3
    }
    resp = session.get(url, headers=headers, allow_redirects=False)
    ck = resp.headers
    code = resp.status_code
    return ck,code

def login_9(url,ck):
    headers = {
        "Host": "jwctsp.kmust.edu.cn",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Referer": "http://i.kust.edu.cn/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cookie":ck
    }
    rep = session.get(url=url, headers=headers,allow_redirects=False)
    ck = rep.headers
    code = rep.status_code
    return ck,code

def login_l(ck):
    urll = "http://jwctsp.kmust.edu.cn/integration/kcas-sso/login"
    urlll = "http://jwctsp.kmust.edu.cn/integration/"
    urllll = "http://jwctsp.kmust.edu.cn/integration/login"
    headers = {
        "Host": "jwctsp.kmust.edu.cn",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Referer": "http://i.kust.edu.cn/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cookie": ck
    }
    response = session.get(urll, headers=headers, allow_redirects=False)
    responsee = session.get(urlll, headers=headers, allow_redirects=False)
    responseee = session.get(urllll, headers=headers, allow_redirects=False)
    return response.status_code,responsee.status_code,responseee.status_code

def home(ck):
    url = "http://jwctsp.kmust.edu.cn/integration/home"
    headers = {
        "Host": "jwctsp.kmust.edu.cn",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Referer": "http://i.kust.edu.cn/",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cookie": ck
    }
    response = session.get(url, headers=headers, allow_redirects=False)
    code = response.status_code
    return code

def cxcj(cookies,username):
    url0 = 'http://jwctsp.kmust.edu.cn/integration/for-std/best/grade/sheet'
    headers0 = {
        'Host': 'jwctsp.kmust.edu.cn',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://jwctsp.kmust.edu.cn/integration/home',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': cookies
    }
    rep = session.get(url0, headers=headers0, allow_redirects=False)
    url1 = rep.headers['Location']
    headers1 = {
        "Host": "jwctsp.kmust.edu.cn",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.70",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "Referer": "http://jwctsp.kmust.edu.cn/integration/home",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
        "Cookie": cookies
    }
    rep1 = session.get(url1, headers=headers1, allow_redirects=False)
    html_data = rep1.text
    soup = BeautifulSoup(html_data, 'html.parser')
    option_elements = soup.select('html > body > div > form > div > div > select > option')
    i=0
    ppcj=""
    for option in option_elements:
        i=i+1
        op_value=option['value']
        url = "http://jwctsp.kmust.edu.cn/integration/for-std/best/grade/sheet/info/" + rep.headers['Location'].split("/")[-1] + "?semrster=" + op_value
        headersd = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': cookies,
            'Host': 'jwctsp.kmust.edu.cn',
            'Proxy-Connection': 'keep-alive',
            'Referer': 'http://jwctsp.kmust.edu.cn/integration/for-std/best/grade/sheet/semester-index/208803',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest'
        }
        response = session.get(url, headers=headersd, allow_redirects=False)
        try:
            cj = re.findall(r'<tbody[^>]*>(.*?)</tbody>', response.text, re.S)
            k=0
            lo=len(cj)
            for ij in cj:
                k=k+1
                cj2 = re.findall(r'<tr[^>]*>(.*?)</tr>', ij, re.S)
                j=0
                for div in cj2:
                    i = 0
                    cj3 = re.findall(r'<td[^>]*>(.*?)</td>', div, re.S)
                    for div2 in cj3:
                        if i == 0:
                            ppcj1 =div2.strip().split('\n')[0] + str("*")
                        if i == 5:
                            ppcj2 =ppcj1 + div2.strip()
                        i = i+1
                    ppc = ppcj2.split("*")
                    pppp = ppc[1]+ str(" ") + ppc[0]
                    write_cj_a(pppp,username)    
                    j=j+1
        except:
            print("限流\n")
        break

def enpwd(p):
    js = """
    ;function twoDigit(a){return(a<10?"0":"")+String(a)}function encryptedString(a,b){var c=new Array();var d=b.length;var e=0;while(e<d){c[e]=b.charCodeAt(e);e++}while(c.length%a.chunkSize!=0){c[e++]=0}var f=c.length;var g="";var h,k,l;for(e=0;e<f;e+=a.chunkSize){l=new BigInt();h=0;for(k=e;k<e+a.chunkSize;++h){l.digits[h]=c[k++];l.digits[h]+=c[k++]<<8}var n=a.barrett.powMod(l,a.e);var m=a.radix==16?biToHex(n):biToString(n,a.radix);g+=m+" "}return g.substring(0,g.length-1)}function decryptedString(a,b){var c=b.split(" ");var d="";var e,f,g;for(e=0;e<c.length;++e){var h;if(a.radix==16){h=biFromHex(c[e])}else{h=biFromString(c[e],a.radix)}g=a.barrett.powMod(h,a.d);for(f=0;f<=biHighIndex(g);++f){d+=String.fromCharCode(g.digits[f]&255,g.digits[f]>>8)}}if(d.charCodeAt(d.length-1)==0){d=d.substring(0,d.length-1)}return d}function BarrettMu(a){this.modulus=biCopy(a);this.k=biHighIndex(this.modulus)+1;var b=new BigInt();b.digits[2*this.k]=1;this.mu=biDivide(b,this.modulus);this.bkplus1=new BigInt();this.bkplus1.digits[this.k+1]=1;this.modulo=BarrettMu_modulo;this.multiplyMod=BarrettMu_multiplyMod;this.powMod=BarrettMu_powMod}function BarrettMu_modulo(a){var b=biDivideByRadixPower(a,this.k-1);var c=biMultiply(b,this.mu);var d=biDivideByRadixPower(c,this.k+1);var e=biModuloByRadixPower(a,this.k+1);var f=biMultiply(d,this.modulus);var g=biModuloByRadixPower(f,this.k+1);var h=biSubtract(e,g);if(h.isNeg){h=biAdd(h,this.bkplus1)}var k=biCompare(h,this.modulus)>=0;while(k){h=biSubtract(h,this.modulus);k=biCompare(h,this.modulus)>=0}return h}function BarrettMu_multiplyMod(a,b){var c=biMultiply(a,b);return this.modulo(c)}function BarrettMu_powMod(a,b){var c=new BigInt();c.digits[0]=1;var d=a;var e=b;while(true){if((e.digits[0]&1)!=0)c=this.multiplyMod(c,d);e=biShiftRight(e,1);if(e.digits[0]==0&&biHighIndex(e)==0)break;d=this.multiplyMod(d,d)}return c}var biRadixBase=2;var biRadixBits=16;var bitsPerDigit=biRadixBits;var biRadix=1<<16;var biHalfRadix=biRadix>>>1;var biRadixSquared=biRadix*biRadix;var maxDigitVal=biRadix-1;var maxInteger=9999999999999998;var maxDigits;var ZERO_ARRAY;var bigZero,bigOne;function setMaxDigits(a){maxDigits=a;ZERO_ARRAY=new Array(maxDigits);for(var b=0;b<ZERO_ARRAY.length;b++)ZERO_ARRAY[b]=0;bigZero=new BigInt();bigOne=new BigInt();bigOne.digits[0]=1}setMaxDigits(20);var dpl10=15;var lr10=biFromNumber(1000000000000000);function BigInt(a){if(typeof a=="boolean"&&a==true){this.digits=null}else{this.digits=ZERO_ARRAY.slice(0)}this.isNeg=false}function biFromDecimal(a){var b=a.charAt(0)=='-';var c=b?1:0;var d;while(c<a.length&&a.charAt(c)=='0')++c;if(c==a.length){d=new BigInt()}else{var e=a.length-c;var f=e%dpl10;if(f==0)f=dpl10;d=biFromNumber(Number(a.substr(c,f)));c+=f;while(c<a.length){d=biAdd(biMultiply(d,lr10),biFromNumber(Number(a.substr(c,dpl10))));c+=dpl10}d.isNeg=b}return d}function biCopy(a){var b=new BigInt(true);b.digits=a.digits.slice(0);b.isNeg=a.isNeg;return b}function biFromNumber(a){var b=new BigInt();b.isNeg=a<0;a=Math.abs(a);var c=0;while(a>0){b.digits[c++]=a&maxDigitVal;a=Math.floor(a/biRadix)}return b}function reverseStr(a){var b="";for(var c=a.length-1;c>-1;--c){b+=a.charAt(c)}return b}var hexatrigesimalToChar=new Array('0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z');function biToString(a,b){var c=new BigInt();c.digits[0]=b;var d=biDivideModulo(a,c);var e=hexatrigesimalToChar[d[1].digits[0]];while(biCompare(d[0],bigZero)==1){d=biDivideModulo(d[0],c);digit=d[1].digits[0];e+=hexatrigesimalToChar[d[1].digits[0]]}return(a.isNeg?"-":"")+reverseStr(e)}function biToDecimal(a){var b=new BigInt();b.digits[0]=10;var c=biDivideModulo(a,b);var d=String(c[1].digits[0]);while(biCompare(c[0],bigZero)==1){c=biDivideModulo(c[0],b);d+=String(c[1].digits[0])}return(a.isNeg?"-":"")+reverseStr(d)}var hexToChar=new Array('0','1','2','3','4','5','6','7','8','9','a','b','c','d','e','f');function digitToHex(a){var b=0xf;var c="";for(i=0;i<4;++i){c+=hexToChar[a&b];a>>>=4}return reverseStr(c)}function biToHex(a){var b="";var c=biHighIndex(a);for(var d=biHighIndex(a);d>-1;--d){b+=digitToHex(a.digits[d])}return b}function charToHex(a){var b=48;var c=b+9;var d=97;var e=d+25;var f=65;var g=65+25;var h;if(a>=b&&a<=c){h=a-b}else if(a>=f&&a<=g){h=10+a-f}else if(a>=d&&a<=e){h=10+a-d}else{h=0}return h}function hexToDigit(a){var b=0;var c=Math.min(a.length,4);for(var d=0;d<c;++d){b<<=4;b|=charToHex(a.charCodeAt(d))}return b}function biFromHex(a){var b=new BigInt();var c=a.length;for(var d=c,e=0;d>0;d-=4,++e){b.digits[e]=hexToDigit(a.substr(Math.max(d-4,0),Math.min(d,4)))}return b}function biFromString(a,b){var c=a.charAt(0)=='-';var d=c?1:0;var e=new BigInt();var f=new BigInt();f.digits[0]=1;for(var g=a.length-1;g>=d;g--){var h=a.charCodeAt(g);var k=charToHex(h);var l=biMultiplyDigit(f,k);e=biAdd(e,l);f=biMultiplyDigit(f,b)}e.isNeg=c;return e}function biDump(a){return(a.isNeg?"-":"")+a.digits.join(" ")}function biAdd(a,b){var c;if(a.isNeg!=b.isNeg){b.isNeg=!b.isNeg;c=biSubtract(a,b);b.isNeg=!b.isNeg}else{c=new BigInt();var d=0;var e;for(var f=0;f<a.digits.length;++f){e=a.digits[f]+b.digits[f]+d;c.digits[f]=e%biRadix;d=Number(e>=biRadix)}c.isNeg=a.isNeg}return c}function biSubtract(a,b){var c;if(a.isNeg!=b.isNeg){b.isNeg=!b.isNeg;c=biAdd(a,b);b.isNeg=!b.isNeg}else{c=new BigInt();var d,e;e=0;for(var f=0;f<a.digits.length;++f){d=a.digits[f]-b.digits[f]+e;c.digits[f]=d%biRadix;if(c.digits[f]<0)c.digits[f]+=biRadix;e=0-Number(d<0)}if(e==-1){e=0;for(var f=0;f<a.digits.length;++f){d=0-c.digits[f]+e;c.digits[f]=d%biRadix;if(c.digits[f]<0)c.digits[f]+=biRadix;e=0-Number(d<0)}c.isNeg=!a.isNeg}else{c.isNeg=a.isNeg}}return c}function biHighIndex(a){var b=a.digits.length-1;while(b>0&&a.digits[b]==0)--b;return b}function biNumBits(a){var b=biHighIndex(a);var c=a.digits[b];var d=(b+1)*bitsPerDigit;var e;for(e=d;e>d-bitsPerDigit;--e){if((c&0x8000)!=0)break;c<<=1}return e}function biMultiply(a,b){var c=new BigInt();var d;var e=biHighIndex(a);var f=biHighIndex(b);var g,h,k;for(var l=0;l<=f;++l){d=0;k=l;for(j=0;j<=e;++j,++k){h=c.digits[k]+a.digits[j]*b.digits[l]+d;c.digits[k]=h&maxDigitVal;d=h>>>biRadixBits}c.digits[l+e+1]=d}c.isNeg=a.isNeg!=b.isNeg;return c}function biMultiplyDigit(a,b){var c,d,e;result=new BigInt();c=biHighIndex(a);d=0;for(var f=0;f<=c;++f){e=result.digits[f]+a.digits[f]*b+d;result.digits[f]=e&maxDigitVal;d=e>>>biRadixBits}result.digits[1+c]=d;return result}function arrayCopy(a,b,c,d,e){var f=Math.min(b+e,a.length);for(var g=b,h=d;g<f;++g,++h){c[h]=a[g]}}var highBitMasks=new Array(0x0000,0x8000,0xC000,0xE000,0xF000,0xF800,0xFC00,0xFE00,0xFF00,0xFF80,0xFFC0,0xFFE0,0xFFF0,0xFFF8,0xFFFC,0xFFFE,0xFFFF);function biShiftLeft(a,b){var c=Math.floor(b/bitsPerDigit);var d=new BigInt();arrayCopy(a.digits,0,d.digits,c,d.digits.length-c);var e=b%bitsPerDigit;var f=bitsPerDigit-e;for(var g=d.digits.length-1,h=g-1;g>0;--g,--h){d.digits[g]=((d.digits[g]<<e)&maxDigitVal)|((d.digits[h]&highBitMasks[e])>>>(f))}d.digits[0]=((d.digits[g]<<e)&maxDigitVal);d.isNeg=a.isNeg;return d}var lowBitMasks=new Array(0x0000,0x0001,0x0003,0x0007,0x000F,0x001F,0x003F,0x007F,0x00FF,0x01FF,0x03FF,0x07FF,0x0FFF,0x1FFF,0x3FFF,0x7FFF,0xFFFF);function biShiftRight(a,b){var c=Math.floor(b/bitsPerDigit);var d=new BigInt();arrayCopy(a.digits,c,d.digits,0,a.digits.length-c);var e=b%bitsPerDigit;var f=bitsPerDigit-e;for(var g=0,h=g+1;g<d.digits.length-1;++g,++h){d.digits[g]=(d.digits[g]>>>e)|((d.digits[h]&lowBitMasks[e])<<f)}d.digits[d.digits.length-1]>>>=e;d.isNeg=a.isNeg;return d}function biMultiplyByRadixPower(a,b){var c=new BigInt();arrayCopy(a.digits,0,c.digits,b,c.digits.length-b);return c}function biDivideByRadixPower(a,b){var c=new BigInt();arrayCopy(a.digits,b,c.digits,0,c.digits.length-b);return c}function biModuloByRadixPower(a,b){var c=new BigInt();arrayCopy(a.digits,0,c.digits,0,b);return c}function biCompare(a,b){if(a.isNeg!=b.isNeg){return 1-2*Number(a.isNeg)}for(var c=a.digits.length-1;c>=0;--c){if(a.digits[c]!=b.digits[c]){if(a.isNeg){return 1-2*Number(a.digits[c]>b.digits[c])}else{return 1-2*Number(a.digits[c]<b.digits[c])}}}return 0}function biDivideModulo(a,b){var c=biNumBits(a);var d=biNumBits(b);var e=b.isNeg;var f,g;if(c<d){if(a.isNeg){f=biCopy(bigOne);f.isNeg=!b.isNeg;a.isNeg=false;b.isNeg=false;g=biSubtract(b,a);a.isNeg=true;b.isNeg=e}else{f=new BigInt();g=biCopy(a)}return new Array(f,g)}f=new BigInt();g=a;var h=Math.ceil(d/bitsPerDigit)-1;var k=0;while(b.digits[h]<biHalfRadix){b=biShiftLeft(b,1);++k;++d;h=Math.ceil(d/bitsPerDigit)-1}g=biShiftLeft(g,k);c+=k;var l=Math.ceil(c/bitsPerDigit)-1;var n=biMultiplyByRadixPower(b,l-h);while(biCompare(g,n)!=-1){++f.digits[l-h];g=biSubtract(g,n)}for(var m=l;m>h;--m){var o=(m>=g.digits.length)?0:g.digits[m];var q=(m-1>=g.digits.length)?0:g.digits[m-1];var r=(m-2>=g.digits.length)?0:g.digits[m-2];var p=(h>=b.digits.length)?0:b.digits[h];var s=(h-1>=b.digits.length)?0:b.digits[h-1];if(o==p){f.digits[m-h-1]=maxDigitVal}else{f.digits[m-h-1]=Math.floor((o*biRadix+q)/p)}var t=f.digits[m-h-1]*((p*biRadix)+s);var u=(o*biRadixSquared)+((q*biRadix)+r);while(t>u){--f.digits[m-h-1];t=f.digits[m-h-1]*((p*biRadix)|s);u=(o*biRadix*biRadix)+((q*biRadix)+r)}n=biMultiplyByRadixPower(b,m-h-1);g=biSubtract(g,biMultiplyDigit(n,f.digits[m-h-1]));if(g.isNeg){g=biAdd(g,n);--f.digits[m-h-1]}}g=biShiftRight(g,k);f.isNeg=a.isNeg!=e;if(a.isNeg){if(e){f=biAdd(f,bigOne)}else{f=biSubtract(f,bigOne)}b=biShiftRight(b,k);g=biSubtract(b,g)}if(g.digits[0]==0&&biHighIndex(g)==0)g.isNeg=false;return new Array(f,g)}function biDivide(a,b){return biDivideModulo(a,b)[0]}function biModulo(a,b){return biDivideModulo(a,b)[1]}function biMultiplyMod(a,b,c){return biModulo(biMultiply(a,b),c)}function biPow(a,b){var c=bigOne;var d=a;while(true){if((b&1)!=0)c=biMultiply(c,d);b>>=1;if(b==0)break;d=biMultiply(d,d)}return c}function biPowMod(a,b,c){var d=bigOne;var e=a;var f=b;while(true){if((f.digits[0]&1)!=0)d=biMultiplyMod(d,e,c);f=biShiftRight(f,1);if(f.digits[0]==0&&biHighIndex(f)==0)break;e=biMultiplyMod(e,e,c)}return d}function RSAKeyPair(a,b,c){this.e=biFromHex(a);this.d=biFromHex(b);this.m=biFromHex(c);this.chunkSize=2*biHighIndex(this.m);this.radix=16;this.barrett=new BarrettMu(this.m)}function twoDigit(a){return(a<10?"0":"")+String(a)}function encryptedString(a,b){var c=new Array();var d=b.length;var e=0;while(e<d){c[e]=b.charCodeAt(e);e++}while(c.length%a.chunkSize!=0){c[e++]=0}var f=c.length;var g="";var h,k,l;for(e=0;e<f;e+=a.chunkSize){l=new BigInt();h=0;for(k=e;k<e+a.chunkSize;++h){l.digits[h]=c[k++];l.digits[h]+=c[k++]<<8}var n=a.barrett.powMod(l,a.e);var m=a.radix==16?biToHex(n):biToString(n,a.radix);g+=m+" "}return g.substring(0,g.length-1)}function decryptedString(a,b){var c=b.split(" ");var d="";var e,f,g;for(e=0;e<c.length;++e){var h;if(a.radix==16){h=biFromHex(c[e])}else{h=biFromString(c[e],a.radix)}g=a.barrett.powMod(h,a.d);for(f=0;f<=biHighIndex(g);++f){d+=String.fromCharCode(g.digits[f]&255,g.digits[f]>>8)}}if(d.charCodeAt(d.length-1)==0){d=d.substring(0,d.length-1)}return d}function toLogin(a){if(a.length!=256){setMaxDigits(131);var b=new RSAKeyPair("010001",'',"00f0d1b6305ea6256c768f30b6a94ef6c9fa2ee0b8eea2ea5634f821925de774ac60e7cfe9d238489be12551b460ef7943fb0fc132fdfba35fd11a71e0b13d9fe4fed9af90eb69da8627fab28f9700ceb6747ef1e09d6b360553f5385bb8f6315a3c7f71fa0e491920fd18c8119e8ab97d96a06d618e945483d39d83e3a2cf2567");var c=encryptedString(b,encodeURIComponent(a))}return c};
    """
    import execjs
    cwd: any = None
    context = execjs.compile(js,cwd=cwd)
    enp = context.call('toLogin', p)
    return enp

if __name__ == "__main__" :
    import os,json
    # os.environ['wjh'] = '{"username": "学号","password": "密码","pushtk":"pushplus token"}'
    configs = os.environ['wjh']
    configs = json.loads(configs)
    username = configs['username']
    password = configs['password']
    token = configs['pushtk']
    password = str(enpwd(password))
    import requests
    from bs4 import BeautifulSoup
    import re
    import time
    while(1):
        try:
            print('开始登录...',end='\n')
            #200 302 302 302 302 302 302 302 302 302 200
            session = requests.session()
            lt,exe,eve,ck1,code1=login_1()
            print('10%',end=' ')
            if code1 == 200:
                ck2,code2=login_2(ck1,lt,exe,eve,username,password)
                print('20%',end=' ')
                if code2 == 302:
                    cookie4,code4=login_3(ck1,ck2)
                    print('30%',end=' ')
                    if code4 == 302:
                        ck6,code6=login_6()
                        print('40%',end=' ')
                        if code6 == 302:
                            ck7,code7=login_7(ck2)
                            print('50%',end=' ')
                            if code7 == 302:
                                ck8,code8=login_8(ck2)
                                print('60%',end=' ')
                                if code8 == 302:
                                    ck9,code9=login_9(ck8['Location'],ck6['Set-Cookie'].split(';')[0])
                                    print('70%',end=' ')
                                    if code9 == 302:
                                        cookie_result = ck9['Set-Cookie'].split(';')[0] + "; " +ck6['Set-Cookie'].split(';')[0]
                                        code10,code11,code12 = login_l(cookie_result)
                                        print('80%',end=' ')
                                        if code10 ==302 and code11== 302 and code12 == 302:
                                            code_home = home(cookie_result)
                                            print('90%',end=' ')
                                            if code_home == 200:
                                                print('100%',end='\n')
                                                print("^^^^^登录成功^^^^^")
                                                login_ok = 1

                                                break
                                        else:
                                            print('continue...')
                                            code10,code11,code12 = login_l(cookie_result)
                                    else:
                                        print('continue...')
                                        ck9,code9=login_9(ck8['Location'],ck6['Set-Cookie'].split(';')[0])
                                else:
                                    print('continue...')
                                    ck8,code8=login_8(ck2)
                            else:
                                print('continue...')
                                ck7,code7=login_7(ck2)
                        else:
                            print('continue...')
                            ck6,code6=login_6()
                    else:
                        print('continue...')
                        cookie4,code4=login_3(ck1,ck2)
                else:
                    print('continue...')
                    ck2,code2=login_2(ck1,lt,exe,eve,username,password)
            else:
                print('continue...')
                lt,exe,eve,ck1,code1=login_1()
        except:
            print('!小子有问题！!赶快检查账号密码！')
            time.sleep(1)
            continue
    if login_ok == 1:
        while(1):
            try:
                file_namea = f"CJ_{username}.txt"
                with open(file_namea, "w", encoding="utf-8") as file:
                    file.write("")  # 将空字符串写入文件
                cxcj(cookie_result,username)
                if compare_and_print_diff(username,token):
                    write_cj_b(username)
                break
            except:
                print('!你小子有问题！')
                time.sleep(1)
                continue
