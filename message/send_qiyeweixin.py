import os
import requests
from jenkins import Jenkins

# ✅ 修复 URL 错误
jenkins_url = "http://112.126.74.187:8080/"
# ✅ 添加 timeout 避免 requests 错误
server = Jenkins(jenkins_url, username='root', password='123456', timeout=10)

job_name = "job/02ces"
job_url = server.get_info(job_name)['url']
job_last_number = server.get_info(job_name)['lastBuild']['number']
report_url = job_url + str(job_last_number) + '/allure'


def push_message():
    content = {}
    file_path = '/var/jenkins_home/workspace/02ces/allure-report/export/prometheusData.txt'
    with open(file_path) as f:
        for line in f.readlines():
            launch_name = line.strip().split(' ')[0]
            num = line.strip().split(' ')[1]
            content[launch_name] = num

    print(content)

    passed_num = content.get('launch_status_passed', '0')
    failed_num = content.get('launch_status_failed', '0')
    broken_num = content.get('launch_status_broken', '0')
    skipped_num = content.get('launch_status_skipped', '0')
    case_num = content.get('launch_retries_run', '0')

    webhook = "https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=aa4c8983-c1df-45c4-9b21-b96ac1d42850"
    content = {
        "msgtype": "text",
        "text": {
            "content": "接口自动化脚本执行结果：\n运行总数：" + case_num
                       + "\n通过数量：" + passed_num
                       + "\n失败数量：" + failed_num
                       + "\n阻塞数量：" + broken_num
                       + "\n跳过数量：" + skipped_num
                       + "\n构建地址：\n" + job_url
                       + "\n报告地址：" + report_url
        }
    }

    response = requests.post(url=webhook, json=content, verify=False)
    print("推送结果状态码:", response.status_code)
    print("响应内容:", response.text)


push_message()
