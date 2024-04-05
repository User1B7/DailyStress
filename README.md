# DailyStress

This Python project is part of a [ZDD](https://github.com/ZDDduesseldorf)-HSD digital health study  to identify patterns and predict when students are most stressed during their academic activities. The data is collected using a GARMIN Forerunner 255 watch and the analysis of various physiological and activity metrics involves AI/ML techniques.

## Contribution
If you have suggestions for improvement, you can open a pull request or report a problem.

## Installation and Run

**Note: This code requires a GARMIN watch and a GARMIN account.**

Download and install:
```bash
git clone https://github.com/User1B7/DailyStress.git
cd DailyStress
pip install -r requirements.txt
```
First, navigate to the *Data_collector/* folder and run the *garmin_collector_main.py* file to download your data as .JSON files to your computer.  
```bash
cd Data_collector
python garmin_collector_main.py 
```
This script automatically creates a folder *data/* to store the data which will be processed in the next step. This data is reformatted for the AI model as .csv files, which are required for later model training.

If you dont want to save your own data but want to load already saved date you can navigate to the *Data_collector/* folder and run the *drive_collector_main.py*
```bash
cd Data_collector
python drive_collector_main.py 
```
This script automatically saves the *data/* folder and all saved files in it.

In the next step you have to manually load the *stundenbuch.csv* and save it into *data/*
<br><br>
[Stundenbuch.csv](https://docs.google.com/spreadsheets/d/1-5QijnBttDqLJFZssCqQ4vqi7CBir6LY4ctp8qOqwQw/edit#gid=1351272459)
<br><br>
This is needed for our labels, because this file contains our interview data

Finaly, you can navigate to the *Data_explorer/* folder and run the notebook *explor_data_random_forest.ipynb* and run the project.



## Correlation
This is the correlation of our features which get used for the 6 decision tree classification models.

![image](https://github.com/User1B7/DailyStress/assets/73638219/2b47f6bd-b4d9-4007-ba20-61ed59358013)
