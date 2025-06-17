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
### 設定 Reddit 帳戶
1. 如果你還沒有 Reddit 帳號，請先建立一個。這是使用 Reddit API 擷取子版資料的必要條件。
2. 建立帳號後，前往 [here](https://www.reddit.com/prefs/apps). 點選頁面底部的 `create another app...` 按鈕。填寫必要欄位並選擇 `web app`. 然後點擊 `create app`
3. 建立完成後，在 `web app` 區塊下方，你會看到你的 client ID （位於應用程式名稱下方）以及 client secret。
請妥善保存這些憑證——你將需要它們來在專案中透過 PRAW API 進行身份驗證。

### 設定 Google Cloud 
1. 建立一個 Google Cloud 帳戶
2. 建立一個新的 Google Cloud [project](https://cloud.google.com/).
3. 前往`IAM & Admin`→`Service Accounts`，點擊「建立服務帳戶」。請為該帳戶指派以下角色:
* `Compute Admin`
* `Service Account User`
* `Storage Admin`
* `Storage Object Admin`
* `BigQuery Admin Roles`
4. 服務帳戶建立完成後，點擊 `Manage Keys` 選單中的三個點，選擇 `Actions Menu`. 點擊 `Add Key` 下拉選單並選擇 `Create new key`. 系統會跳出提示要求你下載金鑰，請選擇 JSON 格式並下載金鑰檔案.
5. 安裝 [Google Cloud CLI](https://cloud.google.com/sdk/docs/install-sdk)
> **NOTE**: 本專案是在 M1 Macbook Pro 上開發。如果你使用的是 Windows 或 Linux，請依照各自平台指示操作.
請執行 `gcloud init` 完成登入設定.
6. 設定環境變數，指向剛下載的服務帳戶 JSON 金鑰檔案:
`export GOOGLE_APPLICATION_CREDENTIALS=<path/to/your/service-account-authkeys>.json`
7.更新權杖/登入環境，認證你的應用程式環境:
`gcloud auth application-default login`
8.確認你的專案已啟用以下 API:
https://console.cloud.google.com/apis/library/iam.googleapis.com 
https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com 
https://console.cloud.google.com/apis/library/compute.googleapis.com
https://console.cloud.google.com/apis/library/bigquery.googleapis.com
https://console.cloud.google.com/apis/library/dataplex.googleapis.com

