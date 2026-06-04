from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
import random

app = Flask(__name__)
CORS(app)

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Sushanta@1430",
    database="skbank"
)

cursor = db.cursor()

@app.route('/register', methods=['POST'])
def register():

    data = request.json

    first_name = data['first_name']
    last_name = data['last_name']
    mobile = data['mobile']
    email = data['email']

    account_number = "SK" + str(random.randint(1000000000,9999999999))
    customer_id = "CID" + str(random.randint(10000,99999))

    sql = """
    INSERT INTO accounts
    (first_name,last_name,mobile,email,account_number,customer_id)
    VALUES (%s,%s,%s,%s,%s,%s)
    """

    val = (
        first_name,
        last_name,
        mobile,
        email,
        account_number,
        customer_id
    )

    cursor.execute(sql,val)
    db.commit()

    return jsonify({
        "account_number": account_number,
        "customer_id": customer_id
    })

@app.route('/login', methods=['POST'])
def login():

    data = request.json

    account_number = data['account_number']
    customer_id = data['customer_id']

    cursor.execute(
        "SELECT * FROM accounts WHERE account_number=%s AND customer_id=%s",
        (account_number,customer_id)
    )

    user = cursor.fetchone()

    if user:
        return jsonify({
            "success": True,
            "name": user[1] + " " + user[2],
            "account_number": user[5],
            "customer_id": user[6],
            "balance": str(user[7])
        })

    return jsonify({"success":False})

app.run(debug=True)