import os
import shutil

sorted_trials_path = 'C:/Users/Data acquisition/Desktop/Manual Data Processing/Session 01 (Sorted)'
sorted_trials = [f for f in os.listdir(sorted_trials_path)]

for i, sorted_trial in enumerate(sorted_trials):
    dart_path = sorted_trials_path + '/' + sorted_trial + '/Dart'
    darts = [f for f in os.listdir(dart_path)]
    selected_dart = darts[0]
    selected_dart_path = dart_path + '/' + selected_dart
    print(selected_dart_path)
    isolated_darts_path = 'C:/Users/Data acquisition/Desktop/Manual Data Processing/Session 01 (Isolated)/Darts'
    isolated_dart_path = isolated_darts_path + '/' + sorted_trial + '.png'
    shutil.copy(selected_dart_path, isolated_dart_path)
