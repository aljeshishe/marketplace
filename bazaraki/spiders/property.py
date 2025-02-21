import email
import json
import re
import scrapy
from tqdm import tqdm
from scrapy.http import Response
from bs4 import BeautifulSoup
import re


HIGH_PRIO = 10

def getall(response, selector, replace=None):
    result = response.css(selector).getall()
    if result is None:
        return None

    result = [item.strip() for item in result]
    if replace:
        pattern = '|'.join(map(re.escape, replace.split()))
        result = [re.sub(pattern, "", item) for item in result]
        result = [item.strip() for item in result]

    return result

def get(response, selector, type=str, replace=None):
    result = response.css(selector).get()
    if result is None:
        return None
    
    result = result.strip()
    
    if replace:
        pattern = '|'.join(map(re.escape, replace.split()))
        result = re.sub(pattern, "", result)
        result = result.strip()

    result = type(result)
    return result 

html_headers_str = """Host: www.facebook.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:135.0) Gecko/20100101 Firefox/135.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: identity
Alt-Used: www.facebook.com
Connection: keep-alive
Cookie: datr=JIqnZow5qnkGa9qpV94F4WyT; c_user=100001857951275; fr=1k6n2UUsdT7LGLUBR.AWXtjLOA489ju3USapvSRJr8L9mEDzvwYyzP7g.BnH5Bu..AAA.0.0.Bnpiw8.AWVt8fzPiuE; sb=ToqnZlhdH_aVuvzChhoREzZY; xs=38%3AJQhc_SwL3f2AbA%3A2%3A1722255951%3A-1%3A14496%3A%3AAcUQ6I51ZQZLaT1xG0SMWZ_LenaGUcJbyZwklCn6kWP6; ps_l=1; ps_n=1; wd=703x1013; usida=eyJ2ZXIiOjEsImlkIjoiQXNramEyYzFjYjV0M28iLCJ0aW1lIjoxNzI3NTQ1NjQ0fQ%3D%3D; presence=C%7B%22t3%22%3A%5B%7B%22o%22%3A0%2C%22i%22%3A%22u.24052952154294604%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8198290400276938%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8479708578816243%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8647792911909990%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22sc.7250117433385889937%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.27390201170593783%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8280212772075879%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8643388819107455%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8536117643093004%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.27498303063116923%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8574592289283638%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.7970065553094064%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8481826755233958%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22sc.7250117433383252638%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22sc.8179238638870654%22%7D%5D%2C%22utc3%22%3A1740136218203%2C%22v%22%3A1%7D
Upgrade-Insecure-Requests: 1
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: none
Sec-Fetch-User: ?1
Priority: u=0, i
Pragma: no-cache
Cache-Control: no-cache"""

html_headers = dict(email.message_from_string(html_headers_str))
del html_headers["Accept-Encoding"]

json_headers_str = """Host: www.facebook.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:135.0) Gecko/20100101 Firefox/135.0
Accept: */*
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate, br, zstd
Content-Type: application/x-www-form-urlencoded
X-FB-Friendly-Name: CometMarketplaceSearchContentPaginationQuery
X-FB-LSD: o9U69_bDfPexFK08zFFRl2
X-ASBD-ID: 359341
Content-Length: 5162
Origin: https://www.facebook.com
Connection: keep-alive
Referer: https://www.facebook.com/marketplace/108107325884650/search?query=ford
Cookie: datr=JIqnZow5qnkGa9qpV94F4WyT; c_user=100001857951275; fr=1k6n2UUsdT7LGLUBR.AWXtjLOA489ju3USapvSRJr8L9mEDzvwYyzP7g.BnH5Bu..AAA.0.0.Bnpiw8.AWVt8fzPiuE; sb=ToqnZlhdH_aVuvzChhoREzZY; xs=38%3AJQhc_SwL3f2AbA%3A2%3A1722255951%3A-1%3A14496%3A%3AAcXFV3DXEMNpr-6h0K8S2R1dUZAVf4VQfSchx95FH4MJ; ps_l=1; ps_n=1; wd=703x1013; usida=eyJ2ZXIiOjEsImlkIjoiQXNramEyYzFjYjV0M28iLCJ0aW1lIjoxNzI3NTQ1NjQ0fQ%3D%3D; presence=C%7B%22t3%22%3A%5B%7B%22o%22%3A0%2C%22i%22%3A%22u.24052952154294604%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8198290400276938%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8479708578816243%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8647792911909990%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22sc.7250117433385889937%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.27390201170593783%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8280212772075879%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8643388819107455%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8536117643093004%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.27498303063116923%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8574592289283638%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.7970065553094064%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8481826755233958%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22sc.7250117433383252638%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22sc.8179238638870654%22%7D%5D%2C%22utc3%22%3A1740139507668%2C%22v%22%3A1%7D
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Pragma: no-cache
Cache-Control: no-cache
TE: trailers"""

