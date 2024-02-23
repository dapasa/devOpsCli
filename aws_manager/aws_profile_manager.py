from profiles_manager.profiles_manager import Manager
import configparser
import os

class AwsConfig(Manager):
    def __init__(self, profile_name):
        self.profile_name = profile_name
        self.path_credentials = '~/.aws/credentials'
        self.path_config = '~/.aws/config'
        
    def get_access_key(self):
        super().__init__(self.profile_name, self.path_credentials)
        return self.get_param('aws_access_key_id')

    def get_secret_key(self):
        super().__init__(self.profile_name, self.path_credentials)
        return self.get_param('aws_secret_access_key')

    def get_region(self):
        super().__init__(f'profile {self.profile_name}', self.path_config)
        return self.get_param('region')
    
    def get_output(self):
        super().__init__(f'profile {self.profile_name}', self.path_config)
        return self.get_param('output')
    
    def profile_check(self):
        super().__init__(self.profile_name, self.path_credentials)
        return self.profile_checker(['aws_access_key_id', 'aws_secret_access_key'])
