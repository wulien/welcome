import iptc


class iptable(object):

    def __init__(self, table=iptc.Table.FILTER):
        self.table = table

    def ShowIptables(self):
        table = iptc.Table(self.table)
        for chain in table.chains:
            print "===================="
            print "Chain: ", chain.name
            for rule in chain.rules:
                print "Rule", "proto:", rule.protocol, "src:", rule.src, "dst:", \
                    rule.dst, "in:", rule.in_interface, "out:", rule.out_interface
                print "Matches:"
                for match in rule.matches:
                    print match.name
                print "Target:"
                print rule.target.name
            print "===================="

    def is_rule_exist(self, ip, chain_name):
        table = iptc.Table(self.table)
        chain = iptc.Chain(table, chain_name)
        for rule in chain.rules:
            src = rule.src.split('/')[0]
            if src == ip:
                return True
        return False

    def add_rule(self, ip):
        if self.is_rule_exist(ip, 'INPUT'):
            return False
        # table = iptc.Table(iptc.Table.FILTER)
        table = iptc.Table(self.table)
        chain = iptc.Chain(table, "INPUT")
        rule = iptc.Rule()
        rule.src = ip
        # rule.in_interface = "eth0"
        rule.protocol = "all"
        rule.target = iptc.Target(rule, "DROP")
        chain.insert_rule(rule)
        return True

    def delete_rule(self, ip):
        if not self.is_rule_exist(ip, 'INPUT'):
            return False
        table = iptc.Table(self.table)
        chain = iptc.Chain(table, "INPUT")
        rule = iptc.Rule()
        rule.src = ip
        # rule.in_interface = "eth0"
        rule.protocol = "all"
        rule.target = iptc.Target(rule, "DROP")
        try:
            chain.delete_rule(rule)
        except:
            return False
        return True

    def add_nat_rule(self, ip):
        if self.is_rule_exist(ip, 'PREROUTING'):
            return False
        table = iptc.Table(iptc.Table.NAT)
        rule = iptc.Rule()
        rule.src = ip
        rule.protocol = "all"
        rule.in_interface = 'eth1'
        chain = iptc.Chain(table, 'PREROUTING')
        rule.target = iptc.Target(rule, "ACCEPT")
        chain.insert_rule(rule)
        return True
