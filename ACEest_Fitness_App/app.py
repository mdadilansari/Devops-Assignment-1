from flask import Flask, request, jsonify

app = Flask(__name__)

workouts = []

@app.route('/')
def home():
    return "Welcome to ACEest Fitness and Gym API!"

@app.route('/add', methods=['POST'])
def add_workout():
    data = request.get_json()
    workout = data.get("workout")
    duration = data.get("duration")

    if not workout or not duration:
        return jsonify({"error": "Workout and duration required"}), 400
    
    workouts.append({"workout": workout, "duration": duration})
    return jsonify({"message": f"{workout} added successfully!"}), 201

@app.route('/workouts', methods=['GET'])
def view_workouts():
    if not workouts:
        return jsonify({"message": "No workouts logged yet."}), 200
    return jsonify(workouts), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
