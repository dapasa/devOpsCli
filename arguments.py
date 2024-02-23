import argparse

def arguments():
    parser = argparse.ArgumentParser(description='cli devops tool')
    subparsers = parser.add_subparsers(dest='command', title='Subcomands')

    aws_parser = subparsers.add_parser('aws', help="Manage Aws profile")
    aws_parser.add_argument('-p','--profile',  help='Check Aws profile')
    aws_parser.add_argument('-a','--add',  help='Add Aws profile')
    aws_parser.add_argument('-r','--read',  help='Read Aws profile')
    aws_parser.add_argument('-r','--read',  help='Read Aws profile')

    github_parser = subparsers.add_parser('github', help="Manage github repository")
    github_parser.add_argument('-d', '--dispatch', help='Dispatch Action Workflow')
    github_parser.add_argument('-as','--secretaws',  help='Create Secrets from aws configuration file')
    github_parser.add_argument('-p','--set-profile',  help='Set github profile to use')
    github_parser.add_argument('-cp','--create-profile',  help='Create github profile')
    github_parser.add_argument('-s','--secret',  help='Create Secret')
    github_parser.add_argument('-S','--secrets',  help='Create Secrets from file')
    
    args = parser.parse_args()
    return args