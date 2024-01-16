import unittest
import os
import json
import app_configuration as ac
import recipes_interface as ri
import users_interface   as ui
import recipes_api   as ra
import inventory_interface as ii


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
    # Unit test: access recipes window
    def test_init_botonrecipespulsado(self):
        # Load the app for the first time
        ventana = ra.CurrentWindow()
        # Click on button recipes
        ventana.recipes_callback()
   
        #Verify the window has changed to recipes 
        self.assertEqual(ventana.name, 'RecipesWindow', "Window should change to 'RecipesWindow'")   

    # Unit test: access recipes database
    def test_get_recipes(self):
        # Load the dummy database
        ri.load_test_database()
        # Retrieve data
        recipes = ri.get_recipes()
        # Check the database connection and the number of entries (initial database contains 2)
        self.assertEqual(len(recipes), 2, "Faulty database")

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
    def test_get_users(self):
        # Load the users database
        ui.load_users_test_database()
        # Retrieve data
        users = ui.get_users()
        #Check the database connection and the number of entries (initial database contains 3)
        self.assertEqual(len(users), 3,"Faulty database")
    
    #Integration test: add/remove users from the database
    def test_add_remove_users(self):
        # Load the dummy database
        ui.load_users_test_database()
        # Add a user
        ui.add_user("Nacho", "Merino Balaguer")
        # Check the database to see if it has been added
        users = ui.get_users()
        self.assertEqual(len(users), 4, "User not added")
        # Remove user
        ui.remove_user("Nacho", "Merino Balaguer")
        # Check the database to see if it has been removed
        users = ui.get_users()
        self.assertEqual(len(users), 3, "User not removed")

    #Integration test: failure to add users with invalid names to the database
    def test_fail_add_remove_users(self):
        # Load the dummy database
        ui.load_users_test_database()
        # Add a user with invalid name or password
        ui.add_user("Esto_no_es_un_nombre_valido_para_un_usuario", "Esto_no_es_una_contraseña_valida_para_un_usuario")
        # Check the database to see if it has been added
        users = ui.get_users()
        self.assertEqual(len(users), 3, "User added")

    #Integration test: failure to remove a user that doesnt exist in the database
    def test_fail_add_remove_users(self):
        # Load the dummy database
        ui.load_users_test_database()
        # Try to remove a user that doesnt exists
        ui.remove_user("Esto_no_es_un_nombre_valido_para_un_usuario", "Esto_no_es_una_contraseña_valida_para_un_usuario")
        # Check the database to see if it has been removed
        users = ui.get_users()
        self.assertEqual(len(users), 3, "User removed")
    
    #Integration test: Open session
    def test_open_session(self):
        #Load the app
        session = ui.User_Session()
        #Open the session
        session.open_session()
        #Verify the state of the session
        self.assertEqual(session.name, 'SesionAbierta', "Session should be open")

    #Integration test: Close session
    def test_close_session(self):
        #Load the app
        session = ui.User_Session()
        #Close the session
        session.close_session()
        #Verify the state of the session
        self.assertEqual(session.name, 'SesionCerrada', "Session should be closed")


