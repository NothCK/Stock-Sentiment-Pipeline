## Setup Google Cloud 
> **NOTE**: Google Cloud Offers a free trial. As long as you don't go over the credit limit or activate/upgrade your billing account you shouldn't be charged.

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
7. Refresh token/session, and authenticate your application environment:
`gcloud auth application-default login`
8. Make sure these APIs are enabled for your project:

https://console.cloud.google.com/apis/library/iam.googleapis.com 
https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com 
https://console.cloud.google.com/apis/library/compute.googleapis.com
https://console.cloud.google.com/apis/library/bigquery.googleapis.com
https://console.cloud.google.com/apis/library/dataplex.googleapis.com

> **NOTE**: Chinese Translation Below
## 設定 Google Cloud 
> **NOTE**: Google Cloud 提供免費試用。只要你不超過額度限制，或沒有啟用／升級你的帳單帳戶，就不會被收費.

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
7. 更新權杖/登入環境，認證你的應用程式環境:
`gcloud auth application-default login`
8. 確認你的專案已啟用以下 API:

https://console.cloud.google.com/apis/library/iam.googleapis.com 
https://console.cloud.google.com/apis/library/iamcredentials.googleapis.com 
https://console.cloud.google.com/apis/library/compute.googleapis.com
https://console.cloud.google.com/apis/library/bigquery.googleapis.com
https://console.cloud.google.com/apis/library/dataplex.googleapis.com

[Previous Step](Reddit.md) | [Next Step](../README.md)

or

[Back to main README](../README.md)