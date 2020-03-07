Rockerbox Techincal Challenge
Joseph Maximilian Barberio

Relevant File Heirarchy:
-> venv_Rockerbox-Challenge
    -> dataframes
        -> common_paths_with_freq.csv
        -> new_user_common_paths.csv
        -> users_time_events_path_new.csv
    -> graphs
        -> model_results.png
        -> tier_1_channels.png
        -> tier_2_channels.png
        -> tier_3_channels.png
        -> tier_4_channels.png
        -> tier_5_channels.png
    -> awesome_company_multi_touch_report.csv
    -> csv_analysis.ipynb
    -> csv_analysis.py
    -> main_analysis.py
    -> README.txt

Structure:
    - I decided to first put everything in a Jupyter Notebook, which allowed
    me to play around with the data and understand what was happening piece
    by piece. After I was able to generate answers to the questions, I
    moved to a more formal structure. I created a virtual environment and
    formal python files to define the helper functions and the main analysis.
    - I understood the challenge to look more towards an ability to produce
    an answer with code, as opposed to knowing all of the proper programming
    conventions that marketing data analysis may have.

Efficiency:
    - This is the largest dataset I have worked with, just in the sheer
    size of the csv file that was provided. I am still learning the most
    efficient ways to deal with enormous amounts of data, and one way I
    have been using was parallel processing on my GeForce RTX 2070. In order
    to make this code runnable on all computers, I decided not to format
    everything to be pushed to a GPU, which makes the main_analysis.py file
    run significantly slower. More specifically, the analysis slows down
    tremendously during the double for-loop at lines 112-116 in
    main_analysis.py.

Answer to Client Questions:
1) Which marketing channels seem to be driving the most purchases?
Do different models show different results? If they do, what do the
differences in results mean?
    - I decided to answer this question by Tier, as each successive Tier
    represents a broader amount of channels. I also measured this by the
    frequency it appeared within the MTA. I made sure to check that every
    row in the MTA had 'conv.purchase' in the action column before taking
    this route. My definition of purchase changes in Question 2, but to
    answer this question, I saw the best method to be in finding the
    frequency of each channel per Tier. For the broader Tiers, the bar
    graphs stored in the graphs folder get messier, so I maxed the
    values in the Jupyter Notebook in order to answer the question here.
    Using the frequency that each channel appears allows me to show which
    channels work better than others.
        - Tier 1:
            - email (6098)
        - Tier 2:
            - kl (5860)
        - Tier 3:
            - house (2771)
        - Tier 4:
            - awesome_company early spring drop 2 2020 (1482)
        - Tier 5:
            - buyer -0-3m 2x+ (933)
    - I then went to look at how often a certain model was used. I simply
    used the helper functions I created before to determine how often each
    of the three models occurred in the MTA.
        - Incredibly enough, first_touch and last_touch both have the same
        frequency, at 119730. This shows that the even model is not as
        effective for driving purchases for Awesome Company.

2) The client would also like to know more about how our customers
interact with their marketing before purchasing.
a) How long does it take a customer to purchase after interacting with a
given marketing channel?
    - I emailed Ana in regards to the wording of this question, and I think
    my confusion came from understanding what the given marketing channel is.
    I answered this question by filtering the MTA to create a list of dataframes
    which each have the 'uid', 'total_events', 'timestamp_events', 'sequence_number',
    'tier_1', and 'new_to_file.' Creating this list of dataframes is the
    slowest part of the program, as described in the efficiency section above.
    These dataframes were only the events denoted by 'total_events' and 'uid.'
    From there I was able to sort these events by the sequence number, and via
    iteration, I computed the difference between the last and the first event
    in seconds. The difference between the last and the first defines my definition
     of a customer purchasing, even though each action in the MTA is flagged with
     'conv.purchase.' This 'time_to_purchase' header is given in the
    'users_time_events_path_new.csv' file in the dataframes folder.

b)	Can you look at each customer and show the path they're taking to
purchase? E.g. Customer A: Direct Mail -> Paid Social -> Paid Search -> Purchase.
    - By the way this question was worded - especially the example - I
    used my sorted list of events to map out the path, and appending a
    purchase flag at the end. The example have a path from the Tier 1 level
    of channels, so I based my analysis only off of the Tier 1 channels.
    This is stored as a combined string in the 'common_paths_with_freq.csv'
    file with the header 'path.' The list of paths is accessible through the
    'diff_paths' variable.

c)	What are the most common paths to purchase?
    - Using the paths from before, I created another dataframe, named
    'common_paths_with_freq.csv,' which has the most common paths with the
    frequencies. In the Jupyter Notebook, I sorted and output the top five
    most common paths.
        - Direct->Purchase (1720)
        - Direct Mail->Purchase (1195)
        - Paid Search->Purchase (1170)
        - Organic Search->Purchase (835)
        - Direct Mail->Direct Mail->Purchase (630)

3) How would you advise this client on where they should continue investing
 marketing dollars? They are currently looking to grow the company's
 customer footprint by bringing on new customers. Is there any other
 information they could potentially provide to help make this determination?
    - If the company is looking to continue to grow a novel consumer base,
    they need to look at the most common paths. More specifically, they need
    to look at the which paths drove the most new customers, and the MTA had
    a column titled 'new_to_file.' I sifted through my 'users_time_events_path_new.csv'
    file to find the frequency of the paths with a 'new_to_file' value of 1.
    This information is storied in the 'new_user_common_paths.csv' file.
    The top five are:
        - Paid Search->Purchase (915)
        - Organic Search->Purchase (635)
        - SMS->Purchase (365)
        - Email->Purchase (335)
        - Paid Social->Purchase (300)
    - In regards to teh other information the company could provide, I feel
    that providing the amount of money being spent per channel would be helpful.
    With this information, I could determine the best way to reallocate funds.
    Some paths clearly work, while some do not, so there may not even by a need
    to spend more money on marketing, as the company can just reallocate.
