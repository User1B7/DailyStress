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
First, navigate to the *Get_GARMIN_Data/* folder and run the *main.py* file to download the data as a .JSON file to your computer.  
```bash
cd Get_GARMIN_Data
python main.py 
```
This script automatically creates a folder *data/* to store the data which will be processed in the next step. This data is reformatted for the AI model as .csv files, which are required for later model training.
