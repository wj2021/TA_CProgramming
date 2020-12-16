from bs4 import BeautifulSoup
import requests
import re

# 学生成绩所在的网址url
data_url = "http://114.212.86.242:10002/index.php/submissions/final/problem/3"

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
def getCode(session_request, token, assignment, problem, stuid, submit_id):
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
    session_requests, token = login('mf1933101', '19961211')
    # 获取网页文档
    r = session_requests.get(data_url, headers={'User-Agent': user_agent})
    # 使用BeautifulSoup库解析网页
    mySoup = BeautifulSoup(r.text, 'html.parser')
    # 每一行保存一个学生的信息
    trs = mySoup.find_all(name='tr')
    stuInfo = {} # Map<String, int[3]> int[2]：[0]是成绩，[1]是是否有延迟, [2]是提交id
    for tr in trs:
        if tr.attrs.get('data-u') is not None:
            tds = tr.find_all('td')
            if tds[2].text[0]=='1' or tds[2].text[0]=='2' : # 按学号过滤非本科生的提交记录
                delay = tds[7].text.strip()
                stuInfo[tds[2].text] = [int(tds[8].text.strip())/10, int(delay[delay.index('\n')+1:delay.index('%')].strip()), tds[1].text.strip()]
    print('submitted_total_count:', len(stuInfo))


    shieds = ['strcpy', 'strncpy', 'strcat', 'strchr', 'strcmp', 'strnicmp', 'strcspn', 'strdup', 
    'stricmp', 'strerror', 'strcmpi', 'strncmp', 'strncpy', 'strnicmp', 'strnset', 'strpbrk',
    'strrchr', 'strrev', 'strspn', 'strstr', 'strtod', 'strtok', 'strtol', 'strupr', 'swap']
    # 通过学生学号获取学生提交的代码

    result = {}

    for stuid, info in stuInfo.items():
        r = getCode(session_requests, token, 18, 3, stuid, info[2])
        find = 0
        for shied in shieds:
            findstr = '[^a-zA-Z0-9_]'+shied+'\\s*\('
            m = re.search(findstr, r.text)
            if m is not None:
                result[stuid] = m.group()
                break
    
    for k, v in result.items():
        print(k, v)