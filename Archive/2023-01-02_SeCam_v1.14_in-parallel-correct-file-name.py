#########################################################
# Import libraries
#########################################################
import datetime                  # To get the current time.
import os                        # To manage the files.
import time
import csv                       # To manage the log file.
from PIL import Image, ImageDraw # To combine the images
from PIL import Image, ImageDraw, ImageFont       # To add text to the image.
import subprocess                # This is for running bash functions through python.

#########################################################
# User defined variables.
#########################################################
dir_main = '/home/andrewdmarques/Desktop/Rmtrackr/Temp' # Location to save all files to
locs =  ['back-door', 'back-north', 'back-south','broken']       # List of all cameras that are present 
devices = ['/dev/video2','/dev/video4','/dev/video0','/dev/video6']   # List of all webcam devices
x = 1                                  # Temp for setting the number of images to take
iter_max = 20
disk_max = 93.0 # The minimum amount of free space that should be kept on the computer [0-100].
error = 'no'
i_columns = 3                     # The number of columns in the collage summary file.
j_rows = 3                        # The number of rows in the collage summary file.
num_cams = i_columns*j_rows       # The total number of panels to be padded for.
time_pic = 5                      # Time (seconds) for each photo to be taken.
time_log = 2                      # Time (minutes) for how often a log status report should be written.


#########################################################
# Define functions.
#########################################################

# Function to initiate the log file.
def initiate_log(dir_main):
    # Determine if there is a log file present.
    log_exist = 'no'
    if os.path.isfile(dir_main + "/log.csv"):
        log_exist = 'yes'
        print('log exists')
    
    # Make the log file if it doesn't exist.
    if log_exist == 'no':
        print('Creating log file')
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

# Function to report a new item to the log.
def append_log(dir_main,error,text):
    # Get the current time in the desired format
    current_time = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    # open the csv file in append mode
    with open(dir_main + "/log.csv",'a', newline='') as csv_file:
        # create a csv writer object
        writer = csv.writer(csv_file)
        # add the new row to the csv file
        writer.writerow([error, current_time, text])
    
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
print(f"free space: {free_space_percent:.2f}%")

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
            
def add_text_to_image(image_path, text):
    # Open the image
    image = Image.open(image_path)

    # Create a drawing context
    draw = ImageDraw.Draw(image)

    # Get the width and height of the image
    width, height = image.size

    # Select a font
    font = ImageFont.truetype('Arial.ttf', 50)

    # Get the size of the text
    text_width, text_height = draw.textsize(text, font=font)

    # Calculate the position of the bottom left corner of the image
    x = 0
    y = height - text_height

    # Add the text to the image
    draw.text((x, y), text, font=font, fill=(255, 255, 255))

    # Save the image
    image.save(image_path)
ff = '/home/andrewdmarques/Desktop/Rmtrackr/Temp/2022-12/31/back-north_11-00-55.jpg'
image = Image.open(ff)
image.show()
add_text_to_image(ff,'test 1 2 3')
image = Image.open(ff)
image.show()

#########################################################
# Run.
#########################################################
print('start')
pic_new = 'no'
# Initiate log.
log_written = 'no'
initiate_log(dir_main)
append_log(dir_main,error,'script started')

while x <= iter_max:
    time.sleep(0.2)
    pic = 'no'
    log_write = 'no'
    # Determine if there is enough memory available to keep taking pictures.
    free_space = get_free_space_percent()
    if free_space <= disk_max:
        text = 'max alloted space reached: ' + str(free_space) + '/' + str(disk_max)
        print(text)
        error = 'yes'
        append_log(dir_main,error,text)
        break
    
    # Determine the current directories to store the files.
    now = datetime.datetime.now()
    dir1 = now.strftime('%Y-%m')
    dir2 = now.strftime('%d')
    dir3 = now.strftime('%H-%M-%S')+'.jpg'
    now_sec = now.strftime('%S')
    now_min = now.strftime('%M')
    print(str(now) + '\t\t' + f"free space: {free_space:.4f}%")
    #print(now)
    #print(int(now_sec)%5 == 0)
    
    # Determine if a photo should be taken.
    if int(now_sec) % time_pic == 0:
        # print(pic_new)
        if pic_new == 'yes':
            pic = 'yes'
            pic_new = 'no'
            # print(pic)
    if int(now_sec) % 5 != 0:
        pic = 'no'
        pic_new = 'yes'
        
    # If it is time to take a picture.
    if pic == 'yes':
        pic = 'no'
        # Format the time as a string in the desired format
        time_string = now.strftime('%Y-%m-%d-%H-%M-%S')
        
        # Record the free space to the log -- every 5 minutes (when time_log = 5)
        if int(now_min) % time_log == 0: # Determine if the minute is on the 5, then write to the log.
            log_write = 'yes'
        if int(now_min) % time_log != 0: # Reset once the minute is no longer on the 5 so that it can be written when apporpriate next time.
            log_written = 'no'
        if log_write == 'yes' and log_written == 'no': # If it is time to write the log and it has not been written yet, then write it.
            log_written = 'yes'
            append_log(dir_main,error,f"free space: {free_space:.2f}%")
            
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
        print('making collage')
        locs_new = pad_list(dir_path,locs,dir3,num_cams)
        collage = create_collage(locs_new,2,2)
        collage_fname = dir_path + '/collage_' + dir3
        collage.save(collage_fname)
        
        # print('time ffmpeg -f v4l2 -video_size 1280x960 -i /dev/video0 -frames 1 ' + fil_name)
        x += 1