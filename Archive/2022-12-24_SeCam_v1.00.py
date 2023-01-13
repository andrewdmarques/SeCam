/home/andrewdmarques/Desktop/Rmtrackr/Training-Photos


time mplayer tv:// -tv driver=v4l2:device=/dev/video2:width=50:height=50 -frames 1000 -vo jpeg


time mplayer tv:// -tv driver=v4l2:device=/dev/video2:width=50:height=50 -frames 100 -vo jpeg:outdir=/home/andrewdmarques/Desktop/Rmtrackr/Training-Photos


time mplayer tv:// -tv driver=v4l2:device=/dev/video2 -frames 10000 -vo jpeg:outdir=/home/andrewdmarques/Desktop/Rmtrackr/Training-Photos/Temp


time ffmpeg -f v4l2 -video_size 1280x960 -i /dev/video2 -frames 1 temp.jpg

# Import libraries
import datetime # To get the current time.
import os       # To manage the files

# User defined variables.
dir_main = '/home/andrewdmarques/Desktop/Rmtrackr/Temp'
loc = 'back-door'
x = 1
max = 10
while x <= max:
    # Determine the current directories to store the files.
    now = datetime.datetime.now()
    dir1 = now.strftime('%Y-%m')
    dir2 = now.strftime('%d')
    dir3 = now.strftime('%H-%M-%S')+'.jpg'
    
    # Format the time as a string in the desired format
    time_string = now.strftime('%Y-%m-%d-%H-%M-%S')
    
    # Make the directory if it is not yet made.
    dir_path = dir_main + '/' + dir1 + '/' + dir2
    if not os.path.exists(dir_path):
            os.makedirs(dir_path)
            
    # Take a photo and save it as the file name.
    fil_name = dir_path + '/' + loc + '_' + dir3
    os.system('time ffmpeg -f v4l2 -video_size 1280x960 -i /dev/video0 -frames 1 ' + fil_name)
    
    