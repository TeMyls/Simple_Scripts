import os
from PIL import Image
import cv2
import potrace
from numpy import asarray



def make_folder(folder_name):
    parent_dir = os.getcwd()
    folder_path = os.path.join(parent_dir,folder_name)
    #this makes the folder in the same directory as the script
    os.makedirs(folder_name)
    return folder_name



def convert_mp4_to_jpgs(video_path,folder_path):
    video_capture = cv2.VideoCapture(video_path)
    still_reading, image = video_capture.read()
    frame_count = 0
    while still_reading:
        cv2.imwrite(f"{folder_path}/frame_{frame_count:03d}.png", image)
        
        # read next image
        still_reading, image = video_capture.read()
        frame_count += 1



        
def image_folder_to_gif(folder_path,gif_name_without_filetype):
    #Takes the name of the folder containing the images you wish to convert in the current directory and outputs a gif 
    #in the current directory
    #All the images must be the exact same size
    
    images = []
    for image in os.listdir(folder_path):
        #the exact path to the image in the folder
       
        image_Path = os.path.join(folder_path,image)
        img = Image.open(image_Path)
        images.append(img)
    
    images[0].save(f"{gif_name_without_filetype}.gif",format = "GIF",save_all=True, append_images=images,  duration = 800, loop=0)
    return f"{gif_name_without_filetype}.gif"



def strip_frames_from_gif(gif,target_folder):
    im = Image.open(gif)
    key_frame_num = 0
    all_gif_frames = im.n_frames
    #extracting the frames of the gif
   
    choice = input("Do you want a specific frame count? y/n? ")
    if choice.lower() == 'y':
        key_frame_num = int(input("How many frames do you want?\nEnter a number:"))
        for i in range(key_frame_num):
            im.seek(all_gif_frames // key_frame_num * i) 
            im.save(target_folder + f'/frame_{i:03d}.png')
            
            
    if choice.lower() == 'n':
        for i in range(all_gif_frames):
            
            im.seek(i)
            im.save(target_folder + f'/frame_{i:03d}.png')
          
           
            
                
                
    print('Frames Striped')
    
    

def make_transparent(folder_with_no_transparency,folder_with_transparency):
    #making the white background of the gif's images transparent
    tick = 0
    for image in os.listdir(folder_with_no_transparency):
        newImage = []
        image_Path = os.path.join(folder_with_no_transparency,image)
        img = Image.open(image_Path)
        img = img.convert("RGBA")
        for item in img.getdata():
            if item[0] >= 200 and item[1] >= 200 and item[2] >= 200:
                newImage.append((255, 255, 255, 0))
            else:
                newImage.append(item)

        img.putdata(newImage)
        img.save(folder_with_transparency + f'/{tick:03d}.png')
        tick = tick + 1
        
    
    
    print('Transparency Done!')


def make_spritesheet(folder_with_frames,spritesheet_folder,gif):
    #Making into spritesheet
    #Note all images must be of equal sizes
    #This was made with frames of a gif in mind
    
    img_ls = []
    img_2ls = []
    for trimg in os.listdir(folder_with_frames):
        image_Path = os.path.join(folder_with_frames,trimg)
        timg = Image.open(image_Path)
        img_ls.append(timg)
    
    im = Image.open(gif)
    print(f"Rows and Colums multiplied together have to be  {im.n_frames}")
    rows = int(input("How many rows: "))
    cols = int(input("How many columns: "))  
    width = img_ls[0].size[0]
    height = img_ls[0].size[1] 
    new_im = Image.new('RGBA',(cols*width,rows*height))
    print(len(img_ls))
    print(len(img_2ls))
    cnt = 0
    
    for i in range(cols):
        
        for j in range(rows):
            
            new_im.paste(img_ls[cnt],(j*width,i*height))
            cnt += 1
    new_im.save(spritesheet_folder + f"/ss.png")
    print('Spritesheet made')  
    
    
def make_svg_trace(folder_with_no_trace,folder_with_trace):   
    #couldn't get this to work
    for image in os.listdir(folder_with_no_trace):
        image_Path = os.path.join(folder_with_no_trace,image)
        img = Image.open(image_Path)
        numpydata = asarray(img)
        bmp = potrace.Bitmap(numpydata)
        path = bmp.trace()
        for curve in path:
        
            for segment in curve:
                
                end_point_x, end_point_y = segment.end_point
                if segment.is_corner:
                    c_x, c_y = segment.c
                else:
                    c1_x, c1_y = segment.c1
                    c2_x, c2_y = segment.c2
                


def mp4_to_gif(video_path,new_folder_name,gif_name):
    print("starting\t")
    new_folder_name = make_folder(new_folder_name)
    convert_mp4_to_jpgs(video_path,new_folder_name)
    image_folder_to_gif(new_folder_name,gif_name)
    print("finished\n")



def gif_to_spritesheet(gif):
    #the gif should be in current dir not in folder
    gif_name = gif.split(".")[0]
    #you have to make empty folders to deposit the frames into
    #making folders
    parent_dir = os.getcwd()
    normal_frames_folder = make_folder(gif_name + '_frames')
    transparent_folder = make_folder(gif_name + '_transparent')
    Spritesheet_folder = make_folder(gif_name + '_spritesheet')
    
    strip_frames_from_gif(gif,normal_frames_folder)
    make_spritesheet(normal_frames_folder,Spritesheet_folder,gif)
    make_transparent(Spritesheet_folder,transparent_folder)
    
    
    
def webp_to_other_img(folder_name_in_directory):
    #Takes the name of the folder containing the webps you wish to convert in the current directory and outputs another folder  
    #filetype being coverted to
    #file_type = input("Which image file type would you like to convert to? Enter without the dot:")
    file_type = "jpg"
    
    #gettingthe current image directory
    parent_dir = os.getcwd()
    #full path of subfolder containing undesired filetype
    folder_name = os.path.join(parent_dir,folder_name_in_directory)
    #name of new folder of images where pngs will be dumped
    new_folder = make_folder(folder_name+ f'_{file_type}')
    
  
    cnt = 0
    print('Processing')
    print(folder_name)
    
    for image in os.listdir(folder_name):
        #the exact path to the image in the folder
        image_Path = os.path.join(folder_name,image)
        img = Image.open(image_Path)
        if image.endswith('.webp'):
            img = img.convert('RGB')
            img.save(new_folder+ '\\' + f"{cnt:03d}" + f".{file_type}")
        cnt = cnt + 1
    print("done")






