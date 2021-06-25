# from flask import request
from flask_restful import Resource
import requests
from flask import Flask, jsonify,request,make_response
from flasgger import Swagger
from flasgger.utils import swag_from
import json

class Greet(Resource):
	@swag_from("config.yml")
	def post(self):
			req = request.get_json()
			print('\n==================Request for getAdressDetails route: ', req)
			required_params = ['address','output_format']
			params = request.json
			received_params = [*params.keys()]
			for required_param in required_params:
				if required_param not in received_params:
					return {"message":"Missing param '"+required_param+"'"},406

			url = "https://maps.googleapis.com/maps/api/geocode/json"
			req_params = (
				('address',params['address']),
				('key','AIzaSyCOD3KvY2DDzEfel-NZ_LKIWXr86EF_EUw')
			)
			response = requests.post(url,params=req_params)
			my_json = json.loads(response.content)
			if my_json['status'] == "OK":
				coordinates = my_json['results'][0]['geometry']['location']
				lat = coordinates["lat"]
				lng = coordinates["lng"]
				result = {"address":params['address'],"coordinates":{"lat":lat ,"lng":lng}}
				return result, 200
			elif my_json['status'] == "ZERO_RESULTS":
				message = "No such address found."
				result = {"message":message}
				return result, 301
			else:
				pass
			
