# LAB 01
 
 - [Cloning Lab Repository](#cloning-lab-repository)

## Cloning Lab Repository

 1. Make sure you have *git* installed: `git --version`
	 If you get an error message, install *git* using your package manager:
		- Debian/Ubuntu: `sudo apt install git`
		- CentOS/RedHat/Fedora: `sudo yum install git`
 2. Clone repository to your home folder:
	 - `cd ~`
	 - `git clone https://github.com/mihudec/ansible_training.git`
 3. You should have a new folder in your home directory called `ansible_training`
	 - `cd ./ansible_training`
	 - `ls`

## Examining the folder structure
Go to the directory `lab01`. The layout should look like this:

```
lab01/
  hosts_pod1.yml			# Inventory file for POD 1
  lab01.yml					# Playbook file
  ansible.cfg				# Ansible config file
  group_vars/				# Directory for group variables
    all.yml					# Variables for group all
```

## Examine inventory file
Look at the contents of inventory file for your POD number:
`cat hosts_pod1.yml`
```yaml
---
all:
  hosts: 
    HQ-RT-01:
      ansible_host: 10.8.8.121
    HQ-RT-02:
      ansible_host: 10.8.8.122
    BR1-RT-01:
      ansible_host: 10.8.8.123
    BR1-DIST-01:
      ansible_host: 10.8.8.125
    BR1-ACC-01:
      ansible_host: 10.8.8.127
    BR1-ACC-02:
      ansible_host: 10.8.8.128
    BR2-RT-01:
      ansible_host: 10.8.8.124
    BR2-DIST-01:
      ansible_host: 10.8.8.126
    BR2-ACC-01:
      ansible_host: 10.8.8.129
    BR2-ACC-02:
      ansible_host: 10.8.8.130
    
```
The top-level key is **all** - this is a group that contains all hosts in the inventory. Each host has the `ansible-host` variable defined. This variable tells Ansible where to connect to reach a particular host. If the host does not have this variable defined, Ansible tries to resolve the hostname (`inventory_hostname`) using DNS.

You can define as many variables you like in the inventory file itself, however, this usually leads to very large and hard-to-read files. Generally speaking, this approach does not scale well. The preferred way of storing variables is by using **host_vars** and **group_vars** which we will cover in the next lab.

## Examine group_vars folder
Folder `group_vars` contains YAML files with variables relevant to specific groups. In this case, the folder contains just one file, `all.yml`:
```yaml
---
### Connection Setup
ansible_connection: network_cli
ansible_network_os: ios
ansible_user: admin
ansible_password: cisco

### Common Variables
domain_name: ansible.lab
```
The first section sets *special* or *built-in* Ansible variables, which determine basic parameters about the connection. The `ansible-connection` variable tells Ansible, which *connection plugin* it should use for hosts in the group *all*. In this case, the `network-cli` is used, which uses an SSH connection in the background. Alternatively, some devices (eg. Cisco Nexus switches) also support HTTP API, which you can use by specifying `ansible_connection: httpapi`
Next, you need to specify the operating system of your network device, in this case, we are using `ios`. This allows Ansible to correctly initialize the connection and interpret its output. Check out other supported OSes and their required parameters in [Ansible for Network Automation Documentation](https://docs.ansible.com/ansible/latest/network/index.html).

> Note: Formely when using Ansible for managing network devices, the network-related modules used `ansible_connection: local`. In newer versions of Ansible, the `network-cli` is the preferred way, as it directly supports some common task for most networking operating systems. Read more about the plugin in the [Network-CLI Connection Plugin Documentation](https://docs.ansible.com/ansible/latest/plugins/connection/network_cli.html).


## Examining the Playbook

### Task, Play, Playbook?

**Task**
A *task* represents a single action that will be performed on a particular host. Task usually leverages a certain *module*, which is basically a script that knows how to perform some action. What the task does, is that it *feeds* certain information into the module - a task usually provides some parameters for the module. 

An example of a task:
```yml
- name: This is an Example Task		# Descriptive name of the task
  example_module:					# This is the name of the module that will be executed
    parameter1: "foo"				# This is parameter1 with value "foo"
    parameter2: "{{ bar }}"			# This is parameter2 whose value is variable bar
```
You can find all the supported parameter in the module's documentation. Be careful as some parameters are required, some may be optional and some may require another parameter to be set.

**Play**
A *play* defines the general logic of what you are trying to accomplish. A play is where multiple tasks are put together in a sequence - or a list. Apart from listing all the tasks it also has to provide a set of hosts or host groups, against which the tasks will be executed.

**Playbook**
Playbooks are files that contain one or multiple *plays*. This means that playbook contains *list* of individual plays, where each play has to be given at minimum the set of **hosts** to run the play against and **tasks** which specify what actions to take. Most of the time the play is given some descriptive **name** which you will see in the output when running the play.

### Playbook for Lab 01
The playbook file name for this lab is `lab01.yml` 
```yml
---
- name: Play LAB01
  hosts: all
  gather_facts: False

  tasks:
    - name: DEBUG Inventory Hostname and IP
      debug:
        msg: "Hostname: {{ inventory_hostname }} IP: {{ ansible_host }}"

    - name: Get Hostname from Remote Host
      ios_command:
        commands: "show running-config | include hostname"
      register: output

    - name: DEBUG Remote Hostname
      debug:
        msg: "{{ output.stdout[0] }}"

    - name: Check and set Hostname and Domain
      ios_system:
        hostname: "{{ inventory_hostname }}"
        domain_name: "{{ domain_name }}"
```

## Running the Playbook
Playbooks are executed by using the command `ansible-playbook`. To see all the supported parameters, run `ansible-playbook --help`. You have to provide at least the name of the playbook file. Usually, you will also want to provide a path to the inventory file/folder by using `-i` or `--inventory` option. If you don't, Ansible will look in the default location (usually */etc/ansible/hosts*).

Run the `lab01.yml` playbook and provide inventory file specific for your POD. 
Replace the X with your POD number: `ansible-playbook -i hosts_podX.yml lab01.yml`
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTU4OTU1MTI2NCw2MjgwNTgwNjgsLTE2MT
Y5Nzc1ODcsLTgzNzkwMTM2Myw2NzkzNzE1MTgsLTYwNDQzOTMy
OSwtMTQxNjMyMTkxNSwtMzU0Mzg5MDQwLC0yNTAyMTY1MzFdfQ
==
-->