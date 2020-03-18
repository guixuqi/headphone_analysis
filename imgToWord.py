import base64
import json
from time import sleep

import requests

# client_id 为官网获取的AK， client_secret 为官网获取的SK
client_id = "RAWIhSeh96TRMm19DNmoxHVl"
client_secret = "6RIYGPd3vXGq1mZDbd2rbBkke4w47tqg"

file_urls = []
# file_urls.append("https://img-blog.csdnimg.cn/20190917201520610.jpg?")
# file_urls.append("https://img-blog.csdnimg.cn/20190917202659674.jpg?")
# file_urls.append("https://img-blog.csdnimg.cn/20190917203723359.jpg?")
# file_urls.append("https://img-blog.csdnimg.cn/20190917210840105.jpg?")
# file_urls.append("https://img-blog.csdnimg.cn/20190917210851894.jpg?")
# file_urls.append("https://img-blog.csdnimg.cn/20190917214821489.jpg?")
# file_urls.append("https://img-blog.csdnimg.cn/20190917214834744.jpg?")
# file_urls.append("https://img-blog.csdnimg.cn/2019091721564187.jpg?")
# file_urls.append("https://img-blog.csdnimg.cn/20190917220242218.jpg?")
# file_urls.append("https://img-blog.csdnimg.cn/20190917222255724.jpg?")
# file_urls.append("https://img-blog.csdnimg.cn/20190917222311673.jpg?")
# file_urls.append("https://img-blog.csdnimg.cn/20190917224133411.jpg?")
# file_urls.append("https://img-blog.csdnimg.cn/20190917225350719.jpg?")
file_urls.append("https://img-blog.csdnimg.cn/20190918001140496.jpg?")


def get_access_token():
    url = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(client_id, client_secret)
    response = requests.get(url)
    if response:
        access_token = response.json()["access_token"]
        # print(access_token)
        return access_token


def img_to_word(file_urls):
    # 通用文字识别
    request_url = "https://aip.baidubce.com/rest/2.0/ocr/v1/general_basic"
    # 二进制方式打开图片文件
    # f = open(file, 'rb')
    # img = base64.b64encode(f.read())
    path = "C:/Users/hhh/Desktop/headphone_analysis/manage.py"
    with open(path, "a+") as fp:
        for file_url in file_urls:
            sleep(1)
            params = {"url": file_url}
            access_token = get_access_token()
            request_url = request_url + "?access_token=" + access_token
            headers = {'content-type': 'application/x-www-form-urlencoded'}
            response = requests.post(request_url, data=params, headers=headers)
            if response:
                codes = response.json()["words_result"]
                print(codes)
                for code in codes:
                    try:
                        fp.write(code["words"] + "\n")
                    except:
                        pass


if __name__ == '__main__':
    img_to_word(file_urls)