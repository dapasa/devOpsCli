from profiles_manager.profiles_manager import Manager
import configparser
import os


class GithubConfigManager(Manager):
    def __init__(self, profile_name = None):
        self.profile_name = profile_name
        super().__init__(self.profile_name, '~/.github/credentials')
        self.github_token = ''
        self.github_owner = ''
        self.github_repo_name = ''
        self.github_branch = ''

    def read_profile(self):
        config = self.read_configuration(['token', 'repo_owner', 'repo_name', 'branch'])
        print(config)
        if config:
            self.github_token = config['token']
            self.github_owner = config['repo_owner']
            self.github_repo_name = config['repo_name']
            self.github_branch = config['branch']
        
    def _set_profile_name_env(self):
        os.environ['github_profile_name'] = self.profile_name
    
    def _get_profile_name_env(self):
        if os.environ.get('github_profile_name'):
            github_profile_name = os.environ.get('github_profile_name')
            self.profile_name = github_profile_name
            return github_profile_name 
        else:
            print('Profile name is not set.')
            profile_name=input("Enter your profile name: ")
            self.profile_name = profile_name
            self._set_profile_name()
            print(f'Profile name was set.')
            
if __name__ == '__main__':
    ga = GithubConfigManager('personal')
    dir(ga)