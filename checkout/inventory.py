# #!/usr/bin/env python3
# # The above shebang (#!) operator tells Unix-like environments
# # to run this file as a python3 script

import os
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route("/inventory/reduce", methods=['PUT'])
def update_inventory_numbers():
    # Check if the order contains valid JSON
    order = None
    if request.is_json:
        order = request.get_json()
        result = {
            "code": 200,
            "data": {},
            "message": "success"
        }
        return jsonify(result), 200


# execute this program only if it is run as a script (not by 'import')
if __name__ == "__main__":
    print("This is flask " + os.path.basename(__file__) +
          ": shipping for orders ...")
    app.run(host='0.0.0.0', port=5552, debug=True)
