from flask import Blueprint, request, current_app, jsonify
from services.EVMLiSA.EVMLiSAParams import EVMLiSAParams
from flask_cors import cross_origin


main_bp = Blueprint("main", __name__)

@main_bp.route("/save-api-key", methods=["POST"])
def save_api_key_route():
    data = request.json
    if "api_key" not in data:
        return jsonify({"error": "API Key non fornita"}), 400
    
    current_app.evmLiSAInterface.save_api_key(data["api_key"])
    return jsonify({"message": "API Key salvata con successo!"}), 200

@main_bp.route("/run-command", methods=["POST"])
@cross_origin()
def run_command():

    data = request.get_json()

    address = data.get("address")
    bytecode = data.get("bytecode")

    try:

        params = EVMLiSAParams(
            address=address, 
            bytecode=bytecode, 
            link_unsound_jumps=True
        ) 

        result, status_code = current_app.evmLiSAInterface.run_command(params)

        print(type(result))

        return jsonify(result), status_code
    
    except Exception as e:
    
        return jsonify({"error": str(e)}), 500