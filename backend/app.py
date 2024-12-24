from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/api/tribes', methods=['GET'])
def get_tribes():
    return jsonify({"message": "Tribes endpoint working!"})

if __name__ == "__main__":
    app.run(debug=True)