from flask import Flask, jsonify, request
import pyodbc
from consts import ODB_CONN_STR

app = Flask(__name__)

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
    return jsonify({"message": "Hello, World!"})

@app.route('/flask')
def flask_route():
    return jsonify({"message": "This is the Flask route."})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)

