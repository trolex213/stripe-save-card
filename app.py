from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/api/save-user', methods=['POST'])
def save_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    org = data.get("org")

    with open("signups.txt", "a") as f:
        f.write(f"Name: {name}, Email: {email}, Org: {org}\n")

    return jsonify({"status": "success"}), 200


@app.route('/api/track-click', methods=['POST'])
def track_click():
    with open("clicks.txt", "a") as f:
        f.write("Button clicked\n")
    return jsonify({"status": "click recorded"}), 200


if __name__ == '__main__':
    app.run(port=4242)
