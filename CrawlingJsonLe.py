from datetime import datetime
import json
# 获取视频列表 json 格式聚合


def getVideoList(url):
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
            p_hov = int(p_hov) + 1;
            setValueByKey('le_index_page',str(p_hov))
            getVideoList("http://www.kuaibozy.com/api.php/provide/vod/?ac=detail&pg="+str(p_hov))
        else:
            return;

def getVideoDetailJson(key):
    is_add = 1
    super_id = key['vod_id']
    cate_name = key['type_name']
    cate_id = getVideoTypeByNickname(cate_name)
    white_title = key['vod_name']
    video_state = key['vod_state']
    if video_state == '':
        video_state = key['vod_remarks']

    introduce = key['vod_content']
    if introduce is not None:
        introduce = stripTags(introduce)
    cover = key['vod_pic']
    video_url_to = ''
    set_number_to = 0
    inforlist = key['vod_play_url']
    if len(inforlist)<=0:
        return
    if inforlist.__contains__('$$$'):
        inforlist = inforlist.split('$$$')
        if inforlist[1].__contains__('m3u8'):
            inforlist = inforlist[1]
        else:
            inforlist = inforlist[0]

    if len(inforlist)<=0:
        return
    inforlist = inforlist.split('#')
    if inforlist is not None and len(inforlist)>0 and isinstance(inforlist,list):
        set_number_to = len(inforlist)
        video_url_to = inforlist[0]
        if video_url_to.__contains__('$'):
            video_url_to = video_url_to.split('$')[1]
        elif video_url_to.__contains__('http'):
            video_url_to = 'http'+video_url_to.split('http')[1]
    alias = ''
    director_names = key['vod_director']
    actor_names = key['vod_actor']
    type_names =  key['vod_tag']
    area_names = key['vod_area']
    language = key['vod_lang']
    release_year_names = key['vod_year']
    video_update_time = key['vod_time']
    if white_title.__contains__('['+release_year_names+']'):
        white_title = white_title.strip().replace('['+release_year_names+']', '')

    print('影片名称：--'+white_title)
    print('背景图：--'+cover)
    print('剧情介绍：--'+introduce)
    print('别名：--'+alias)
    print(str(cate_id)+'影片类型：--'+cate_name)
    if cate_name.__contains__('主播美女') or cate_name.__contains__('韩国美女') or cate_name.__contains__('展会美女') or cate_name.__contains__('写真美女') or cate_name.__contains__('VIP福利') or cate_name.__contains__('伦理片'):
        type_names = '伦理片'
    print('剧情分类：--'+type_names)
    print('影片地区：--'+area_names)
    print('影片导演：--'+director_names)
    print('影片演员：--'+actor_names)
    print('更新时间：--'+video_update_time)
    print('上映年份：--'+release_year_names)
    print('影片状态：--'+video_state)
    print('影片语言：--'+language)

    if video_state.__contains__('预告'):
        is_add = 0

    yearid = insertVideoReleaseYear(cate_id, release_year_names)
    #y_id = getVideoByTitleByYear(cate_id,white_title,release_year_names);
    y_id = 0
    json_to = {'cate_id':cate_id,'title':white_title,'nickname':alias,'language': language,
               'cover':cover,'introduce':introduce,'release_year_names':release_year_names,'tag':video_state,'actor_names':actor_names,
               'update_time':video_update_time,'create_time':datetime.now(),'director_names':director_names,'type_names':type_names,
               'super_id':super_id,'area_names':area_names,'describe':video_state,'release_year_id':yearid,'video_url':video_url_to,
               'download_url':'','y_vid':y_id,'status':1,'is_del':1,
               'w_name':'admin'}
    v_id = getIsSupId(super_id);
    is_update = 0;
    if v_id > 0:
        updateVideo(json_to)
        print('已存在!'+str(v_id))
        #videoSubset = getIsYid(y_id)
        # if videoSubset is not None and len(videoSubset) >0 and videoSubset[0].id >0 and set_number_to > videoSubset[0].set_number:
        #      onlyJson = {'id':videoSubset[0].id,'tag':video_state,'set_number':set_number_to}
        #      updateVideoOnly(onlyJson)
    else:
        try:
            if is_add == 1:
                is_update = 1;
                v_id = addVideo(json_to)
        except Exception as e:
            print(e.args)
    if len(inforlist) >0 and is_add == 1:
        for index,res_urls in enumerate(inforlist):
            if res_urls is not None and len(res_urls) >0:
                url_value = ''
                title = ''
                if res_urls.__contains__('$'):
                    str_split = res_urls.split('$')
                    url_value = str_split[1]
                    title = str_split[0]
                elif res_urls.__contains__('http'):
                    str_split = res_urls.split('http')
                    url_value = 'http'+str_split[1]
                    title = str_split[0]
                title = title.strip()
                if isVideoSubsetSaved(v_id,title,url_value):
                    print(str(index)+'--'+str(title)+'--'+url_value+'--视频已存在！')
                else:
                    json_res = {'v_id':v_id,'title':title,'sort':str(index),'video_url':url_value,'download_url':'','update_time':video_update_time}
                    addVideoSubset(json_res)
                    print(str(index)+'--'+str(title)+'--'+url_value)
    if is_update == 1:
        jsonStatus = {'id':v_id,'status':0}
        updateVideoStatus(jsonStatus);


if __name__=="__main__":
    print("爬取乐多资源网站首页数据");
    result = getValueByKey('le_index_page')
    if result is not None:
        getVideoList('http://www.kuaibozy.com/api.php/provide/vod/?ac=detail&pg='+str(result[0].value))