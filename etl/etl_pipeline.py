import configparser
import datetime
import pandas as pd
import pathlib
import praw
import sys
import numpy as np
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.config_read import REDDIT_SECRET, REDDIT_CLIENT_ID




# Options for extracting data from PRAW
# SUBREDDIT = ["bigdata","dataengineering","snowflake","databricks"]
# TIME_FILTER = "day"
LIMIT = None


POST_FIELDS = (
    "id",
    "title",
    "subreddit",
    "score",
    "num_comments",
    "author",
    "created_utc",
    "url",
    "selftext",
    "upvote_ratio",
    "over_18",
    "edited",
    "spoiler",
    "stickied",
)

COLUMN_RENAME_MAP = {
    "selftext": "Self_Text_Description",
    "subreddit": "Topic"
}


# try:
#     output_name = sys.argv[1]
# except Exception as e:
#     print(f"Error with file input. Error {e}")
#     sys.exit(1)


def api_connect():
    """Connect to Reddit API"""
    try:
        instance = praw.Reddit(
            client_id=REDDIT_CLIENT_ID, client_secret=REDDIT_SECRET, user_agent="AdditionalFudge7027"
        )
        return instance
    except Exception as e:
        print(f"Unable to connect to API. Error: {e}")
        sys.exit(1)


# TODO: Improve error handling
def subreddit_posts(reddit_instance,subreddit:list,TIME_FILTER):
    """Create posts object for Reddit instance"""
    all_posts = []
    try:
        for subreddit_name in subreddit:
            subreddit = reddit_instance.subreddit(subreddit_name)
            posts = subreddit.top(time_filter=TIME_FILTER, limit=LIMIT)
            all_posts.extend(posts)  # Append posts from the current subreddit to the list
        return all_posts
    except Exception as e:
        print(f"There's been an issue. Error: {e}")
        sys.exit(1)



# TODO: Improve error handling
def extract_data(posts):
    list_of_items = []
    try:
        for submission in posts:
            to_dict = vars(submission)
            sub_dict = {field: to_dict[field] for field in POST_FIELDS}
            list_of_items.append(sub_dict)
            extracted_data_df = pd.DataFrame(list_of_items)
            extracted_data_df.rename(columns=COLUMN_RENAME_MAP, inplace=True)
    except Exception as e:
        print(f"There has been an issue. Error {e}")
        sys.exit(1)

    return extracted_data_df


def transform_basic(df):
    df["Self_Text_Description"] = np.where(df["Self_Text_Description"].empty, df["Self_Text_Description"],"No description")
    df["created_utc"] = pd.to_datetime(df["created_utc"], unit="s")
    df["over_18"] = np.where(
        (df["over_18"] == "False") | (df["over_18"] == False), False, True
    ).astype(bool)
    df["edited"] = np.where(
        (df["edited"] == "False") | (df["edited"] == False), False, True
    ).astype(bool)
    df["spoiler"] = np.where(
        (df["spoiler"] == "False") | (df["spoiler"] == False), False, True
    ).astype(bool)
    df["stickied"] = np.where(
        (df["stickied"] == "False") | (df["stickied"] == False), False, True
    ).astype(bool)
    return df


def load_to_csv(extracted_data_df,output_name:str):
    """Save extracted data to CSV file in /tmp folder"""
    extracted_data_df.to_csv(f"/opt/airflow/data/output/reddit_{output_name}.csv", index=False)

    return f"/opt/airflow/data/output/reddit_{output_name}.csv"

def etl_pipeline(output_name:str,subreddit,time_filter):
    reddit_instance = api_connect()
    subreddit_posts_object = subreddit_posts(reddit_instance,subreddit,time_filter)
    extracted_data = extract_data(subreddit_posts_object)
    transformed_data = transform_basic(extracted_data)
    file_path = load_to_csv(transformed_data,output_name)
    return file_path

    

# if __name__ == "__main__":
#     main()