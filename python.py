from apiclient.discovery import build
import argparse
import unidecode
import pandas as pd

DEVELOPER_KEY = "AIzaSyC8Omwl32t7kJRfIjphsEWN2BdJGqbQ6jM"
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"

#global variable declaration
titles =[]
PublishTime =[]
videoIds=[]
channelTitles=[]
video_descriptions=[]
viewCounts=[]
likeCounts=[]
dislikeCounts=[]
commentCounts=[]
favouriteCounts=[]
URLS=[]
Audience_Response=[]

#youtube_movie_review will search for the given movie trailer in youtube,take 10 results and create dataframe
def youtube_movie_review(options):
    youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
    print(youtube) #youtube object is returned
    #Call the search.list method to retrieve results matching the specified query term.
    search_response = youtube.search().list(q=options.q, part="id,snippet", maxResults=options.max_results).execute()
    print(search_response)


    for search_result in search_response.get("items", []):
        if search_result["id"]["kind"] == "youtube#video":
            title = search_result["snippet"]["title"]
            title = unidecode.unidecode(title)
            titles.append(title)
            print("Title: " + title)
            publishedAt=search_result["snippet"]["publishedAt"]
            PublishTime.append(publishedAt)
            print("publishedAt :"+str(publishedAt))
            channelTitle=search_result["snippet"]["channelTitle"]
            print("channel title : "+channelTitle)
            channelTitles.append(channelTitle)
            videoId=search_result["id"]["videoId"]
            print("videoId: "+str(videoId))
            videoIds.append(videoId)
            url=""+videoId
            URLS.append(url)
            video_description=search_result['snippet'] ['description']
            print("Description : "+video_description)
            video_descriptions.append(video_description)


            video_response = youtube.videos().list(id=videoId,part="statistics").execute()

            for video_result in video_response.get("items",[]):
                viewCount = video_result["statistics"]["viewcount"]
                viewCounts.append(viewCount)
                if 'likeCount' not in video_result["statistics"]:
                    likeCount = 0
                else:
                    likeCount = video_result["statistics"]["likeCount"]
                likeCounts.append(likeCount)

                if 'dislikeCount' not in video_result["statistics"]:
                    dislikeCount = 0
                else:
                    dislikeCount = video_result["statistics"]["dislikeCount"]
                dislikeCounts.append(dislikeCount)
                if 'commentCount' not in video_result["statistics"]:
                    commentCount = 0
                else:
                    commentCount = video_result["statistics"]["commentCount"]
                commentCounts.append(commentCount)
                if 'favoriteCount' not in video_result["statistics"]:
                    favouriteCount = 0
                else:
                    favouriteCount = video_result["statistics"]["favouriteCount"]
                favouriteCounts.append(favouriteCount)
    #print(title)
    print("Total Views : "+ str(viewCount))
    print("Total Likes : "+ str(likeCount))
    print("Total Dislikes :"+str(dislikeCount))
    print("Total Comments : "+str(commentCount))


    dict1={"Title":titles,"PublishTime":PublishTime,"URL": URLS,"Channel_Name":channelTitles,"Description":video_descriptions,"viewCount":viewCount}
    df = pd.Dataframe.from_dict(dict1, orient ='index')
    df1 = df.transpose()
    df1.columns = ['Title','PublishTime','URL','Channel_Name','Description','viewCount','commentCount','likeCount','dislikeCount','Audience_Response']
    #print(df1)
    #df1[Audience_Response]=NULL
    for ind in df1.index:
        if int(df1['likeCount'][ind])>int(df1['dislikeCount'][ind]):
            df1['Audience_response'][ind]="Positive"
        elif int(df1('likeCount')[ind])==int(df1['dislikeCount'][ind]):
            df1['Audience_Response'][ind]="Neutral"
        elif int(df1('likeCount')[ind])<int(df1['dislikeCount'][ind]):
            df1['Audience_reponse'][ind]="Negative"
    print(df1)
    return df1
    

if __name__ == "__main__":
    print("Enter the movie name released in 2020 : ")
    x = str(input())
    parser = argparse.ArgumentParser(description='youtube search')
    parser.add_argument("--q", help="Search term", default=x+"Movie Trailer 2020")
    parser.add_argument("--max-results", help="Max results", default=10)
    args = parser.parse_args()
    #call youtube search method and pass this combined argument
    youtube_response_df=youtube_movie_review(args)  #result is getting returned as a dataframe
    youtube_response_df.to_csv(r"C:\Users\Owner\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Python 3.9\newfolder"+x+".csv",header=True)