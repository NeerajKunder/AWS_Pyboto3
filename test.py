from src.ec2.vpc import VPC
from src.ec2.ec2 import EC2
from src.client_locator import EC2Client
from src.client_locator import ROUTE53Client
from src.route53 import ROUTE53
import boto3

route53_client = ROUTE53Client().get_client()
client = boto3.client('route53')
ip = '54.164.221.21'
response = client.change_resource_record_sets(
    HostedZoneId='Z2VSWVRC447OFG',
    ChangeBatch={

        'Changes': [
            {
                'Action': 'CREATE',
                'ResourceRecordSet': {
                    'Name': 'neerajkunder.net',
                    'Type': 'A',
                    'SetIdentifier': 'my_a_record',
                    'GeoLocation': 'NA',
                    'TTL': 60,
                    'ResourceRecords': [
                        {
                            'Value': ip
                        },
                    ],
                }
            },
        ]
    }
)
print(response)



