import requests
from flask import Flask, jsonify,request,make_response
from flasgger import Swagger
from flasgger.utils import swag_from
import json
from flask_restful import Api,Resource
from simplexml import dumps

app = Flask(__name__)
api = Api(app)
app.config['SWAGGER'] = {
	'title': 'Verloop API Documentation',
	'description':"This API renders Lattitude and Longitude of a corresponding address.",
	'uiversion': 3,
	'version':"2.2.0",
	'termsOfService':False,
	'host':'localhost:4500',
}
swagger = Swagger(app)

@api.representation('application/json')
def output_json(data, code, headers=None):
	resp = make_response(json.dumps(data), code)
	resp.headers.extend({"content-type": "application/json"})
	return resp

@api.representation('application/xml')
def output_xml(data, code, headers=None):
	resp = make_response(dumps({'root' : data}), code)
	resp.headers.extend({"content-type": "application/xml"})
	return resp

class Enroute(Resource):
	@swag_from("config.yml")
	def post(self):
			flag = True #Indicating request to be created or not
			flag2 = True #Indicating output_format param is passed or not
			req = request.get_json()
			print('\n==================Request for getAdressDetails route: ', req)
			required_params = ['address','output_format']
			params = request.json
			received_params = [*params.keys()]
			for required_param in required_params:
				if required_param not in received_params:
					result = {"message":"Missing param '"+required_param+"'"}
					code = 406
					flag = False
					break
			if flag:
				# Requesting Google API
				url = "https://maps.googleapis.com/maps/api/geocode/json"
				req_params = (
					('address',params['address']),
					('key','AIzaSyCOD3KvY2DDzEfel-NZ_LKIWXr86EF_EUw')
				)
				response = requests.post(url,params=req_params)
				my_json = json.loads(response.content)
				# If request is successfully created
				if my_json['status'] == "OK":
					coordinates = my_json['results'][0]['geometry']['location']
					lat = coordinates["lat"]
					lng = coordinates["lng"]
					result = {"address":params['address'],"coordinates":{"lat":lat ,"lng":lng}}
					code = 200
				elif my_json['status'] == "ZERO_RESULTS":
					message = "No such address found."
					result = {"message":message}
					code = 201
				else:
					pass
			else:
				if "output_format" in result['message']:
					flag2 = False
			if flag2:
				if params['output_format'] == "json":
					result = output_json(result, code)
				elif params['output_format'] == 'xml':
					result = output_xml(result, code)
				else:
					result = {"message":"output_format value should be either json or xml."}
			print('\n==================Response for getAdressDetails route: ', result)
			return result

api.add_resource(Enroute,'/getAdressDetails')

if __name__ == "__main__":
	app.run(debug=True,host='localhost', port=4500)
