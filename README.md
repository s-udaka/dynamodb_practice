## 動かす環境
- docker-composeでDynamoDB localを動かす
- Anaconda仮想環境上のPython(Flask)からコンテナ上のDynamoDB localにアクセス
- NoSQL Workbenchでコンテナ上のDynamoDB localにアクセスし、テーブルの内容を確認

## 起動手順
- `docker-compose up -d`でDynamoDB localのコンテナを立ち上げる
- `python flask/main.py`でFlaskアプリを立ち上げる
  - 前提条件(Anacondaで仮想環境構築済み)
  - `conda install boto3`
  - `conda install flask`