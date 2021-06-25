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
def output_json(data):
	resp = make_response(json.dumps(data))
	resp.headers.extend({"content-type": "application/json"})
	return resp

@api.representation('application/xml')
def output_xml(data):
	resp = make_response(dumps({'root' : data}))
	resp.headers.extend({"content-type": "application/xml"})
	return resp

class Enroute(Resource):
	@swag_from("config.yml")
	def post(self):
		try:
			req = request.get_json()

			if self.validation(req):
				# Requesting Google API
				url = "https://maps.googleapis.com/maps/api/geocode/json"
				params = (('address',req['address']),('key','AIzaSyCOD3KvY2DDzEfel-NZ_LKIWXr86EF_EUw'))
				response = requests.post(url,params=params)
				my_json = json.loads(response.content)
				if response.status_code == 200:
					# If request is successfully created
					if my_json['status'] == "OK":
						coordinates = my_json['results'][0]['geometry']['location']
						result = {"address":req['address'],"coordinates":{"lat":coordinates["lat"] ,"lng":coordinates["lng"]}}
					else:
						result = {"message":my_json['status']}
					if req['output_format'] == "json":
						result = output_json(result)
					else:
						result = output_xml(result)
					return result
				else:
					pass
		except:
			pass

	def validation(self,req):
		if 'output_format' in req and 'address' in req and req['output_format'] in ['json','xml']:
			return True
		return False


api.add_resource(Enroute,'/getAdressDetails')

if __name__ == "__main__":
	app.run(debug=True,host='localhost', port=4500)
