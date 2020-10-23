## CheatDetection
使用moss判断一个文件夹下所有学生的代码是否存在抄袭，运行完毕moss返回的网址输出在控制台中。

## CheckError
判断一个文件夹下学生的代码是否正确，相当于OJ的评分，需要自己构造输入和提供正确程序用来计算输出。

## GetScore
从oj上获取学生的成绩并写入到指定excel表中。

## Example
C/C++练习代码。

## RouteClean
由于南大VPN EasyConnet在开启后会进行全局代理，导致访问非校内资源卡顿，我们发现该VPN软件是通过在本地添加路由表的方式进行代理的，所以我们只要删除本地无用的路由表即可实现只在访问校内资源时通过VPN。

南大校内资源ip地址在登录EasyConnet可以看见，见njuUrl.txt。

RouteClean.exe由于利用cmd命令删除路由表，需要以管理员身份运行才有效。