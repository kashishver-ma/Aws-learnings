import pymysql
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)


# DB connection details
try:
    db = pymysql.connect(
        host="calc-db.c9saw08808qv.ap-south-1.rds.amazonaws.com",
        user="admin",
        password="1234admin",
        database="calculator"
    )
    print("✅ Connected to RDS successfully")
except Exception as e:
    print("❌ Failed to connect to RDS:", e)

@app.route('/calculate', methods=['POST'])
def calculate():
    data = request.get_json()
    print("Received data:", data)  # debug

    num1 = data.get('num1')
    num2 = data.get('num2')
    operation = data.get('operation')
    print(f"Parsed num1={num1}, num2={num2}, operation={operation}")  # debug

    if operation == "add":
        result = num1 + num2
    elif operation == "subtract":
        result = num1 - num2
    elif operation == "multiply":
        result = num1 * num2
    elif operation == "divide":
        if num2 == 0:
            return jsonify({"error": "Cannot divide by zero"}), 400
        result = num1 / num2
    else:
        return jsonify({"error": "Invalid operation"}), 400

    print(f"Calculated result: {result}")  # debug

    # Store in DB
    try:
        with db.cursor() as cursor:
            cursor.execute(
                "INSERT INTO calculations (num1, num2, operation, result) VALUES (%s, %s, %s, %s)",
                (num1, num2, operation, result)
            )
            db.commit()
            print("✅ Inserted into DB successfully")  # debug
    except Exception as e:
        print("❌ Failed to insert into DB:", e)

    return jsonify({"result": result})

@app.route('/history', methods=['GET'])
def history():
    try:
        with db.cursor() as cursor:
            cursor.execute("SELECT * FROM calculations ORDER BY id DESC LIMIT 10")
            rows = cursor.fetchall()
            print("Fetched history:", rows)  # debug
    except Exception as e:
        print("❌ Failed to fetch history:", e)
        rows = []
    return jsonify(rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
