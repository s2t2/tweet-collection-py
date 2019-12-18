# Deploying to Heroku

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
heroku config:set APP_NAME="impeachment"
heroku config:set APP_ENV="production"
heroku config:set STORAGE_ENV="remote"

heroku config:set TWITTER_HANDLE="@____"
heroku config:set ADMIN_HANDLES="@____, @_____"

heroku config:set TWITTER_CONSUMER_KEY="____"
heroku config:set TWITTER_CONSUMER_SECRET="____"
heroku config:set TWITTER_ACCESS_TOKEN="____-____"
heroku config:set TWITTER_ACCESS_TOKEN_SECRET="____"

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
