# 随机UA
import json
import random
import re


def get_ua():
    first_num = random.randint(55, 62)
    third_num = random.randint(0, 3200)
    fourth_num = random.randint(0, 140)
    os_type = [
        '(Windows NT 6.1; WOW64)', '(Windows NT 10.0; WOW64)', '(X11; Linux x86_64)',
        '(Macintosh; Intel Mac OS X 10_12_6)'
    ]
    chrome_version = 'Chrome/{}.0.{}.{}'.format(first_num, third_num, fourth_num)

    ua = ' '.join(['Mozilla/5.0', random.choice(os_type), 'AppleWebKit/537.36',
                   '(KHTML, like Gecko)', chrome_version, 'Safari/537.36']
                  )
    return ua


def js2py(html):
    try:
        # i = json.dumps(html)  # 将页面内容编码成json数据
        # j = json.loads(i)  # 将json数据解码为Python对象
        comment = re.findall(r'{"productAttr":.*}', html)  # 网页内容筛选
        comm_dict = json.loads(comment[0])  # 将json对象obj解码为对应的字典dict
    except:
        comm_dict = {}
    return comm_dict
