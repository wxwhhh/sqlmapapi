import requests
import json
import time

def sqlmapapi(url):
    data = {'url': url}
    headers = {'Content-Type': 'application/json'}
    # 1.创建任务，获取ID号
    test_new_url = 'http://127.0.0.1:8775/task/new'
    resp = requests.get(test_new_url)
    test_id = resp.json()["taskid"]
    if 'success' in resp.content.decode('utf-8'):
        print('第一步任务创建成功！！')
        # 2.设置任务ID的扫描信息
        task_set_url = 'http://127.0.0.1:8775/option/' + test_id + '/set'
        task_set_resp = requests.post(task_set_url, data=json.dumps(data), headers=headers)
        #print(task_set_resp.content.decode('utf-8'))
        if 'success' in task_set_resp.content.decode('utf-8'):
            print('第二步任务信息创建成功！！')
            # 3.启动对应id的扫描任务
            task_start_url = 'http://127.0.0.1:8775/scan/' + test_id + '/start'
            task_start_resp = requests.post(task_start_url, data=json.dumps(data), headers=headers)
            #print(task_start_resp.content.decode('utf-8'))
            if 'success' in task_start_resp.content.decode('utf-8'):
                print('第三步启动对应id的扫描任务！！')
            while 1:
                # 4.读取扫描状态
                task_status_url = 'http://127.0.0.1:8775/scan/' + test_id + '/status'
                task_status_resp = requests.get(task_status_url)
                #print(task_status_resp.content.decode('utf-8'))
                if 'running' in task_status_resp.content.decode('utf-8'):
                    print('第四步：SQLMAPAPI 扫描中！！')
                    pass
                else:
                    #5.扫描结果查看打印保存
                    task_data_url = 'http://127.0.0.1:8775/scan/' + test_id + '/data'
                    task_status_resp = requests.get(task_data_url).content.decode('utf-8')
                    with open(r'scan_sql.txt','a+') as f:
                        f.write(url+'\n')
                        f.write(task_status_resp +'\n')
                        f.write("！！+++++++++++++++++++++++++++++++扫描目标分割线+++++++++++++++++++++++++++++++++++！！"+ '\n')
                        f.close()
                        #print(task_status_resp.content.decode('utf-8'))
                    task_delete_id = 'http://127.0.0.1:8775/task/' + test_id + '/delete'
                    task_delete_resp = requests.get(task_delete_id).content.decode('utf-8')
                    if 'success' in task_delete_resp:
                        print("第五步：当前任务结束！删除任务")
                    break
            time.sleep(3)

if __name__ == '__main__':
    for url in open('ip.txt','r'):
        url = url.rstrip('\n')
        sqlmapapi(url)