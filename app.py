from flask import Flask, jsonify, request
from models.minioptimus import Society, Norm, Case  # Import de tes classes

app = Flask(__name__)

# Instancier les systèmes
society = Society()

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Optimus backend API!"})

@app.route('/create_norm', methods=['POST'])
def create_norm():
    norm = society.parliament.create_norm()
    return jsonify({
        "id": norm.id,
        "text": norm.text,
        "valid": norm.valid,
        "complexity": norm.complexity
    })

@app.route('/check_constitutionality', methods=['POST'])
def check_constitutionality():
    norm_id = request.json.get('norm_id')
    norm = next((n for n in society.parliament.norms if n.id == norm_id), None)
    if not norm:
        return jsonify({"error": "Norm not found"}), 404
    society.judicial_system.check_constitutionality(norm)
    return jsonify({
        "id": norm.id,
        "valid": norm.valid,
        "complexity": norm.complexity
    })

@app.route('/create_case', methods=['POST'])
def create_case():
    norm_id = request.json.get('norm_id')
    norm = next((n for n in society.parliament.norms if n.id == norm_id), None)
    if not norm:
        return jsonify({"error": "Norm not found"}), 404
    case = society.judicial_system.create_case(norm)
    if not case:
        return jsonify({"error": "Cannot create case for invalid norm"}), 400
    return jsonify({
        "id": case.id,
        "text": case.text,
        "constitutional": case.constitutional
    })

@app.route('/simulate_day', methods=['POST'])
def simulate_day():
    try:
        asyncio.run(society.simulate_day())
        return jsonify({"message": "Day simulated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)