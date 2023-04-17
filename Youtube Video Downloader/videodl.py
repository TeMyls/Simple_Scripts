from pytube import YouTube,Playlist,Channel
import os

#The purpose of the script is to download from youtube

def make_folder(folder_name):
  parent_dir = os.getcwd()
  folder_path = os.path.join(parent_dir,folder_name)
  #this makes the folder in the same directory as the script
  os.makedirs(folder_name)
  return folder_name

def make_playlist_object(play_list_link):
  return Playlist(play_list_link)
  
def make_channel_object(channel_link):
  return Channel(channel_link)

def show_playlist(play_list):
  dct = {}
  urls_ls = play_list.video_urls
  titles_ls = [video.title for video in play_list.videos]
  #print(urls_ls[0])
  #print(titles_ls[0])
    
    
  for i in range(len(urls_ls)):
    dct.update({titles_ls[i]:urls_ls[i]})
  for i in dct:
    print(f'title:{i}\n\t{dct[i]}')
  print("Finished")
  return dct

def show_channel(channel):
  dct = {}
  urls_ls = channel.video_urls
  titles_ls = [video.title for video in channel.videos]
  for i in range(len(urls_ls)):
    dct.update({titles_ls[i]:urls_ls[i]})
  for i in dct:
    print(f'title:{i}\n\t{dct[i]}')
  print("Finished")
  return dct
      

def dl_whole_channel(channel,SAVE_PATH = os.getcwd()):
  #The channel variable is a Channel object derived from a link to the Channel
  #By default the playlist will download in the current directory
  choice = input("Any Restricted Videos in the Channel?y/n?")
  
  if choice == 'y':
    print(f'Downloading {channel.channel_name}\'s videos with no restrictions')
    yt_dct = show_channel(channel)
    for video in channel.videos:
      try:
        print(f"Downloading{video.title}")
        yt = YouTube(yt_dct[video.title],
                    use_oauth=True,
                    allow_oauth_cache=True
            )


        yt.streams.get_highest_resolution().download(SAVE_PATH)
      except:
        print("error")
        break
    print("done")
  else:
    print(f'Downloading {channel.channel_name}\'s videos')
    for video in channel.videos:    
      video.streams.get_highest_resolution().download(SAVE_PATH)
    print("done")
  


    

def dl_playlist(play_list,SAVE_PATH = os.getcwd()):
  #The play_list variable is a playlist object derived from a link to the playlist
  #By default the playlist will download in the current directory
  choice = input("Any Restricted Videos in the Playlist?y/n?")
  if choice == "y":
        
    print(f'Downloading {play_list.title} with no restrictions')
    yt_dct = show_playlist(play_list)
    print(f"Downloading{video.title}")
    for video in play_list.videos:
        try:
            
          yt = YouTube(yt_dct[video.title],
                      use_oauth=True,
                      allow_oauth_cache=True
              )


          yt.streams.get_highest_resolution().download(SAVE_PATH)
        except:
            print("Error")
            break
    print("Done!")
    
  else:
        
    print(f'Downloading {play_list.title}')
    show_playlist(play_list)
    for video in play_list.videos:
      try:
          print(f"Downloading{video.title}")
          video.streams.get_highest_resolution().download(SAVE_PATH)
      except:
          print("Error")
          break
    print("Done!")


def dl_single_video(link,SAVE_PATH = os.getcwd()):
  #The purpose of this program is to download a single video a put it ontp the folder of choice
  #By default the playlist will download in the current directory unless spec
  choice = 'y' #input("Video Restrictions?y/n?")
  yt = ''
  if choice == "y":
    yt = YouTube(link,
                  use_oauth=True,
                  allow_oauth_cache=True
                
                )
  else:
    yt = YouTube(link)
  video = yt.streams.get_highest_resolution()
  #video = yt.streams.filter(only_audio=True).first()
  print("Title:",yt.title)#Number of views of video
  print("Number of views:" ,yt.views)#Length of the video
  print("Length of video:" ,yt.length,"seconds")#Description of video
  print("Description: ",yt.description)#Rating
  print("Ratings: ",yt.rating)



  #print("Streams: ",yt.streams)
  # filters out all the files with "mp4" extension 
  #audvidfiles = yt.streams.filter(progressive=True)
  #print(audvidfiles)

  #to set the name of the file
  #yt.set_filename('GeeksforGeeks Video')
  # get the video with the extension and
  # resolution passed in the get() function 
  #print(type(yt))

  #dl_video = yt.streams.get_by_itag(139)
  print("Starting Download")
  
  try:

    video.download(SAVE_PATH)
  except:
      print("Some Error!")
  print('Task Completed!')
  


