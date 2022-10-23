# API client library
from urllib import response
import googleapiclient.discovery
import json
import csv
import pandas as pd

# API information
api_service_name = "youtube"
api_version = "v3"
DEVELOPER_KEY = None # edit your own api
# 'AIzaSyBkKE6ZI95Wwozp16hiPHGAWUZwVYviRbQ'
# 'AIzaSyC-bg0gBMpo8IjtbAqaNNNZe8PmwI0Owmg'
# 'AIzaSyAR3BnbuKzE2PeS-CuJD6La7N3nJbokfWM'
# 'AIzaSyDrstpKz66VHqsZk12_k1YhFMzHVsx1IVQ'
# 'AIzaSyC19lhUF88kR9gmvfFYdwmmb-fxSK_jYiA'
# 'AIzaSyAqv0yMEpl3dBJc7OOyYphOnGd1Osb0IZo'
# 'AIzaSyCGFYowtLze6UjX4_HO2-0zYrAqrC9pyAE'
# 'AIzaSyDR_6EoxnVhFtJXLs7FebQycwH0CaMIozU'
# 'AIzaSyA2HRqtfajgKjgapP6cZyDAXvY12UFVTAE'
# 'AIzaSyAO_zN8_oJs6EyVDChXmgVhG1UgEVRBzno'
# 'AIzaSyD7uVpIG3awGKxJvbXCfoxwT04jfbTj2D4'
# 'AIzaSyDa5FYuDKvj1kgekYoStrs9fgvDoHjLTJM'
# 'AIzaSyAJEUHsyaklWnxPu-23gfChonIo_hhcVoc'
# 'AIzaSyCirm_ky2AqVEnNP94FuSfHRsWHRSRMX7o'
# 'AIzaSyAlYSnBJXjuwIIq69QhkiX59wTYYawuEUA'
# 'AIzaSyC_lxLU6jTd8qwFDY4VjIglzMEtAA_xdYE'
# 'AIzaSyCv6kVP_jewQf62fqJFtz7xPlaAWXNJsOI'
# 'AIzaSyA-o4CaTLC2ID2wAQsLGXnFy787wUSUIso'

# API client
youtube = googleapiclient.discovery.build(
        api_service_name, api_version, developerKey = DEVELOPER_KEY)



def main(search, quota):
        nextPageToken = None
        flag = True
        res = []
        cnt = 0
        while flag:
                try:
                        response = youtube.search().list(
                                        part="id,snippet",
                                        type='video',
                                        q=search,
                                        maxResults=50,
                                        fields="nextPageToken,items(id(videoId),snippet(publishedAt, channelId, title))",
                                        pageToken=nextPageToken
                                ).execute()
                        nextPageToken = response.get('nextPageToken', None)
                        flag = True if nextPageToken else False
                        # print(response['items'])
                        # iterate over items
                        for item in response['items']:
                                vid = item['id']['videoId']
                                publishedAt = item['snippet']['publishedAt']
                                channelId = item['snippet']['channelId']
                                title = item['snippet']['title']                                

                                stats1 = youtube.videos().list(
                                        part="statistics",
                                        id=vid,
                                        fields="items(statistics)"
                                ).execute()
                                print(stats1['items'])
                                views = stats1['items'][0]['statistics'].get('viewCount', 0)
                                likes = stats1['items'][0]['statistics'].get('likeCount', 0)
                                comments = stats1['items'][0]['statistics'].get('commentCount', 0)


                                stats2 = youtube.channels().list(
                                        part="statistics, snippet",
                                        id=channelId,
                                        fields="items(snippet(title)), items(statistics(subscriberCount))"
                                ).execute()
                                username = stats2["items"][0]["snippet"]["title"]
                                subscriptions = stats2["items"][0]["statistics"]["subscriberCount"]
                                
                                tmp_dic = {
                                        "title": title,
                                        "videoId": vid,
                                        "userName": username,
                                        "subscriptions": subscriptions,
                                        "views": views,
                                        "publishAt": publishedAt,
                                        "commments": comments,
                                        "likes": likes
                                }
                                cnt += 1
                                print(cnt)
                                res.append(tmp_dic)
                                if cnt == quota:
                                        flag = False
                except Exception as e:
                        print(e)
                        flag = False


        with open(f'{search}.json', 'w') as output_file:
                json.dump(res, output_file, ensure_ascii=False)

        df = pd.read_json(f'{search}.json')
        df.to_excel(f'{search}.xlsx')
        


