import boto3


class cl_dynamodb:
    def __init__(self):
        self.dynamodb = boto3.resource(
            'dynamodb',
            endpoint_url="http://localhost:8000",
            region_name='ap-northeast-1',
            aws_access_key_id='dummyid',
            aws_secret_access_key='dummysec'
        )
        self.userid = ""
        self.username = ""
        self.password = ""
        self.message = ""
        self.user_tbl = None
    
    def check_user_tbl(self):
        flg = False
        try:
            res = self.dynamodb.tables.all()  # Tableを全て取得
        except Exception as e:
            print(e.args)
        for table in res:
            print(table.table_name)
            if "User" == table.table_name:  # テーブル名がUserのテーブルがあればTrueに
                flg = True
                print("Userテーブルあった")
        # self.user_tbl = self.dynamodb.Table('User')
        # if self.user_tbl:
        #     flg = True
        #     print("ユーザーテーブルの確認完了")
        return flg
    
    def create_user_tbl(self):
        if not self.check_user_tbl():  # Userテーブルが存在しなければ作成する
            table = self.dynamodb.create_table(
                TableName='User',
                KeySchema=[
                    {
                        'AttributeName': 'userid',
                        'KeyType': 'HASH'  # Partition key
                    }
                ],
                AttributeDefinitions=[
                    {
                        'AttributeName': 'userid',
                        'AttributeType': 'S'
                    }
                ],
                ProvisionedThroughput={
                    'ReadCapacityUnits': 1,
                    'WriteCapacityUnits': 1
                }
            )
            print("ユーザーテーブル作成成功")
    
    def set_column(self, userid, username, password, message):
        self.userid = userid
        self.username = username
        self.password = password
        self.message = message
    
    def ins_user_rec(self):
        flg = False
        if self.check_user_tbl():  # Userテーブルが存在する場合のみユーザー登録を実行
            table = self.dynamodb.Table('User')
            response = table.put_item(
                Item={
                    'userid': self.userid,
                    'username': self.username,
                    'password': self.password,
                    'message': self.message
                }
            )
            flg = True
            print("ユーザーレコード挿入成功")
        return flg

    def read_user_rec(self, userid):
        if self.check_user_tbl():  # Userテーブルが存在する場合のみユーザー検索を実行
            try:
                table = self.dynamodb.Table('User')
                response = table.get_item(Key={'userid': userid})
            except Exception as e:
                print(e.args)
            else:
                return response['Item']

    def delete_user_tbl(self):
        if self.check_user_tbl():  # Userテーブルが存在する場合のみ削除を実行
            table = self.dynamodb.Table('User')
            table.delete()
            print("ユーザーテーブル削除成功")
