<!-- @format -->

# Elasticsearch index creation

- Run the following code into [Kibana](https://www.elastic.co/kibana)

```
PUT test-index-768
{
  "settings": {
    "number_of_replicas": 0,
    "number_of_shards": 3
  },
  "mappings": {
    "dynamic": "false",
    "_source": {
      "excludes": [
        "embedding"
      ]
    },
    "properties": {
      "embedding": {
        "type": "dense_vector",
        "dims": 768,
        "index": true,
        "similarity": "dot_product"
      }
    }
  }
}
```
