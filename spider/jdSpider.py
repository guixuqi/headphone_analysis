import json
import os
import re
import time
from lxml import etree
import requests
from libs.config import jd_rank_url, jd_detail_url, jd_review_url, datas_file
from libs.utils import get_ua, js2py
import pandas as pd, numpy, openpyxl, xlrd
from retrying import retry


class JDSpider:
    def __init__(self):
        self.list_url = jd_rank_url
        self.headers = {"user-agent": get_ua()}
        # self.headers = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.70 Safari/537.36"}
        self.url_main = "https:"
        self.detail_url = jd_detail_url
        self.review_url = jd_review_url
        self.list_datas = []
        requests.adapters.DEFAULT_RETRIES = 5  # 增加重连次数
        self.session = requests.session()
        self.session.keep_alive = False  # 关闭多余连接

    @retry(stop_max_attempt_number=5)
    def parse_url(self, url, headers):
        resp = self.session.get(url, headers=headers, timeout=60)
        html = etree.HTML(resp.text)
        return html

    def parse_list_data(self, html, list_datas):
        lis = html.xpath("//ul[@class='gl-warp clearfix']/li[@class='gl-item']")
        for li in lis:
            dicts = {}
            try:
                sku_id = li.xpath("./div/@data-sku")[0]
                # try:
                #     img_url = self.url_main + li.xpath(".//div[@class='p-img']/a/img/@src")[0]
                # except:
                #     try:
                #         img_url = self.url_main + li.xpath(".//div[@class='p-img']/a/img/@source-data-lazy-img")[0]
                #     except:
                #         img_url = ""
                title = li.xpath(".//div[@class='p-name']//em/text()")[0].strip()
                shop_name = li.xpath(".//div[@class='p-shop']/@data-shop_name")[0]
                price = self.parse_price_data(sku_id)[0]["p"]
                # price = float("%.2s" % price)
                comment_count = self.parse_comments_data(sku_id)["CommentsCount"][0]["CommentCountStr"]
                comment_count = comment_count.replace("+", "")
                comment_count = int(float(comment_count.replace("万", "")) * 10000) if re.search("万", comment_count) else int(float(comment_count))
            except:
                continue
            dicts["sku_id"] = sku_id
            print(sku_id)
            # dicts["img_url"] = img_url
            dicts["title"] = title
            dicts["shop_name"] = shop_name
            dicts["price"] = price
            dicts["comment_count"] = comment_count
            list_datas.append(dicts)
        next_href = html.xpath("//a[@class='pn-next']/@href")
        self.list_url = "https://list.jd.com/" + next_href[0] if next_href else ""
        return list_datas

    @retry(stop_max_attempt_number=5)
    def parse_price_data(self, sku_id):
        url = "https://p.3.cn/prices/mgets?skuIds={}".format("J_" + sku_id)
        resp = self.session.get(url, headers=self.headers)
        return json.loads(resp.text)

    @retry(stop_max_attempt_number=5)
    def parse_comments_data(self, sku_id):
        url = "https://club.jd.com/comment/productCommentSummaries.action?referenceIds={}".format(sku_id)
        resp = self.session.get(url, headers=self.headers)
        return json.loads(resp.text)

    def parse_detail_data(self, html, dict_data):
        brand = html.xpath("//div[@class='p-parameter']/ul[@class='p-parameter-list']/li/@title")
        try:
            ul = html.xpath("//div[@class='p-parameter']/ul[@class='parameter2 p-parameter-list']")[0]
        except:
            return {}
        name = ul.xpath("./li[contains(text(),'商品名称')]/@title")
        # number = ul.xpath("./li[contains(text(),'商品编号')]/@title")
        weight = ul.xpath("./li[contains(text(),'商品毛重')]/@title")
        production = ul.xpath("./li[contains(text(),'商品产地')]/@title")
        line_type = ul.xpath("./li[contains(text(),'连接类型')]/@title")
        purpose = ul.xpath("./li[contains(text(),'用途')]/@title")
        wear = ul.xpath("./li[contains(text(),'佩戴方式')]/@title")
        brand = brand[0] if brand else ""
        name = name[0] if name else ""
        # number = number[0] if number else ""
        weight = weight[0] if weight else ""
        production = production[0] if production else ""
        line_type = line_type[0] if line_type else ""
        purpose = purpose[0] if purpose else ""
        wear = wear[0] if wear else ""
        dict_data["brand"] = brand
        dict_data["name"] = name
        # dict_data["number"] = number
        dict_data["weight"] = weight
        dict_data["production"] = production
        dict_data["line_type"] = line_type
        dict_data["purpose"] = purpose
        dict_data["wear"] = wear
        return dict_data

    @retry(stop_max_attempt_number=5)
    def parse_review_url(self, data):
        resp = self.session.get(self.review_url, headers=self.headers, params=data, timeout=60)
        return resp.text

    def parse_review_data(self, comm_dict, writer, sku_id):
        try:
            comment_summary = comm_dict['comments']  # 得到包含评论的字典组成的列表
        except:
            return
        if len(comment_summary) < 1:
            return
        comment_lists = []
        for comment in comment_summary:  # 遍历每个包含评论的字典，获得评论和打分
            comment_dict = {}
            try:
                comment_dict["skuId"] = sku_id  # 评论ID
                comment_dict["reviewId"] = comment['guid']  # 评论ID
                comment_dict["reviewTime"] = comment['creationTime']  # 评论时间
                comment_dict["content"] = ''.join(comment['content'].split())
                comment_dict["score"] = comment['score']  # 用户打分
                comment_dict["nickName"] = comment['nickname']  # 用户名
                comment_dict["productColor"] = comment['productColor'] if comment['productColor'] else ""  # 颜色
                comment_dict["productSize"] = comment['productSize'] if comment['productSize'] else ""  # 版本
                print(comment_dict["nickName"])
                comment_lists.append(comment_dict)
            except:
                continue
        self.save_data(writer, comment_lists, "reviews")
        writer.save()
        # 通过一页评论数量判断是不是最后一页评论
        if len(comment_summary) < 10:
            return True

    def review_datas(self, sku_id, list_dict, writer):
        data = {
            'productId': sku_id,
            'score': 0,
            'sortType': 6,  # 以时间排序
            'page': 0,
            'pageSize': 10,
            'isShadowSku': 0,
            'rid': 0,
            'fold': 1
        }
        for i in range(1):
            try:
                data['page'] = i
                html = self.parse_review_url(data)
                if not html:
                    continue
                comm_dict = js2py(html)
                if i == 0:
                    try:
                        productCommentSummary = comm_dict['productCommentSummary']
                        score = productCommentSummary['goodRateShow']
                        score = float(score)
                    except:
                        score = 0
                    list_dict["score"] = score
                    tags = []
                    try:
                        hotCommentTagStatistics = comm_dict['hotCommentTagStatistics']
                        for tag in hotCommentTagStatistics:
                            # tag_dict = {}
                            # tag_dict["name"] = tag["name"]
                            # tag_dict["count"] = tag["count"]
                            # tags.append(tag_dict)
                            tag_str = tag["name"] + "({})".format(tag["count"])
                            tags.append(tag_str)
                    except:
                        pass
                    tags_str = ",".join(tags)
                    list_dict["tags"] = tags_str
                finish = self.parse_review_data(comm_dict, writer, sku_id)
                if finish:
                    break
            except Exception as e:
                continue
            time.sleep(2)
            if i % 10 == 0:
                time.sleep(5)
        return list_dict

    def save_data(self, writer, datas, sheet_name):
        if os.path.exists(datas_file):
            try:
                df = pd.read_excel(datas_file, sheet_name=sheet_name)
                df = df.append(datas)
            except:
                df = pd.DataFrame(datas)
        else:
            df = pd.DataFrame(datas)
        df.to_excel(excel_writer=writer, columns=[i for i in datas[0].keys()], index=False, encoding="utf-8", sheet_name=sheet_name)

    def run(self):
        writer = pd.ExcelWriter(datas_file)
        while self.list_url:
            list_datas = []
            self.list_datas = []
            # 请求列表页
            list_html = self.parse_url(self.list_url, self.headers)
            # 分析列表页(抓取和保存)
            list_datas = self.parse_list_data(list_html, list_datas)
            for dict_data in list_datas:
                sku_id = dict_data["sku_id"]
                # 拼接详情页url和headers
                detail_url = self.detail_url.format(sku_id)
                self.headers['Referer'] = self.list_url
                # 请求详情页
                detail_html = self.parse_url(detail_url, self.headers)
                # 分析详情页(抓取和保存)
                dict_datas = self.parse_detail_data(detail_html, dict_data)
                # 分析评论页(请求,抓取和保存)
                self.headers['Referer'] = detail_url
                dict_datas = self.review_datas(sku_id, dict_datas, writer)
                self.list_datas.append(dict_datas)
            self.save_data(writer, self.list_datas, "lists")
            writer.save()
        writer.close()


if __name__ == '__main__':
    jd = JDSpider()
    jd.run()