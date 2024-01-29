### todo
- flowchart needs to be updated with the documentation 
- add a dropdown for target selection in the GUI 
- output should be formatted in standardized format example compatible with eeglab
- gui not responding when collecting data
- product links need to be added to the documentation
- retest components of the kit

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
