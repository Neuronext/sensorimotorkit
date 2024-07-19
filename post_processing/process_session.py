import os
import shutil

#Constants
session_id = '02'
dart_index = '75'

#Step 1: Rearrange files to make access more intuitive
def rearrange():
    raw_trial_path = 'C:/Users/Data acquisition/Desktop/Manual Data Processing/Session ' + session_id + ' (Raw)'
    raw_trials = [f for f in os.listdir(raw_trial_path)]
    rearranged_trial_path = 'C:/Users/Data acquisition/Desktop/Manual Data Processing/Session ' + session_id + ' (Rearranged)'
    next_trial = 1

    for i, raw_trial in enumerate(raw_trials):
        current_trial = i + next_trial
        new_trial_path = rearranged_trial_path + "/" + str(current_trial)
        new_body_path = new_trial_path + "/Body"
        new_dart_path = new_trial_path + "/Dart"
        new_gloves_path = new_trial_path + "/gloves.csv"
        old_trial_path = raw_trial_path + "/" + raw_trial
        old_body_path = old_trial_path + "/body_left/raw"
        old_dart_path = old_trial_path + "/dart/raw"
        old_gloves_path = old_trial_path + "/gloves/gloves.csv"
        if os.path.exists(old_body_path):
            old_body_images = [f for f in os.listdir(old_body_path)]
        else:
            old_body_images = []
        if os.path.exists(old_dart_path):
            old_dart_images = [f for f in os.listdir(old_dart_path)]
        else:
            old_dart_images = []
        os.makedirs(new_trial_path)
        os.makedirs(new_body_path)
        os.makedirs(new_dart_path)
        if os.path.exists(old_gloves_path):
            shutil.move(old_gloves_path, new_gloves_path)
        for old_body_image in old_body_images:
            shutil.move(old_body_path + "/" + old_body_image, new_body_path + "/" + old_body_image)
        for old_dart_image in old_dart_images:
            shutil.move(old_dart_path + "/" + old_dart_image, new_dart_path + "/" + old_dart_image)

#Step 2: Gather the darts
def gather_darts():
    sorted_trials_path = f'C:/Users/Data acquisition/Desktop/Manual Data Processing/Session {session_id} (Rearranged)'
    sorted_trials = [f for f in os.listdir(sorted_trials_path)]

    for sorted_trial in sorted_trials:
        dart_path = os.path.join(sorted_trials_path, sorted_trial, 'Dart')
        if os.path.exists(dart_path):
            darts = [f for f in os.listdir(dart_path)]
            selected_dart = 'No dart image'
            
            if darts:
                found_trial_number = False
                for dart in darts:
                    trial_number = dart[6:8]
                    if trial_number == dart_index:
                        found_trial_number = True
                        selected_dart = dart
                        break
                
                if not found_trial_number:
                    try:
                        selected_dart = darts[int(dart_index)]
                    except (IndexError, ValueError):
                        selected_dart = darts[-1]
            
            selected_dart_path = os.path.join(dart_path, selected_dart)
            isolated_darts_path = f'C:/Users/Data acquisition/Desktop/Manual Data Processing/Session {session_id} (Isolated)/Darts'
            os.makedirs(isolated_darts_path, exist_ok=True)
            isolated_dart_path = os.path.join(isolated_darts_path, f'{sorted_trial}.png')
            
            if os.path.exists(selected_dart_path):
                shutil.copy(selected_dart_path, isolated_dart_path)


