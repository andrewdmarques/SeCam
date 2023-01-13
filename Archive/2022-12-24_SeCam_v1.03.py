#########################################################
# Import libraries
#########################################################
import datetime # To get the current time.
import os       # To manage the files.
import time
import csv      # To manage the log file.

#########################################################
# User defined variables.
#########################################################
dir_main = '/home/andrewdmarques/Desktop/Rmtrackr/Temp' # Location to save all files to
loc =  = ["back-door", "back-north", "back-south"]      # List of all cameras that are present 
x = 1                                  # Temp for setting the number of images to take
iter_max = 5
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
        
        fil_name = dir_path + '/' + loc + '_' + dir3
        os.system('time ffmpeg -f v4l2 -video_size 1280x960 -i /dev/video0 -frames 1 ' + fil_name)
        # print('time ffmpeg -f v4l2 -video_size 1280x960 -i /dev/video0 -frames 1 ' + fil_name)
        x += 1