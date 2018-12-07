# -*- coding: utf-8 -*-
"""
Spyder Editor


"""
import csv as csv
import numpy as np
import pandas as pd
columns = ['video_id', 'title', ]

#Load Data from viral videos

ca_vid = pd.read_csv("C:/Users/Girijesh/Desktop/DM Docs/Project/project_data/CAvideos.csv")
gb_vds = pd.read_csv("C:/Users/Girijesh/Desktop/DM Docs/Project/project_data/GBvideos.csv",  error_bad_lines= False )
us_vid = pd.read_csv("C:/Users/Girijesh/Desktop/DM Docs/Project/project_data/USvideos.csv", error_bad_lines = False)
us_comments =pd.read_csv("C:/Users/Girijesh/Desktop/DM Docs/Project/project_data/UScomments.csv", error_bad_lines = False)
de_vid = pd.read_csv("C:/Users/Girijesh/Desktop/DM Docs/Project/project_data/DEvideos.csv", error_bad_lines =False)
gb_comments = pd.read_csv("C:/Users/Girijesh/Desktop/DM Docs/Project/project_data/GBcomments.csv", error_bad_lines= False)
us_vid1= pd.read_csv("C:/Users/Girijesh/Desktop/DM Docs/Project/project_data/Usvideos1.csv", error_bad_lines =False)

 #print(us_vid['date'].unique())
 #print(gb_vds['date'].unique())
 
# print('')
#us_vid_head = us_vid.head()#video, title, tags, published date, caetogory_id, views, likes, dislikes, comment_total, thumbnail, date
#category
import json
with open('C:/Users/Girijesh/Desktop/DM Docs/Project/project_data/US_category_id.json') as json_data:
    d = json.load(json_data)
    category_tit= []
    category_id = []
    for row in d['items']:
        category_tit.append(row['snippet']['title'])
        category_id.append(row["id"])
        #category_tit["id"] = row["id"]
        #category_tit["title"]
        
        #Pandas
        import pandas
        us_vid1["trending_date"] = pd.to_datetime(us_vid1["trending_date"], format = "%y.%d.%m")
        us_vid1["std_trending_date"] = pd.to_datetime(us_vid1["trending_date"]).apply(lambda x:x.date().strftime('%y.%d.%m'))
        us_vid1["publish_time"] = pd.to_datetime(us_vid1["publish_time"])
        us_vid1["std_publish_time"] = pd.to_datetime(us_vid1["publish_time"]).apply(lambda x:x.date().strftime('%y.%d.%m'))
        
      

        
        us_vid1["trending_year"]   = us_vid1["trending_date"].dt.year  
        us_vid1["trending_month"]   = us_vid1["trending_date"].dt.month
        us_vid1["trending_day"] = us_vid1["trending_date"].dt.day
        us_vid1["trending_week"] = us_vid1["trending_date"].dt.dayofweek
        us_vid1["publish_year"]   = us_vid1["publish_time"].dt.year
        us_vid1["publish_month"]   = us_vid1["publish_time"].dt.month
        us_vid1["publish_day"] = us_vid1["publish_time"].dt.day
        us_vid1["publish_week"] = us_vid1["publish_time"].dt.dayofweek
        us_vid1["publish_hour"] = us_vid1["publish_time"].dt.hour
        
        # Numbering on week??
        
        day_maping= {0: 'Mon', 1:'Tue', 2: 'Wed', 3: 'Thu', 4: 'Fri', 5: 'Sat', 6: 'Sun'}
        us_vid1["publish_week"] = us_vid1["publish_week"].map(day_maping)
        us_vid1["trending_week"] = us_vid1["trending_week"].map(day_maping)
        
        # Data Type for each variable 
        us_vid1.dtypes
        us_category = pd.DataFrame({"id": category_id, "title": category_tit})
        
      #Number of Tags in video:       
        x= us_vid1.loc[:, 'tags'].tolist()
        tags_lis = []
        import re
        for j in x:
            for k in j.split("\n"):
                tags_lis.append(re.sub(r"[^a-zA-Z0-9]+", ' ', k))
                
                tags_df= pd.DataFrame({"tags_n":tags_lis})
                
                tag_num = []
                for i in tags_df['tags_n']:
                    tag_num.append(len(i.split()))
                    
                    tag_num_df = pd.DataFrame({"tag_count": tag_num})
                    
                    us_vid1["tag_count"] = tag_num_df["tag_count"]
                    
                   # Days between Publish and Trending time: 
                    from datetime import datetime
                    import datetime
                    date_format = "%y.%d.%m"
                    
                    
                    ii = []
                    for i in us_vid1["std_trending_date"]:
                        ii.append(datetime.datetime.strptime(i, date_format))
                       jj = [] 
                        for j in us_vid1["std_publish_time"]:
                            jj.append(datetime.datetime.strptime(j, date_format))
                          cc= []  
                          
                          for k in range(len(ii)):
                              cc.append(ii[k] -jj[k])
                              us_vid1["no_of_days"] = cc
                            
                            no_days= pd.DataFrame({"days_between": cc})
                            
                            # Average Views over time:
                                views= []
                                views = us_vid1["views"]
                                        
                                Avg_views= []
                                
                                for ll in range(len(views)):
                                    Avg_views.append(views[ll]/cc[ll])
                                
                                # Average Likes Over Time:
                                    
                                    
                                    
                                    #Average Dislikes over time:
                                       from collections import Counter
                                 #Converting into lower case
                                    us_vid1["tags"] = us_vid1["tags"].str.lower()
                                                                       
                                  #Counting
                                       tag_freq = pd.DataFrame({"tag_freq": Counter("".join(us_vid1["tags"]).split('|')).most_common() })
                                       
                                           
                                       ll = []
                                       mn = []
                                       for row in tag_freq["tag_freq"]:
                                           ll.append(row[0])
                                           mn.append(row[1])
                                           us_vid["tags"] = us_vid1["tags"].split('|')
                                           
                                           tag_1= pd.DataFrame({"tag_names": ll, "counts": mn})
                                           
                                           tag_1["tag_weights"]= tag_1["counts"]/sum(tag_1["counts"])
                                           
                                           split_tag = us_vid1["tags"].str.split('|')
                                           i=0
                                           tag_score=[]
                                           for x in range(0,1):
                                               #print(rola)
                                               for y in range(len(split_tag[0])):
                                                   tag_score.append.loc(tag_1[tag_1['tag_names']==split_tag[0][0], 'tag_weights'])
                                                   #print(tag_score)
                                           dict_tag = dict(zip(tag_1.tag_names, tag_1.tag_weights))
                                           
                                           
                                           split_tag['score']=split_tag.map(dict_tag)
                                           
                                          for i in range(len(split_tag)):
                                              print(i)#28950
                                              split_tag['score']=split_tag[i].map(dict_tag)
                                          
                                              for j in range(len(split_tag[i])):
                                                  print(j)# 
                                                  if split_tag[i][j]== ([row for  row in tag_1["tag_names"]]):
                                                      print(tag_1["tag_weights"])
                                                  
                                                 # for row in tag_1["tag_names"]:
                                                  #    print(row)
                                           
                                           
                                           
                                           
                
                
                
    
        
        
        
    
        
 
