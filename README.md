# taptap_request-clouddb
taptap 网址数据爬虫保存至云DB服务器（当前仅有排行榜数据 ，后续会开发固定监控数据）
主要依赖 request\pymysql库来进行实现，本人为anaconda环境下运行
-------------------------------------------------------------------------------------
当前主要是通过对taptap返回的XHR文件中请求网址进行request操作，当前请求网址中主要参数为from(从第几名开始默认0）、limit（单次请求app数量，max=15)、type_name（排行榜分类）来获取对应参数数据；
本次选择的也是热门、预约、热玩三个榜进行爬取前50名的数据。其中热玩榜在from=30时仅会返回9个数据，导致热玩榜数据可能会爬取59个，可以通过mysql语句进行剔除

-------------------------------------------------------------------------------------
![image](https://github.com/user-attachments/assets/28e5a9f6-8228-47a6-90fc-f96dda826be6)
通过taptap加载的xhr文件可以找到排行榜游戏数据的来源
其中UID后相关信息为无关信息
![image](https://github.com/user-attachments/assets/472e5f14-aa3f-4f98-97cd-5d5231bb97d2)
![image](https://github.com/user-attachments/assets/c2c333f5-7db6-458b-afd8-6a91260be239)
可以通过该xhr文件获得请求网址以及header相关信息
