# chef-gpt-api

你的專屬料理廚師 ChefGPT API

## 協作專案

Web Repo: [pock999/chef-gpt-web](https://github.com/pock999/chef-gpt-web)

## 環境

- Python 3.9.18
- Docker 20.10.20

## 使用指南

1. 啟動 PostgreSQL 服務

使用 Docker 啟動 PostgreSQL

```shell
. script/start_postgresql.sh
```

設定資料庫帳號密碼

```shell
# 1. 進入容器內
sudo docker exec -it postgres /bin/bash

# 2. 進入資料庫
psql -h localhost -U postgres

# 3. 建立使用者
CREATE USER chef WITH PASSWORD 'chef';

# 4. 建立資料庫
CREATE DATABASE 'chefgpt' WITH OWNER = chef;

# 5. 離開
\q
```

初始化資料表，參考 `sql/init_table.sql`。

2. 啟動 Qdrant 服務

使用 Docker 啟動 Qdrant

```shell
. script/start_qdrant.sh
```

3. 安裝 Python 套件

```shell
pip install poetry
poetry install
```

4. 設定環境

   複製一個 `env_default.yml` 並改名為 `env.yml`，修改裡面的內容。

5. 準備語料

預設是使用 [Anduin2017/HowToCook](https://github.com/Anduin2017/HowToCook) 的食譜，經過簡轉繁與移除備註資料，將處理後的 Markdown 放到 data/recipe 資料夾內。

6. 下載 LLM 權重

使用 TheBloke 釋出的 [Chinese-Alpaca-2](https://huggingface.co/TheBloke/Chinese-Alpaca-2-7B-GGUF) GGUF 模型，也可以替換成其他 llama2 模型。

7. 啟動服務

```shell
uvicorn main:app --host 0.0.0.0 --port 8000
```

8. 開始使用

- API：http://127.0.0.1:8000/api/v1
- API 文件：http://127.0.0.1:8000/docs 或 http://127.0.0.1:8000/redoc
