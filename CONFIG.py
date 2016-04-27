import comm

comm_host = "http://127.0.0.1:9001"

index_host = 'http://{}:{}/'.format(comm.get_service_ip('index', comm_host), 8001)
spell_host = 'http://{}:{}/'.format(comm.get_service_ip('spell', comm_host), 8002)

#index_host = "http://127.0.0.1:8001/"
#spell_host = "http://127.0.0.1:8002/"

SEARCH_SERVER_PORT = 8000
