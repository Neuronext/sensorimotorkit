import os
import shutil

raw_trial_path = 'C:/Users/Data acquisition/Desktop/Manual Data Processing/Session 01 (Raw)'
raw_trials = [f for f in os.listdir(raw_trial_path)]

processed_trial_path = 'C:/Users/Data acquisition/Desktop/Manual Data Processing/Session 01 (Processed)'
processed_trials = [f for f in os.listdir(processed_trial_path)]

last_processed_trial = int(processed_trials[-1])
next_trial = last_processed_trial + 1

for i, raw_trial in enumerate(raw_trials):
    current_trial = i + next_trial
    new_trial_path = processed_trial_path + "/" + str(current_trial)
    new_body_path = new_trial_path + "/Body"
    new_dart_path = new_trial_path + "/Dart"
    new_gloves_path = new_trial_path + "/gloves.csv"
    old_trial_path = raw_trial_path + "/" + raw_trial
    old_body_path = old_trial_path + "/body_left/raw"
    old_dart_path = old_trial_path + "/dart/raw"
    old_gloves_path = old_trial_path + "/gloves/gloves.csv"
    old_body_images = [f for f in os.listdir(old_body_path)]
    old_dart_images = [f for f in os.listdir(old_dart_path)]
    os.makedirs(new_trial_path)
    os.makedirs(new_body_path)
    os.makedirs(new_dart_path)
    shutil.move(old_gloves_path, new_gloves_path)
    for old_body_image in old_body_images:
        shutil.move(old_body_path + "/" + old_body_image, new_body_path + "/" + old_body_image)
    for old_dart_image in old_dart_images:
        shutil.move(old_dart_path + "/" + old_dart_image, new_dart_path + "/" + old_dart_image)




