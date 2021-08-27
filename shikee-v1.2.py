#coding:utf-8

import requests
import re
import json
from lxml import etree
import time
import logging

logging.basicConfig(level=logging.DEBUG, datefmt='%Y/%m/%d %H:%M:%S',format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

userDict = {
    '腾讯1年': '37c5d542badd1bee1a4b4225a3499992fac91753ef738ae9509dcea72b07705f13d35a680d82ed1df2b51e20a60462c0c4c39a237c1026e2ea632efab1e61f7c9ed79f5e7e772467b9630f51296109776a23e1d1a7f93cb325f5d03f61296a44889034944053e4cc8ca2d2439a1325406915123120f33217a58719882c0efa51',
    '猪拱的菜': '37c5d542badd1bee1a4b4225a3499992fac91753ef738ae9509dcea72b07705f13d35a680d82ed1df2b51e20a60462c0c4c39a237c1026e2ea632efab1e61f7c9ed79f5e7e772467b9630f51296109776a23e1d1a7f93cb325f5d03f61296a44889034944053e4cc8ca2d2439a1325406915123120f33217a58719882c0efa51',
    'yanyan燕燕子': 'aa0625cb68ee731cc850793eb6c0ef7c8089d08eb3b7a0338f2477ece18286cdac3c7e8a7471fd398438b94bddb5131e3cdc2e2951324f4df85d7ae1464f4f06f6a449da4826a6017201c41e30e6d1bc78bf15f55d3ba96080561ca9b8c4568827434ff5cf7f9eda0e2d29bf12a32fc3ed904a13fa8db0c1c6252a2bba14f7df',
    'ming明子': 'aa0625cb68ee731cc850793eb6c0ef7c8089d08eb3b7a0338f2477ece18286cdac3c7e8a7471fd398438b94bddb5131e3cdc2e2951324f4df85d7ae1464f4f06f6a449da4826a6017201c41e30e6d1bc78bf15f55d3ba96080561ca9b8c4568827434ff5cf7f9eda0e2d29bf12a32fc3ed904a13fa8db0c1c6252a2bba14f7df',
    '冰雪聪明lc': 'aa0625cb68ee731cc850793eb6c0ef7c8089d08eb3b7a0338f2477ece18286cdac3c7e8a7471fd398438b94bddb5131e3cdc2e2951324f4df85d7ae1464f4f06f6a449da4826a6017201c41e30e6d1bc78bf15f55d3ba96080561ca9b8c4568827434ff5cf7f9eda0e2d29bf12a32fc3ed904a13fa8db0c1c6252a2bba14f7df',
    '小宝宝babybaby': 'aa0625cb68ee731cc850793eb6c0ef7c8089d08eb3b7a0338f2477ece18286cdac3c7e8a7471fd398438b94bddb5131e3cdc2e2951324f4df85d7ae1464f4f06f6a449da4826a6017201c41e30e6d1bc78bf15f55d3ba96080561ca9b8c4568827434ff5cf7f9eda0e2d29bf12a32fc3ed904a13fa8db0c1c6252a2bba14f7df',
    '小小小小女孩5292': 'aa0625cb68ee731cc850793eb6c0ef7c8089d08eb3b7a0338f2477ece18286cdac3c7e8a7471fd398438b94bddb5131e3cdc2e2951324f4df85d7ae1464f4f06f6a449da4826a6017201c41e30e6d1bc78bf15f55d3ba96080561ca9b8c4568827434ff5cf7f9eda0e2d29bf12a32fc3ed904a13fa8db0c1c6252a2bba14f7df',
    '浅唱浅听': '208c5a17f798d4d9c52b05c42ff08901ed93828f0ad56a08e8a96d38cbc58559a4da7a3017e46519392d157ac47e61cdb44fed47ca115e5dc3b90a4c841d895089aa3dadd38eefc5088e01d0a163277856d442ad90c5125f36d772330cb533cdde8be4fef265ca366e450df9f4189c5266bbe0556020a23806c205cd13f0f772',
    'cicynia': '208c5a17f798d4d9c52b05c42ff08901ed93828f0ad56a08e8a96d38cbc58559a4da7a3017e46519392d157ac47e61cdb44fed47ca115e5dc3b90a4c841d895089aa3dadd38eefc5088e01d0a163277856d442ad90c5125f36d772330cb533cdde8be4fef265ca366e450df9f4189c5266bbe0556020a23806c205cd13f0f772',
    '舒服干活': '208c5a17f798d4d9c52b05c42ff08901ed93828f0ad56a08e8a96d38cbc58559a4da7a3017e46519392d157ac47e61cdb44fed47ca115e5dc3b90a4c841d895089aa3dadd38eefc5088e01d0a163277856d442ad90c5125f36d772330cb533cdde8be4fef265ca366e450df9f4189c5266bbe0556020a23806c205cd13f0f772',
    '海阔天空mei': '208c5a17f798d4d9c52b05c42ff08901ed93828f0ad56a08e8a96d38cbc58559a4da7a3017e46519392d157ac47e61cdb44fed47ca115e5dc3b90a4c841d895089aa3dadd38eefc5088e01d0a163277856d442ad90c5125f36d772330cb533cdde8be4fef265ca366e450df9f4189c5266bbe0556020a23806c205cd13f0f772'
}
chooseUserDict = {}
userList = [i for i in userDict.keys()]
while True:
    for user in userList:
        print(userList.index(user),user)
    chooseUserNum=input('请输入需要选择的用户的序号：')
    if chooseUserNum == '':
        break
    username = userList[int(chooseUserNum)]
    password = userDict[username]
    chooseUserDict[username] = password

sleepTime = 2
priceInterval = 250
pageCount = '100'
keyword = ""
#keyword = '坐垫 脚垫 柜 蒸锅 手表 花信 抽湿机 甩脂机 乐器 按摩椅 信用卡 压缩 拖鞋 缝纫机 麻将机 电脑 笔记本 主机 鞋 沙发 床 办公桌 录音笔 耳机 自行车 车 豆浆机 派克服 洗衣机 冰箱 京东 调料盒 抱枕 马桶 电视柜 显示屏 花酒 水槽 洗碗机 坐便器 y Y 30 25 20 18 15 12 10 8'
url = 'http://login.shikee.com/check/?&_1566806437460'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'}
get_proinfo_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36',
            'Host': 'platinum.shikee.com',
            'Upgrade-Insecure-Requests': '1'
           }


