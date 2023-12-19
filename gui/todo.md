- one round of testing to make sure
    - data folder is getting populated properly = this needs to reflect in csv file as well 
    - all the information is stored properly in datafolder 
    - all the process are polled properly 
    - the user should have access to what process needs to be polled  - should be able to add in constants?
    - the gui should look pretty - last thing to do

- need to interface the gui from the main.py 
- folder to save
    - this needs to be a popup 
    - this also needs to propagate through to the program
    - maybe write this in the metadata file in the root of the kit 
    - probably also add duration time to the metadata - this needs to be displayed on variable display 
- add traffic lights for the showing if the process is working - these will be taken from a list of variables
- metadata also needs to have a comments section, participant id, handedness, age, gender all of which need to be displayed on the gui, 
comments can be written in the gui at any time of the experiment - even after stop button is pressed 
- data visualization 
    - camera displays needs to be added
    - glvoe data 


- currently not working
    - the traffic lights are not shown 
    - counter for the number of trials is not shown
    - metadata some fields need to be populated only once per batch, others per trial <ask_tansu>
    - start batch does not end - should i exit it? - think its ok because we need to close using the x icon


- visualization of the data stream
- gui should look nice
    - the buttons should change color when clicked
    - the traffic lights should poll on the process properly
    - user should be able to change the items for which they want to see the traffic lights
    - traffic lights should be circular
    - the forms should looks neater, comments should have more space than the rest
    - the forms should be in a scrollable window
    - layout - some should go on the right side instead of below - decide and cleanup