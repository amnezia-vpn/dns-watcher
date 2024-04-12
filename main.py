import sys
import warnings
import os
import dns.message
import dns.name
import dns.query
import dns.rdata
import dns.rrset
import requests
import random
from urllib.parse import urlparse
from urllib3.util import connection

warnings.filterwarnings("ignore")

domains_list_path = os.environ.get('DOMAINS_LIST_PATH', './domains.yaml')
dns_server = os.environ.get('DNS_SERVER', '1.1.1.1')
resolution_protocol = os.environ.get('RESOLUTION_PROTOCOL', 'UDP')
timeout = 5

def resolve(host):
    ips = []
    hosts = [host]
    while len(hosts) > 0:
        next_host = hosts.pop()
        try:
            name = dns.name.from_text(next_host)
            query = dns.message.make_query(name, dns.rdatatype.A)
            match resolution_protocol:
                case 'UDP':
                    response = dns.query.udp(query, dns_server, timeout)
                case 'HTTPS':
                    response = dns.query.https(query, dns_server, timeout)
            answers = response.answer
            for answer in answers:
                for record in answer:
                    address = record.to_text()
                    if address[len(address) - 1] != ".":
                        ips.append(record.to_text())
                    else:
                        hosts.append(address)
        except:
            pass
    print("debug: host '{0}' has been resolved via {1} using {2} into the following addresses: {3}".format(host, dns_server, resolution_protocol, ips))
    return ips

create_connection_original = connection.create_connection

def create_connection_patched(address, *args, **kwargs):
    host, port = address
    ips = resolve(host)
    if len(ips) > 0:
        ip = ips[random.randint(0, len(ips) - 1)]
        print("debug: {0} will be used".format(ip))
        return create_connection_original((ip, port), *args, **kwargs)
    else:
        raise Exception()

connection.create_connection = create_connection_patched

session = requests.Session()
session.trust_env = False

try:
    domains_list = open(domains_list_path, 'r')
    domains = domains_list.read().splitlines()
except:
    print("error: cannot open a domains list")
    sys.exit(1)

for domain in domains:
    try:
        response = session.get('http://' + domain, verify=False) 
        final_domain = urlparse(response.url).netloc
    except:
        pass
    print()
