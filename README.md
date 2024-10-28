# 说明
这是深圳大学自动抢羽毛球场/网球场脚本，包含校区选择、球类选择、时间选择、场馆选择、添加同行人、支付的功能。羽毛球场/网球场是从还未被预约的场地中进行选择；支付是通过体育经费进行支付，运行前请确保体育经费充足。该脚本仅用于抢第二天的羽毛球场/网球场。

# 配置
python环境配置详见requirements.txt，同时还要确保电脑有安装Google Chrome和Chromedriver,Chromedriver的下载与安装位置详见 https://googlechromelabs.github.io/chrome-for-testing/ 和 https://blog.csdn.net/weixin_45798684/article/details/105356932 ，注意Google Chrome和Chromedriver的版本需匹配。

# 运行
运行前请先将information.txt中以下信息填写，具体要求看文件内介绍，注意要严格按照要求填写信息（若程序运行错误，很可能是信息没按照格式填写）   
```
chromedriver=
username=
password=
campus=
ball=
appointment=
venues=
payment_password=
companions_id=
```
填写完成后，在当天12:30前运行脚本，脚本会一直运行，直到12:30时开始并完成抢场才运行结束，若抢场成功，会显示“预约并支付成功”。  
在当天12:30后运行脚本，也可以对场地进行预约
