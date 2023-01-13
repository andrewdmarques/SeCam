#########################################################
# Import libraries
#########################################################
import datetime # To get the current time.
import os       # To manage the files.
import time
import csv      # To manage the log file.
from PIL import Image, ImageDraw # To combine the images

#########################################################
# User defined variables.
#########################################################
dir_main = '/home/andrewdmarques/Desktop/Rmtrackr/Temp' # Location to save all files to
locs =  ['back-door', 'back-north', 'back-south','broken']       # List of all cameras that are present 
devices = ['/dev/video2','/dev/video4','/dev/video0','/dev/video6']   # List of all webcam devices
x = 1                                  # Temp for setting the number of images to take
iter_max = 100
disk_max = 95
error = 'no'




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

# Function that combines the photos.
def create_collage(filenames):
  # Create a blank image with a white background
  width, height = 800, 400
  collage = Image.new('RGB', (width, height), (255, 255, 255))

  # Create a black image to use as a placeholder for non-existent files
  black_image = Image.new('RGB', (100, 100), (0, 0, 0))

  # Load the images
  images = []
  for filename in filenames:
    try:
      image = Image.open(filename)
    except FileNotFoundError:
      image = black_image
    images.append(image)

  # Calculate the size and position of each image in the collage
  image_width, image_height = int(width / 4), int(height / 2)
  for i, image in enumerate(images):
    x = (i % 4) * image_width
    y = (i // 4) * image_height
    collage.paste(image, (x, y, x + image_width, y + image_height))

  return collage

# Function that determines how many locations are present then returns a list with dummy items to bring it to a total of 8.
def pad_list(dir_path,locs,dir3):
  # Add dummy items until there are at least 8 items in the list
  while len(locs) < 8:
    items = locs
    items.append('dummy')
  # Get the filenames for the items.
  file_names = []
  for ii in list(range(1:len(items))):
      file_name.append(dir_path + '/' + locs[ii] + '_' + dir3)
  return file_names

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
        for ii in list(range(0,len(locs))):
            print(ii)
            print(locs[ii])
            pic_command = take_pic(ii,devices,locs,dir_path,dir3)
            print(pic_command)
        
        # Make a collage with all the images from this timepoint.
        locs_new = pad_list(locs)
        
        
        # print('time ffmpeg -f v4l2 -video_size 1280x960 -i /dev/video0 -frames 1 ' + fil_name)
        x += 1