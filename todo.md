### todo
- gui not responding when collecting data
- acquire time in gui
- code for the skeleton plot for the body camera
- eeg visualization:
    - voltage plot for all the egg channels
    - mean, min, max across all the channels - show which channel as well
- add a dropdown for target selection in the GUI 
- fix the drift in mediapipe
    - check if it is coming from the training data 
    - check if you are able to train mediapipe further for angled data, from huggingface 
- check for emotional decoding module from meta, check if it has facial detection module
- check if finegrained hand data can be obtained, especially to track a person exploring an aobject in their hand
- check for output compatibility with eeglab, erplab, fieldtrip, update documentation and readme accordingly 
[updated 02/16]
- eye tracking using body cam
- make the body cam images colored and not grayscale
- eeg signals are not getting collected
- gui does not responding, hence not exactly sure when the data collection starts and ends
- also i think the data collection is happening for a shorter duration than expected
- add target selection to the GUI
    - read images from the folder and display them in the dropdown
- two computer setup is working for emg and eyetracking, so the gui should reflect the start and end of the trial for those
- can we play a sound for start and end of trial
- output should be formatted in standardized format example compatible with eeglab
- retest components of the kit
- flowchart needs to be updated with the documentation <need_help_jack>
- product links need to be added to the documentation <need_help_jack>

### software issues jack is facing
- fft for the eeg data - 16 channel csvs
  - this is required for finding bandpower for corresponding brain waves
  - to find dominant frequency
- csv for gloves is not formatted properly, it has a lot of extra commas
  - the csv file contains the xyz coord of the fingers, required for aligning with the finger images
- finding the dart in the image


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
