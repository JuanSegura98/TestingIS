import pickle
import os

class Security:
  def __init__(self):
    self.require_password = True
    self.use_externalAPI = True

class AppConfiguration:
  def __init__(self):
    self.security = Security()
    self.allow_notifications = False
    self.dark_mode = False

def save_config(app_configuration, path):
    # Verify path
    directory = os.path.dirname(path)
    if not os.path.exists(directory):
       return -1
    # Serialize the object to a binary string
    serialized_data = pickle.dumps(app_configuration)
    # Save the serialized data to a file
    with open(path, "wb") as file:
        file.write(serialized_data)
    return 0

def load_config(path):
    # Verify the existance of load file
    if not os.path.exists(path):
       return -1
    # Read the serialized data from the file
    with open(path, "rb") as file:
        loaded_data = file.read()
        return pickle.loads(loaded_data)

def init_appconfig():
  app_config = AppConfiguration()
  return app_config
