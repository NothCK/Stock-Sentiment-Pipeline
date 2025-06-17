# Stock-Sentiment-Pipeline
[English Version](../README.md)

從 Reddit ([r/stocks](https://www.reddit.com/r/stocks/), [r/valueinvesting](https://www.reddit.com/r/valueinvesting/)) 擷取股票情緒資料的資料管線

本專案旨在回答以下問題:
- Which stocks are discussed the most?
- Whats the average sentiment for every stock mentioned (per week)?
- What posts have the most engagement? (Most comments, upvotes)

最終結果將以 Google Looker Studio 報表呈現

## 動機
- 本專案源自我對資料工程與美國股市的濃厚興趣。
- 我的目標是透過建立端到端的資料處理流程，實作自然語言處理（NLP）元件，學習並展示現代資料工程的實務應用。
- 為了超越基本要求，我刻意導入與業界接軌的工具，包括 dbt、Apache Airflow、Docker 以及以 BigQuery 為基礎的雲端儲存技術。
- 儘管本專案不以擴展性為主要目標，我仍希望能撰寫模組化、可讀性高且接近實際生產環境的程式碼，反映真實工程標準。

## 架構

## 輸出結果

## 事實表結構

## 重現步驟
請依照下列步驟來設定資料處理流程。我已在可能的地方加入說明，若有需要，你也可以自行修改或優化.
> **NOTE**: 本專案是在 M1 MacBook Pro 上開發的。如果你使用的是 Windows 或 Linux，遇到問題時可能需要調整某些元件。

首先，請將此資料庫（repository）複製到你的主目錄中，然後依照步驟操作.
```bash
git clone https://github.com/NothCK/Stock-Sentiment-Pipeline.git
cd Stock-Sentiment-Pipeline
```

1. [Reddit Configuration](instructions/Reddit.md)
2. [Google Cloud Platform](instructions/google_cloud.md)
3. 