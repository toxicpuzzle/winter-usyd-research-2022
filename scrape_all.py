from fileinput import filename
from google_play_scraper import app
import google_play_scraper
from app_store_scraper import AppStore
import pandas as pd
import sys


def save_reviews_from(google_app_id : str, apple_app_name : str, file_name: str):
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
        count=100,
        sort=google_play_scraper.Sort.NEWEST
    )

    # include app store reviews for the same app
    apple_result = AppStore(country="us", app_name=apple_app_name)

    apple_result.review(how_many=100);
    apple_frame = pd.DataFrame(apple_result.reviews);
    apple_frame = apple_frame.loc[:, ["rating", "review"]]
    apple_frame["store"] = "apple"
    print(apple_frame);

    google_frame = pd.DataFrame(result)
    google_frame = google_frame.loc[:,[ "score", "content"]]
    google_frame = google_frame.rename(columns={"score": "rating", "content": "review"})
    google_frame["store"] = "google"
    final_frame = pd.concat([apple_frame, google_frame], axis=0, ignore_index=True)
    final_frame.to_csv(file_name)

app_id = sys.argv[1]
apple_name = sys.argv[2]
file_name = sys.argv[3] # File to save all reviews to.
save_reviews_from(app_id, apple_name, file_name)