import unittest
import reporter
import json
import os

class TestReporter(unittest.TestCase):

    def get_config(self):
        """Get a bearer key for the purpose of testing from the JSON config file in volatile/tests_config.json"""
        config = {}
        path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'volatile', 'tests_config.json')

        if not os.path.exists(path):
            raise IOError(f'The test config JSON file is not in {path}.')

        with open(path, 'r') as config_json_stream:
            config = json.load(config_json_stream)
        return config

    def test_get_contexts(self):
        """Test the ability to list all contexts."""
        config = self.get_config()
        self.assertTrue('bearer_key' in config, msg='There was no bearer_key fetched from the config JSON')
        
        contexts = reporter.get_contexts(config['bearer_key'])

        self.assertTrue(len(contexts) > 0)

    def test_get_known_existing_context(self):
        """Get a context we know exists."""
        config = self.get_config()
        self.assertTrue('bearer_key' in config, msg='There was no bearer_key fetched from the config JSON')
        self.assertTrue('known_existing_context' in config, msg='There was no known_existing_context in the config JSON')

        self.assertTrue(reporter.get_context(config['known_existing_context'], config['bearer_key']))

    # def test_create_context(self):
    #     """Create a context."""
    #     config = self.get_config()
    #     self.assertTrue('bearer_key' in config, msg='There was no bearer_key fetched from the config JSON')

    #     reporter.create_context('tests.py', config['bearer_key'])

    def test_set_status(self):
        """Set a status to a given test payload."""
        config = self.get_config()
        self.assertTrue('bearer_key' in config, msg='There was no bearer_key fetched from the config JSON')

        reporter.set_status('harald_le_success', 'pytest', config['bearer_key'])

if __name__ == '__main__':
    unittest.main()
