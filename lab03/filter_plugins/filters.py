#!/usr/bin/python3
from nuaal.Parsers import CiscoIOSParser
from nuaal.utils import int_name_convert
from ccutils.ccparser import BaseConfigParser, ConfigToJson

class FilterModule(object):
    def __init__(self):
        pass

    def filters(self):
        return {
            "ios_parse": self.nuaal_parse,
            "config_to_json": self.config_to_json,
            "mac_per_interface": self.mac_per_interface,
            "get_vty_acl": self.get_vty_acl,
            "get_ntp_servers": self.get_ntp_servers,
            "get_syslog_servers": self.get_syslog_servers

        }

    def nuaal_parse(self, text, command):
        parser = CiscoIOSParser(verbosity=2)
        return parser.autoparse(text=text, command=command)

    def config_to_json(self, config):
        cparser = BaseConfigParser(config=config)
        ctj = ConfigToJson(config=cparser)
        return ctj.data

    def mac_per_interface(self, mac_table):
        interfaces = set()
        result = dict()
        for entry in mac_table:
            int_long = int_name_convert(int_name=entry["ports"], out_type="long")
            interfaces.add(int_long)
            entry["ports"] = int_long
        for interface in interfaces:
            for entry in mac_table:
                if entry["ports"] == interface:
                    if interface not in result.keys():
                        result[interface] = 1
                    else:
                        result[interface] += 1
        return result

    def get_vty_acl(self, config):
        result = dict()
        cparser = BaseConfigParser(config=config)
        for line in cparser.find_objects(regex=r"line vty"):
            children = line.re_search_children(regex=r"access-class .*? in")
            if not len(children):
                continue
            elif len(children) == 1:
                result[line.text] = {"acl": children[0].re_search(regex=r"access-class (.*?) in", group=1), "acl_line": children[0].text.strip()}
        return result

    def get_ntp_servers(self, config):
        result = dict()
        cparser = BaseConfigParser(config=config)
        ntp_regex = r"^ntp server (?:vrf (?P<vrf>\S+) )?(?P<server>\S+)(?:$| (?P<prefer>prefer))"
        for line in cparser.find_objects(regex=ntp_regex):
            result[line.text] = line.re_search(regex=ntp_regex, group="ALL")
            if result[line.text]["prefer"]:
                result[line.text]["prefer"] = True 
            else:
                result[line.text]["prefer"] = False 
        return result

    def get_syslog_servers(self, config):
        result = []
        cparser = BaseConfigParser(config=config)
        syslog_regex = r"^logging host"
        for line in cparser.find_objects(regex=syslog_regex):
            result.append(line.text)
        return result

        
