from django.http import JsonResponse
from elasticsearch import Elasticsearch, ElasticsearchException, TransportError
from django_logging import log
from django.conf import settings


es = Elasticsearch([settings.ELASTIC_HOST],
    port=9200,)

def getfuzzy(request, search_field, es_word):
 totalhits =0
 search_value_list =[]
 map={}
 try:
        # fuzzy search
        result = es.search(index="logstash-*", body={"query": {"fuzzy": {search_field:{"value":es_word,"fuzziness" : 5}}}})
        # regexp search
        #result = es.search(index="logstash-*", body={"query": {"regexp": {search_field:{"value":es_word+".*"}}}})
        for hit in result['hits']['hits']:
             map.setdefault("record",[]).append(hit["_source"][search_field])
             search_value_list.append(hit["_source"][search_field])
        return JsonResponse(map)
 except TransportError:
    log.error("Cannot connect to elastic")
    return JsonResponse({'totalHits': 0})
 except ElasticsearchException as e:
    log.error("elastic exception "+ str(e))
    return JsonResponse({'totalHits': 0})
 except Exception:
    log.error("General Exception")
    return JsonResponse({'totalHits': 0})