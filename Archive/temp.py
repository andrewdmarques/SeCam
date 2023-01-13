while x <= max:
  # Determine the current directories to store the files.
  now = datetime.datetime.now()
  dir1 = now.strftime('%Y-%m')
  dir2 = now.strftime('%d')
  dir3 = now.strftime('%H-%M-%S')+'.jpg'
  now_sec = now.strftime('%S')
  
  if now_sec % 5 == 0:
    # Format the time as a string in the desired format
    time_string = now.strftime('%Y-%m-%d-%H-%M-%S')
  
  
  