from flask import Flask, jsonify
import mysql.connector
import redis
import json

app = Flask(__name__)

# Connect to Redis
redis_client = redis.StrictRedis(host='localhost', port=6379, db=0)


# Connect to MySQL
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="root",
        database="grocerydb"
    )


@app.route('/fruit/<int:fruit_id>')
def get_data(fruit_id):
    # First, try to get the data from the cache (Redis)
    fruit = redis_client.get(f'fruit:{fruit_id}')
    
    if fruit:
        data = {
            "from_cache": True,
            "data": json.loads(fruit)
        }
        return jsonify(data), 200

    # If data is not in cache, fetch from MySQL
    db = get_db_connection()
    cursor = db.cursor(dictionary=True)
    cursor.execute('SELECT id, name, quantity FROM fruit WHERE id = %s', (fruit_id,))
    fruit = cursor.fetchone()
    
    if fruit:
        # Store the fetched data in Redis for future requests
        redis_client.set(f'fruit:{fruit_id}', json.dumps(fruit))
        data = {
            "from_cache": False,
            "data": fruit
        }
        return jsonify(data), 200
    else:
        return jsonify({'error': 'Fruit not found'}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0')
