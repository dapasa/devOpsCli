from github_manager.github_actions_manager import GitHubActionsManager
from github_manager.github_repo_manager import GitHubRepoManager
from github_manager.github_profile_manager import GithubConfigManager
from aws_manager.aws_profile_manager import AwsConfig
import shutil
import os

class GitHub:
    def __init__(self, aws_profile = None, workflow_file_name = None, profile = None):
        self.aws_profile = aws_profile
        self.github_workflow_file_name = workflow_file_name
        self.github_profile = profile
        self.github_config_manager = ''
        self.secrets_file = ''
        
    def add_secret(self, secret):
        print("Adding Github Secret")
        if self.github_profile != None:
            self.github_config_manager = GithubConfigManager(self.github_profile)
        else:
            self.github_config_manager = GithubConfigManager(os.environ.get('github_profile_name'))
            
        self.github_config_manager.read_profile()
        repo = GitHubRepoManager(self.github_config_manager.github_token, self.github_config_manager.github_owner, self.github_config_manager.github_repo_name)
        secret_name = secret
        value = input(f"Enter the secret value: ")
        print(f"Secret: \"{secret_name}\" value: \"{value}\"")
        repo.create_secrets(secret_name, value)
        next = True
        while next:
            response = input(f"Do you want add another secret? (y/n): ")
            while response not in ['y', 'n']:
                response = input('Please enter "y" or "n": ')
            if response == 'n':
                next = False
            else:
                secret_name = input(f"Enter the secret name: ")
                value = input(f"Enter the secret value: ")
                print(f"Secret: \"{secret_name}\" value: \"{value}\"")
                repo.create_secrets(secret_name, value)
    
    def add_secrets(self, secret_file):
        self.secrets_file = secret_file
        print("Adding Github Secrets from file")
        if self.github_profile != None:
            self.github_config_manager = GithubConfigManager(self.github_profile)
        else:
            self.github_config_manager = GithubConfigManager(os.environ.get('github_profile_name'))
        self.github_config_manager.read_profile()
        repo = GitHubRepoManager(self.github_config_manager.github_token, self.github_config_manager.github_owner, self.github_config_manager.github_repo_name)
        with open(self.secrets_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    name, value = line.split('=', 1)
                    print(repo.create_secrets(name.strip(), value.strip()))
    
    def aws_secrets_to_secrets_file(self):
        print("Reading and sending AWS secrets to secrets file")
        aws = AwsConfig(self.aws_profile)
        configuration = aws.read_configuration()
        print(configuration)
        if configuration:
            found_line = False
            for name in configuration:
                with open('secrets', 'r') as file:
                    lines = file.readlines()
                    for i, line in enumerate(lines):
                        line.strip()
                        print(line)
                        print(line.startswith(f'{name} =', 0))
                        if line.startswith(f'{name} ='):
                            lines[i] = f'{name} = {configuration[name]}\n'
                            found_line = True
                            break
                    
                    if not found_line:
                        lines.append(f'{name} = {configuration[name]}\n')
                    else:
                        print(f'Secret \"{name}\" exist in the secrets file')
                        response = input(f"Do you want add replace it? (y/n): ")
                        while response not in ['y', 'n']:
                            response = input('Please enter "y" or "n": ')

                        if response == 'n':
                            continue    
            
                with open('secrets', 'w') as f:
                    f.writelines(lines)
    
    def dispatch(self):
        print('Checking Input Variables for Workflow')
        if self.github_profile != None:
            self.github_config_manager = GithubConfigManager(self.github_profile)
        else:
            self.github_config_manager = GithubConfigManager(os.environ.get('github_profile_name'))
        self.github_config_manager.read_profile()

        actions = GitHubActionsManager(self.github_config_manager.github_token, self.github_config_manager.github_owner, self.github_config_manager.github_repo_name, self.github_config_manager.github_branch, self.github_workflow_file_name)
        if os.path.exists('inputs'):
            print('Inputs already exists. Showing...')
            with open('inputs', 'r') as f:
                for line in f:
                    print(line.strip())
            response = input(f"Do you want to continue with this configuration?: (y/n)")
            while response not in ['y', 'n']:
                response = input('Please enter "y" or "n": ')
            if response == 'n':
                print('Exiting...')
                exit()
        else:
            print('Not have any input configured. We need to configure the new ones.')
            inputs=actions.get_input_variables('remote')
            new_lines=''
            for inp in inputs:
                inp_value = input(f"Enter value for input {inp}:")
                new_lines += f"{inp} = {inp_value}\n"
            
            with open('inputs', 'w') as f:
                f.writelines(new_lines)

        with open('inputs', 'r') as f:
            lines = f.readlines()
            inputs = {}
            for line in lines:
                name, value = line.strip().split(" = ")
                inputs[name] = value

        print(actions.dispatch_workflow(inputs))

    def create_profile(self):
        print(self.github_profile)
        self.github_config_manager = GithubConfigManager(self.github_profile)
        if not self.github_config_manager.profile_exists():
            response = input(f'Profile {self.github_profile} not exist. Do you want to create it? ')
            while response not in ['y', 'n']:
                response = input('Please enter "y" or "n": ')
            if response == 'n':
                exit()
                
            src_file = './github_manager/.profile'
            dst_dir = os.path.expanduser('~/.github') #github_config_manager.profile_file_path
            
            os.makedirs(dst_dir, exist_ok=True)
            shutil.copy(src_file, os.path.join(dst_dir, 'credentials'))
            
            token = input(f"Enter your GitHub token: ")
            repo_owner = input(f"Enter repository owner: ")
            repo_name = input(f"Enter repository name: ")
            branch = input(f"Enter repository name: ")
            params = {'token': token, 'repo_owner': repo_owner, 'repo_name': repo_name, 'branch': branch}
            
            try:
                self.github_config_manager.configure_profile(params)
                self.github_config_manager._set_profile_name_env()
            except Exception as e:
                print(e)
      
    def set_profile(self):
        pass
 