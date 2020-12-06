from flask import *
from dynamodb_mgr import cl_dynamodb
app = Flask(__name__)


@app.route('/', methods=["GET"])
def index():
    cl_dd = cl_dynamodb()
    # cl_dd.delete_user_tbl()  # Userテーブルが存在する場合は削除する
    cl_dd.create_user_tbl()  # Userテーブルが存在しなければ作成する
    return render_template("index.html")


@app.route('/logout', methods=["GET"])
def logout():
    return render_template("index.html")


@app.route('/login', methods=["POST"])
def login():
    userid = request.form["userid"]
    password = request.form["password"]
    cl_dd = cl_dynamodb()
    user_rec = cl_dd.read_user_rec(userid)
    if password == user_rec['password']:
        return render_template("user_detail.html", userid=userid, username=user_rec['username'], message=user_rec['message'])
    else:
        return render_template("index.html")


@app.route('/create', methods=["GET"])
def create():
    return render_template("create.html")


@app.route('/comp', methods=["POST"])
def comp():
    cl_dd = cl_dynamodb()
    userid = request.form["userid"]
    username = request.form["username"]
    password = request.form["password"]
    message = request.form["message"]
    cl_dd.set_column(userid, username, password, message)
    if cl_dd.ins_user_rec():
        return render_template("user_detail.html", userid=userid, username=username, message=message)
    else:
        return render_template("create.html")


if __name__ == '__main__':
    app.run(debug=True)
