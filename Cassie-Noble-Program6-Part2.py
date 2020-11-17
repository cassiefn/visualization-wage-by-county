# Cassie Noble
# CSCI 127
# Program 6: Data Visualization
# Part 2
# 7/5/2018
# -------------------------------------------------

# Program Description:
# This program takes in a file of employment information about individuals employed in Child Care Centers
# across the state of Montana, collected through the Early Childhood Project Practitioner Registry.
# The dataframe is condensed to only analyze Early Childhood Teacher positions types, and wages that are
# reported (if not reported, wage = 0) and above minimum wage (otherwise data is outdated). Wages are then sorted
# by county, and averages are calculated for each county. The mean wage per county is then displayed as a bar graph.

# -------------------------------------------------

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# -------------------------------------------------

# calculate mean wage for each county and store in new dataframe
def calc_mean_wage(dict):
    # initialize dataframe with county and mean wage columns
    columns = ["county", "mean hourly wage"]
    mean_wage_df = pd.DataFrame(columns = columns)

    # loop through all keys in dictionary
    for key in dict:
        sum = 0
        total = 0
        # loop through all values in dictionary and calculate mean wage
        for wage in dict[key]:
            sum += wage
            total += 1
        mean = sum / total

        # create temporary dataframe containing just this row of info, then add to new dataframe
        temp_df = pd.DataFrame([[key, mean]], columns = columns)
        mean_wage_df = mean_wage_df.append(temp_df, ignore_index = True)

    # sort wages in dataframe to descending
    mean_wage_df = mean_wage_df.sort_values(by = "mean hourly wage", ascending = False)

    return mean_wage_df

# -------------------------------------------------

# create dictionary to store all wages for one county under that county key
def create_county_dict(df):
    county_dict = {}
    # loop through all lines in condensed dataframe
    for line in df.values:
        # add new dictionary key if it does not exist already, and add associated wage as dictionary value
        county_dict.setdefault(line[1], []).append(line[0])
    return county_dict

# -------------------------------------------------

# create condensed dataframe containing hourly wage and county info filtering position types and wages
def condense_df(df):
    # initialize dataframe with wage and county columns
    columns = ["hourly wage", "county"]
    condensed_wages = pd.DataFrame(columns = columns)

    # loop through original dataframe
    for line in df.values:
        if line[1] == 33:           # limit position types to early childhood teacher
            if line[10] >= 8.3:     # limit wages to those reported wage as not 0 and above minimum wage
                # create temporary dataframe containing just this row of info, then add to condensed dataframe
                temp_df = pd.DataFrame([[line[10], line[-1]]], columns = columns)
                condensed_wages = condensed_wages.append(temp_df, ignore_index = True)

    return(condensed_wages)

# -------------------------------------------------

def main():
    wage_data_frame = pd.read_csv("wage-county.csv")        # read in csv file

    condensed_wages = condense_df(wage_data_frame)          # condense to smaller dataframe
    county_dict = create_county_dict(condensed_wages)       # create dictionary linking counties with wages
    mean_wage_df = calc_mean_wage(county_dict)              # calculate mean wage for each county

    # plot mean wage by county data
    mean_wage_df.plot(x = "county", y = "mean hourly wage", kind = "bar", color = "b")
    plt.title("Mean Hourly Wage by County for Early Childhood Teachers")
    plt.xlabel("Counties in Montana")
    plt.ylabel("Mean Hourly Wage (U.S. Dollars)")

    # create yticks array and convert yticks labels to display as currency
    yticks = np.arange(2, 19, 2)
    yticklab = []
    for tick in yticks:
        yticklab.append("${:,.2f}".format(tick))
    plt.yticks(yticks, yticklab)

    # create horizontal line at minimum wage and add legend
    plt.axhline(y = 8.3, color = "r", ls = "dashed")
    plt.legend(["Montana minimum wage ($8.30)"])

    plt.show()
# -------------------------------------------------

main()



