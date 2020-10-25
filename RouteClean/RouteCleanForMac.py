# netstat -nr
# sudo route -v delete -net 10.10.12.0 -gateway 10.10.12.1

from __future__ import print_function
import os
import re
import sys

# nju resouces
njuIps = ['36.152.24.0', '211.162.81.0', '211.162.26.0', '112.25.191.0', '58.193.225.0',
          '221.6.40.128', '58.240.127.0', '218.94.142.0', '58.192.0.0', '202.127.247.0',
          '219.219.0.0', '210.29.240.0', '210.28.128.0', '202.38.126.0', '202.38.2.0',
          '202.38.3.0', '180.209.0.0', '202.119.0.0', '114.212.0.0', '58.193.224.0',
          '172.0.0.0', '10.254.253.0']

# execute command, and return the output
def execCmd(cmd):
    r = os.popen(cmd)
    out = r.read()
    r.close()
    return out

def addZeros(network):
    if re.search(r'^\d+$', network):
        return network + '.0.0.0'
    if re.search(r'^\d+\.\d+$', network):
        return network + '.0.0'
    if re.search(r'^\d+\.\d+\.\d+$', network):
        return network + '.0'
    if re.search(r'^\d+\.\d+\.\d+\.\d+$', network):
        return network
    return '0.0.0.0'

def generateMask(num):
    array = [0 for i in range(32)]
    for i in range(int(num)):
        array[i]=1
    ans = [0, 0, 0, 0]
    for k in range(0, 4):
        order = 128
        res = 0
        for j in range(8*k, 8*k+8):
            res = res + array[j]*order
            order = order/2
        ans[k] = int(res)
    return str(ans[0]) + '.' + str(ans[1]) + '.' + str(ans[2]) + '.' + str(ans[3])

def routeIsNeed(network, ips):
    tmp = re.split('\/', network)
    network = addZeros(tmp[0])
    # print('netwaork is: %s'%network)
    mask = generateMask(tmp[1])
    # print('mask is: %s'%mask)
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


if __name__ == "__main__":
    # Test whether the user is root
    if os.geteuid() != 0: 
        print("This program must be run as root. Aborting!")
        input('\nPlease press any key to exit...')
        sys.exit(1)

    print('Getting route tables...')
    result = execCmd("netstat -nr")
    route_list = re.findall(r'', result)
    ip_pattern = '\d+\.\d+\.\d+\.\d+'
    pattern = '\d+(\.\d+)?(\.\d+)?(\.\d+)?\/\d+\s+'+ip_pattern
    route_list = re.findall(r'('+pattern+')', result)
    ip_gateway = ''
    for rl in route_list:
        # print(rl[0])
        if re.search(r'114\/9', rl[0]):
            row = re.split(r'\s+', rl[0])
            ip_gateway = row[1]
            # print(ip_gateway)
            break
    print('Get route tables successful!')
    
    # delete useless route tables
    print('=========================================================')
    print('Cheking and deleting useless route tables...')
    routeLen = len(route_list)
    deleteCount = 0
    preProgress = -1
    for idx,rl in enumerate(route_list):
        row = re.split(r'\s+', rl[0])
        if row[1] == ip_gateway and routeIsNeed(row[0], njuIps) == False:
            # sudo route -v delete -net 10.10.12.0 -gateway 10.10.12.1
            execCmd("sudo route -v delete -net " + row[0] + " -gateway " + row[1])
            deleteCount = deleteCount+1
        currProgress = round(100*(idx+1)/routeLen)
        if(currProgress != preProgress):
            preProgress = currProgress
            print(str(currProgress)+"%", end=' ')
            sys.stdout.flush()

    print("\nDeleted %d useless routing tables successful!"%deleteCount)
    print('=========================================================')
    input('\nPlease press any key to exit...')