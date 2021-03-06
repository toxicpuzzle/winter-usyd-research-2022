from fileinput import filename
from google_play_scraper import app
import google_play_scraper
from app_store_scraper import AppStore
import pandas as pd
import sys


def save_reviews_from(google_app_id : str, file_name: str):
    # result = app(
    #     app_id=google_app_id,
    #     lang='en', # defaults to 'en'
    #     country='us' # defaults to 'us'
    # )

    # reviews(continuation_token) will keep crawling after 3 review items
    result,continuation_token = google_play_scraper.reviews(
        app_id=google_app_id,
        lang='en',
        country='us',
        count=3000,
        sort=google_play_scraper.Sort.NEWEST
    )

    google_frame = pd.DataFrame(result)
    google_frame.to_csv(file_name)

app_id = sys.argv[1]
file_name = sys.argv[2] # File to save all reviews to.
save_reviews_from(app_id, file_name)