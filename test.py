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

def standard_data():
    df = pd.read_excel(GOODS EXCEL PATH)
    #1、将价格转化为整数型
    raw sales df['sales], values
    new sales [
    for sales in raw sales
    sales sales[:-3I
    sales sales, replace(+',')
    if·万' in sales
    sales s sales[:-1
    in sales
    sales sales replace(
    +000
    3
    Lse
    sales s sales +0000
    894123456
    sales int(sales)
    new sales, append (sales
    df[' sales= new sales
    print(df[ sales I values)
    #2、将地区转化为只包含省
    raw location s df[ location. values
    new location
    4
    for location in raw location
    f
    in location
    location location [ location find()]
    new location, append location
    #df. Location与df[ ocation]效果类似
    012345678961
    df location new location
    print(df location I values)
    #3、生成新的 excel
    writer= pd Exce wRiter(GOODS_ STANDARD EXCEL PATH)
    # columns参数用于指定生成的 excel中列的顺序
    encoding=utf-8, sheet name= cheet) price','location','sales',comment_url'l, index=False.
    df to excel(excel writer=writer, columns=[title
    writer. save()
    writer. close()


64 Edef analysis title():
65
66
词云分析商品标题
67
ireturn:
68
69
#引入全局数据
70
global DF STANDARD
71
#数据清洗,去掉无效词
72
jieba, analyse set stop words (STOP WORDS FILE PATH)
73
#1、词数统计
74
keywords_ count_list jieba, analyse textrank('.join(DF_STANDARD title), topk=50, withWeight=True)
75
print(keywords_count_list)
76
#生成词云
77
word cloud
78
WordCloud(
79
add(", keywords_count_list, word_size_ range=[20, 1001, shape=Symbo lType. DIAMOND)
80
set_ global opts( title_opts=opts. TitleOpts( title="避孕套功能词云T0P50")
81
82
word cloud, render('title-word-cloud html)
83
84#2、避孕套商品标题词频分析生成柱状图
85
#2.1统计词数
86
#取前20高频的关键词
87
keywords_count_dict =ti[o]: 0 for i in reversed keywordscount_ list[: 201)1
88
cut_words jieba cut('.join(DF_STANDARD title))
89
for word in cut words i
90
for keyword in keywords_count_ _dict keys():
91
if word
keyword
92
keywords_count_ dict [keyword] keywords_count_dict [keyword]+ 1
93
print(keywords_ count_dict)
94
#2.2生成柱状图
95
keywords count bar
96
Bar(
97
add xaxis(list(keywords count dict keys()))
98
add_yaxis(", list(keywords_count_ _dict values()))
99
reversal axis
100
set_series_opts(label_ opts=opts. LabelOpts(position="right))
101
set global opts(
102
title_opts=opts. Titleopts(tite="避孕套功能T0P20"),
103
yaxIs_0pts=opts, AXisopts(name="功能"),
104
xaXIs_0pts=opts.Axis0pts(name=商品数")
105
106
107
keywords_count_ bar. render('title-word-count-bar html)
108
109
#3、标题高频关键字与平均销量关系
110
keywords sales dict analysis title keywords (keywords count list, sales 20)
111
#生成柱状图
keywords sales bar =
113
Bar(
114
add_xaxis(list(keywords_sales_dict keys()))
115
add_yaxis(", list(keywords_sales_dict values()))
116
reversal axis(
117
set_ series_opts(label_opts=opts. Labe lOpts(position=right)
118
set global opts(
119
title_opts=opts. TitleOpts( title="避孕套商品功能与平均销量ToP20"),
120
yaxIs_opts=opts.AXis0pts(name="功能"),
121
xaXIs_0pts=opts.Axis0pts(name="平均销量")
122
123
124
keywords sales bar. render('title-word-sales-bar html)
144 def analysis_title_keywords( keywords_count_list, column, top_num)->dict
145
146
分析标题关键字与其他属性的关系
147
param keywords_count_1ist:关键字列表
148
param column:需要分析的属性名
149
param top_ num:截取前多少个
150
a return:
151
152
#1、获取高频词,生成一个dict={" keyword1:[]," keyword2:l,
153
keywords co lumn dict =ti[o:[ for i in keywords count list
154
for row in DF STANDARD. iterrows():
155
for keyword in keywords co lumn dict keys()
156
if keyword in row [1]. title:
157
#2、将标题包含关键字的属性值放在列表中,dict={" keyword1:[属性值1,属性值2,·]
158
keywords_co lumn_dict [keyword]. append (row [1] [co lumnI)
159
#3、求属性值的平均值,dict={" keyword1:平均值1, keyword2,平均值2}
160
for keyword in keywords_ co lumn_dict keys()
161
keyword_co lumn_list keywords_ co lumn_dict [keyword]
162
keywords co lumn dict [keyword] sum( keyword column list)/ len( keyword column list)
163
#4、根据平均值排序,从小到大
164
keywords _price_dict dict (sorted (keywords_column_dict items(), key=lambda d: d[11))
165
#5、截取平均值最高的20个关键字
166
keywords_price_dict = ik: keywords_price_ _dict [k] for k in list(keywords_price_ _dict keys())[-top_num: 1]
167
print(keywords_ price dict
168
return keywords_price_dict
126
#4、标题高频关键字与平均售价关系
127
keywords price dict analysis title keywords(keywords count list,price, 20)
#生成柱状图
129
keywords_price_bar =
130
Baro
131
add_xaxis(list(keywords_price_dict keys()))
132
add yaxis(", list(keywords price dict values()))
133
reversal axis
134
set_series_opts(Label_opts=opts. Labe lOpts(position="right))
135
set_global_opts(
136
title_opts=opts. TitleOpts(tite="避孕套商品功能与平均售价T0P20),
137
yaxIs_0pts=opts.Axis0pts(name="功能"),
xaxIs_0pts=opts.AXis0pts(name="平均售价")
139
141 keywords_price_bar. render('title-word-price-bar. html')
142
144 def analysis_title_keywords( keywords_count_list, column, top_num)->dict
145
146
分析标题关键字与其他属性的关系
147
param keywords_count_1ist:关键字列表
148
param column:需要分析的属性名
149
param top_ num:截取前多少个
150
a return:
151
152
#1、获取高频词,生成一个dict={" keyword1:[]," keyword2:l,
153
keywords co lumn dict =ti[o:[ for i in keywords count list
154
for row in DF STANDARD. iterrows():
155
for keyword in keywords co lumn dict keys()
156
if keyword in row [1]. title:
157
#2、将标题包含关键字的属性值放在列表中,dict={" keyword1:[属性值1,属性值2,·]
158
keywords_co lumn_dict [keyword]. append (row [1] [co lumnI)
159
#3、求属性值的平均值,dict={" keyword1:平均值1, keyword2,平均值2}
160
for keyword in keywords_ co lumn_dict keys()
161
keyword_co lumn_list keywords_ co lumn_dict [keyword]
162
keywords co lumn dict [keyword] sum( keyword column list)/ len( keyword column list)
163
#4、根据平均值排序,从小到大
164
keywords _price_dict dict (sorted (keywords_column_dict items(), key=lambda d: d[11))
165
#5、截取平均值最高的20个关键字
166
keywords_price_dict = ik: keywords_price_ _dict [k] for k in list(keywords_price_ _dict keys())[-top_num: 1]
167
print(keywords_ price dict
168
return keywords_price_dict
71 def analysis_price()
172
173
分析商品价格
174
Areturn:
176
#引入全局数据
77
global DF STANDARD
178
#设置切分区域
179
price list bins=[0,20,40,60,80,108,120,150,200,1000001
80
#设置切分后对应标签
81
price list_ Labels=["0-20,21-40,141-60,‘61-80,81-100,101-120,121-150,1151-200,1200以上"]
82
#分区统计
183
price count cut and sort data(price list bins, price list labels, DF STANDARD price)
84
print (price count)
85
#生成柱状图
186
bar =
87
Bar(
88
add_xaxis(list (price_count. keys()))
89
add yaxis(", list(price count, values()))
90
set global opts(
91
title_opts=opts. TitleOpts( title="避孕套商品价格区间分布柱状体")
92
yaxIs_opts=opts. AxisOpts(name=个商品"),
93
94
) xaxis_0pts=0ts,AXis0pts(name=商品售价:元")
195
96
bar. render('price-barhtml)
97
#生成饼图
98
age count list
[list(z) for z in zip(price_count. keys(), price_count values())
99
pIe
200
Pie()
201
add( age count list)
02
sset_ global_opts( title_opts=opts. Titleopts(tite="避孕套商品价格区间饼图")
203
set_series_opts(label_opts=opts. LabelOpts( formatter=tb): icy))
04
05
pie. render( ' price-pie html)
272 def cut_and_sort_data(listBins, listLabels, data_list)->dict:
273
274
统计List中的元素个数,返回元素和 count
275
:param ListBins:数据切分区域
276
param ListLabels:切分后对应标签
277
param data_list:数据列表形式
278
return:key为元素 value为 count的dict
279
280
data labels_list pd cut (data_list, bins=listBins, Labels=listLabels, include_ lowest=True)
281
#生成一个以 ListLabels为顺序的字典,这样就不需要后面重新排序
282
data count i: 0 for i in listLabels]
283
#统计结果
284
for value in data labels list
285
#get( value,num)函数的作用是获取字典中 value对应的键值,nm=0指示初始值大小
286
data count Ivalue]= data count. get(value)+1
287
return data count
288
208 def analysis_sales()
209
210
销量情况分布
211
return:
212
213
#引入全局数据
214
gLobal DF_STANDARD
215
#设置切分区域
216
ListBins=[0,1000,5000,10000,50000,100000,1000000
217
#设置切分后对应标签
218
1 istlabe1s=[一千以内',一千到五千,"五千到一万,一万到五万’,"五万到十万,'+万以上
219
#分区统
220
sales count s cut and sort data (listBins, listLabels DF STANDARD, sales)
221
print(sales_count
222
#生成柱状图
223
bar =
224
Baro
225
add_xaxis(list(sales_count. keys()))
226
add_yaxis(", list(sales_count values()))
227
set_global_opts(
228
title_opts=opts. Titleopts(tite="避孕套商品销量区间分布柱状图"),
229
yaxIs_opts=opts. AXisopts(name="个商品"),
230
XaX1s_0pts=opts. AxisOpts(name="销售件数")
231
232
233
bar. render(' sales-bar. html)
234
#生成饼图
235
age_ count_list [list(z) for z in zip(sales_count. keys(), sales_count values())1
236
p
le
237
Pie()
238
a add( age count list)
239
set_ global_opts( title_opts=opts. Title0pts( title="避孕套商品销量区间饼图")
240
set_series_opts(label_opts=opts. LabelOpts(formatter=tb]: ic]))
241
242
pie. render('sales-pie html)
272 def cut_and_sort_data(listBins, listLabels, data_list)->dict:
273
274
统计List中的元素个数,返回元素和 count
275
:param ListBins:数据切分区域
276
param ListLabels:切分后对应标签
277
param data_list:数据列表形式
278
return:key为元素 value为 count的dict
279
280
data labels_list pd cut (data_list, bins=listBins, Labels=listLabels, include_ lowest=True)
281
#生成一个以 ListLabels为顺序的字典,这样就不需要后面重新排序
282
data count i: 0 for i in listLabels]
283
#统计结果
284
for value in data labels list
285
#get( value,num)函数的作用是获取字典中 value对应的键值,nm=0指示初始值大小
286
data count Ivalue]= data count. get(value)+1
287
return data count
288
245 def analysis_price_sales():
246
247
商品价格与销量关系分析
248
return:
249
250
#引入全局数据
251
gLobal DF STANDARD
252
d千
DF STANDARD copy
253
df['group]=pd. qcut(df. price, 12)
254
df group value counts). reset index()
255
df group_sales df[['sales','group 'Il groupby('group)mean(). reset_index()
256
df group_str [str(i) for i in df_group_sales['group 'I]
257
print(df_ group_str)
258
#生成柱状图
259
bar
260
Baro
261
add_xaxis(df_group_str)
262
add_yaxis(", list(df_ group_sales[']), category_ gap=50%)
263
set global opts(
264
title_opts=opts. TitleOpts(tite=避孕套商品价格分区与平均销量柱状图"),
265
yaxIs_0pts=opts.AXis0pts(name="价格区间")
266
xaXIs_0pts=opts.AXis0pts(name="平均销量")
267
268
269
bar. render('price-sales-bar. html)
290 def analysis_province_sales():
291
292
省份与销量的分布
293
a return:
294
295
#引入全局数据
296
gLobal DF STANDARD
297
298
#1、全国商家数量分布
299
province_sales DF_STANDARD location value_counts()
300
province sales list
[list(item) for item in province_sales items()
301
print(provincesales_list)
302
#1.1生成热力图
303
province sales map
304
Map(
305
add("前两千款避孕套商家数量全国分布图", province_sales_List," china")
306
set global opts(
307
visua lmap opts=opts. Visua LMapOpts(max =647)
308
309
310
province_ sales_map, render(' province-seller-map html
311
#1.2生成柱状图
312
province_sales_ bar =
313
Bar(
314
add_xaxis(province_ sales index tolist()
315
add_yaxis(", province_ sales values. tolist(), category_gap=50%)
316
set global opts(
317
title_opts=opts. TitleOpts( title="前两千款避孕套商家数量地区柱状图")
318
yaxIs_opts=opts.Axis0pts(name="商家数量"),
319
xaxis_opts=opts. AxisOpts(name=tX", axis label_opts=t rotate: 901)
320
321
322
province_sales_ bar. render(' province-seller-bar html)
353
#3、全国商家省份平均销量分布
354
province_sales_mean= DF_STANDARD pivot_ table(index=' location', values='sales', aggfunc=np. mean)
355
#根据平均销量排序
356
province sales mean, sort values(' sales, inp lace=True, ascending=False)
357
province_ sales_mean_list [list(item) for item in
358
zip(province_ sales_mean index, np. ravel(province_sales_mean values))
359
360
print(province sales mean_ list)
361
#3.1生成热力图
362
province sales_ mean_map
363
Map()
364
ad("前两千款避孕套商家平均销量全国分布图", province_ sales_mean_List," china")
365
set_global_opts(
366
visualmap opts=opts. Visua LMapOpts(max=1536)
367
368
369
provincesales_ mean_map, render('province-sales-mean-map html)
370
#3.2生成柱状图
371
province sales mean_bar
372
Bar()
373
add_xaxis(province_sales_mean index tolist())
374
add_yaxis(", list(np. ravel(province_sales_sum. va lues)), category_gap=50%")
375
set_global_opts(
376
title_opts=pts. TitleOpts(tite="前两千款避孕套各省商家平均销量地区柱状图"),
377
yaxIs_opts=opts.AXis0pts(name="平均销量"),
378
xaxis_opts=opts. AxisOpts(name=tX", axis label_ opts=t rotate: 901)
379
380
381
province sales mean bar. render( province-sales-mean-bar. html)
382
