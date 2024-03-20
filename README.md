# growth_curve_outcomes
Growth curve outcomes

Please cite:
 - TODO


Tool for Growth Curve Analysis - Instructions for Use
Developed by Yonatan Eavri.

1. Preparing the file of spectrophotometer OD600 data for analysis
Insert the data into an excel sheet accordingly:

 *	Columns are the groups and the repeats - add as many groups and repeats as required

 *	Rows are time (according to the output of your spectrophotometer).

 Save as DATA.csv 
 
 Here is an example DATA file with 4 groups (A-D) with triplicate results and time by hour (20 minute intervals or 3 points per hour)
 
 -- Table -- 
 
 Note 1: the format of the DATA file must be csv
 
 Note 2: the group triplicates need to have the same name.

2. Using the scripts to obtain the study outcomes
Run the script average.py on the folder that contains DATA.scv. This will create a file by the name of AVERAGES.csv.
Run the script extract.py. This will create a file by the name of OUT.xlsx which contains the outcomes.

3. Attached files
•	Template Excel file for DATA.csv (add as many groups and repeats as required)
•	Script file average.py
•	Script file extract.py
