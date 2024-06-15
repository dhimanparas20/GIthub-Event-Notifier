from flask import Flask, render_template, make_response, request, session, redirect, url_for, current_app, jsonify
from flask_restful import Api, Resource
from pyMongo import MongoDB
from os import environ, system
import json
from datetime import datetime
import pytz

app = Flask(__name__)
api = Api(app)
app.config['SECRET_KEY'] = "c365a380254da310e47c24a692dad2e8"
mydb = MongoDB("GithubActions", "Data")

class Home(Resource):
    def get(self):
        data = list(mydb.fetch(show_id=True))  # Fetch data from MongoDB
        for item in data:
            item['_id'] = str(item['_id'])  # Convert ObjectId to string
        return jsonify(data)
    
    def post(self):
        try:
            if request.headers['Content-Type'] == 'application/json':
                data = request.json
                data_json = json.dumps(request.json)
                try:
                    action = data['action'] 
                except:
                    action = None    
                
                if action == "opened" or action == "closed":
                    actiontype, id, timestamp = None,None,None
                    if action == "opened":
                        id = data['pull_request']['id']
                        timestamp = data['pull_request']['created_at']
                        actiontype = "PULL_REQUEST"
                    elif action == "closed":
                        timestamp = data['pull_request']['merged_at']
                        id = data['pull_request']['merge_commit_sha']
                        actiontype = "MERGE"

                    from_branch = data['pull_request']['head']['ref']
                    to_branch = data['pull_request']['base']['ref']
                    author = data['pull_request']['user']['login']
                    
                    dt = datetime.fromisoformat(timestamp)
                    utc_dt = dt.astimezone(pytz.UTC)
                    readable_format = utc_dt.strftime("%d-%B-%Y - %I:%M %p UTC")
                    schema = {
                        "request_id": id,
                        "author": author,
                        "action": actiontype,
                        "from_branch": from_branch,
                        "to_branch": to_branch,
                        "timestamp": readable_format
                    }
                    resp = mydb.insert(data=schema)
                    if resp == True:
                        schema["_id"] = str(schema["_id"])
                        return schema
                
                else:
                    branch = data['ref']
                    author = data['commits'][0]['author']
                    reqID = data['commits'][0]['id']
                    timestamp = data['commits'][0]['timestamp']
                    dt = datetime.fromisoformat(timestamp)
                    utc_dt = dt.astimezone(pytz.UTC)
                    readable_format = utc_dt.strftime("%d-%B-%Y - %I:%M %p UTC")
                    
                    schema = {
                        "request_id": reqID,
                        "author": author['name'],
                        "action": "PUSH",
                        "from_branch": branch.split("/")[-1],
                        "to_branch": branch.split("/")[-1],
                        "timestamp": readable_format
                    }
                    resp = mydb.insert(data=schema)
                    if resp == True:
                        schema["_id"] = str(schema["_id"])
                        return schema
            
            return {"error": "Invalid Data Type"}
        
        except Exception as e:
            print("Exception:" ,e)
            return {"error": str(e)}

@app.route('/')
def index():
    return render_template('index.html')

api.add_resource(Home, '/api/events')

if __name__ == '__main__':
    system("clear")
    app.run(debug=True, port=5000, host="0.0.0.0", threaded=True)
