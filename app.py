import os
from connection import estf
from elasticsearch_dsl import Search
from elasticsearch_dsl.query import MultiMatch
from flask import (
    Flask,
    render_template,
    request,
)
import requests
import json


app = Flask(__name__)
app.secret_key = os.urandom(16)

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/search")
def search():
    query = request.args.get("query")
    s = Search(using=estf, index="our-index")
    m = MultiMatch(query=query, fields=["title", "extract"])
    s = s.query(m)
    results = s.execute()
    data = {
    	"search_request": {
        '_source':['title', 'extract'],
        "query": {"match" : { "extract": query }},
  },   
        "query_hint": "airport",
        "field_mapping": {
         "title": ["_source.title"],
        "content": ["_source.text_entry"]
  },
         "algorithm": "Bisecting K-Means"
 } 
    response = requests.post('http://localhost:9200/our-index/_search_with_clusters?pretty', data=json.dumps(data), headers= {
    'Content-Type': 'application/json'
  })

    result =response.text
    d = json.loads(result)
    cluster_labels = [cluster['phrases'][:2] for cluster in d["clusters"]]
    
    return render_template(
        "search.html",
        results=results,
        query=query,
        cluster_labels=cluster_labels
    )

# @app.route('/search/<int:page_num>')
# def search(page_num):
#     searches = Search.query.paginate(per_page=5, page = page_num, error_out=True)

#     return render_template('search.html', searches = searches)


if __name__ == "__main__":
    app.run(debug=True)
