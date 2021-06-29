from Config import getDate
import json

#每天同步1-3页数据
from CrawlingJsonKb import getVideoDetailJson
from VideoDao import getValueByKey
from WithVideoByYear import updateVideoJh


def getVideoListByPage(url):
    print('------'+url)
    result = getDate(url);
    if result is None:
        print("采集异常")
    else:
        resJson = json.loads(result)
        status = resJson['code']
        if status == 1:
            data = resJson['list']
            for key in data:
                getVideoDetailJson(key)
            p_hov = url.split('&pg=')[1]
            p_hov = int(p_hov) - 1;
            if p_hov ==0 :
                return ;
            else:
                getVideoListByPage("http://www.kuaibozy.com/api.php/provide/vod/?ac=detail&pg="+str(p_hov))
        else:
            return;

if __name__=="__main__":
    print('1-3页数据')
    result = getValueByKey('kb_index_page_reverse')
    if result is not None:
        getVideoListByPage('http://www.kuaibozy.com/api.php/provide/vod/?ac=detail&pg='+str(result[0].value))
    updateVideoJh(2000)