json_headers = dict(email.message_from_string(json_headers_str))
del json_headers["Accept-Encoding"]
del json_headers["Content-Length"]



def get_request_body(cursor=None):
    data_str = r'''av=100001857951275
__aaid=0
__user=100001857951275
__a=1
__req=1b
__hs=20140.HYP:comet_pkg.2.1...1
dpr=2
__ccg=EXCELLENT
__rev=1020287122
__s=qaph7d:g2shdo:8gcswm
__hsi=7473842244321722437
__dyn=7xeXzWK2l2o8ong569yaxG4Qih0noeEb8nwgUaofUjyUW3qi7UK360CEboG4E2vwpUe8hw8u2a0Z82_CxS320qa321Rwwwg8a8462mcw8a0XohwGxu782lwj8bU9kbxS2617wc61awkovwRwlE-U2exi4UaEW4UmwkUtxGm2SU4i5o6Kexfxmu3W3y2616DBx_wHwfC2-awLyESE2KwkQ0z8c84u2ubwHwKG4UrwFg2fwxyo6J0qo4e16wWzUfHDzUiBG2OUqwjVqwLwHwea1ww
__csr=h4fns9OgHawhPH95jbb25hljEjbaD48AQykGifsuHLkhNiJbhaIGZfZlmEOkKZdcliuTFTL8Z4H8_ait5RRWLGnmUBaUGAlkmy7i8juquZaAqtrEBqyaAjKXlalVqVEiKUx7GUScVaCHKZfgJdTxaaAVqmmZ2Frh-kFoCGyK8yoyqVEyUKAdALwMmdG9ggGXCzFeK8UytoO8wBK8x2mV8k-ubVV98hKeHAhUx162Kjg84may8kJ3Hxm7qzA5A5UGumiXBAHx2t1y4oSEGui5oCm4ECmuETyomKh1aim5qBxKfGHwOGcxm6aVp9osxm58O3i7A5FoyK-6oizbAx53FrzUKFoaU884N28N4Ugx6bGu4oOm-dCBBKfwhJ0gUhxe7U4q9G15AAwxg5Rx2h0sUclxZ0IBhE8EG0h21ewu40JaiwHwRx21jqwe9a9wnoem1szlDzK5kt0zyXxAw3CCgB0iA5lLO2o23a1r57wtE8U4y12x-u3m48Ba3e0KswozJUjCK3Sq0xo-dg26gO2gwy15GGmq2K6E21gswCxmag42DZwGgfohK4tjBgjCAUR2UW2ieAKu7Aey8kxCiUkg8e3m06RE1B813U0_eF9UKmfw1Ee0pW08LAo1kXbypkqm1hw6Co2Xxmq04H0E9BF1jxpwiU1H806pK0uC0466EigG95EE0dA8420Fpng1081Xkh3pUfUngG0BiuhfhQ7U1OO04Gw_wv8gwa_wmRw3gUeVCcyE7q09Aw2sEgCG1vwaK8w70xCdF0Aw67w2UZ28pgco5B0houxi3J0AQy7s-zDzWgWegpolzo9-HuS4kA0EUap2jw4wxa5d122C480CAw1zE8pE2LDxS27o6az0iE0EKqEiAz8-0QE1po0A21kWweO0aag14AEhgiOFw4fG05T81QGG2W0FpU0mPBu3-1AcEiggJPk0AUd83HweK0K84-0CoeUaE28G4k5dw4dw1ia5o3iw2O20
__comet_req=15
fb_dtsg=NAcMFMgCsOUjx04XraTdL5AXxgFK5McWTH5PFn0KR33Ip97gavi5WoA:38:1722255951
jazoest=25244
lsd=o9U69_bDfPexFK08zFFRl2
__spin_r=1020287122
__spin_b=trunk
__spin_t=1740139500
fb_api_caller_class=RelayModern
fb_api_req_friendly_name=CometMarketplaceSearchContentPaginationQuery
variables={"count":24,"cursor":"__CURSOR__","params":{"bqf":{"callsite":"COMMERCE_MKTPLACE_WWW","query":"ford"},"browse_request_params":{"commerce_enable_local_pickup":true,"commerce_enable_shipping":true,"commerce_search_and_rp_available":true,"commerce_search_and_rp_category_id":[],"commerce_search_and_rp_condition":null,"commerce_search_and_rp_ctime_days":null,"filter_location_latitude":34.675,"filter_location_longitude":33.0333,"filter_price_lower_bound":0,"filter_price_upper_bound":214748364700,"filter_radius_km":100},"custom_request_params":{"browse_context":null,"contextual_filters":[],"referral_code":null,"saved_search_strid":null,"search_vertical":"C2C","seo_url":null,"surface":"SEARCH","virtual_contextual_filters":[]}},"scale":2}
server_timestamps=true
doc_id=9423540494371697'''
    import urllib

    if cursor is not None:
        data_str = data_str.replace("__CURSOR__", cursor.replace('"', r'\"'))
        
    result = []
    for line in data_str.split("\n"):
        key, value = line.split("=")
        value = urllib.parse.quote(value)
        result.append(f"{key}={value}")
    data = "&".join(result)
    return data