def searchProduct(pageCount):
    proUrls = {}
    for page in range(1,int(pageCount)+1):
        time.sleep(sleepTime)
        searchApi = 'http://list.shikee.com/list-{}.html?type=0&cate=0&posfree=0&try_order=0&try_type=0&qr_code=0&sort=desc&pkey=0'.format(page)
        searchResult = requests.get(url=searchApi,headers=headers).text
        logger.debug('searchProduct - searchProduct:{}'.format(searchResult))
        html = etree.HTML(searchResult)
        logger.debug('searchProduct - html:{}'.format(html))
        proUrl = html.xpath('//div[@class="item-box"]/a/@href | //div[@class="item-box"]/h4/a/@title')
        logger.debug('searchProduct - proUrl - html.xpath:{}'.format(proUrl))
        proUrl = {proUrl[i]:proUrl[i+1] for i in range(0,len(proUrl),2) }
        logger.debug('searchProduct - proUrl:{}'.format(proUrl))
        proUrls = dict(proUrls,**proUrl)
    logger.debug('searchProduct - proUrls:{}'.format(proUrls))
    return(proUrls)

def apply(proId,cache_key):
    applyUrl = 'http://platinum.shikee.com/detail/apply/{}?callback=trysapply'.format(proId)
    apply_post_data = {'cache_key': cache_key}
    apply_reponse = s.post(url=applyUrl,headers=headers,data=apply_post_data,allow_redirects=False).text
    logger.debug('apply - apply_respose:{}'.format(apply_reponse))
    #print(apply_reponse)
    apply_reponse = re.findall(r'trysapply\((.*)\);', apply_reponse)
    logger.debug('apply - re.findall:{}'.format(apply_reponse))
    apply_reponse = ''.join(apply_reponse)
    logger.debug('apply - join:{}'.format(apply_reponse))
    apply_reponse = apply_reponse.encode('utf-8').decode('unicode_escape')
    logger.debug('apply - encode:{}'.format(apply_reponse))
    apply_reponse = json.loads(apply_reponse,strict=False)
    logger.debug('apply - json.loads:{}'.format(apply_reponse))
    return apply_reponse




