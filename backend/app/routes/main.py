from flask import Blueprint, request, render_template, current_app, jsonify, send_file
from extensions import db
from services.EVMLiSA.EVMLiSAParams import EVMLiSAParams
from flask_cors import cross_origin


main_bp = Blueprint("main", __name__)

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