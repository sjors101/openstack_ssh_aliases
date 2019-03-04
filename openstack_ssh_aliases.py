#!/usr/bin/python3
# Create ssh aliases based on dynamic infrastructure
# sjors101, 4/3/2019
#
# add to your ~/.bashrc
# if [ -f ~/.os_aliases ]; then
#     . ~/.os_aliases
# fi

import os, json

output_file = "/root/.os_aliases"
ssh_user = "ubuntu"

def get_secrets(filename):
    try:
        pwd = os.path.dirname(os.path.realpath(__file__))
        with open(pwd + "/" + filename, "r") as read_file:
            secrets = json.load(read_file)

        for os_key, os_value in secrets.items():
            os.environ[os_key] = os_value
    except:
        print("Can't open file: " + pwd + "/" + filename)
        exit(1)


def get_instances():
    get_secrets("secrets.json")
    try:
        instances = os.popen('openstack server list --format json').read()
        instances = json.loads(instances)
        return instances
    except:
        print("Can't access OpenStack")
        exit(1)


def write_aliases():
    # clean-up old aliasfile
    if os.path.exists(output_file):
        os.remove(output_file)
    else:
        print("The file does not exist")

    instances = get_instances()
    sshkey = (os.environ["env_sshkey"])

    for instance in instances:
        networks = (instance["Networks"])
        networks = networks.split('=', 1)[-1]
        networks = networks.split(',', 1)[0]
        host = instance["Name"]

        with open(output_file, 'a') as f:
            print("alias ssh_"+host+"='ssh "+ssh_user+"@"+networks+" -i "+sshkey+"'", file=f)


if __name__ == '__main__':
    write_aliases()

