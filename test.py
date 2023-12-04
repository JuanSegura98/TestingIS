import unittest
import os
import app_configuration as ac

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


if __name__ == '__main__':
    unittest.main()