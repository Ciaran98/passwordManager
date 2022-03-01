from fileinput import filename
import json
import os.path
import tempfile
from cryptography.fernet import Fernet

# This portion of the code creates the necessary file for storing the encrypted passwords
# This method is what is used to create the JSON file that will be used to store the encrypted passwords
def create_file(filename):
	try:
		f = open(filename, 'x')
		f.close()
	except FileExistsError:
		print("File already Exists")



# This method is used to create the desired format for the storage json file
def import_format(filename):
	json_file_format = """{
	"passworddata": [
	]
}
"""
	to_python = json.loads(json_file_format)
	with open(filename, 'w') as f:
		json.dump(to_python,f, indent = 4)





# generate new cipher key, will only be used if there is no config file / cipher key already
def gen_key_file(filename, ciph_key):
	conf = {
		"key" : ciph_key.decode('UTF-8')
	}
	with open(filename, "w") as confWrite:
		json.dump(conf, confWrite)



# Read the cipherkey from the config file
def read_ciph_key(filename):
	with open(filename, 'r') as confRead:
		data = json.load(confRead)
		ciph = bytes(data['key'], 'UTF-8')
	return ciph

def get_filepath():
	filepath = R"C:\Users\$USERNAME\Documents\PMPro\PMStorage.json"
	filepath = os.path.expandvars(filepath)
	return filepath

def get_confpath():
	confpath = R"C:\Users\$USERNAME\Documents\PMPro\config.json"
	confpath = os.path.expandvars(confpath)
	return confpath

	# This next portion determines where the users documents folder is located
docPath = R"C:\Users\$USERNAME\Documents"
docPath = os.path.expandvars(docPath) + "\PMPro"

	# Check if the folder already exists, if it doesn't, make a new one
if not os.path.exists(docPath):
	os.mkdir(docPath)

	# Append the name of the json file we wish to use for storage to the end of the filepath
confPath = docPath + "\config.json"
docPath = docPath+ "\PMStorage.json"


	# Check if the file path does not already exist, if it doesn't, the program will execute the create_file method, creating the JSON file in the desired path
	# Does nothing if the file already exists. These two if statements create both the json storage file, and the config file
if not os.path.exists(docPath):
	create_file(docPath)
	import_format(docPath)

if not os.path.exists(confPath):
	create_file(confPath)
	gen_key_file(confPath,Fernet.generate_key())


# Initiates the cipherKey Variable that will be used in the encryption of your passwords
#cipherKey = read_ciph_key(confPath)



# Read the data from the json file
def get_data(filename):
	with open(filename, 'r') as f:
		data = json.load(f)
		return data



# Get password at specified index
def get_password_from_index(filename, index):
	with open(filename, 'r') as f:
		data = json.load(f)
		encryptedPass = bytes(data["passworddata"][index]["encrypted"],'UTF-8')
	return encryptedPass

def get_data_from_index(filename, index):
	with open(filename, 'r') as f:
		data = json.load(f)
	return data["passworddata"][index]




# Function to write data to json file
def write_data(new_data,filename):
	with open(filename, 'r+') as f:
		file_data = json.load(f)
		file_data["passworddata"].append(new_data)
		f.seek(0)
		json.dump(file_data, f, indent = 4)



# Function to write the input to a python dictionary object,
# takes the password and encrypts it using the encrypt_password function,
# decodes it from binary using the decode function,
# and prepares the object for use in writing to a json file
def prepare_input(email,platform,password,cipher_key):
	encrypted = encrypt_password(password,cipher_key).decode('UTF-8')
	data = {
		"email" : email,
		"platform" : platform,
		"encrypted" : encrypted
	}
	return data



# Encrypt the given password using the Cryptography Library
def encrypt_password(password,cipher_key):
	cipher = Fernet(cipher_key)
	passwordBytes = bytes(password,'UTF-8')
	encrypted = cipher.encrypt(passwordBytes)
	return encrypted



# Decrypt the password using the cipher key
def decrypt_password(encrypted_pass,cipher_key):
	cipher = Fernet(cipher_key)
	decryptedPass = cipher.decrypt(encrypted_pass)
	return decryptedPass.decode("utf-8")


# Get number of passwords stored in the json file
def get_password_count(filename):
	with open(filename, 'r') as f:
		data = json.load(f)
		return len(data["passworddata"])

# Delete password at specified index

def delete_password(filename,index):
	with open(filename, 'r') as f:
		data = json.load(f)
	del data['passworddata'][index]
	with open(filename,'w') as w:
		json.dump(data,w,indent=4)
		
# Reset the cipher key at will for security reasons

def reset_cipher_key():
	old_key = read_ciph_key(get_confpath())
	new_key = Fernet.generate_key()
	with open(get_filepath(), 'r') as f:
		data = json.load(f)
	for current_pass in range(get_password_count(get_filepath())):
		old_encrypted = data['passworddata'][current_pass]['encrypted']
		old_encrypted = decrypt_password(bytes(old_encrypted,'UTF-8'),old_key)
		new_encrypted = encrypt_password(old_encrypted,new_key)
		data['passworddata'][current_pass]['encrypted'] = new_encrypted.decode('UTF-8')
	with open(get_filepath(),'w') as w:
		json.dump(data,w,indent=4)
	gen_key_file(get_confpath(),new_key)
	
