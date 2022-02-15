import json
import argparse
from cryptography.fernet import Fernet

# Designated filepath for the JSON file for storing passwords
filepath = "../pytestfolder/test.json"

# Key for the Cipher used to decrypt the passwords, its only here temporarily
cipherKey = b'xIyAn6_l4qZ2wE6lEpWy3JbyeYlZm-W-sYfyAc7zYx4='

# Create a file to store passwords in if one does not already exist
def create_file(filename):
	try:
		json_file_format = """{
    "passworddata": [
    ]
}
"""
		to_python = json.loads(json_file_format)
		f = open(filename, 'x')

		with open(filename, 'w') as f:
			json.dump(to_python,f, indent = 4)
			f.close
		print("File Created")
	except:
		print("File already exists")

# Read the data from the json file
def get_data(filename):
	with open(filename, 'r') as f:
		data = json.load(f)
		for x in range(len(data["passworddata"])):
			print("Platform: " + data["passworddata"][x]["platform"] + " Password: " + data["passworddata"][x]["encrypted"])
	f.close()

# Get password at specified index
def get_password_from_index(filename, index):
	with open(filename, 'r') as f:
		data = json.load(f)
		encryptedPass = bytes(data["passworddata"][index]["encrypted"],'UTF-8')
	f.close()
	return encryptedPass

# Function to search for password by platform
def get_password_from_platform_name(filename, platform):
	with open(filename, 'r') as f:
		data = json.load(f)
		for x in range(len(data["passworddata"])):
			if platform == data["passworddata"][x]["platform"]:
				print("Not sure if this will be used")
	f.close()

# Function to write data to json file
def write_data(new_data,filename):
	with open(filename, 'r+') as f:
		file_data = json.load(f)
		file_data["passworddata"].append(new_data)
		f.seek(0)
		json.dump(file_data, f, indent = 4)
		f.close()

# Function to write the input to a python dictionary object,
# takes the password and encrypts it using the encrypt_password function,
# decodes it from binary using the decode function,
# and prepares the object for use in writing to a json file
def prepare_input(email,platform,password):
	encrypted = encrypt_password(password).decode('UTF-8')
	data = {
		"email" : email,
		"platform" : platform,
		"encrypted" : encrypted
	}
	return data

# Encrypt the given password using the Cryptography Library
def encrypt_password(password):
	cipher = Fernet(cipherKey)
	passwordBytes = bytes(password,'UTF-8')
	encrypted = cipher.encrypt(passwordBytes)
	return encrypted

# Decrypt the password using the cipher key
def decrypt_password(encryptedPass):
	cipher = Fernet(cipherKey)
	decryptedPass = cipher.decrypt(encryptedPass)
	print(decryptedPass.decode("utf-8"))


# Get number of passwords stored in the json file
def get_password_count(filename):
	with open(filename, 'r') as f:
		data = json.load(f)
		print(len(data["passworddata"]))


def perform_operation(operation):
    match operation:
        case 'list':
        	get_data(filepath)
        case 'new':
        	create_file(filepath)
        case 'write':
        	email = input("Please enter your Email Address: ")
        	password = input("Please enter your Password: ")
        	platform = input("Please enter the platform associated with this account: ")
        	data = prepare_input(email,platform,password)
        	write_data(data,filepath)
        case 'get':
        	index = int(input("Which password do you want to retrieve: "))
        	encryptedPassword = get_password_from_index(filepath, index)
        	decrypt_password(encryptedPassword)