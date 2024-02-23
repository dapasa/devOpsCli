from github import Github
import yaml

#github.enable_console_debug_logging()

class ResourceNotFoundError(Exception):
    pass

class GitHubActionsManager:
    def __init__(self, token, owner, repo_name, branch, workflow_file_name):
        self._g = Github(token)
        self._owner = owner
        self._name = repo_name
        self._repo = self._g.get_repo(f"{self._owner}/{self._name}")
        self._workflow_branch = branch
        self._workflow_id = ''
        self._workflow_file_name = workflow_file_name
        self._workflow_file = self._repo.get_contents(f".github/workflows/{self._workflow_file_name}", self._workflow_branch)
        self._workflow_yaml = yaml.safe_load(self._workflow_file.decoded_content)
        self._workflow_name = self.get_workflow_name()

    def wokrkflow_id(self):
        for workflow in self._repo.get_workflows():
            print(workflow)
            if self._workflow_name == workflow.name:
                return workflow.id
    
    def get_workflow_name(self):
        return self._workflow_yaml.get('name', {})

    def dispatch_workflow(self, inputs=None):

        """
        Dispatches a workflow with optional input parameters.
        """
        if inputs:
            inputs = {key: str(value) for key, value in inputs.items()}

        self._workflow_id = self.wokrkflow_id()

        if not self._workflow_id:
            raise ResourceNotFoundError(f"Workflow with name \"{self._workflow_name}\" not found")
        else:
            return self._repo.get_workflow(self._workflow_id).create_dispatch(self._workflow_branch, inputs)

    def get_input_variables(self, env):
        if env == 'local':
            pass
        elif env == 'remote':
            inputs = self._workflow_yaml.get(True, {}).get('workflow_dispatch', {}).get('inputs',{})
            return_inputs = []
            for input_name, input_config in inputs.items():
                return_inputs.append(input_name)
            
            return return_inputs
        else:
            pass
            
            
if __name__ == '__main__':
    print("")
    # ga = GitHubActionsManager('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', 'trading-inc', 'prototype-v2', 'add-Infra', 'docker-image.yml')
    # try:
    #   print(ga.get_workflow_name())
    # except ResourceNotFoundError as e:
    #   print(e)