# LAB 01

1. [Cloning Lab Repository](#cloning-Lab-Repository)

## Cloning Lab Repository

 1. Make sure you have *git* installed: `git --version`
	 2. If you get an error message, install *git* using your package manager:
		- Debian/Ubuntu: `sudo apt install git`
		- CentOS/RedHat/Fedora: `sudo yum install git`
 2. Clone repository to your home folder:
	 - `cd ~`
	 - `git clone https://github.com/mijujda/ansible_training.git`
 3. You should have a new folder in your home directory called `ansible_training`
	 - `cd ./ansible_training`
	 - `ls`

## Examining the folder structure
Go to directory `lab01`. The layout should look like this:

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
The top-level key is **all** - this is a group that contains all hosts in the inventory. Each host has `ansible-host` variable defined. This approach is used if host's names cannot be resolved by DNS.

## Examining the Playbook
The playbook file name is `lab01.yml`
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
`ansible-playbook -i hosts_pod1.yml lab01.yml`
<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE2MTY5Nzc1ODcsLTgzNzkwMTM2Myw2Nz
kzNzE1MTgsLTYwNDQzOTMyOSwtMTQxNjMyMTkxNSwtMzU0Mzg5
MDQwLC0yNTAyMTY1MzFdfQ==
-->