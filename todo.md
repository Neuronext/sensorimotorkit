### current tasks - high priority
- making sure the intervals are spaced at the same time - 250 fps - 4ms
- np reshape should be done later - or check get_image_data what does it give
- dart camera is acquired at the same time 
- timestamp should be added to the image name instead of indexes
- videos are not getting saved properly
- the frame rate should be 125, we can use binning/subsampling to cut out the extra pixels
- append images instead 
- SpinView images are currently in Gray, convert to RGB
- The frame rate is currently 150+ fps, need to reduce it to a resonable value
- remove credentials.json from the repo
- bypass onboard storage and write directly to disk
- resolution of one body camera is (1200, 960) and the other is (600, 960)


### current tasks - low priority
- Add code to do actual body tracking
- Add documentation for the code
- Add timestamps for the images in order to sync different data streams
- fix the conda env and add requirements.txt as a part of the github repo 

### from before
adding more cameras
set up onedrive/aws in order to push all the vids/csvs to cloud
create a cron job to push all the data to google cloud
more people tracking - check the algo 
start with the inital set up for motor primers