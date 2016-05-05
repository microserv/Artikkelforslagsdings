import comm

#Communicationhost, can be used to retrieve IP-addresses og other hosts (services)
comm_host = "http://127.0.0.1:9001"

#Example usage of the communication service. Use local-config.py for such setups if necessary ...
#index_host = 'http://{}:{}/'.format(comm.get_service_ip('indexer', comm_host), 8001)
#spell_host = 'http://{}:{}/'.format(comm.get_service_ip('spell-check', comm_host), 8002)

#... the default is to run all services on the same host
index_host = "http://127.0.0.1:8001/"
spell_host = "http://127.0.0.1:8002/"

SEARCH_SERVER_PORT = 8000

try:
    from local_config import *
except ImportError:
    print('Local settings file not found.')
