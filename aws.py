from aws_manager.aws_profile_manager import AwsConfig
import json

class Aws:
    def __init__(self, profile):
        self.profile = profile
    
    def check_configuration(self):
        print("Checking AWS Configuration")
        aws = AwsConfig(self.profile)
        
        if aws.profile_check():
            print(f"Profile \"{self.profile}\" is already configured.")
        else:
            print(f"Profile \"{self.profile}\" is missconfigured or not exists.")
            response = input(f"Do you want reconfigure \"{self.profile}\" profile? (y/n): ")
            
            while response not in ['y', 'n']:
                response = input('Please enter "y" or "n": ')
                
            if response == 'y':
                access_key = input(f"Enter the access_key: ")
                secret_key = input(f"Enter the secret_key: ")
                aws.configure_profile(access_key, secret_key)
                if aws.profile_checker():
                    print(f"Profile \"{self.profile}\" configured")
                
            else:
                print('Exiting...')
                exit()

    def add_configuration(self):
        print("Adding AWS Configuration")
        aws = AwsConfig(self.add)
        if aws.profile_checker():
            print(f"Profile \"{self.add}\" is already configured")
            print('Exiting...')
            exit()
        else:
            access_key = input(f"Enter the access_key: ")
            secret_key = input(f"Enter the secret_key: ")
            aws.configure_profile(access_key, secret_key)
            if aws.profile_checker():
                print(f"Profile \"{self.add}\" configured")
    
    def read_configuration(self):
        print(f"Reading configuration for profile: \"{self.profile}\" ")
        aws = AwsConfig(self.profile)
        acces_key = aws.get_access_key()
        secret_key = aws.get_secret_key()
        region = aws.get_region()
        output = aws.get_output()
        configuration = {"acces_key": acces_key, "secret_key": secret_key, "region": region, "output" : output}
        if configuration:
            print(json.dumps(configuration, indent=4))
        else:
            print(f"An error occur reading the aws configuration for the profile: \"{self.profile}\" ")
            print("To know how check your configuration profile run aws -h to see the help")
   