class TestInventario(unittest.TestCase):
    # Unit test: access inventory database
    def test_get_inventory(self):
        # Load the users database
        ii.load_inventory_test_database()
        # Retrieve data
        inventory = ii.get_inventory()
        #Check the database connection and the number of entries (initial database contains 3)
        self.assertEqual(len(inventory), 6,"Faulty database")

    # Unit test: inventory edition
    def test_edit_inventory(self):
        # Load the users database
        ii.load_inventory_test_database()
        # Edit the element
        ii.edit_inventory("Huevo", "Huevos", 12, ["Alimento proteico"])
        # Get the current values of the element
        inventory = ii.get_inventory()
        edited_element = next((item for item in inventory if item[1] == "Huevos"), None)
        # Validation
        self.assertIsNotNone(edited_element, "El elemento editado no se encuentra en la base de datos")
        self.assertEqual(edited_element[2], 12, "La cantidad del elemento editado no coincide")
        self.assertIn("Alimento proteico", edited_element[5], "La etiqueta 'Proteína' no se encuentra en las etiquetas del elemento")

    # Unit test: tag elimination
    def test_delete_tags(self):
        # Load the users database
        ii.load_inventory_test_database()
        # Delete the tags
        ii.edit_inventory("Leche", "Leche", 2, [], ["Bebida"])
        # Get the current values of the element
        inventory = ii.get_inventory()
        edited_element = next((item for item in inventory if item[1] == "Leche"), None)
        edited_tags = json.loads(edited_element[5])
        # Validation
        self.assertIsNotNone(edited_element, "Elemento no encontrado en el inventario")
        # Check if 'Bebida' tag was deleted correctly
        self.assertNotIn("Bebida", edited_tags, "La etiqueta 'Bebida' no se eliminó correctamente")
        # Check if 'Lacteo' tag is still present
        self.assertIn("Lacteo", edited_tags, "La etiqueta 'Lacteo' debería estar presente")

    # Unit test: inventory order by modified
    def test_order_inventory(self):
        # Load the users database
        ii.load_inventory_test_database()
        # Order the elements
        ii.order_inventory("modified")
        # Get the current values of the element
        inventory = ii.get_inventory()
        # Validation
        self.assertEqual(inventory[0][1], "Queso", "El primer elemento no está ordenado correctamente por fecha de modificación")
        self.assertEqual(inventory[-1][1], "Leche", "El último elemento no está ordenado correctamente por fecha de modificación")

    # Unit test: inventory filter by name
    def test_filter_inventory(self):
        # Load the users database
        ii.load_inventory_test_database()
        # Filter the elements
        ii.filter_inventory("name", "Tomate")
        # Get the current values of the element
        inventory = ii.get_inventory()
        # Validation
        self.assertTrue(all("Tomate" in item[1] for item in inventory), "No todos los elementos tienen el nombre 'Tomate'")
        self.assertFalse(any("Manzana" in item[1] for item in inventory), "Se encontró un elemento con el nombre 'Manzana'")

    # Integration test
    def test_integration(self):
        # Load the users database
        ii.load_inventory_test_database()
        # Edit the elements
        ii.edit_inventory("Manzana", "Manzana", 2, ["Favorito"])
        ii.edit_inventory("Queso", "Queso", 2, ["Favorito"])
        ii.edit_inventory("Huevo", "Huevos", 12, ["Favorito","Alimento proteico"])
        ii.edit_inventory("Leche", "Leche", 2, ["Favorito"])
        # Order the elements
        ii.order_inventory("name")
        # Filter the elements
        ii.filter_inventory("tags", "Favorito")
        # Get the current values of the element
        inventory = ii.get_inventory()
        edited_element = next((item for item in inventory if item[1] == "Huevos"), None)
        # Validation of one of the edited elements
        self.assertIsNotNone(edited_element, "El elemento editado no se encuentra en la base de datos")
        self.assertEqual(edited_element[2], 12, "La cantidad del elemento editado no coincide")
        self.assertIn("Alimento proteico", edited_element[5], "La etiqueta 'Alimento proteico' no se encuentra en las etiquetas del elemento")
        # Order validation
        self.assertEqual(inventory[0][1], "Huevos", "El primer elemento no está ordenado correctamente por nombre")
        self.assertEqual(inventory[-1][1], "Queso", "El último elemento no está ordenado correctamente por nombre")
        # Filter validation
        self.assertTrue(all("Favorito" in item[5] for item in inventory), "No todos los elementos tienen la etiqueta 'Favorito'")


class TestAPIconection(unittest.TestCase):
    # Unit test: API conection
    def test_init_APIconnection(self):
        #instance of API
        recipes_api = ra.RecipesAPI()
        #API funciona correctamente
        recipes_api.APIAvailable = True
        recipes_api.message= False
        #verify the connection is right 
        self.assertTrue(recipes_api.APIAvailable,'App should conncect API')
        self.assertFalse(recipes_api.message,'App should not show the message')
        
        #Verify the message is visible when there is no connection
        #recipes_api.APIAvailable=False
        #self.assertFalse(recipes_api.APIAvailable,'App should NOT conncect API')
        #En el instante en que se comprueba message debe ser falso todavia
        #self.assertFalse(recipes_api.message,'App should not show the message') 
        #recipes_api.message=True
        #Messaje is shown on scren 
        #ra.ErrorMessage(True)
        #self.assertFalse(recipes_api.APIAvailable,'App should NOT conncect API')
        #self.assertTrue(recipes_api.message,'App should not show the message') 
        #Verify the message is visible when there is no connection

        recipes_api.error()
        self.assertFalse(recipes_api.APIAvailable,'App should NOT conncect API')
        #Message should be in screen
        self.assertTrue(recipes_api.message,'App should not show the message') 


class TestRecipeSearch (unittest.TestCase):
    #Unit test: API conection
    def test_init_APIconnection(self):
        #instance of API
        recipes_api = ra.RecipesAPI()
        #Verify API is available
        recipes_api.APIAvailable = True
        recipes_api.message= False
        #verify the connection is right 
        self.assertTrue(recipes_api.APIAvailable,'App should conncect API')
        self.assertFalse(recipes_api.message,'App should not show the message')

    def test_init_Search_bar(self):
        search = ra.SearchBar()
        search.visibilitykeyboard=False
        #verify keyboard is hidden 
        self.assertFalse(search.visibilitykeyboard,'Keyboard should be hidden')
        #User click on the search bar
        search.searchbar_callback()
        self.assertTrue(search.visibilitykeyboard, 'keyboard should be visible')
        #Get the recipe name form the search bar 
        search.recipesearch()
        self.assertTrue(search.recipe,'The recipe name has been lost')
        self.assertTrue(search.recipefound,'Should NOT  be a recipe with this name')      


if __name__ == '__main__':
    unittest.main()