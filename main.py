import sys
import warnings
import argparse
import requests
from urllib.parse import urlparse

warnings.filterwarnings("ignore")

parser = argparse.ArgumentParser()
parser.add_argument('domains_list_path', type=str)
args = parser.parse_args()

try:
    domains_list = open(args.domains_list_path, 'r')
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

