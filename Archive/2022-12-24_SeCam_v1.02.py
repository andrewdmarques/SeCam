# Import libraries
import datetime # To get the current time.
import os       # To manage the files
import time

# User defined variables.
dir_main = '/home/andrewdmarques/Desktop/Rmtrackr/Temp'
loc = 'back-door'
x = 1
max = 5
print('start')
pic_new = 'no'
while x <= max:
    time.sleep(0.2)
    pic = 'no'
    # Determine the current directories to store the files.
    now = datetime.datetime.now()
    dir1 = now.strftime('%Y-%m')
    dir2 = now.strftime('%d')
    dir3 = now.strftime('%H-%M-%S')+'.jpg'
    now_sec = now.strftime('%S')
    #print(int(now_sec)%5 == 0)
    
    # Determine if a photo should be taken.
    if int(now_sec) % 5 == 0:
        # print(pic_new)
        if pic_new == 'yes':
            pic = 'yes'
            pic_new = 'no'
            # print(pic)
    if int(now_sec) % 5 != 0:
        pic = 'no'
        pic_new = 'yes'
        
    
    if pic == 'yes':
        pic = 'no'
        # Format the time as a string in the desired format
        time_string = now.strftime('%Y-%m-%d-%H-%M-%S')
        
        # Make the directory if it is not yet made.
        dir_path = dir_main + '/' + dir1 + '/' + dir2
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            
        # Take a photo and save it as the file name.
        fil_name = dir_path + '/' + loc + '_' + dir3
        os.system('time ffmpeg -f v4l2 -video_size 1280x960 -i /dev/video0 -frames 1 ' + fil_name)
        # print('time ffmpeg -f v4l2 -video_size 1280x960 -i /dev/video0 -frames 1 ' + fil_name)
        x += 1