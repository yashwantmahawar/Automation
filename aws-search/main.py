import boto3
import sys
import logging
import csv
import os


class style():
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'
    UNDERLINE = '\033[4m'
    RESET = '\033[0m'


# Static Values
supported_resources = "ec2"


# AWS session
def create_aws_session():
    return boto3.Session(profile_name='profilename')


def update_ec2():
    with open("/tmp/ec2.csv", "w") as inventory_write:
        inventory_writer = csv.writer(inventory_write, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        session = create_aws_session()
        ec2client = session.client("ec2")
        ec2 = ec2client.describe_instances()
        instance_list = ec2["Reservations"]

        print("update", len(instance_list))

        for instance in instance_list:
            i = instance["Instances"][0]

            name = "name_not_found"
            private_ip = "no_private_ip"
            sg_name = ""

            if "PrivateIpAddress" in i:
                private_ip = i["PrivateIpAddress"]

            if "Tags" in i:
                for tag in i["Tags"]:
                    if tag["Key"].lower() == "name":
                        name = tag["Value"]

            for sg in i["SecurityGroups"]:
                sg_name = sg_name + sg["GroupName"] + "-" + sg["GroupId"] + " "

            sg_name = sg_name.strip()
            inventory_writer.writerow(["ec2", private_ip, name, sg_name])


def search_ec2(ec2_arguments):
    detailed = False
    if "-d" in ec2_arguments:
        detailed = True
        ec2_arguments.remove("-d")

    if len(ec2_arguments) == 0:
        print("Please add search parameters")
    else:
        print("Searching with given parameters [" + ", ".join(ec2_arguments) + "]")
        with open("/tmp/ec2.csv", "r") as inventory:
            inventory_reader = csv.reader(inventory, delimiter=',', quoting=csv.QUOTE_MINIMAL)

            count = 0
            for line in inventory_reader:
                if all(argument in ",".join(line) for argument in ec2_arguments):
                    count += 1
                    if detailed:
                        print(line)
                    else:
                        print(style.GREEN + line[1] + style.RESET, line[2])
            print("total instance found", count)


def main():
    if len(sys.argv) < 2:
        print("please use search parameter supported parameter are [" + supported_resources + "]")
        exit(1)
    elif sys.argv[1] == "update":
        if len(sys.argv) > 2:
            if sys.argv[2] == "ec2":
                print("Updating ec2")
                update_ec2()
            else:
                print("Not supported yet")
        else:
            print("Updating all supported resources")
    elif sys.argv[1] == "ec2":
        search_ec2(sys.argv[2:])

    else:
        print("execute default")



if __name__ == '__main__':
    main()
