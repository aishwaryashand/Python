import requests
from flask import Flask, jsonify,request,make_response,Response
from flasgger import Swagger
from flasgger.utils import swag_from
import json
from flask_restful import Api,Resource
from simplexml import dumps
import rest

app = Flask(__name__)
# api = Api(app)
app.config['SWAGGER'] = {
	'title': 'Verloop API Documentation',
	'description':"This API renders Lattitude and Longitude of a corresponding address.",
	'uiversion': 3,
	'version':"2.2.0",
	'termsOfService':False,
	'host':'localhost:4500',
}
swagger = Swagger(app)

# @api.representation('application/json')
# def output_json(data, code, headers=None):
# 	resp = make_response(json.dumps({'response' : data}), code)
# 	resp.headers.extend(headers or {})
# 	return resp

# @api.representation('application/xml')
# def output_xml(data, code, headers=None):
# 	resp = make_response(dumps({'response' : data}), code)
# 	resp.headers.extend(headers or {})
# 	return resp

@app.route("/getAdressDetails", methods=["POST"])
@swag_from("config.yml")
def post():
	# try:
		try:
			print("\n==================Request for getAdressDetails route: " + str(json.loads(request.data)))
		except:
			return jsonify({"status_code":405,"status":False,'message':"Data is not JSON serializable."})
		required_params = ['address','output_format']
		params = request.json
		received_params = [*params.keys()]
		for required_param in required_params:
			if required_param not in received_params:
				return jsonify({"status_code":406,"status":False,"message":"Missing param '"+required_param+"'"})

		url = "https://maps.googleapis.com/maps/api/geocode/json"
		req_params = (
			('address',params['address']),
			('key','AIzaSyCOD3KvY2DDzEfel-NZ_LKIWXr86EF_EUw')
		)
		response = requests.post(url,params=req_params)
		my_json = json.loads(response.content)
		if my_json['status'] == "OK":
			print(my_json['results'][0]['geometry']['location'])
		elif my_json['status'] == "ZERO_RESULTS":
			print("No such address found.")
		else:
			pass
		result = {"status_code":200,"status":True,"address":params['address']}
		# r = Response(response=result, status=200, mimetype="application/json")
		# r.headers["Content-Type"] = "application/json"
		# my_resp = make_response(result)
		# my_resp.headers['Content-Type'] = 'application/json'
		return result,{'Content-Type': 'application/xml','mimetype':'application/xml'}

# api.add_resource(rest.Greet,'/getAdressDetails')

if __name__ == "__main__":
	app.run(debug=True,host='localhost', port=4500)
