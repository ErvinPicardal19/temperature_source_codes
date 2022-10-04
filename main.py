from flask import Flask, jsonify, request, make_response
import json
import uuid
from datetime import date

with open("./temp.json", "r") as jsonFile:
    tempDB = json.load(jsonFile)
    
def res(response, code):
    return make_response(jsonify(response, code))

app = Flask(__name__)

@app.route('/api/v1/temp', methods=["GET"])
def getAllTemp():
    return res({"success": True, "data": tempDB},200)

@app.route('/api/v1/temp/<id>', methods=["GET"])
def getSingleTemp(id):
    print(id)
    for data in tempDB:
        print(data)
        if data["temp_id"] == str(id):
            return jsonify({
                "success": True,
                "data": data
            })
    res = make_response(jsonify({
            "success": False,
            "msg": "Does not exist"
        }), 404)
    return res


@app.route('/api/v1/temp', methods=["POST"])
def createNewTemp():
    if str(request.get_json()["temperature"]) == "":
        return res({"success": False, "msg": "Please provide temperature"}, 404)
    
    new_id = str(uuid.uuid1())
    new_date = str(date.today())
    new_temp = str(request.get_json()["temperature"])
    
    tempDB.append({
        "temp_id": new_id,
        "date": new_date,
        "temperature": new_temp
    })
    
    with open("./temp.json", "w") as j:
        json.dump(tempDB, j)
    
    return res({"success": True, "data": tempDB}, 200)

@app.route('/api/v1/temp/<id>', methods=["PUT"])
def updateTemp(id):
    for data in tempDB:
        if data["temp_id"] == str(id):
            data["temperature"] =  request.get_json()["temperature"]
            with open("./temp.json", "w") as j:
                json.dump(tempDB, j)
            return jsonify({
                "success": True,
                "data": data
            })
    res = make_response(jsonify({
            "success": False,
            "msg": "Does not exist"
        }), 404)
    return res

@app.route('/api/v1/temp/<id>', methods=["DELETE"])
def deleteTemp(id):
    for i,data in enumerate(tempDB):
        if data["temp_id"] == str(id):
            tempDB.pop(i)
            with open("./temp.json", "w") as j:
                json.dump(tempDB, j)
            return jsonify({
                "success": True,
                "data": data
            })
    res = make_response(jsonify({
            "success": False,
            "msg": "Does not exist"
        }), 404)
    return res
    

if __name__ == "__main__":
    app.run(debug=True)