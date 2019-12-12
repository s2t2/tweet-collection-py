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

### Custom Topics

Set the `TOPICS` environment variable to customize the list of tweet keywords to filter.

### Google API Credentials

To store tweets to a local CSV file, skip this section. Otherwise, to store tweets in Google Big Query, set the `STORAGE_ENV` environment variable to "remote" and continue...

Login to the [Google Big Query console](https://console.cloud.google.com/bigquery), create a dataset called something like "impeachment" and set the `BQ_DATASET_NAME` environment variable accordingly. Within it, create a table called something like "tweets", and set the `BQ_TABLE_NAME` environment variable accordingly. Use the following table schema:

    id_str:STRING,full_text:STRING,geo:STRING,created_at:TIMESTAMP,user_id_str:STRING,user_screen_name:STRING,user_description:STRING,user_location:STRING,user_verified:BOOLEAN

From the Google Cloud console, enable the BigQuery API, then generate and download the corresponding service account credentials (for example into the root directory of this repo as "credentials.json") and set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable accordingly.

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
# APP_ENV="production" STORAGE_ENV="remote" WILL_NOTIFY=True python -m app.tweet_collector
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

## Deploying

Create a new app server (first time only):

```sh
heroku create impeachment-tweet-collection # (use your own app name here)
```

Provision and configure the Google Application Credentials Buildpack to generate a credentials file on the server:

```sh
heroku buildpacks:set heroku/python
#heroku buildpacks:add https://github.com/elishaterada/heroku-google-application-credentials-buildpack
# this isn't working at the moment, so instead:
heroku buildpacks:add https://github.com/heavyperil/heroku-google-application-credentials-buildpack
heroku config:set GOOGLE_CREDENTIALS="$(< credentials.json)" # references local creds
heroku config:set GOOGLE_APPLICATION_CREDENTIALS="google-credentials.json"
```

Configure the rest of the environment variables:

```sh
heroku config:set APP_ENV="production"
heroku config:set STORAGE_ENV="remote"

heroku config:set TOPICS="____, _____, ____"

heroku config:set TWITTER_CONSUMER_KEY="____"
heroku config:set TWITTER_CONSUMER_SECRET="____"
heroku config:set TWITTER_ACCESS_TOKEN="____-____"
heroku config:set TWITTER_ACCESS_TOKEN_SECRET="____"

heroku config:set BQ_PROJECT_NAME="tweet-collector-py"
heroku config:set BQ_DATASET_NAME="impeachment"
heroku config:set BQ_TABLE_NAME="tweets_production"

heroku config:set SENDGRID_API_KEY="____"
heroku config:set FROM_EMAIL="____"
heroku config:set TO_EMAILS="____"
```

Deploy:

```sh
# from master branch
git checkout master
git push heroku master

# or from another branch
git checkout mybranch
git push heroku mybranch:master
```

Test everything is working in production:

```sh
heroku run "python -m app.storage_service"
```

Run the collection script in production, manually:

```sh
heroku run "python -m app.tweet_collector"
```

... though ultimately you'll want to setup a Heroku "dyno" (hobby tier) to run the collection script as a background process (see the "Procfile"):

```sh
heroku run collector
```

Checking logs:

```sh
heroku logs --ps collector
```
