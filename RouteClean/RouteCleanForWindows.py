# route print -4
# route delete 157.0.0.0
# route ADD 157.0.0.0 MASK 255.0.0.0 157.55.80.1 METRIC 3 IF 2
#          destination        mask     gateway             interface

from __future__ import print_function
import os
import re
import sys
import ctypes

# nju校内资源网络地址
njuIps = ['36.152.24.0', '211.162.81.0', '211.162.26.0', '112.25.191.0', '58.193.225.0',
          '221.6.40.128', '58.240.127.0', '218.94.142.0', '58.192.0.0', '202.127.247.0',
          '219.219.0.0', '210.29.240.0', '210.28.128.0', '202.38.126.0', '202.38.2.0',
          '202.38.3.0', '180.209.0.0', '202.119.0.0', '114.212.0.0', '58.193.224.0',
          '172.0.0.0', '10.254.253.0']

# execute command, and return the output
def execCmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text

def routeIsNeed(network, mask, ips):
    net_s = network.split('.')
    mask_s = mask.split('.')
    for ip in ips:
        ip_s = ip.split('.')
        if(int(ip_s[0]) & int(mask_s[0]) == int(net_s[0]) and 
           int(ip_s[1]) & int(mask_s[1]) == int(net_s[1]) and 
           int(ip_s[2]) & int(mask_s[2]) == int(net_s[2]) and 
           int(ip_s[3]) & int(mask_s[3]) == int(net_s[3])):
            return True
    return False


if __name__ == '__main__':
    # 判断是否具有管理员权限
    if ctypes.windll.shell32.IsUserAnAdmin() == False:
        print("权限不足，请以管理员身份运行该程序！")
        input('\n请按任意键退出程序...')
        sys.exit(1)

    print('正在获取路由表信息...')
    result = execCmd("route print -4")
    result = re.sub(r'\s+', ' ', result)
    ipPattern = '\d+\.\d+\.\d+\.\d+'
    pattern = '(' + ipPattern + '\s' + ipPattern + '\s(' + ipPattern + '|[\uAC00-\uD7A3\u0800-\u9fa5A-Za-z]+)\s' + ipPattern + '\s' + '\d+)'
    routerList = re.findall(pattern, result)
    ipGateway = ''
    for rl in routerList:
        # print(rl[0])
        if(re.search(r'114.0.0.0', rl[0])):
            row = re.split(r'\s', rl[0])
            ipGateway = row[2]
            break
    print('获取路由表成功!')

    print('=========================================================')
    print('正在检测并删除无用路由表...')
    routeLen = len(routerList)
    deleteCount = 0
    preProgress = -1
    for idx,rl in enumerate(routerList):
        row = re.split(r'\s', rl[0])
        if row[2] == ipGateway and routeIsNeed(row[0], row[1], njuIps) == False:
            execCmd("route delete " + row[0])
            deleteCount = deleteCount+1
        currProgress = round(100*(idx+1)/routeLen)
        if(currProgress != preProgress):
            preProgress = currProgress
            print(str(currProgress)+"%", end=' ')
            sys.stdout.flush()

    print("\n删除 %d 条多余路由表成功!"%deleteCount)
    print('=========================================================')
    input('\n请按任意键退出程序...')