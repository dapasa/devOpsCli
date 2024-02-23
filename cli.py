from arguments import arguments
from aws import Aws
from git_hub import GitHub
args = arguments()
#print(args)

def run():     
    if args.command == 'aws':        
        if args.profile:
            aws = Aws(args.profile)
            aws.check_configuration()
            
        if args.add:
            aws = Aws(args.add)
            aws.add_configuration()
        
        if args.read:
            aws = Aws(args.read)
            aws.read_configuration()
            
    if args.command == 'github':
        if args.secret:
            github = GitHub()
            github.add_secret(args.secret)
        
        if args.secrets:
            github = GitHub()
            github.add_secrets()
        
        if args.secretaws:
            github = GitHub(args.secretaws)
            github.aws_secrets_to_secrets_file()
        
        if args.dispatch:
            github = GitHub(None, args.dispatch , None)
            github.dispatch()
        
        if args.create_profile:
            github = GitHub(None, None, args.create_profile)
            github.create_profile()
        
        if args.set_profile:
            github = GitHub(None, None, args.create_profile)
            github.set_profile()
            

if __name__ == "__main__":
    run()