if __name__ == '__main__':
        # finished_searches = ["青春版牡丹亭", "临川四梦 牡丹亭", "玉茗堂四梦 牡丹亭", "杜丽娘慕色还魂", "牡丹亭梦", "Dream in Peony Pavilion",
        # "The Peony Pavilion", "a dream in the garden", "Strolling in the Garden", "皂罗袍", "好姐姐 牡丹亭", "步步姣 牡丹亭", "游园惊梦",
        # "全本牡丹亭", "春香闹学", "离魂", "《牡丹亭惊梦》李克勤", "电视剧版《牡丹亭》", "舞剧牡丹亭", "话剧牡丹亭", "牡丹亭组曲", "牡丹亭外", "电影牡丹亭", "Kunqu Opera Music+牡丹亭",
        # "昆曲 牡丹亭", "Kunqu  Peony Pavilion", "粤剧 牡丹亭", "Hong Kong Opera Peony Pavilion", "Cantonese Opera Peony Pavilion",
        # "越剧 牡丹亭", "Yueju Opera", "潮剧 牡丹亭", "Teochew Opera Peony Pavilion", "汤显祖 牡丹亭", "愈振飞 牡丹亭", "石小梅 牡丹亭", "唐涤生 牡丹亭", "单雯 牡丹亭",
        # "梅兰芳 牡丹亭","坂东玉三郎 牡丹亭", "TAMASABURO BANDO The Peony Pavilion", "张继青 牡丹亭", "当德彪西遇上杜丽娘", "陈士争 牡丹亭", "白先勇 牡丹亭",
        # "张志红 牡丹亭", "马瑶瑶 牡丹亭", "任建辉 牡丹亭", "白雪仙 牡丹亭", "陈宝珠 牡丹亭", "梅雪诗 牡丹亭", "谢国璋 牡丹亭", "温宇航", "言怀 牡丹亭", "Declaring Ambition The Peony Pavilion", "标目 牡丹亭", "Legend The Peony Pavilion", "训女 牡丹亭",
        # "Admonishing the Daughter The Peony Pavilion", "腐叹 牡丹亭", "The Pedant's Lament The Peony Pavilion", "延师 牡丹亭",
        # "Engaging the Tutor The Peony Pavilion", "怅眺 牡丹亭", "Desperate Hope The Peony Pavilion", "闺塾 牡丹亭", "The Schoolroom The Peony Pavilion",
        # "劝农 牡丹亭", "Hastening the Plow The Peony Pavilion", "肃苑 牡丹亭", "Sweeping the Garden The Peony Pavilion","惊梦 牡丹亭", "The Interrupted Dream The Peony Pavilion", "慈戒 牡丹亭", "A Kindly Warning The Peony Pavilion",
        # "寻梦 牡丹亭", "Pursuing the Dream The Peony Pavilion", "诀谒 牡丹亭", "In Search of Patronage The Peony Pavilion", "写真 牡丹亭", "The Self-Portrait The Peony Pavilion",
        # "虏谍 牡丹亭", "A Spy For The Tartars The Peony Pavilion", "A Spy For The Tartars The Peony Pavilion", "诘病 牡丹亭", "The Invalid The Peony Pavilion", "道觋 牡丹亭", "The Tao Sorceress The Peony Pavilion",
        # "牝贼 牡丹亭", "The Brigandess The Peony Pavilion", "闹殇 牡丹亭", "The Death of Du Liniang The Peony Pavilion", "谒遇 牡丹亭",
        # "The interview The Peony Pavilion", "旅寄 牡丹亭", "Traveler's Refuge The Peony Pavilion", "冥判 牡丹亭", "Infernal Judgement The Peony Pavilion", "拾画 牡丹亭",
        # "The Portrait Discovered The Peony Pavilion", "忆女 牡丹亭", "Maternal Remembrance The Peony Pavilion", "玩真 牡丹亭", "The Portrait Venerated The Peony Pavilion", "魂游 牡丹亭",
        # "Spirit Wandering The Peony Pavilion", "幽媾 牡丹亭", "Making Love with a Ghost The Peony Pavilion", "旁疑 牡丹亭", "Suspicions The Peony Pavilion", "欢挠 牡丹亭",
        # "Rapture Disrupted The Peony Pavilion", "缮备 牡丹亭", "Defence Strategy The Peony Pavilion", "冥誓 牡丹亭", "Spectral Vows The Peony Pavilion", "秘议 牡丹亭", "Secret Discussion The Peony Pavilion",
        # "诇药 牡丹亭", "Searching for a Magic Potion The Peony Pavilion", "回生 牡丹亭",  "Resurrection The Peony Pavilion", "骇变 牡丹亭", "The Alarm The Peony Pavilion",
        # "淮警 牡丹亭", "The Scourge of the Huaiyang The Peony Pavilion", "如杭 牡丹亭", 'Hangzhou The Peony Pavilion', "仆侦 牡丹亭", "In Search of the Master The Peony Pavilion",
        # "耽试 牡丹亭", "Delayed Exam The Peony Pavilion", "移镇 牡丹亭", "Transfer to Huaian The Peony Pavilion", "御淮 牡丹亭", "The Siege of Huaian The Peony Pavilion",
        # "急难 牡丹亭", "Concern for the Besieged The Peony Pavilion", "折寇 牡丹亭", "War Against the Bandits The Peony Pavilion", "寇间 牡丹亭", "A Dupe for the Enemy The Peony Pavilion",
        # "围释 牡丹亭", "The End of the Siege The Peony Pavilion", "遇母 牡丹亭", "Mother and Daughter Reunited The Peony Pavilion", "淮泊 牡丹亭", "Arrival in Huaian The Peony Pavilion",
        # "闹宴 牡丹亭", "Uproar at the Banquet The Peony Pavilion", "榜下 牡丹亭", "Honors bestowed The Peony Pavilion", "索元 牡丹亭", "Searching for the Prize Candidate The Peony Pavilion",
        # "硬拷 牡丹亭", "Interrogation under the Rod The Peony Pavilion", "闻喜 牡丹亭", "Hearing Good News The Peony Pavilion",
        # "圆驾 牡丹亭", "Reunion The Peony Pavilion"]

        searches = []
        for search in searches:
                main(search, quota=1000)
                print(search)
