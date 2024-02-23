import configparser
import os
import boto3
from botocore.exceptions import ClientError
from tabulate import tabulate


class AwsResource:
    def __init__(self, profile_name):
        self.profile_name = profile_name
        self.session = boto3.Session(profile_name=self.profile_name)

    def get_elastic_ips(self, resource_name):
        ec2 = self.session.client('ec2')
        filters = [
            {'Name': 'tag:Name', 'Values': [resource_name]}
        ]
        response = ec2.describe_addresses(Filters=filters)
       # print(response)
        table = []
        for addr in response['Addresses']:
            row = [addr.get('PublicIp', ''), addr.get('AllocationId', ''), addr.get('InstanceId', ''), addr.get('AssociationId', ''), addr.get('Domain', '')]
            table.append(row)

        headers = ['Public IP', 'Allocation ID', 'Instance ID', 'Association ID', 'Domain']
        print(tabulate(table, headers=headers))

    def create_elastic_ips(self):
        ec2 = self.session.client('ec2')
        response = ec2.allocate_address(Domain='vpc')
        print(response)

    def destroy_elastic_ips(self, allocationId):
        ec2 = self.session.client('ec2')
        response = ec2.release_address(
            AllocationId= allocationId,
        )
        print(response)
    
    def associatte_eip_to_instance(self, allocationId, instance_id):
        ec2 = self.session.client('ec2')
        response = ec2.associate_address(AllocationId=allocationId, InstanceId=instance_id)
        print(response)

    def get_instances(self, resource_name):
        ec2 = self.session.client('ec2')
        filters=[
            {'Name': 'tag:Name', 'Values': [resource_name]},
        ]
        response = ec2.describe_instances(Filters=filters)
        #print(response)
        instances = []
        for reservation in response['Reservations']:
            for instance in reservation['Instances']:
                row = [instance.get('InstanceId', ''), instance.get('InstanceType', ''), instance.get('PrivateIpAddress', ''), instance.get('PublicIpAddress', ''), instance.get('State', {}).get('Name', '')]
                instances.append(row)

        # display the instances in a table format
        headers = ['Instance ID', 'Instance Type', 'Private IP', 'Public IP', 'Status']
        print(tabulate(instances, headers=headers))

if __name__ == '__main__':  
    grs = AwsResource('personal')
    try:
        grs.associatte_eip_to_instance('eipalloc-027b9411c28a219d3', 'i-0eeb66c05120e301f')
    except ClientError as e:
        print(e)