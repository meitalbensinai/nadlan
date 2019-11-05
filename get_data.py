import requests
from urllib.parse import urlencode, quote_plus
import json
import pandas as pd

NEIGHBORHOOD_LITERAL = 'שכונת'

CITIES_AND_NEIGHBORHOODS = {'רעננה': ['נווה זמר']}

def get_data_from_site(city, neighborhood):
    query = urlencode({"query": " ". join([city, NEIGHBORHOOD_LITERAL,neighborhood])}, quote_via=quote_plus)
    get_data_by_query_url = 'https://www.nadlan.gov.il/Nadlan.REST/Main/GetDataByQuery?{QUERY}'.format(QUERY=query)
    response = requests.get(get_data_by_query_url)
    query_data = json.loads(response.text)
    query_results = {'IsLastPage': False}
    all_results = []
    while True:
        if query_results['IsLastPage']:
            break
        query_data['PageNo'] = query_data['PageNo'] + 1
        get_assest_and_deals_url = 'https://www.nadlan.gov.il/Nadlan.REST/Main/GetAssestAndDeals'
        response = requests.post(get_assest_and_deals_url,
                                 data=json.dumps(query_data, ensure_ascii=False).replace("False", "false").replace("True", "true").replace("None", "null").encode('utf-8'),
                                 headers={'Content-type': 'application/json;charset=UTF-8'})
        query_results = json.loads(response.text)
        all_results += query_results['AllResults']
    data_frame = pd.DataFrame(all_results)
    data_frame.to_csv(city + "-" + neighborhood + ".csv")
    

if __name__ == '__main__':
    for city in CITIES_AND_NEIGHBORHOODS.keys():
        for neighborhood in CITIES_AND_NEIGHBORHOODS[city]:
            get_data_from_site(city, neighborhood)
