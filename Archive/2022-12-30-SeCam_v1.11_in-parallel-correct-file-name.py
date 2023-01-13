#########################################################
# Import libraries
#########################################################
import datetime                  # To get the current time.
import os                        # To manage the files.
import time
import csv                       # To manage the log file.
from PIL import Image, ImageDraw # To combine the images
import subprocess                # This is for running bash functions through python

#########################################################
# User defined variables.
#########################################################
dir_main = '/home/andrewdmarques/Desktop/Rmtrackr/Temp' # Location to save all files to
locs =  ['back-door', 'back-north', 'back-south','broken']       # List of all cameras that are present 
devices = ['/dev/video2','/dev/video4','/dev/video0','/dev/video6']   # List of all webcam devices
x = 1                                  # Temp for setting the number of images to take
iter_max = 12
disk_max = 95
error = 'no'
i_columns = 3                     # The number of columns in the collage summary file.
j_rows = 3                        # The number of rows in the collage summary file.
num_cams = i_columns*j_rows       # The total number of panels to be padded for.
time_loop = 5                     # Time (seconds) for each photo to be taken.



#########################################################
# Define functions.
#########################################################

# Function to initiate the log file.
def initiate_log():
    # Determine if there is a log file present.
    log_exist = 'no'
    if os.path.isfile(dir_main + "/log.csv"):
        log_exist = 'yes'
    
    # Make the log file if it doesn't exist.
    if log_exist == 'no':
        # Get the current time in the desired format
        current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        # Open the CSV file for writing
        with open(dir_main + "/log.csv", "w", newline="") as csv_file:
            # Create a CSV writer object
            writer = csv.writer(csv_file)
            # Write the header row
            writer.writerow(["error", "time", "text"])
            # Write the first data row
            writer.writerow(["no", current_time, "initiate"])
    
# Define function that takes pictures
def take_pic(ii,devices,locs,dir_path,dir3):
        fil_name = dir_path + '/' + locs[ii] + '_' + dir3
        pic_command = 'time ffmpeg -f v4l2 -video_size 1280x960 -i  ' + devices[ii] + ' -frames 1 ' + fil_name
        os.system(pic_command)
        return(pic_command)
    
# Function to take images in parallel.
def parallel_image(devices,locs,dir_path,dir3):
    processes = []
    for ii in range(len(devices)):
        fil_name = dir_path + '/' + locs[ii] + '_' + dir3
        pic_command = "time ffmpeg -f v4l2 -video_size 1280x960 -i " + devices[ii] + " -vframes 1 " + fil_name
        processes.append(subprocess.Popen(pic_command, shell=True))
    
    for process in processes:
        process.wait()
    
    print("Pictures taken with all webcams.")
#parallel_image(devices,locs,dir_path,dir3)

    
# Function to determine how much free space is available and returns a value XX.XXXXX
def get_free_space_percent():
    # Get the file system stats
    stats = os.statvfs("/")
    # Get the block size
    block_size = stats.f_bsize
    # Get the total number of blocks
    total_blocks = stats.f_blocks
    # Get the number of free blocks
    free_blocks = stats.f_bfree
    # Calculate the total amount of disk space (in bytes)
    total_size = block_size * total_blocks
    # Calculate the amount of free disk space (in bytes)
    free_size = block_size * free_blocks
    # Calculate the percent of free space
    free_space_percent = (free_size / total_size) * 100
    # Return the result
    return free_space_percent

free_space_percent = get_free_space_percent()
print(f"Free space: {free_space_percent:.2f}%")

# Function that determines how many locations are present then returns a list with dummy items to bring it to a total of 8.
def pad_list(dir_path,locs,dir3,num_cams):
  # Add dummy items until there are at least 8 items in the list
  items = locs.copy()
  while len(items) <= num_cams:
    items.append('dummy')
  # Get the filenames for the items.
  file_names = []
  for ii in list(range(1,len(items))):
      file_names.append(dir_path + '/' + items[ii] + '_' + dir3)
  return file_names

# Function that combines the photos into a collage. The input dimensions are i columns and j rows.
def create_collage(file_names, i, j):
  # Create a blank image with a white background
  collage = Image.new("RGB", (j*1280, i*960), (255, 255, 255))
  
  # Iterate through the file names
  for k, file_name in enumerate(file_names):
    try:
      # Open the image file
      img = Image.open(file_name)
      
      # Check if the image has a different size than the others
      if img.size != (1280, 960):
        # If it does, then resize it to (1280, 960)
        img = img.resize((1280, 960))
      
      # Calculate the position to paste the image
      x = (k % j) * 1280
      y = (k // j) * 960
      
      # Paste the image onto the collage
      collage.paste(img, (x, y))
    except FileNotFoundError:
      # If the file doesn't exist, then create a blank black image to take its place
      img = Image.new("RGB", (1280, 960), (0, 0, 0))
      
      # Calculate the position to paste the image
      x = (k % j) * 1280
      y = (k // j) * 960
      
      # Paste the image onto the collage
      collage.paste(img, (x, y))
      
  # Return the collage image
  return collage
#XXX Remove this.
#collage = create_collage(file_names,3,3)
#collage.save('/home/andrewdmarques/Desktop/Rmtrackr/Temp/collage.jpg')

# Function that can be used to delete a list of files.
def delete_files(file_names,delete):
    if delete == 'yes':
        for file_name in file_names:
            try:
              # Delete the file
              os.remove(file_name)
            except FileNotFoundError:
              # If the file doesn't exist, do nothing
              pass
            

    


#########################################################
# Run.
#########################################################
print('start')
pic_new = 'no'
while x <= iter_max:
    time.sleep(0.2)
    pic = 'no'
    # Determine the current directories to store the files.
    now = datetime.datetime.now()
    dir1 = now.strftime('%Y-%m')
    dir2 = now.strftime('%d')
    dir3 = now.strftime('%H-%M-%S')+'.jpg'
    now_sec = now.strftime('%S')
    print(now)
    #print(int(now_sec)%5 == 0)
    
    # Determine if a photo should be taken.
    if int(now_sec) % time_loop == 0:
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
        for ii in list(range(0,len(locs))):
            print(ii)
            print(locs[ii])
            #pic_command = take_pic(ii,devices,locs,dir_path,dir3)
            #print(pic_command)
        parallel_image(devices,locs,dir_path,dir3)
        
        # Make a collage with all the images from this timepoint.
        locs_new = pad_list(dir_path,locs,dir3,num_cams)
        
        
        # print('time ffmpeg -f v4l2 -video_size 1280x960 -i /dev/video0 -frames 1 ' + fil_name)
        x += 1