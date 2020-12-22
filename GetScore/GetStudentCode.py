from bs4 import BeautifulSoup
import requests
import json
import os
import time

# 学生成绩所在的网址url
data_url = "http://114.212.86.242:10002/index.php/submissions/final/problem/5"

login_url = 'http://114.212.86.242:10002/index.php/login'
view_code_url = 'http://114.212.86.242:10002/index.php/submissions/view_code'

user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.69 Safari/537.36 Edg/81.0.416.34'

# 使用requests模拟登录
def login(username, password):
    # 获取合法token
    _session_requests = requests.session()
    _r = _session_requests.get(login_url)
    soup = BeautifulSoup(_r.text, 'html.parser')
    token = soup.find(name="input", attrs={'name': 'shj_csrf_token', 'type': 'hidden'})
    if token is None:
        raise Exception("connecting error!")
    post_data = {
        'shj_csrf_token': token.attrs.get('value'),
        'username': username,
        'password': password
    }
    _session_requests.post(login_url, data=post_data, headers={'User-Agent': user_agent})
    return _session_requests, token.attrs.get('value')


# 通过学号获取学生提交的代码
def getCode(session_request, token, assignment, problem, submit_id, stuid):
    if token is None or token == '':
        raise Exception("token error!")
    post_data = {
        'shj_csrf_token': token,
        'type': 'code',
        'username': stuid,
        'submit_id': submit_id,
        'assignment': assignment,
        'problem': problem
    }
    header = {
        'User-Agent': user_agent,
        'X-Requested-With': 'XMLHttpRequest'
    }
    r = session_request.post(view_code_url, data=post_data, headers=header)
    return r


if __name__ == '__main__':
    # 登录oj
    session_requests, token = login('xxxxxxxx', 'xxxxxxxx')
    # 获取网页文档
    r = session_requests.get(data_url, headers={'User-Agent': user_agent})
    # 使用BeautifulSoup库解析网页
    mySoup = BeautifulSoup(r.text, 'html.parser')
    # 每一行保存一个学生的信息
    trs = mySoup.find_all(name='tr')
    stuSubmitIds = []
    for tr in trs:
        if tr.attrs.get('data-u') is not None:
            tds = tr.find_all('td')
            if tds[2].text[0]=='1' or tds[2].text[0]=='2' : # 按学号过滤非本科生的提交记录
                truple = [tds[1].text, tds[2].text]
                stuSubmitIds.append(truple)
    print('submitted_total_count:', len(stuSubmitIds))

    # 通过学生学号获取学生提交的代码并保存到桌面的文件夹中
    savepath = "C:/Users/Jun/Desktop/code_"+str(int(time.time()))+"/"
    if not os.path.exists(savepath):
        os.mkdir(savepath)
    for stuSubmitId in stuSubmitIds:
        r = getCode(session_requests, token, 18, 5, stuSubmitId[0], stuSubmitId[1])
        dic = json.loads(r.text)
        # save code to file
        filepath = savepath + str(stuSubmitId[1]) + "." + str(dic['lang'])
        with open(filepath, mode='w+', encoding='utf-8') as f:
            f.write(dic['text'])