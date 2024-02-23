from github import Github
import json

class GitHubRepoManager:
    def __init__(self, token, owner, name):
        self._g = Github(token)
        self._owner = owner
        self._name = name
        self._repo = self._g.get_repo(f"{self._owner}/{self._name}")
    
    def create_secrets(self, secret_name, value):
        return self._repo.create_secret(secret_name, value)

    def delete_secrets(self, secret_name):
        return self._repo.delete_secret(secret_name)