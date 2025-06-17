# Stock-Sentiment-Pipeline
[Chinese Version](instructions/chinese-version.md)
A data pipeline to extract stock sentiment data from Reddit ([r/stocks](https://www.reddit.com/r/stocks/), [r/valueinvesting](https://www.reddit.com/r/valueinvesting/))

Questions This Project Seeks to Answer:
- Which stocks are discussed the most?
- Whats the average sentiment for every stock mentioned (per week)?
- What posts have the most engagement? (Most comments, upvotes)

The output will be displayed as a Google Looker Studio Report

## Motivation
- This project was initiated based on my strong interest in data engineering and the US stock market.
- My goal is to learn and demonstrate modern data engineering practices, including hands-on NLP components, by building an end-to-end pipeline.
- I intentionally designed the project to go beyond minimal requirements by incorporating industry-relevant tools like dbt, Apache Airflow, Docker, and cloud-based storage with BigQuery.
- While scalability is not the primary focus, I aim to produce modular, readable, and production-like code that reflects real-world engineering standards.

## Architecture

## Output

## Structure of Fact Tables

## Replication Steps
### Setup Reddit Account
1. Create a Reddit account if you don’t already have one. This is required to access Reddit’s API for scraping subreddit data.
2. Once you have an account go [here](https://www.reddit.com/prefs/apps). Click on the `create another app...` button at the bottom of the page. Fill in the required fields and select `web app`. Click on `create app`
3. Once created, under the `web app` section, you’ll find your client ID (just below the app name) and client secret.
Save these credentials — you'll need them to authenticate with the PRAW API in your project

### Setup Google Cloud 
1. Create a google cloud account
2. Setup a new google cloud [project](https://cloud.google.com/).
3. Go to `IAM & Admin` -> `Service Accounts` -> click create a new service account. Give the service account:
* `Compute Admin`
* `Service Account User`
* `Storage Admin`
* `Storage Object Admin`
* `BigQuery Admin Roles`
4. After the service account has been created, click on `Manage Keys` inside the three dots under the `Actions Menu`. Click on the `Add Key` dropdown and click on `Create new key`. A prompt should pop up asking to download it as a json or P12 file. Choose JSON format and download the key file.
5. Install the the [Google Cloud CLI](https://cloud.google.com/sdk/docs/install-sdk)
> **NOTE**: This was developed using an M1 Macbook Pro. If you're on Windows or Linux, you need to follow your respective directions.
Make sure you log in by running `gcloud init`.
6. Set the environment variable to point to your downloaded service account keys json file:
`export GOOGLE_APPLICATION_CREDENTIALS=<path/to/your/service-account-authkeys>.json`
7.Refresh token/session, and authenticate your application environment:
`gcloud auth application-default login`
8. Make sure these APIs are enabled for your project:
https://console.cloud.google.com/apis/library/iam.googleapis.com 
https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com 
https://console.cloud.google.com/apis/library/compute.googleapis.com
https://console.cloud.google.com/apis/library/bigquery.googleapis.com
https://console.cloud.google.com/apis/library/dataplex.googleapis.com

