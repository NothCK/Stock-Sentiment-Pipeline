# Stock-Sentiment-Pipeline (In Progress)
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
Follow the steps below to set up the pipeline. I've included explanations where possible, but feel free to modify or improve them as needed.
> **NOTE**: This was developed using an M1 Macbook Pro. If you're on Windows or Linux, you may need to amend certain components if issues are encountered.

First clone the repository into your home directory and follow the steps.
```bash
git clone https://github.com/NothCK/Stock-Sentiment-Pipeline.git
cd Stock-Sentiment-Pipeline
```

1. [Reddit Configuration](instructions/Reddit.md)
2. [Google Cloud Platform](instructions/google_cloud.md)
3. 
