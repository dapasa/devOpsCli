import configparser
import os

class Manager:
    def __init__(self, profile_name, profile_file_path):
        self.profile_name = profile_name
        self.profile_file_path = profile_file_path
        self.config = configparser.ConfigParser()
        self.config_path = os.path.expanduser(self.profile_file_path)
        self.config.read(self.config_path)

    def profile_exists(self):
        print(self.profile_name)
        print(self.config.has_section(self.profile_name))
        return self.config.has_section(self.profile_name)

    def get_param(self, param):
        return self.config.get(self.profile_name, param)
    
    def configure_profile(self, params = {}):
        if self.profile_exists is False:
            # Create a new profile in the shared credentials file
            self.config[self.profile_name] = params
            with open(self.config_path, 'a') as configfile:
                self.config.write(configfile)
        else:
            # Update the existing profile
            if not self.config.has_section(self.profile_name):
                self.config.add_section(self.profile_name)

            for param in params:
                self.config.set(self.profile_name, param, params[param])

            with open(self.config_path, 'w') as configfile:
                self.config.write(configfile)

    def profile_checker(self, params = []):
        if self.profile_exists():
            try:
                for param in params:
                    self.get_param(param)

                return True
            except configparser.NoOptionError as e:
                print(e)
                return False
        
        return False
    
    def read_configuration(self, params = []):
        if self.profile_checker():
            configuration = {}
            for index, param in enumerate(params):
                configuration[params[index]] = self.get_param(param)
                
            return configuration
        else:
            return False
        
        
if __name__ == '__main__':
    pass