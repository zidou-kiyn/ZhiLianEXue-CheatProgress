# python程序之速刷【智联E学】-大学生职业规划短视频观看任务

## 前言

![](http://lsky.zidoukn.cn/i/2024/10/23/6718c6456ba08.png)

大学生久受职业规划课程之苦，在此分析网站后开发出了全自动并行刷课程的程序

## 源码仓库地址

[Github-zidou-kiyn/ZhiLianEXue-CheatProgress](https://github.com/zidou-kiyn/ZhiLianEXue-CheatProgress)

[Gitee-zidoukn/ZhiLianEXue-CheatProgress](https://gitee.com/zidoukn/ZhiLianEXue-CheatProgress)

## 使用教程

### 配置文件-cookies & params

1. 在浏览器端进入[智联E学](https://course.zhaopin.com/)网站，进入课程学习界面，**F12**打开浏览器开发者工具，切换到**网络**，**F5**刷新网页，在分类中选择**Fetch/XHR![](http://lsky.zidoukn.cn/i/2024/10/23/6718dc24e495e.png)**
2. 点击如上图所示的请求中 `https://course.zhaopin.com/api/studentclasstask/getcourseinfo?******`，在标头处将cookie的内容复制到**cookies.txt**中![](http://lsky.zidoukn.cn/i/2024/10/23/6718cb12e66d2.png)![](http://lsky.zidoukn.cn/i/2024/10/23/6718cb4c174ab.png)
3. 将载荷中各个参数对应的值替换到**params.json**中，注意，这边不是直接全部复制过去，需要对位替换![](http://lsky.zidoukn.cn/i/2024/10/23/6718cb8476665.png)![](http://lsky.zidoukn.cn/i/2024/10/23/6718cbf26ded9.png)

### 启动程序

配置好参数后即可按照下面两种方式运行，全自动完成视频任务，需要的时长**约为最长的视频的时长**，程序重新运行不会重新开始刷进度，可延续，所以直接运行即可，省心

#### python运行

使用清华源安装第三方库 `requests`、`loguru`

```cmd
pip install requests -i https://pypi.tuna.tsinghua.edu.cn/simple

pip install loguru -i https://pypi.tuna.tsinghua.edu.cn/simple
```

安装好后即可直接运行

#### windows一键运行

直接启动**main.exe**程序即可

## 效果展示

![](http://lsky.zidoukn.cn/i/2024/10/23/6718d043dfe48.png)![](http://lsky.zidoukn.cn/i/2024/10/23/6718d043dfe48.png)
![](http://lsky.zidoukn.cn/i/2024/10/23/6718cd662d663.png)
