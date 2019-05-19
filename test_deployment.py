from src.ec2.vpc import VPC
from src.ec2.ec2 import EC2
from src.client_locator import EC2Client
from src.client_locator import ROUTE53Client
from src.route53 import ROUTE53


def main():
    # Create a VPC
    ec2_client = EC2Client().get_client()
    vpc = VPC(ec2_client)

    vpc_response = vpc.create_vpc()

    print('VPC created:' + str(vpc_response))

    # Add name tag to VPC
    vpc_name = 'Boto3-VPC'
    vpc_id = vpc_response['Vpc']['VpcId']
    vpc.add_name_tag(vpc_id, vpc_name)

    print('Added ' + vpc_name + ' to ' + vpc_id)

    # Create an IGW
    igw_response = vpc.create_internet_gateway()
    #igw_response_2 = vpc.create_internet_gateway()

    igw_id = igw_response['InternetGateway']['InternetGatewayId']

    vpc.attach_igw_to_vpc(vpc_id, igw_id)

    # Create a public subnet
    public_subnet_response = vpc.create_subnet(vpc_id, '10.0.1.0/24')
    #public_subnet_response_2 = vpc.create_subnet(vpc_id, '10.0.2.0/24')
    public_subnet_id = public_subnet_response['Subnet']['SubnetId']
    #public_subnet_id_2 = public_subnet_response_2['Subnet']['SubnetId']

    print('Subnet created for VPC ' + vpc_id + ':' + str(public_subnet_response))
    #print('Subnet created for VPC ' + vpc_id + ':' + str(public_subnet_response_2))
    # Add name tag to Public Subnet
    vpc.add_name_tag(public_subnet_id, 'Public-Subnet-1')
    #vpc.add_name_tag(public_subnet_id_2, 'Public-Subnet-2')

    # Create a public route table
    public_route_table_response = vpc.create_public_route_table(vpc_id)
    #public_route_table_response_2 = vpc.create_public_route_table(vpc_id)

    rtb_id = public_route_table_response['RouteTable']['RouteTableId']
    #rtb_id_2 = public_route_table_response_2['RouteTable']['RouteTableId']

    # Adding the IGW to public route table
    vpc.create_igw_route_to_public_route_table(rtb_id, igw_id)
    #vpc.create_igw_route_to_public_route_table(rtb_id_2, igw_id)

    # Associate Public Subnet with Route Table
    vpc.associate_subnet_with_route_table(public_subnet_id, rtb_id)
    #vpc.associate_subnet_with_route_table(public_subnet_id_2, rtb_id_2)

    # Allow auto-assign public ip addresses for subnet
    vpc.allow_auto_assign_ip_addresses_for_subnet(public_subnet_id)
    #vpc.allow_auto_assign_ip_addresses_for_subnet(public_subnet_id_2)

    # Create a Private Subnet
    #private_subnet_response = vpc.create_subnet(vpc_id, '10.0.2.0/24')
    #private_subnet_id = private_subnet_response['Subnet']['SubnetId']

    #print('Created private subnet ' + private_subnet_id + ' for VPC ' + vpc_id)

    # Add name tag to private subnet
    #vpc.add_name_tag(private_subnet_id, 'Boto3-Private-Subnet')

    # EC2 Instances
    ec2 = EC2(ec2_client)

    # Create a key pair
    key_pair_name = 'Boto3-KeyPair'
    f = open("C:\\Users\\Neeraj Kunder\\PycharmProjects\\AWS\\boto3keypair.pem", "w")
    key_pair_response = ec2.create_key_pair(key_pair_name)
    boto3keypair = str(key_pair_response['KeyMaterial'])
    f.write(str(boto3keypair))

    print('Created Key Pair with name ' + key_pair_name + ':' + str(key_pair_response))

    # Create a Security Group
    public_security_group_name = 'Boto3-Public-SG'
    public_security_group_description = 'Public Security Group for Public Subnet Internet Access'
    public_security_group_response = ec2.create_security_group(public_security_group_name, public_security_group_description, vpc_id)

    public_security_group_id = public_security_group_response['GroupId']

    # Add Public Access to Security Group
    ec2.add_inbound_rule_to_sg(public_security_group_id)

    print('Added public access rule to Security Group ' + public_security_group_name)

    user_data = """#!/bin/bash
                yum update -y
                yum install -y httpd 
                service httpd start
                chkconfig httpd on
                echo "<html><body><h1>
                Hello! <b>This is my USA Web Server</b> created using Python!
                </h1></body></html>" > /var/www/html/index.html"""

    ami_id = 'ami-0de53d8956e8dcf80' #us-east-1

    # Launch a public EC2 Instance
    ec2.launch_ec2_instance(ami_id, key_pair_name, 1, 1, public_security_group_id, public_subnet_id, user_data)
    #ec2.launch_ec2_instance(ami_id, key_pair_name, 1, 1, public_security_group_id, public_subnet_id_2, user_data_2)
    print('Launching Public EC2 Instance using AMI ' + ami_id)
    input("Press Enter to Continue")


def fetch_ip():
    ec2_client = EC2Client().get_client()
    ec2 = EC2(ec2_client)
    ec2_response = ec2.describe_ec2_instances()
    ip_addr = ec2_response['Reservations'][0]['Instances'][0]['PublicIpAddress']
    print(ip_addr)
    return ip_addr


def create_resource_records():
    ip_addr = fetch_ip()
    route53_client = ROUTE53Client().get_client()
    r53 = ROUTE53(route53_client)
    r53_response = r53.add_resource_record(
        ip=ip_addr,
        set_id='USA',
        cont_code='NA',
    )
    print(str(r53_response))

    # Adding another Security Group for Private EC2 Instance
    #private_security_group_name = 'Boto3-Private-SG'
    #private_security_group_description = 'Private Security Group for Private Subnet'
    #private_security_group_response = ec2.create_security_group(private_security_group_name, private_security_group_description, vpc_id)

    #private_security_group_id = private_security_group_response['GroupId']

    # Add rule to private security group
    #ec2.add_inbound_rule_to_sg(private_security_group_id)

    # Launch a private EC2 Instance
    #ec2.launch_ec2_instance(ami_id, key_pair_name, 1, 1, private_security_group_id, private_subnet_id, """""")

    #print('Launching Private EC2 Instance using AMI' + ami_id)


if __name__ == '__main__':
    #main()
    fetch_ip()
    create_resource_records()
    # modify_instance()
    # stop_instance()
    # start_instance()
    #terminate_instance()

