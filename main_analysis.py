"""
The code that produces all of the graphs and csv files with the necessary dataframes.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from csv_analysis import *

mta = pd.read_csv('awesome_company_multi_touch_report.csv',
                  delimiter=',')

## Question 1

purchases = filter_and_copy(mta, 'action', 'action=conv.purchase')  # fitler for purchases

# Produces lists for each of the fives tiers of marketing channels.
t1_entries = different_entries(mta, 'tier_1')
t2_entries = different_entries(mta, 'tier_2')
t3_entries = different_entries(mta, 'tier_3')
t4_entries = different_entries(mta, 'tier_4')
t5_entries = different_entries(mta, 'tier_5')

# Counts all of the entries of each channel and produces a dictionary for graphing.
t1_count = count_entries(mta, 'tier_1', t1_entries)
t2_count = count_entries(mta, 'tier_2', t2_entries)
t3_count = count_entries(mta, 'tier_3', t3_entries)
t4_count = count_entries(mta, 'tier_4', t4_entries)
t5_count = count_entries(mta, 'tier_5', t5_entries)

# Tier 1 Marketing Channels
plt.figure()
f, ax = plt.subplots(figsize=(20,10)) # (width, height)
t1_bar = ax.bar(range(len(t1_count)), t1_count.values())
ax.set_xticks(range(len(t1_count)))
ax.set_xticklabels(t1_count.keys(), rotation=45)
ax.set_title('Tier 1 Channel Purchase Conversions')
ax.set_xlabel('Categories')
ax.set_ylabel('Count')
add_numbers(ax, t1_bar)
plt.savefig('graphs/tier_1_channels.png')

# Tier 2 Marketing Channels
plt.figure()
f, ax = plt.subplots(figsize=(20,10)) # (width, height)
t2_bar = ax.bar(range(len(t2_count)), t2_count.values())
ax.set_xticks(range(len(t2_count)))
ax.set_xticklabels(t2_count.keys(), rotation=45)
ax.set_title('Tier 2 Channel Purchase Conversions')
ax.set_xlabel('Categories')
ax.set_ylabel('Count')
add_numbers(ax, t2_bar)
plt.savefig('graphs/tier_2_channels.png')

# Tier 3 Marketing Channels
plt.figure()
f, ax = plt.subplots(figsize=(20,10)) # (width, height)
t3_bar = ax.bar(range(len(t3_count)), t3_count.values())
ax.set_title('Tier 3 Channel Purchase Conversions')
ax.set_xlabel('Categories')
ax.set_ylabel('Count')
add_numbers(ax, t3_bar)
plt.savefig('graphs/tier_3_channels.png')

# Tier 4 Marketing Channels
plt.figure()
f, ax = plt.subplots(figsize=(20,10)) # (width, height)
t4_bar = ax.bar(range(len(t4_count)), t4_count.values())
ax.set_title('Tier 4 Channel Purchase Conversions')
ax.set_xlabel('Categories')
ax.set_ylabel('Count')
add_numbers(ax, t4_bar)
plt.savefig('graphs/tier_4_channels.png')

# Tier 5 Marketing Channels
plt.figure()
f, ax = plt.subplots(figsize=(20,10)) # (width, height)
t5_bar = ax.bar(range(len(t5_count)), t5_count.values())
ax.set_title('Tier 5 Channel Purchase Conversions')
ax.set_xlabel('Categories')
ax.set_ylabel('Count')
add_numbers(ax, t5_bar)
plt.savefig('graphs/tier_5_channels.png')

# Models
first_touch = mta[mta['first_touch'] == 1]
last_touch = mta[mta['last_touch'] == 1]
even = mta[mta['even'] == 1]
model_count_list = [np.size(first_touch), np.size(last_touch), np.size(even)]

# Different Models Purchase Results
plt.figure()
f, ax = plt.subplots(figsize=(20,10)) # (width, height)
models_bar = ax.bar(range(len(model_count_list)), model_count_list)
ax.set_xticks(range(len(model_count_list)))
ax.set_xticklabels(['first_touch', 'last_touch', 'even'])
ax.set_title('Different Models Purchase Results')
ax.set_xlabel('Models')
ax.set_ylabel('Count')
add_numbers(ax, models_bar)
plt.savefig('graphs/models_results.png')

## Question 2

# list of all users and all different number of events
users = different_entries(mta, 'uid')
events = different_entries(mta, 'total_events')

# SEE README FOR COMMENTS ON EFFICIENCY
event_list_per_user = []
# creates list of dataframes per user
for user in users:
    for event in events:
        add = mta[(mta['uid'] == user) & (mta['total_events'] == event)][['uid', 'timestamp_events', 'total_events', 'sequence_number', 'tier_1', 'new_to_file']]
        if add.empty == False:
            event_list_per_user.append(add)

# total_events is number of events leading up to conversion which is denoted by action, even if the row does not
# correspond to the final
uid_time = pd.DataFrame(columns = ['uid', 'time_to_purchase', 'total_events', 'path', 'new_to_file'])

time = 0
for df in event_list_per_user:
    path = []
    df.sort_values('sequence_number') # sorts the data frame
    for i in range(len(df)):
        path.append(df['tier_1'].iat[i])
        if df['sequence_number'].iat[i] == 1:
            fst = to_time(df.iat[i, 1])
        if df['sequence_number'].iat[i] == (df['total_events'].iat[i]):
            lst = to_time(df.iat[i, 1])
            te = df['total_events'].iat[i]
            time = lst - fst
    path.append('purchase') # as the example shows
    path_str = ''.join(path)
    uid_time = uid_time.append({'uid': df.iat[0, 0], 'time_to_purchase': time, 'total_events': te, 'path': path_str, 'new_to_file': df['new_to_file'].iat[0]}, ignore_index=True)

uid_time.to_csv('dataframes/users_time_events_path_new.csv')


diff_paths = different_entries(uid_time, 'path')
diff_paths_str = []
common_paths = pd.DataFrame(columns=['path', 'freq'])

for i in range(len(diff_paths)):
    diff_paths_str.append(''.join(diff_paths[i]))

for path in range(len(diff_paths_str)):
    size = np.size(uid_time[(uid_time['path']) == diff_paths_str[path]])
    common_paths = common_paths.append({'path': diff_paths[path], 'freq': size}, ignore_index=True)

common_paths.to_csv('dataframes/common_paths_with_freq.csv')

new_user_common_paths = pd.DataFrame(columns = ['path', 'freq'])
for path in range(len(diff_paths_str)):
    size = np.size(uid_time[(uid_time['path'] == diff_paths_str[path]) & (uid_time['new_to_file'] == 1)])
    if size > 0:
        new_user_common_paths = new_user_common_paths.append({'path': diff_paths[path], 'freq': size}, ignore_index=True)

new_user_common_paths.to_csv('dataframes/new_user_common_paths.csv')