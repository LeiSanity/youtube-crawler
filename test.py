# API client library
import googleapiclient.discovery
import json
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

                        # iterate over items
                        for item in response['items']:
                                vid = item['id']['videoId']
                                publishedAt = item['snippet']['publishedAt']
                                channelId = item['snippet']['channelId']
                                title = item['snippet']['title']                                

                                # retrieve info based on video id
                                stats1 = youtube.videos().list(
                                        part="statistics",
                                        id=vid,
                                        fields="items(statistics)"
                                ).execute()
                                views = stats1['items'][0]['statistics'].get('viewCount', 0)
                                likes = stats1['items'][0]['statistics'].get('likeCount', 0)
                                comments = stats1['items'][0]['statistics'].get('commentCount', 0)

                                # retrieve info based on channel id
                                stats2 = youtube.channels().list(
                                        part="statistics, snippet",
                                        id=channelId,
                                        fields="items(snippet(title)), items(statistics(subscriberCount))"
                                ).execute()
                                username = stats2["items"][0]["snippet"]["title"]
                                subscriptions = stats2["items"][0]["statistics"]["subscriberCount"]
                                
                                # standard output
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

                                # limit number of outputs
                                cnt += 1
                                print(cnt)             
                                res.append(tmp_dic)
                                if cnt == quota:
                                        flag = False
                except Exception as e:
                        print(e)
                        flag = False

        # write json file
        with open(f'{search}.json', 'w') as output_file:
                json.dump(res, output_file, ensure_ascii=False)

        # convert to xlsx file
        df = pd.read_json(f'{search}.json')
        df.to_excel(f'{search}.xlsx')
        

if __name__ == '__main__':
        # finished_searches = ["青春版牡丹亭", "临川四梦 牡丹亭", "玉茗堂四梦 牡丹亭", "杜丽娘慕色还魂", "牡丹亭梦", "Dream in Peony Pavilion"]

        # add search terms into list
        searches = ["lakers"] # for example
        for search in searches:
                main(search, quota=1000)
                print(search)
