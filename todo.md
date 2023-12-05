### retest
- retest the frame rates by changing binning and resolution
- testing if dart camera is working with the body cameras
- the frame rate should be 125, we can use binning/subsampling to cut out the extra pixels

### short scripts
- script for feature extraction for modalitites like eeg, emg etc
- script to run feature extraction module for a given day
- software should have compatibility with gloves for both right and left hands
- output should be formatted in standardized format example compatible with eeglab
- push all the images to gcloud/aws on a daily basis, create cron job

### enhancement
- can probably use Python Taskflow in order to parallelize data acquisition for multiple modalities
- expand the tracking to include more than one person
- add better logging
    - all print statements should have a [MAIN/MODALITY] prefix associated with it
    - refactor all the print statements to use the logging module