import subprocess

cmds = ('echo 1  > /proc/sys/net/ipv4/ip_forward',
        'cat /proc/sys/net/ipv4/ip_forward',
        'iptables -t nat -F',
        'iptables -t nat -A PREROUTING -i eth1 -p tcp --dport 80 -j REDIRECT --to-port 9000',
        'iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE',
        'iptables -A FORWARD -i eth1 -j ACCEPT',
        'service mysqld start',
        'python ../manage.py syncdb',
        )


def start():
    for cmd in cmds:
        try:
            subprocess.check_call(cmd, shell=True)
        except:
            print cmd, '----occor ERROR'
        print cmd, '----is OK'
    print 'all is OK'

if __name__ == '__main__':
    start()
