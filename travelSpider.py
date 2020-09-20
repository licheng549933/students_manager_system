import time
import re
import requests
import pymysql

pattern_01 = '<li class="clearfix">.*?/post/(?P<user_id>\d+).*?</li>'
pattern_02 = '.*?<span class="time f666 with-point">(?P<created_time>.*?)</span>.*?<h1 class="title f333 clearfix".*?>(?P<title>.*?)</h1>.*?<div class="re-summary" ' \
             'id="mainContent">.*?<p>(?P<content>.*?)</p>                    </div>'
pattern_topic_img = """<a class="avatar-pic" href="/post/(?P<u_id>\d+)" target="_blank">.*?<img alt=".*?" src="(?P<title_img>.*?)"\s"""

def get_userId_list():
    """获取日志id列表"""
    userId_list = []
    for i in range(1, 88):
        url = 'http://www.iqingyi.com/notes/p/{}'.format(i)
        html = requests.get(url=url).text
        res_list = re.findall(pattern_01, html, re.S)
        for id in res_list:
            userId_list.append(id)
    return userId_list

def get_detail(user_id):
    """获取详情页面"""
    two_url = 'http://www.iqingyi.com/post/{}'.format(user_id)
    res = requests.get(url=two_url)
    str_res = re.search(pattern_02, res.text, re.S)
    user_id = user_id
    created_time = str_res.group('created_time').strip()
    content = str_res.group('content').strip()
    title = str_res.group('title').strip()
    return user_id, title, created_time, content

def get_topic_img(notes_id):
    """获取一级页面的首页展示图地址,参数-日志地址"""
    topic_img_dict = {}
    for i in range(1, 7):
        adsress = 'http://www.iqingyi.com/notes/p/{}'.format(i)
        html = requests.get(url=adsress).text
        res = re.findall(pattern_topic_img, html, re.S)
        for tup in res:
            topic_img_dict[tup[0]] = tup[1]
    return topic_img_dict[notes_id]

def get_total_dict(user_id_list):
    """获取总详情页,二级页面汇总"""
    total_detail_dict = {}
    user_id_list = user_id_list
    for id in user_id_list:
        detail_tuple = get_detail(id)
        total_detail_dict[detail_tuple[0]] = {'title': detail_tuple[1], 'created_time': detail_tuple[2],
                                              'content': detail_tuple[3]}
    return total_detail_dict

def insert_data(data_list):
    """数据持久化"""
    database = pymysql.connect(host='127.0.0.1',
                               port=3306,
                               user='root',
                               password='123456',
                               database='lc_549933',
                               charset='utf8'
                               )
    sql_sentense = 'insert into travel_details (user_id,note_title,created_time,content) values (%s,%s,%s,%s)'
    cur_obj = database.cursor()
    cur_obj.execute("set names utf8")
    try:
        cur_obj.executemany(sql_sentense, data_list)
    except Exception as e:
        print(e)
    database.commit()

def get_execute_list(userId_list=None):
    """返回看可以执行executemany的列表数据,[(),(),()...]"""
    total_detail_dict = get_total_dict(userId_list)
    execute_list = []
    for i in total_detail_dict:
        execute_list.append((i,
                             total_detail_dict[i]['title'],
                             total_detail_dict[i]['created_time'],
                             total_detail_dict[i]['content']))
    return execute_list

if __name__ == '__main__':
    #start_time
    t1 = time.localtime()
    fomated_time_01 = "{}:{}:{}".format(t1.tm_hour, t1.tm_min, t1.tm_sec)
    print(fomated_time_01)
    print("peocess is running...")
    #主执行程序
    user_id_list = get_userId_list()
    executeMany_list = get_execute_list(userId_list=user_id_list)
    insert_data(executeMany_list)
    #end_time
    t2 = time.localtime()
    fomated_time_02 = "{}:{}:{}".format(t2.tm_hour, t2.tm_min, t2.tm_sec)
    print(fomated_time_02)