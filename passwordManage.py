import pm
filepath = "../pytestfolder/testalt.json"


pm.read_data(filepath)

pm.get_password(filepath, 2)

data = pm.return_data_input("howdily","doodily","hash")

#pm.write_data(data,filepath)