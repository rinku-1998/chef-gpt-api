# chef-gpt-api

Chef GPT API

## 協作專案

Web Repo: [pock999/chef-gpt-web](https://github.com/pock999/chef-gpt-web)

## 環境

- Python 3.12

## 使用指南

1. 安裝 Python 套件

```shell
pip install poetry
poetry install
```

2. 設定環境
   在專案目錄下新增一個 `env.yml` 檔，並在裡面輸入：

```
DB_URL: "postgresql://<DB_USER>:<DB_PASSWORD>@<DB_HOST>:<DB_PORT>/<DB_NAME>"
```

3. 啟動服務

```shell
uvicorn main:app --host 0.0.0.0 --port 8000
```

4. 開始使用

- API：http://127.0.0.1:8000/api/v1
- API 文件：http://127.0.0.1:8000/docs 或 http://127.0.0.1:8000/redoc
