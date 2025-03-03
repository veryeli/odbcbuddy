"""Runs main app"""
import json
from datetime import datetime, time


from flask import Flask, jsonify, request
from flask.json.provider import DefaultJSONProvider
import pyodbc
from consts import ODB_CONN_STR


app = Flask(__name__)

class CustomJSONProvider(DefaultJSONProvider):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        if isinstance(obj, time):
            return obj.strftime('%H:%M:%S')
        return super().default(obj)

app.json = CustomJSONProvider(app)

def get_db_connection():
    connection = pyodbc.connect(ODB_CONN_STR)
    return connection

# Define a route to test the connection
@app.route('/test', methods=['GET'])
def test_connection():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(1) from case_reporting_view")
        result = cursor.fetchone()
        return jsonify({'status': 'success', 'result': result[0]})
    except Exception as e:
        return jsonify({'status': 'error',
            'message': str(e),
            'conn_str': ODB_CONN_STR})

@app.route('/query', methods=['POST'])
def execute_query():
    data = request.get_json()
    query = data.get('query')
    if not query:
        return jsonify({'status': 'error', 'message': 'No query provided'}), 400

    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]
        results = [dict(zip(columns, row)) for row in rows]
        return jsonify({'status': 'success', 'results': results})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/')
def index():
    return jsonify({"message": "Hello, Friend!"})

@app.route('/flask')
def flask_route():
    return jsonify({"message": "This is the Flask route."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

