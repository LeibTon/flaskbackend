from flask import Flask, json, request
from flask_cors import CORS
from random_experiment import Experiment
app = Flask(__name__)
CORS(app)

@app.route("/project/random_experiment/",methods=["POST"])
def random_experiment():
    content = request.json
    temp = Experiment(content["random"],content["r"],content["part"])
    print("Object created")
    result = temp.main()
    print("Result evaluated")
    return json_response(result)
    '''
    except:
        return json_response({'Error':'Error while processing'},400)
'''

def json_response(payload,status=200):
    return (json.dumps(payload),status, {'content-type':'application/json'})


if __name__ =="__main__":
    app.run()
