
# LAB 00

1. [Install and configure Ansible](#install-and-configure-ansible)
2. [Ansible configuration files](#ansible-configuration-files)

## Install Ansible
There are many ways to install ansible on Linux-like OSes. Most distributions have Ansible in there package repositories, however, these are sometimes outdated. The easiest way to install _latest_ version of Ansible is by using Python Package Manager - **pip**. 

    pip3 install ansible

If everything goes well, you should be able to run the following command:

    ansible --version

```
ansible 2.8.5
  config file = /etc/ansible/ansible.cfg
  configured module search path = ['/home/training/.ansible/plugins/modules', '/usr/share/ansible/plugins/modules']
  ansible python module location = /usr/local/lib/python3.7/dist-packages/ansible
  executable location = /usr/local/bin/ansible
  python version = 3.7.3 (default, Apr  3 2019, 05:39:12) [GCC 8.3.0]
    
```
From the output you can tell that we're running Ansible version 2.8.5, using Python 3.7.3 and the default configuration file is located at `/etc/ansible/ansible.cfg`

> If you want, you can clone the Ansible repository directly from [GitHub](https://github.com/ansible/ansible) to get the truly latest version. For more information about Ansible installation, check out [the docs](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html).

## Ansible configuration files
By default, Ansible looks for configuration parameters in following files:

 - `/etc/ansible/ansible.cfg`
 - `~/.ansible.cfg`
 - `./ansible.cfg`

Some parameters you'll probably want to change are:
 - `host_key_checking` - If this is set to True (default), Ansible will perform strict SSH keys checking, meaning it will not connect to those hosts, which do not have their key in `~/.ssh/known_hosts`. In production this is probably a good thing, however in a lab environment, change this to **False** (and uncomment the line).
 - `host_key_auto_add` - Alternative to `host_key_checking`, except that this option will automatically add new SSH keys to `known_hosts`. The default value is False. This might be useful when you deploy a new Ansible machine and you need to add SSH keys for all hosts in your inventory.
 - `forks` - Number of concurrent threads (how many hosts can run in parallel). This can be changed when running a playbook by adding parameter `-f` or `--forks`.

<!--stackedit_data:
eyJoaXN0b3J5IjpbLTE4MDcxOTUwMjRdfQ==
-->