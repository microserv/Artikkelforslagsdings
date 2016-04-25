import comm

comm_host = "http://127.0.0.1:9001"
index_host = 'http://{}:{}/'.format(comm.get_service_host('index', comm_host), 8001)
spell_host = 'http://{}:{}/'.format(comm.get_service_host('spell', comm_host), 8002)

#spell_host = "http://127.0.0.1:8002/"
#index_host = "http://127.0.0.1:8001/"
