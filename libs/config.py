import os

jd_rank_url = "https://list.jd.com/list.html?cat=652,828,842"
# jd_rank_url = "https://list.jd.com/list.html?cat=652,828,842&page=239&sort=sort_totalsales15_desc&trans=1&JL=6_0_0#J_main"
jd_detail_url = "https://item.jd.com/{}.html"
jd_review_url = "https://sclub.jd.com/comment/productPageComments.action"
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
datas_file = os.path.join(BASE_DIR, "libs\\jd_datas.xlsx")
# datas_file = BASE_DIR.join("/libs/jd_review_datas.xlsx")