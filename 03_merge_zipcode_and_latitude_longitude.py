#!/usr/bin/env python
# coding: utf-8

# ## Import

import unicodedata

import pandas as pd
from tqdm import tqdm

# setting
pd.set_option("display.max_colwidth", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", 500)

tqdm.pandas()

# ### convert arabia num to kanji num
# https://neu101.seesaa.net/article/159968583.html
#!/usr/bin/env python
# -*- coding: utf8 -*-
import re

char2int = {
  u'0' :0, u'1' :1, u'2' :2, u'3' :3, u'4' :4,
  u'5' :5, u'6' :6, u'7' :7, u'8' :8, u'9' :9,
  u'０':0, u'１':1, u'２':2, u'３':3, u'４':4,
  u'５':5, u'６':6, u'７':7, u'８':8, u'９':9,
}

numKanji0 = [ u'', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九' ]
numKanji1 = [ u'', u'',   u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九' ]
numKanji  = [ numKanji0, numKanji1, numKanji1, numKanji1 ]

numPlace1 = [ u'', u'十', u'百', u'千' ]
numPlace4 = [ u'', u'万', u'億', u'兆', u'京', u'垓' ]

def convert_pure_integerstring(match):
  source = match.group()
  numstr = re.sub( u'[,，]', u'', source )
  s = []
  for ch in ((u'0'*((4-len(numstr)%4)&3))+numstr): s.insert(0,char2int[ch])

  list = []
  while len(s):
    temp = u''
    for i in range(4):
      if s[i]: temp = numKanji[i][s[i]] + numPlace1[i] + temp
    list.append(temp)
    s = s[4:]

  if len(list) > len(numPlace4): return source

  result = u''  # (a),(b),(c),(d)
  for i in range(len(list)):  # (a),(b),(c),(d)
    if list[i]:
        if len(list) > 1 and list[i] == u'千': list[i] = u'一' + list[i]  # (d)
        result = list[i] + numPlace4[i] + result

  return result if result else u'零'

def convert_integerstring(string):
  if string == None or string == u'': return u''
  p = re.compile(u'[0-9０-９][0-9０-９,，]*[0-9０-９]|[0-9０-９]')
  return p.sub( convert_pure_integerstring, string )

print(convert_integerstring('１条通'))


# ## zipcode
# https://www.post.japanpost.jp/zipcode/dl/oogaki-zip.html
#
# ```
# 全国地方公共団体コード（JIS X0401、X0402）………　半角数字
# （旧）郵便番号（5桁）………………………………………　半角数字
# 郵便番号（7桁）………………………………………　半角数字
# 都道府県名　…………　半角カタカナ（コード順に掲載）　（※1）
# 市区町村名　…………　半角カタカナ（コード順に掲載）　（※1）
# 町域名　………………　半角カタカナ（五十音順に掲載）　（※1）
# 都道府県名　…………　漢字（コード順に掲載）　（※1,2）
# 市区町村名　…………　漢字（コード順に掲載）　（※1,2）
# 町域名　………………　漢字（五十音順に掲載）　（※1,2）
# 一町域が二以上の郵便番号で表される場合の表示　（※3）　（「1」は該当、「0」は該当せず）
# 小字毎に番地が起番されている町域の表示　（※4）　（「1」は該当、「0」は該当せず）
# 丁目を有する町域の場合の表示　（「1」は該当、「0」は該当せず）
# 一つの郵便番号で二以上の町域を表す場合の表示　（※5）　（「1」は該当、「0」は該当せず）
# 更新の表示（※6）（「0」は変更なし、「1」は変更あり、「2」廃止（廃止データのみ使用））
# 変更理由　（「0」は変更なし、「1」市政・区政・町政・分区・政令指定都市施行、「2」住居表示の実施、「3」区画整理、「4」郵便区調整等、「5」訂正、「6」廃止（廃止データのみ使用））
# ```


filename = 'data/KEN_ALL.CSV'
names = [
    "全国地方公共団体コード",
    "（旧）郵便番号",
    "郵便番号",
    "都道府県名カタカナ",
    "市区町村名カタカナ",
    "町域名カタカナ",
    "都道府県名",
    "市区町村名",
    "町域名",
    "一町域が二以上の郵便番号で表される場合の表示",
    "小字毎に番地が起番されている町域の表示",
    "丁目を有する町域の場合の表示",
    "一つの郵便番号で二以上の町域を表す場合の表示",
    "更新の表示",
    "変更理由",
]
dtype_dict = {
    "全国地方公共団体コード": str,
    "郵便番号": str,
}
zipcode_df = pd.read_csv(filename, encoding='shift-jis', names=names, dtype=dtype_dict)
print(zipcode_df.shape)

# clean
use_cols = ["全国地方公共団体コード", "郵便番号", "都道府県名", "市区町村名", "町域名"]
zipcode_df = zipcode_df[use_cols]


# ## latitude longitude
dtype_dict = {
    "市区町村コード": str,
}
filename = 'data/latitude_longitude.csv'
latlong_df = pd.read_csv(filename, encoding='cp932', dtype=dtype_dict)
print(latlong_df.shape)

# clean
use_cols = ["都道府県名", "市区町村コード", "市区町村名", "大字町丁目名", "緯度", "経度"]
latlong_df = latlong_df[use_cols]


# ### 市町村名の違い
shichoson_remap_dict = {
    '東津軽郡外ヶ浜町': '東津軽郡外ケ浜町', 
    '龍ケ崎市': '龍ヶ崎市', 
    '鎌ケ谷市': '鎌ヶ谷市', 
    '袖ケ浦市': '袖ヶ浦市', 
    '三宅島三宅村': '三宅村',
    '八丈島八丈町': '八丈町', 
    '糟屋郡須惠町': '糟屋郡須恵町'
}
shichoson = '東津軽郡外ヶ浜町'
if shichoson in shichoson_remap_dict:
    shichoson = shichoson_remap_dict[shichoson]


def add_latlong(r):
    # init
    shichoson = r["市区町村名"]
    # convert some shichoson
    if shichoson in shichoson_remap_dict:
        shichoson = shichoson_remap_dict[shichoson]
    # get small latitude longitude
    ll_small_df = latlong_df[latlong_df["市区町村名"] == shichoson]
    choiki = r["町域名"]
    print(shichoson, choiki, ' '*30, end='\r')
    # convert arabia num to kanji num
    choiki = convert_integerstring(choiki)

    if choiki == "以下に掲載がない場合":
        ll_match_df = ll_small_df

    # exactly match or partly match "旭ケ丘"
    # ll_match_df = ll_small_df[ll_small_df["大字町丁目名"] == choiki]
    if not choiki == "以下に掲載がない場合":
        ll_match_df = ll_small_df[ll_small_df["大字町丁目名"].str.contains(choiki)]

    if "（" in choiki:
        chome = choiki.split("（")[1]
        choiki = choiki.split("（")[0]
        # in case of "大通西（１〜１９丁目）"
        if "〜" in chome:
            # get chome
            chome = chome.replace("丁目", "")
            chome = chome.replace("番地", "")
            chome = chome.replace("）", "")
            # print(chome)
            chome_s = chome.split("〜")[0]
            chome_e = chome.split("〜")[1]
            # print(choiki, chome_s, chome_e, ' '*30)
            ll_match_df = ll_small_df[ll_small_df["大字町丁目名"].str.contains(choiki)]

            # in case of '留萌市 留萌原野（１〜１２線）'
            if not ll_match_df.empty:
                # ll_match_df = ll_match_df.iloc[chome_s-1:chome_e, :]
                # get index start
                temp_ll_df = ll_match_df[ll_match_df["大字町丁目名"] == choiki+chome_s+"丁目"]
                # index start:
                if temp_ll_df.empty:
                    index_s = ll_match_df.index[0]
                else:
                    index_s = temp_ll_df.index[0]
                # get index end
                temp_ll_df = ll_match_df[ll_match_df["大字町丁目名"] == choiki+chome_e+"丁目"]
                # index end:
                if temp_ll_df.empty:
                    index_e = ll_match_df.index[-1]
                else:
                    index_e = temp_ll_df.index[0]
                # print(choiki, index_s, index_e)
                ll_match_df = ll_match_df.loc[index_s:index_e, :]

        # in case of 南郷通（南）'
        else:
            ll_match_df = ll_small_df[ll_small_df["大字町丁目名"].str.contains(choiki)]

    if ll_match_df.empty:
        # ll_match_df = ll_small_df[ll_small_df["大字町丁目名"].str.contains(choiki)]
        print('no result for ', shichoson, choiki, ' '*30, end='\r')
        # TODO check if this is correct
        # In case of '湯沢市' '藤花' not in lat long data, use average
        ll_match_df = ll_small_df

    lat = ll_match_df["緯度"].mean()
    lon = ll_match_df["経度"].mean()
    # print(lat, lon)
    # return lat, lon
    r['latitude'] = lat
    r['longitude'] = lon
    return pd.Series(r)

# ## test
aa_df = a_df.apply(add_latlong, axis=1)
print(aa_df.isna().sum())


# ## run all
# df = zipcode_df.progress_apply(add_latlong, axis=1)
df = zipcode_df.apply(add_latlong, axis=1)
# df = zipcode_df[zipcode_df["市区町村名"] == "札幌市南区"].apply(add_latlong, axis=1)
print(df.shape)
print(df.isna().sum())

# ## save
filename = 'data/zipcode_latitude_longitude.csv'
df.to_csv(filename, index=False)