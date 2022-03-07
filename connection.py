from elasticsearch import Elasticsearch

estf = Elasticsearch(
        hosts= ["http://localhost:9200"]
        , headers={
                'Accept': 'application/json',
                'Content-Type': 'application/json'}
        )


