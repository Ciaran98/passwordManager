import pm
filepath = "../pytestfolder/test.json"

pm.create_file(filepath)

encryptedPassword = pm.get_password_from_index(filepath, 0)

pm.decrypt_password(encryptedPassword)

data = pm.prepare_input("email.com","amazon","hotdogsandbalony")

pm.write_data(data,filepath)