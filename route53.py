
class ROUTE53:
    def __init__(self, client):
        self._client = client
        """ :type : pyboto3.route53"""

    def add_resource_record(self, set_id, cont_code, ip):
        return self._client.change_resource_record_sets(
            HostedZoneId='Z2VSWVRC447OFG',
            ChangeBatch={
                'Comment': 'comment',
                'Changes': [
                    {
                        'Action': 'CREATE',
                        'ResourceRecordSet': {
                            'Name': 'neerajkunder.net',
                            'Type': 'A',
                            'SetIdentifier': set_id,
                            'GeoLocation':
                                {
                                    'ContinentCode': cont_code
                                },
                            'TTL': 60,
                            'ResourceRecords': [{'Value': ip}],
                        }
                    },
                ]
            }
        )
