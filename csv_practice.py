"""
    This program is to practice reading in a csv file with multiple columns.

    Author: Abby Lloyd
    Date: Feb 7, 2023

"""

import csv

# Declare a variable to hold the input file name
input_file_name = "/Users/Abby/Documents/44-671 Streaming Data/Module 5/streaming-05-smart-smoker/smoker-temps.csv"
# Create a file object for input (r = read access)
input_file = open(input_file_name, "r")
# Create a csv reader for a comma delimited file
reader = csv.reader(input_file, delimiter=",")
# Then, for each data row in the reader
for row in reader:
    for (t, ch1, ch2, ch3) in reader:
        print(f'{t}, {ch1}, {ch2}, {ch3}')