# Contributor's Guide

Hey, so you want to run this app yourself? Great. Follow the instructions in this guide.

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

### Google API Credentials

To store tweets to a local CSV file, skip this section. Otherwise, to store tweets in Google Big Query, set the `STORAGE_ENV` environment variable to "remote" and continue...

Login to the [Google Big Query console](https://console.cloud.google.com/bigquery), create a dataset called something like "impeachment" and set the `BQ_DATASET_NAME` environment variable accordingly. Within it, create a table called something like "tweets", and set the `BQ_TABLE_NAME` environment variable accordingly. Use the following table schema:

    id_str:STRING,full_text:STRING,geo:STRING,created_at:TIMESTAMP,user_id_str:STRING,user_screen_name:STRING,user_description:STRING,user_location:STRING,user_verified:BOOLEAN

From the Google Cloud console, enable the BigQuery API, then generate and download the corresponding service account credentials and set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable accordingly.

### Twitter API Credentials

Obtain credentials which provide access to the Twitter API. Set the environment variables `TWITTER_CONSUMER_KEY`, `TWITTER_CONSUMER_SECRET`, `TWITTER_ACCESS_TOKEN`, and `TWITTER_ACCESS_TOKEN_SECRET` accordingly.

### Sendgrid API Credentials

[Sign up for a SendGrid account](https://signup.sendgrid.com/) and verify your account, as necessary. [Create an API Key](https://app.sendgrid.com/settings/api_keys) with "full access" permissions, and set it as the  `SENDGRID_API_KEY` environment variable.

Finally set the `FROM_EMAIL` and `TO_EMAILS` environment variables to designate sender and recipients of error notification emails.

## Usage

Test the storage service:

```sh
python -m app.storage_service
```

Run the tweet collector:

```sh
python -m app.tweet_collector

# BATCH_SIZE=200 STORAGE_ENV="remote" python -m app.tweet_collector
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
