import pymysql 
import read_json_file
from read_json_file import load_config
import time

config = load_config(read_json_file.json_path)
cloud_db_config = config['cloud_db_config']



# 连接到数据库（只需连接一次）
def connect_to_db():
    try:
        print("尝试连接到数据库...")
        connection = pymysql.connect(
            host=cloud_db_config['host'],
            database=cloud_db_config['database'],
            port=cloud_db_config['port'],
            user=cloud_db_config['user'],
            password=cloud_db_config['password']
        )
        print("成功连接到数据库")
        return connection
    except pymysql.MySQLError as e:
        print(f"连接数据库时发生错误: {e}")
    except Exception as e:
        print(f"发生未知错误: {e}")
        
        
# 存储数据到数据库
def store_data_to_db(connection, data, list_type):
    cursor = connection.cursor()

    insert_query = """
    INSERT INTO `guderian`.`taptap_data` (app_id, game_name, score, request_time, list_type, download_count, reserve_count, rank) 
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    
    app_data = []  # 用于存储所有要插入的数据
    for index, game in enumerate(data["data"]["list"], start=1):
        app = game["app"]
        app_id = app["id"] 
        game_name = app["title"]
        stat = app["stat"]
        score = stat["rating"]["score"]
        request_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

        # 根据榜单类型选择有效的 `count` 字段
        if list_type == "hot":
            # 在 `hot` 类型中，先检查 `reserve_count`，如果无效则使用 `hits_total`
            download_count = stat.get('hits_total', 0)  # 获取下载数量
            reserve_count = stat.get('reserve_count', 0)  # 获取预约数量
        else:
            # 在其他类型下，默认使用 `hits_total` 或 `reserve_count`
            download_count = stat.get('hits_total', 0)
            reserve_count = stat.get('reserve_count', 0)
        
        rank = index  # 游戏的名次
        app_data.append((app_id, game_name, score, request_time, list_type, download_count, reserve_count, rank))

    if app_data:
        try:
            cursor.executemany(insert_query, app_data)  # 批量插入
            connection.commit()  # 提交事务
            print(f"成功插入 {len(app_data)} 条数据")
        except pymysql.MySQLError as e:
            print(f"数据库错误: {e}")
            connection.rollback()  # 出错时回滚事务
        finally:
            cursor.close()  # 确保游标关闭
    else:
        print("没有可插入的数据")