import sys
import warnings
import os
import requests
from urllib.parse import urlparse

warnings.filterwarnings("ignore")

domains_list_path = os.environ.get('DOMAINS_LIST_PATH', './domains.yaml')

try:
    domains_list = open(domains_list_path, 'r')
    domains = domains_list.read().splitlines()
except:
    print("error: cannot open a domains list")
    sys.exit(1)

for domain in domains:
    print(domain)
    try:
        request = requests.get('https://' + domain, verify=False) 
        final_domain = urlparse(request.url).netloc
        print("\t" + final_domain)
    except:
        print()
