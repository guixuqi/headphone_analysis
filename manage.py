import pdExc as pd

"""
1.标题关键词数量排行
2.价格区间0-100,100-300,300-1000,1000以上排行
3.品牌评论总数排行,品牌价格区间0-100,100-300,300-1000,1000以上排行
4.店铺数量排行,店铺评论总数排行
5.评论数量排行及好评分
6.评论分高低排行及评论量
7.连接类型,佩戴方式排行
8.评论量前3的型号排行及评论量
9.评论区间分布关系
10.价格区间0-100,100-300,300-1000,1000以上评论量排行
"""
url_rank = "https://list.jd.com/list.html?cat=652,828,842"


"""
单个产品
1.评论关键词TOP10
2.好中差评占比
3.不同颜色的评论占比
4.不同配置的评论占比
5.评论时间区间分析
"""

url = "https://top.jd.com/sale?cateId=653"