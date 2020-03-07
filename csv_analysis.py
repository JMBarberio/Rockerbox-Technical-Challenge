"""
Contains all of the helper functions for analysis of the MTA (from csv)
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def filter_and_copy(df, column_name, desired):
    """
    Gives a copy of the original dataframe filtered for the desired values with respect to a column.
    """
    filtered = df.copy()
    col = filtered[column_name]
    for value in col:
        if value != desired:
            filtered.drop([value], axis=0)

    return filtered


def different_entries(df, column_name):
    """
    Gives a list with all of the different possible values for the corresponding header from the MTA.
    """
    entries = []
    col = df[column_name]
    for value in col:
        if value not in entries:
            entries.append(value)

    return entries


def count_entries(df, column_name, entries):
    """
    Gives a dictionary of the amount of times an entry is repeated for the corresponding column_name.

    The entries parameter corresponds to a list created by different_entries.
    """
    dicti = {}
    col = df[column_name]
    for entry in entries:
        dicti[entry] = 0
        for value in col:
            if value == entry:
                dicti[entry] += 1

    return dicti

def add_numbers(ax, bars):
    for bar in bars:
        height = bar.get_height()
        ax.annotate('{}'.format(height),
                    xy=(bar.get_x() + bar.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')


def to_time(tse):
    '''
    Converts a "timestamp_events" string to seconds.
    '''
    s_year = 3.154e7  # seconds in a year
    s_month = 2.628e6  # seconds in a month
    s_day = 86400  # seconds in a day
    s_hour = 3600  # seconds in an hour
    s_minute = 60  # seconds in a minute
    tse = tse.split(' ')
    ymd = tse[0].split('-')
    ymd = list(map(int, ymd))
    hms = tse[1].split(':')
    hms = list(map(int, hms))
    final = (ymd[0] * s_year) + (ymd[1] * s_month) + (ymd[2] * s_day) + (hms[0] * s_hour) + (hms[1] * s_minute) + hms[2]

    return final

