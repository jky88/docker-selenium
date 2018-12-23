1） 查找Selenium相关镜像
命令为：
docker search selenium

此次我们需要3个镜像（1个Hub，2个Node），同时为了可以直观的看到实验结果，决定选用自带VNC Server的版本。获取官网上的镜像命令为：
docker pull selenium/hub
docker pull selenium/node-firefox-debug
docker pull selenium/node-chrome-debug
如果下载镜像不成功，就多试几次，再不行就翻墙再下载。

2）输入查看镜像列表命令为：
docker images

3.运行docker镜像
镜像已经准备好了以后，接下来就是运行镜像，在docker的世界里叫做启动容器，通俗点就是启动了虚拟机。
输入以下命令：
docker run -d --name selenium-hub -p 4444:4444 selenium/hub
docker run -d -P -p 5900:5900 --link selenium-hub:hub selenium/node-chrome-debug
docker run -d -P -p 5901:5900 --link selenium-hub:hub selenium/node-firefox-debug
docker ps -a
以上四条命令的作用分别是：
第一条：启动一个Hub的镜像，名称为selenium-hub
第二条：启动一个node的镜像（带chrome浏览器），和vnc通信的端口为5900
第三条：启动一个node的镜像（带firefox浏览器），和vnc通信的端口为5901
检查hub和node的链接情况，用命令：
docker logs selenium-hub

使用过Selenium Grid的人都应该比较熟悉此处的日志，实际上就是用java 去启动selenium-server-standalone-×××.jar，然后注册node到selenium-server上。
最后通过浏览器来访问：http://[hubip]:4444/grid/console 的时候会出现以下的界面：
(此处的URL里面的不是4444端口是因为，CC先生的虚拟机用的是NAT网络模式，所以将docker容器里的4444端口映射成了宿主机的8127)

4.安装VNC viewer，查看docker容器
vnc viewer是一款优秀的远程控制工具软件
官网下载地址：https://www.realvnc.com/en/connect/download/viewer/
安装好以后File->New connection,在弹出的界面中输入node的ip和端口号，保存后启动。
连接，会要求输入密码，默认密码就是secret
（注：图片中的端口号为8128而不是5900同样是因为NAT的缘故做了映射，正常情况下就是ip:5900）

5.打开Pycharm运行测试脚本
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

 #指定运行主机与端口号,也就是上一步在浏览器中输入的地址，只是换了之后的相对路径/grid/console换为/wd/hub

driver = webdriver.Remote(
     command_executor='http://172.16.0.21:8127/wd/hub',
     desired_capabilities=DesiredCapabilities.CHROME)

base_url='http://www.xiami.com/song/1797262971'
driver.get(base_url)
driver.implicitly_wait(300)
driver.find_element_by_link_text('立即播放').click()
time.sleep(6000)
driver.close()

此时debug模式的好处就体现出来了。你可以在第4步打开的VNC Viewer窗口中观看到完整的脚本运行过程。

至此为止，我们也就把Docker+Selenium Grid+Python的方式构建好了一个分布式测试环境。（并在虾米音乐上为马云爸爸打call了无数次）

彩蛋：
用于Docker中的不确定性和做实验时也许新建了很多个容器，看起来很多很烦，你可以试试以下几个命令：

清除(关闭全部容器) ：docker kill $(docker ps -a -q)
删除全部容器：docker rm $(docker ps -a -q)
再次查看容器情况，运行：docker ps –a 发现整个世界都清净了。

后续还可以探索的方向还有：

页面上中文的乱码问题
和RF的结合，生成可行的测试报告
和Jenkins结合，完成整个持续集成
定制适合业务场景的Dockerfile
etc

参考：
https://github.com/SeleniumHQ/docker-selenium
https://testerhome.com/topics/8517
http://www.docker.org.cn/book/docker/what-is-docker-16.html

作者：CC先生之简书
链接：https://www.jianshu.com/p/382ebaa4b7a9
來源：简书
简书著作权归作者所有，任何形式的转载都请联系作者获得授权并注明出处。