def filterPro():
    filterResult = {}
    urls = searchProduct(pageCount)
    applyCount = 0
    for proUrl,title in urls.items():
        proId = re.sub('\D','',proUrl)

        getDataUrl = 'http://platinum.shikee.com/data/%s' %proId
        logger.debug('filterPro - getDataUrl:{}'.format(getDataUrl))
        time.sleep(sleepTime)
        try:
            proInfo2 = s.get(getDataUrl,headers=get_proinfo_headers,allow_redirects=False).text
            logger.debug('filterPro - proInfo2:{}'.format(proInfo2))
            proInfo1 = ''.join(re.findall('var try_dynamic=(.*);',proInfo2))
            logger.debug('filterPro - proInfo1:{}'.format(proInfo1))
            proInfo = json.loads(proInfo1)
            logger.debug('filterPro - proInfo:{}'.format(proInfo))
        except Exception as e:
            logger.error(proUrl,proInfo2,'商品信息获取失败：',e)
            continue
        cache_key = proInfo['key']
        logger.debug('filterPro - cache_key:{}'.format(cache_key))
        is_apply = proInfo['is_apply']
        logger.debug('filterPro - is_apply:{}'.format(is_apply))
        coin_price = proInfo['coin_price'][:-1] if len(proInfo['coin_price']) >= 2 else  proInfo['coin_price']
        logger.debug('filterPro - coin_price:{}'.format(coin_price))

        if coin_price == '0':
            proDetail = s.get(proUrl,headers=headers,allow_redirects=False).text
            proDetail = etree.HTML(proDetail)
            if proUrl.startswith('http://platinum'):
                coin_price = proDetail.xpath('//li[@class="tryGuaranteeMoney"]/em/text()')
                coin_price = ''.join(coin_price)
                coin_price = coin_price.split('.')[0]
            else:
                coin_price = proDetail.xpath('//li/span[text()="单品试用活动款："]/following-sibling::em/text()')
                coin_price = ''.join(coin_price)
                coin_price = coin_price.split('.')[0]

        if coin_price.strip() == '':
            logger.info(proUrl,proInfo,proDetail,'未获取到价格')
            continue

        for word in keyword.split(' '):
            if word in title:
                wordFilter = True
                break
            else:
                wordFilter = False

        if int(coin_price) >= priceInterval  and wordFilter == True and  is_apply == False:
            try:
                applyResult = apply(proId,cache_key)
                if applyResult['success'] == True:
                    logger.info('商品：',proUrl,title,'价格：',coin_price,'元',applyResult['info'])
                    time.sleep(sleepTime)
                    applyCount += 1
                else:
                    logger.info('商品：',proUrl,title+'价格：',coin_price,'元',applyResult['info'])
            except Exception as e:
                logger.error('程序运行错误：',e)

    logger.info('一共申请了',applyCount,'件商品')


if  not chooseUserDict:
    exit('未选择需要申请的用户，自动退出！')
else:
    for username, password in chooseUserDict.items():
        data = {
            'username': username,
            'password': password,
            'vcode': '',
            'to': 'http://www.shikee.com/'
        }
        s = requests.session()
        r = s.post(url, headers=headers, data=data)
        filterPro()





