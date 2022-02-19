import json
import os.path
from cryptography.fernet import Fernet

# This portion of the code creates the necessary file for storing the encrypted passwords
# This method is what is used to create the JSON file that will be used to store the encrypted passwords
def create_file(filename):
	try:
		f = open(filename, 'x')
		f.close()
	except FileExistsError:
		print("File already Exists")



# This method is used to create the desired format for the json file
def import_format(filename):
	json_file_format = """{
    "passworddata": [
    ]
}
"""
	to_python = json.loads(json_file_format)
	with open(filename, 'w') as f:
		json.dump(to_python,f, indent = 4)



# This next portion determines where the users documents folder is located
docPath = R"C:\Users\$USERNAME\Documents"
docPath = os.path.expandvars(docPath) + "\PMPro"


# A try except block is used to make sure the file does not already exist, and if it does, it will back out and throw the exception
if not os.path.exists(docPath):
	os.mkdir(docPath)



# Append the name of the json file we wish to use for storage to the end of the filepath
confPath = docPath + "\config.json"
docPath = docPath+ "\PMStorage.json"


# generate new cipher key, will only be used if there is no config file / cipher key already
def gen_key_file(filename):
	key = Fernet.generate_key()
	conf = {
		"key" : key.decode('UTF-8')
	}
	with open(filename, "w") as confWrite:
		json.dump(conf, confWrite)


# Read the cipherkey from the config file
def read_ciph_key(filename):
	with open(filename, 'r') as confRead:
		data = json.load(confRead)
		ciph = bytes(data['key'], 'UTF-8')
	return ciph

# Check if the file path does not already exist, if it doesn't, the program will execute the create_file method, creating the JSON file in the desired path
# Does nothing if the file already exists. These two if statements create both the json storage file, and the config file
if not os.path.exists(docPath):
	create_file(docPath)
	import_format(docPath)


if not os.path.exists(confPath):
	create_file(confPath)
	gen_key_file(confPath)

# Initiates the cipherKey Variable that will be used in the encryption of your passwords
cipherKey = read_ciph_key(confPath)

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


# Match case statement for carrying out user designated operations
def perform_operation(operation):
    match operation:
        case 'list':
        	get_data(docPath)
        case 'write':
        	email = input("Please enter your Email Address: ")
        	password = input("Please enter your Password: ")
        	platform = input("Please enter the platform associated with this account: ")
        	data = prepare_input(email,platform,password)
        	write_data(data,docPath)
        case 'get':
        	index = int(input("Which password do you want to retrieve: "))
        	encryptedPassword = get_password_from_index(docPath, index)
        	decrypt_password(encryptedPassword)