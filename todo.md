### todo
- add a dropdown for target selection in the GUI 
- fix the drift in mediapipe 
  - this cannot be done for the blazepose model that is used for body pose estimation. can use these instead: (human)[https://github.com/vladmandic/human/tree/main] or (human-models)[https://github.com/vladmandic/human-models/tree/main]. seems like some effort to bring it up. 
- check for emotional decoding module from meta, check if it has facial detection module : can use (this)[https://github.com/vladmandic/human] 
- check if finegrained hand data can be obtained, especially to track a person exploring an aobject in their hand
- check for output compatibility with eeglab, erplab, fieldtrip, update documentation and readme accordingly 
- gui not responding when collecting data
- retest components of the kit
- flowchart needs to be updated with the documentation <need_help_jack>

### <ask_jack> for the following
- eeg + emg issues
    - they are not working together 
    - we do not stream all the channels currently
    - 16 channels of the data need to go into 16 individual files for these modalities

### retest
- retest the frame rates by changing binning and resolution
- testing if dart camera is working with the body cameras
- the frame rate should be 125, we can use binning/subsampling to cut out the extra pixels

### gui todos?
- metadata needs to include duration time
- Trial couner should be bigger 
- traffic lights should be circular
- comments should have a bigger scrollable text box
- retest the behaviour of the comments/other form fields on start, stop, pause
- after the trail is over the user needs to explicitly click on x button to close the gui - <ask_tansu>
- data visualization 
    - camera displays needs to be added
    - glove data 

### cleanup todos
- codebase cleanup
- cleanup the print statements

### short scripts
- script to run feature extraction module for a modality for a given day
- push all the images to gcloud/aws on a daily basis, create cron job

### enhancements
- software should have compatibility with gloves for both right and left hands
- expand the tracking to include more than one person
- add better logging
    - all print statements should have a [MAIN/MODALITY] prefix associated with it
    - refactor all the print statements to use the logging module
