import json
filepath = "../pytestfolder/testalt.json"

# Create a file to store passwords in if one does not already exist
def create_file():
	try:
		f = open("test.json", "x")
		print("File Created")
	except:
		print("File already exists")

# Read the data from the json file
def read_data(filename):
	try:
		with open(filename, 'r') as f:
			data = json.load(f)
			for x in range(len(data["passworddata"])):
				print("Platform: " + data["passworddata"][x]["platform"] + " Password: " + data["passworddata"][x]["password"])
		f.close()
	except:
		print("An error has occured")


def get_password(filename, index):
	try:
		with open(filename, 'r') as f:
			data = json.load(f)
			print("Platform: " + data["passworddata"][index]["platform"] + " Password: " + data["passworddata"][index]["password"])
		f.close()
	except:
		print("An error has occured")

# Function to write data to json file
def write_data(new_data,filename):
	try:
		with open(filename, 'r+') as f:
			file_data = json.load(f)
			file_data["passworddata"].append(new_data)
			f.seek(0)
			json.dump(file_data, f, indent = 4)
			f.close()
	except:
		print("An error has occured")


y = {
	"platform" : "amazon",
	"password" : "password1",
	"hash" : "blank"
}

#read_data(filepath)
#write_data(y)