from flask import Flask
from flask_restful import Api, Resource, reqparse

app = Flask(__name__)
api = Api(app)

classes = [
	{
		"name" : "6B",
		"master" : "Németh József"
	}
]

pupils = [
	{
		"id"  : 1,
		"class_name" : "6B",
		"family_name" : "Mészáros",
		"first_name" : "András",
		"birth_date" : "1961-04-28",
		"birth_place" : "Budapest VIII"
	}
]

class Class(Resource):

	def get(self, name):
		if(name == "all"):
			result = []
			for schoolclass in classes:
				result.append(schoolclass["name"])
			return result, 200

		for schoolclass in classes:
			if(name == schoolclass["name"]):
				return schoolclass, 200
		return "Class with name {} not found.".format(name), 404

	def post(self, name):  # new schoolclass
		for schoolclass in classes:
			if(name == schoolclass["name"]):
				return "Class with name {} already exists.".format(name), 400

		parser = reqparse.RequestParser()
		parser.add_argument("master")
		args = parser.parse_args()

		schoolclass = {
			"name" : name,
			"master" : args["master"]
		}
		classes.append(schoolclass)
		return schoolclass, 201

	def delete(self, name):
		global classes
		global pupils
		if(name == "all-cascaded"):
			classes = []
			pupils = []
			Pupil.last_id = 0
			return "All classes has been deleted.", 200

		for pupil in pupils:
			if(name == pupil["class_name"]):
				return "Class {} is not empty.".format(name), 400

		for schoolclass in classes:
			if (name == schoolclass["name"]):
				classes = [schoolclass for schoolclass in classes if schoolclass["name"] != name]
				return "Class {} has been deleted.".format(name), 200

		return "Class with name {} not found.".format(name), 404


class Pupil(Resource):

	last_id = 0

	def get(self, id):
		if(id == "all"):
			return pupils, 200

		for pupil in pupils:
			if(id == str(pupil["id"])):
				return pupil, 200

		return "Pupil with id {} not found.".format(id), 404

	def post(self, id):  # new pupil
		if (id == "next"):
			# create new pupil id
			new_id = Pupil.last_id + 1
		elif (id.isdigit()):
			new_id = int(id)
		else:
			return "Id '{}' should be 'next' or an integer number >= 0 .".format(id), 400

		# check pupil id
		for pupil in pupils:
			if (new_id == pupil["id"]):
				return "Pupil with id {} (originally {}) already exists.".format(new_id, id), 400

		parser = reqparse.RequestParser()
		parser.add_argument("class_name")
		parser.add_argument("family_name")
		parser.add_argument("first_name")
		parser.add_argument("birth_date")
		parser.add_argument("birth_place")
		args = parser.parse_args()

		# check wether pupil exists
		family_name = args["family_name"]
		first_name = args["first_name"]
		birth_date = args["birth_date"]
		birth_place = args["birth_place"]

		for pupil in pupils:
			if (
				family_name == pupil["family_name"] and
				first_name == pupil["first_name"] and
				birth_date == pupil["birth_date"] and
				birth_place == pupil["birth_place"]
			):
				return "Pupil {} {} {} {} already exists. (id: {}, originally {})".format(family_name, first_name, birth_date, birth_place, pupil["id"], id), 400

		# check class name
		class_name = args["class_name"]

		for school_class in classes:
			if (class_name == school_class["name"]):
				# class name found
				pupil = {
					"id" : new_id,
					"class_name" : args["class_name"],
					"family_name" : args["family_name"],
					"first_name" : args["first_name"],
					"birth_date" : args["birth_date"],
					"birth_place" : args["birth_place"]
				}

				if (new_id > Pupil.last_id):
					Pupil.last_id = new_id

				pupils.append(pupil)
				return pupil, 201


		return "Class with name {} not found.".format(class_name), 400


	def delete(self, id):
		global pupils
		if(id == "all"):
			pupils = []
			return "All pupils has been deleted.", 200

		for pupil in pupils:
			if (id == str(pupil["id"])):
				pupils = [pupil for pupil in pupils if str(pupil["id"]) != id]
				return "Pupil {} {} {} {} (id: {}) has been deleted.".format(pupil["family_name"], pupil["first_name"], pupil["birth_date"], pupil["birth_place"], id), 200

		return "Pupil with id {} not found.".format(id), 404



api.add_resource(Class, "/class/<string:name>")
api.add_resource(Pupil, "/pupil/<string:id>")

app.run(debug=True, ssl_context = 'adhoc')  # DEVelopment ONLY

