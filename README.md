# Tweet Collection (Python)

This app listens for tweets about a specified set of topics and keywords, then stores the tweets in a local CSV file or a Google BigQuery table.

## Installation

Create and activate a virtual environment, using anaconda for example, if you like that kind of thing:

```sh
conda create -n tweets-env python=3.7 # (first time only)
conda activate tweets-env
```

Install package dependencies:

```sh
pip install -r requirements.txt # (first time only)
```

## Setup

Create a ".env" file and set your environment variables there. See the ".env.example" file and instructions below for more details.

### Twitter API Credentials

Obtain credentials which provide read and write access to the Twitter API. Set the environment variables `TWITTER_CONSUMER_KEY`, `TWITTER_CONSUMER_SECRET`, `TWITTER_ACCESS_TOKEN`, and `TWITTER_ACCESS_TOKEN_SECRET` accordingly.

### Google API Credentials

> To store tweets to a local CSV file, skip this section. Otherwise, to store tweets in Google BigQuery, set the `STORAGE_ENV` environment variable to "remote" and continue...

From the Google Cloud console, enable the BigQuery API, then generate and download the corresponding service account credentials (for example into the root directory of this repo as "credentials.json") and set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable accordingly.

#### Google BigQuery Setup

Login to the [Google BigQuery console](https://console.cloud.google.com/bigquery), create three datasets named "impeachment_production", "impeachment_development", and "impeachment_test". If you choose a different dataset name stem besides "impeachment" then set the `APP_NAME` env var accordingly.

Within each dataset, create a table called "tweets", using the following table schema:

    status_id:STRING,
    status_text:STRING,
    truncated:BOOLEAN,
    retweet_status_id:STRING,
    reply_status_id:STRING,
    reply_user_id:STRING,
    is_quote:BOOLEAN,
    geo:STRING,
    created_at:TIMESTAMP,
    user_id:STRING,
    user_name:STRING,
    user_screen_name:STRING,
    user_description:STRING,
    user_location:STRING,
    user_verified:BOOLEAN,
    user_created_at:TIMESTAMP

And create a topics table with the following schema:

    [
        {
            "name": "topic",
            "type": "STRING",
            "mode": "REQUIRED"
        },
        {
            "name": "created_at",
            "type": "TIMESTAMP"
        }
    ]

### Sendgrid API Credentials

> If you don't care about sending notification emails, skip this section. Otherwise set the `WILL_NOTIFY` environment variable to "True" and continue...

[Sign up for a SendGrid account](https://signup.sendgrid.com/) and verify your account, as necessary. [Create an API Key](https://app.sendgrid.com/settings/api_keys) with "full access" permissions, and set it as the `SENDGRID_API_KEY` environment variable.

Finally set the `FROM_EMAIL` and `TO_EMAILS` environment variables to designate sender and recipients of error notification emails.

### Seeding Topics

To specify the list of keywords and phases to filter, create a topics CSV file at "data/topics.csv", and insert / modify contents resembling:

    topic
    impeach
    impeached
    impeachment
    #TrumpImpeachment
    #ImpeachAndConvict
    #ImpeachAndConvictTrump
    #IGReport
    #SenateHearing
    #IGHearing
    #FactsMatter
    Trump to Pelosi

> NOTE: "topic" is the column name, and is required

If using local storage, this CSV file will act as the topics list. Otherwise if using remote storage, seed the development and production databases (and test the storage service):

```sh
APP_ENV="development" STORAGE_ENV="remote" python -m app.storage_service
APP_ENV="production" STORAGE_ENV="remote" python -m app.storage_service
```

> NOTE: yes, seed the production database from your local machine, and not on production iteself, because there will be no topics CSV file on the production server (use your own)

> NOTE: the test database will be seeded with mock values the first time tests are run

## Usage

Run the tweet collector:

```sh
python -m app.tweet_collector
# ... OR ...
BATCH_SIZE=200 STORAGE_ENV="remote" python -m app.tweet_collector
# ... OR ...
APP_ENV="development" STORAGE_ENV="remote" WILL_NOTIFY=True python -m app.tweet_collector
```

## Testing

Install pytest:

```sh
pip install pytest # (first time only)
```

Run tests:

```sh
pytest --disable-pytest-warnings
```

## [Deploying](DEPLOYING.md)

## [License](LICENSE.md)
