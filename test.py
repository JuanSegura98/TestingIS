import unittest
import os
import app_configuration as ac
import recipes_interface as ri
import users_interface   as ui

class TestAppConfiguration(unittest.TestCase):
    # Unit test: init_appconfig
    def test_init_appconfig(self):
        # Load the configuration for the first time
        config = ac.init_appconfig()
        # Verify that the notifications are muted by default
        self.assertFalse(config.allow_notifications, "Notifications must be muted by default")
        # Verify that the dark mode is disabled by default
        self.assertFalse(config.dark_mode, "Dark mode must be disabled by default")

    # Unit test: config.security
    def test_security(self):
        # Load the configuration for the first time
        config = ac.init_appconfig()
        # Verify that password is requested when login by default
        self.assertTrue(config.security.require_password, "Password must be requested by default")
        # Verify that the API is used by default
        self.assertTrue(config.security.use_externalAPI, "The connection to the API is done by default")

    # Unit test: save config
    def test_save_config(self):
        # Load the configuration for the first time
        config = ac.init_appconfig()
        # Save default settings
        # In an existing path => should return 0 if the path exists
        self.assertEqual(ac.save_config(config, "cfg/data.conf"), 0, "The configuration could not be saved")
        # Verify that a file has been created
        self.assertTrue(os.path.exists("cfg/data.conf"), "The configuration file was not created")
        # In a non existing path => should return -1 
        self.assertEqual(ac.save_config(config, "nonexistingpath/data.conf"), -1, "The error code is not correct")
        # Double check that the file is not created
        self.assertFalse(os.path.exists("nonexistingpath/data.conf"), "A configuration file was created when it should not")

    # Unit test: load config
    def test_load_config(self):
        # Verify the error code for unexisting config
        if(not os.path.exists("nonexistingpath/data.conf")):
            self.assertEqual(ac.load_config("nonexistingpath/data.conf"), -1, "Tried to load an unexisting file")
        
        # Verify the loading of the configuration file
        if(os.path.exists("cfg/data.conf")):
            config = ac.load_config("cfg/data.conf")
            self.assertTrue(config is not None)
    
    # Integration test:save and load config file
    def test_save_load_config(self):
        # Load the configuration for the first time
        config = ac.init_appconfig()
        # Change some values
        config.allow_notifications = True    
        config.dark_mode = True
        config.security.require_password = False
        
        # Save the configuration
        self.assertEqual(ac.save_config(config, "cfg/data.conf"), 0, "The configuration could not be saved")

        # Load the configuration
        config_loaded = ac.load_config("cfg/data.conf")

        # Verify the values
        self.assertTrue(config_loaded.allow_notifications, "Notifications value not loaded correctly")
        self.assertTrue(config_loaded.dark_mode, "Darkmode value not loaded correctly")
        self.assertFalse(config_loaded.security.require_password, "Require password value not loaded correctly")

class TestRecipes(unittest.TestCase):
    # Unit test: access recipes database
    def get_recipes(self):
        # Load the dummy database
        ri.load_test_database()
        # Retrieve data
        recipes = ri.access_recipes_callback()
        # Check the database connection and the number of entries (initial database contains 2)
        self.assertEquals(len(recipes), 2, "Faulty database")

    # Integration test: add/remove from favourites
    def test_add_remove_favourites_recipes(self):
        # Load the dummy database
        ri.load_test_database()
        # No recipes should be favourite by default
        favourite_recipes = ri.get_favourite_recipes()
        self.assertEqual(len(favourite_recipes), 0, "Dummy database initialised with favourites")

        # Add to favourites
        ri.add_favourites("Macarroni")
        # Update favourites
        favourite_recipes = ri.get_favourite_recipes()
        self.assertEqual(len(favourite_recipes), 1, "Database not updated")

class TestUsers(unittest.TestCase):
    # Unit test: access users database
    def get_users(self):
        # Load the users database
        ui.load_users_test_database()
        # Retrieve data
        users = ui.access_users_callback()
        #Check the database connection and the number of entries (initial database contains 3)
        self.assertEquals(len(users), 3,"Faulty database")
    
    #Integration test: add/remove users from the database
    def test_add_remove_users(self):
        # Load the dummy database
        ui.load_users_test_database()
        # Add a user
        ui.add_user("Nacho", "Merino Balaguer")
        # Check the database to see if it has been added
        users = ui.get_user()
        self.assertEqual(len(users), 4, "User not added")
        # Remove user
        ui.remove_user("Nacho", "Merino Balaguer")
        # Check the database to see if it has been removed
        users = ui.get_user()
        self.assertEqual(len(users), 3, "User not removed")

    #Integration test: failure to add users with invalid names to the database
    def test_fail_add_remove_users(self):
        # Load the dummy database
        ui.load_users_test_database()
        # Add a user with invalid name or password
        ui.add_user("Esto_no_es_un_nombre_valido_para_un_usuario", "Esto_no_es_una_contraseña_valida_para_un_usuario")
        # Check the database to see if it has been added
        users = ui.get_user()
        self.assertEqual(len(users), 3, "User added")

    #Integration test: failure to remove a user that doesnt exist in the database
    def test_fail_add_remove_users(self):
        # Load the dummy database
        ui.load_users_test_database()
        # Try to remove a user that doesnt exists
        ui.remove_user("Esto_no_es_un_nombre_valido_para_un_usuario", "Esto_no_es_una_contraseña_valida_para_un_usuario")
        # Check the database to see if it has been removed
        users = ui.get_user()
        self.assertEqual(len(users), 3, "User removed")
        
if __name__ == '__main__':
    unittest.main()