def get_cursor(data):
    if not data["data"]["marketplace_search"]["feed_units"]["page_info"]["has_next_page"]:
        return None
    cursor = data["data"]["marketplace_search"]["feed_units"]["page_info"]["end_cursor"]
    return cursor

def flatten_dict(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else k
        if isinstance(v, dict):
            items.extend(flatten_dict(v, new_key, sep=sep).items())
        elif isinstance(v, list):
            for i, elem in enumerate(v):
                items.extend(flatten_dict({f"{i}": elem}, new_key, sep=sep).items())
        else:
            items.append((new_key, v))
    return dict(items)


class PropertySpider(scrapy.Spider):
    name = "property_spider"

    def __init__(self, urls: str, fast=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_urls = urls.split(",")
        self.fast = int(fast)
        self.pb = tqdm(desc="Crawling Pages", unit="page", total=0) 

    def start_requests(self):
        for url in self.start_urls:
            self.logger.info(f"Starting to scrape {url}")
            yield scrapy.Request(url=url, method="GET", callback=self.parse_start_page, priority=HIGH_PRIO, headers=dict(html_headers), errback=self.error_handler)
    
    def parse_start_page(self, response: Response):
        """
        Parse the initial page to find the maximum page number.
        """
        scripts = BeautifulSoup(response.text, 'html.parser').find_all('script')
        found_scripts = [script for script in scripts if re.search("formatted_amount", script.string or "")]
        assert len(found_scripts) == 1, f"Expected to find exactly one script with formatted_amount, but found {len(found_scripts)}"
        data = json.loads(found_scripts[0].string)
        if "search" in response.url:
            edges = data["require"][0][3][0]["__bbox"]["require"][0][3][1]["__bbox"]["result"]["data"]["marketplace_search"]["feed_units"]["edges"]
            page_info = data["require"][0][3][0]["__bbox"]["require"][0][3][1]["__bbox"]["result"]["data"]["marketplace_search"]["feed_units"]["page_info"]
        else:
            edges = data["require"][0][3][0]["__bbox"]["require"][0][3][1]["__bbox"]["result"]["data"]["viewer"]["marketplace_feed_stories"]["edges"]
            page_info = data["require"][0][3][0]["__bbox"]["require"][0][3][1]["__bbox"]["result"]["data"]["viewer"]["marketplace_feed_stories"]["page_info"]

        if page_info["has_next_page"]:
            yield self._list_page_request(cursor=page_info["end_cursor"])

        for edge in edges:
            yield self._ad_page_request(id=edge["node"]["story_key"] )


    def _ad_page_request(self, id):            
        self.pb.total += 1
        self.pb.refresh()
        return scrapy.Request(url=f"https://www.facebook.com/marketplace/item/{id}", method="GET", callback=self.parse_ad_page, headers=html_headers)

    def _list_page_request(self, cursor):
        self.logger.info(f"Requesting list page with {cursor=}")
        return scrapy.Request(url="https://www.facebook.com/api/graphql", method="POST", callback=self.parse_list_page, priority=HIGH_PRIO, headers=json_headers, body=get_request_body(cursor))

    def parse_list_page(self, response):
        try:
            data = json.loads(response.text)

            if not self.fast:
                cursor = data["data"]["marketplace_search"]["feed_units"]["page_info"]["end_cursor"]
                yield self._list_page_request(cursor=cursor)


            edges = data["data"]["marketplace_search"]["feed_units"]["edges"]
            for edge in edges:
                if "listing" in edge["node"]:
                    yield self._ad_page_request(id=edge["node"]["story_key"] )
                else:
                    self.logger.info(f"Skipping edge without listing: {edge}")
        except Exception as e:
            pass
        
    def parse_ad_page(self, response):
        """
        Parse a single page for property listings.
        """
        try:
            soup = BeautifulSoup(response.text, 'html.parser')
            scripts = soup.find_all('script')
            found_scripts = [script for script in scripts if re.search("redacted_description", script.string or "")]
            assert len(found_scripts) == 1, f"Expected to find exactly one script with redacted_description, but found {len(found_scripts)}"
            data = json.loads(found_scripts[0].string)

            self.pb.update(1)
            result = flatten_dict(data["require"][0][3][0]["__bbox"]["require"][3][3][1]["__bbox"]["result"]["data"]["viewer"]["marketplace_product_details_page"]["target"])
            return result 
        except Exception as e:
            pass
            
    def closed(self, reason):  
        if self.pb:  
            self.pb.close()     
            
    def error_handler(self, failure):
        self.logger.error(f"Request failed: {failure.value}")            