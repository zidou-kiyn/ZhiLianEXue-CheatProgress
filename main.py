import requests
import json
import time
import os
from loguru import logger

# 使用绝对路径,避免vscode打开文件忘记打开对应文件夹导致找不到文件 加强代码的稳健性
current_dir = os.path.dirname(os.path.abspath(__file__))
_cookies = os.path.join(current_dir, 'cookies.txt')
_params = os.path.join(current_dir, 'params.json')

# 过滤课程数据,提取必要的信息
def filter_class_data(data):
    filtered_data = {
        "classTaskId": data["data"]["classTaskId"],
        "id": data["data"]["id"],
        "chapterDTOS": []
    }

    for chapter in data["data"]["chapterDTOS"]:
        filtered_chapter = {
            "id": chapter["id"],
            "chapterLessions": []
        }
        for lesson in chapter["chapterLessions"]:
            filtered_lesson = {
                "fileName": lesson["fileName"],
                "id": lesson["id"],
                "newestProgress": lesson["newestProgress"],
                "rate": lesson["rate"],
                "totalTime": lesson["totalTime"]
            }
            filtered_chapter["chapterLessions"].append(filtered_lesson)
        filtered_data["chapterDTOS"].append(filtered_chapter)

    return filtered_data

# 移除已完成的课程
def remove_finished_lessons(class_info, finished_id):
    for chapter in class_info["chapterDTOS"]:
        chapter["chapterLessions"] = [
            lesson for lesson in chapter["chapterLessions"] if lesson["id"] not in finished_id
        ]

# 移除没有课程的章节
def remove_empty_chapters(class_info):
    class_info["chapterDTOS"] = [
        chapter for chapter in class_info["chapterDTOS"] if chapter["chapterLessions"]
    ]

# 加载cookies文件并转换为字典
def load_cookies():
    with open(_cookies,"r",encoding="utf-8") as f:
        cookies_str = f.read()
    cookies_dict = {}
    for cookie in cookies_str.split('; '):
        key, value = cookie.split('=', 1)
        cookies_dict[key] = value
    return cookies_dict

# 根据cookies生成请求头
def load_headers(cookies):
    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8',
        'priority': 'u=1, i',
        'referer': 'https://course.zhaopin.com/',
        'sec-ch-ua': '"Google Chrome";v="129", "Not=A?Brand";v="8", "Chromium";v="129"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'token': cookies['token'],
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
    }
    return headers

# 加载请求参数
def load_params():
    with open(_params,"r",encoding="utf-8") as f:
        params = json.loads(f.read())
    return params

# 获取课程信息并过滤
def get_class_info(cookies, headers, params):
    response = requests.get(
        'https://course.zhaopin.com/api/studentclasstask/getcourseinfo',
        params=params,
        cookies=cookies,
        headers=headers,
    )

    return filter_class_data(response.json())

# 模拟进度上报
def cheat_progress(cookies, headers, params,
                   classId, chapterId, lessionId,
                   courseId, classTaskId, reportTime,
                   progress, reportType):
    json_data = {
        'classId': classId,
        'chapterId': chapterId,
        'lessionId': lessionId,
        'courseId': courseId,
        'classTaskId': classTaskId,
        'reportTime': reportTime,
        'progress': progress,
        'reportType': reportType,
    }
    response = requests.post(
        'https://course.zhaopin.com/api/studyrecord/studentlearnrecord',
        params=params,
        cookies=cookies,
        headers=headers,
        json=json_data,
    )
    return response


# 加载cookies、请求头和参数
cookies = load_cookies()
headers = load_headers(cookies)
params = load_params()

finished_id = []  # 已完成课程的ID列表
count = 0  # 循环计数器

# 配置日志输出到文件，并设置文件大小达到1MB后自动轮转
logger.add("run.log", rotation="1 MB")  # 文件达到1MB后自动轮转

try:
    while True:
        class_info = get_class_info(cookies, headers, params)

        remove_finished_lessons(class_info, finished_id)  # 移除已完成课程
        remove_empty_chapters(class_info)  # 移除空章节

        if len(class_info["chapterDTOS"]) <= 0:
            logger.info("视频任务完成 退出程序")
            break

        for chapter in class_info['chapterDTOS']:
            for lession in chapter['chapterLessions']:
                logger.info("当前课程-{}".format(lession['fileName']))
                if lession['rate'] >= 1:
                    finished_id.append(lession['id'])
                    logger.info("当前课程已完成 课程id添加到完成列表中")
                    continue

                classId = params['classId']
                chapterId = chapter['id']
                lessionId = lession['id']
                courseId = class_info['id']
                classTaskId = class_info['classTaskId']

                if count <= 0:
                    reportTime = int(time.time())
                    progress = lession['newestProgress']
                    if progress <= 1:
                        progress = 1
                    reportType = 1
                    response = cheat_progress(cookies, headers, params,
                                   classId, chapterId, lessionId,
                                   courseId, classTaskId, reportTime,
                                   progress, reportType)
                    logger.info("当前课程尚未开始观看 开始请求")
                    if response.status_code != 200:
                        logger.error("开始观看失败 报错信息:{}".format(response.text))
                    continue

                if lession['newestProgress'] > 0:
                    reportTime = int(time.time())
                    progress = lession['newestProgress'] + 30
                    if progress > lession['totalTime']:
                        progress = lession['totalTime']
                    reportType = 2
                    response = cheat_progress(cookies, headers, params,
                                   classId, chapterId, lessionId,
                                   courseId, classTaskId, reportTime,
                                   progress, reportType)
                    logger.info("当前课程正在观看 开始刷新")
                    if response.status_code != 200:
                        logger.error("刷新记录失败 报错信息:{}".format(response.text))
                    continue

        count += 1
        logger.info("等待30s继续刷新记录")
        time.sleep(30)
except Exception as e:
    logger.exception("程序错误退出")  # 捕获所有异常并记录堆栈信息

time.sleep(3)  # 程序结束前等待3秒
