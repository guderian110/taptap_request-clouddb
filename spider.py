import json
import requests
import time
import random
import read_json_file
from read_json_file import response_path
from read_json_file import load_config,save_json_to_file
from database import connect_to_db,store_data_to_db


config = load_config(read_json_file.json_path)
base_url = config['base_url']
cloud_db_config = config['cloud_db_config']
headers = config['headers']


# 遍历请求
def fetch_data():
    print("开始执行爬取数据任务...")  # 确认 fetch_data 被执行

    connection = connect_to_db()  # 创建数据库连接
    if not connection:
        print("无法连接到数据库，程序退出！")
        return
    
    types = ['hot', 'reserve', 'pop']  # 榜单类型
    
    for list_type in types:
        all_game_data = []  # 用来保存所有请求的游戏数据
        total_fetched = 0  # 当前已获取的总游戏数量
        
        while total_fetched < 50:  # 只要获取的数据量不足 50 条，继续请求
            limit = 10  # 默认每次请求的数量为 10
            current_from_value = total_fetched  # 从已经获取的数据量开始

            url = base_url.format(current_from_value, limit, list_type)
            random_wait_time = random.uniform(10, 20)
            time.sleep(random_wait_time)
            print(f"请求 URL: {url}")  # 打印请求 URL

            try:
                response = requests.get(url, headers=headers)
                print(f"响应状态码: {response.status_code}")  # 打印响应状态码

                if response.status_code == 200:
                    response.encoding = 'utf-8'
                    data = response.json()  # 尝试将响应内容转为 JSON
                    game_list = data["data"]["list"]
                    current_fetched = len(game_list)
                    total_fetched += current_fetched
                    all_game_data.extend(game_list)  # 合并数据
                    print(f"成功获取 {list_type} 榜单的数据: 从 {current_from_value} 请求的数据，当前已获取 {total_fetched} 条数据")

                    # 检查是否已达到50条数据
                    if total_fetched >= 50:
                        print(f"已成功获取 {total_fetched} 条数据，停止请求")
                        break  # 退出内层循环

                else:
                    print(f"请求失败: {response.status_code} - {response.text}")

            except requests.exceptions.RequestException as e:
                print(f"请求发生异常: {e}")

            time.sleep(20)  # 限制请求频率

        # 将所有获取的数据传递给 `store_data_to_db` 进行存储
        store_data_to_db(connection, {"data": {"list": all_game_data}}, list_type)

    save_json_to_file({"data": {"list": all_game_data}}, response_path) 
    connection.close()  # 关闭数据库连接

if __name__ == "__main__":
    fetch_data()