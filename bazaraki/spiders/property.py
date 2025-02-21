import email
import json
import re
import scrapy
from tqdm import tqdm
from scrapy.http import Response

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
Accept-Encoding: br
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

html_headers = email.message_from_string(html_headers_str)
# del html_headers["Accept-Encoding"]

json_headers_str = """Host: www.facebook.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:135.0) Gecko/20100101 Firefox/135.0
Accept: */*
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: zstd
Content-Type: application/x-www-form-urlencoded
X-FB-Friendly-Name: MWQuickPromotionThreadViewBannerContainerQuery
X-FB-LSD: q-mS07NJZrDNA4EUsVupeq
X-ASBD-ID: 359341
Content-Length: 1971
Origin: https://www.facebook.com
Alt-Used: www.facebook.com
Connection: keep-alive
Referer: https://www.facebook.com/marketplace/108107325884650/search?query=ford
Cookie: datr=JIqnZow5qnkGa9qpV94F4WyT; c_user=100001857951275; fr=1k6n2UUsdT7LGLUBR.AWXtjLOA489ju3USapvSRJr8L9mEDzvwYyzP7g.BnH5Bu..AAA.0.0.Bnpiw8.AWVt8fzPiuE; sb=ToqnZlhdH_aVuvzChhoREzZY; xs=38%3AJQhc_SwL3f2AbA%3A2%3A1722255951%3A-1%3A14496%3A%3AAcUQ6I51ZQZLaT1xG0SMWZ_LenaGUcJbyZwklCn6kWP6; ps_l=1; ps_n=1; wd=703x1013; usida=eyJ2ZXIiOjEsImlkIjoiQXNramEyYzFjYjV0M28iLCJ0aW1lIjoxNzI3NTQ1NjQ0fQ%3D%3D; presence=C%7B%22t3%22%3A%5B%7B%22o%22%3A0%2C%22i%22%3A%22u.24052952154294604%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8198290400276938%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8479708578816243%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8647792911909990%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22sc.7250117433385889937%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.27390201170593783%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8280212772075879%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8643388819107455%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8536117643093004%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.27498303063116923%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8574592289283638%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.7970065553094064%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8481826755233958%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22sc.7250117433383252638%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22sc.8179238638870654%22%7D%5D%2C%22utc3%22%3A1740137635948%2C%22v%22%3A1%7D
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Pragma: no-cache
Cache-Control: no-cache
TE: trailers"""

json_headers = email.message_from_string(json_headers_str)
# del html_headers["Accept-Encoding"]



def get_request_body(cursor):
    data_str = r'''av=100001857951275
__aaid=0
__user=100001857951275
__a=1
__req=1z
__hs=20127.HYP:comet_pkg.2.1...1
dpr=2
__ccg=EXCELLENT
__rev=1019959221
__s=huhmu0:ty2brg:bobr9e
__hsi=7469069495959316336
__dyn=7xeXzWK2l2o8ong569yaxG4Qih0noeEb8nwgUaqwYxebzEdF8vyUco2qwJyEiw9-1DwUx60xU8E3Qwb-q7oc81EEc87m2210wEwgo9oO0wE3Jx62G5Usw9m1cwLwBgK7o8o4u0Mo4G1hx-3m1mzXw8W58jwGzEjxq1jxS6Fobrwh8lwqUW4-5pUfEe88o4qum7-2K0-obUG2-azqwaW1jg2cwMwhU9UK2K2WEjxK2B08-269wqQ1FwgUjwOwWzUfHDzUiwRK6E4-mEbUaU3yw
__csr=gJfb6RsQr2cb8j2kITeBkYG9aJR9d_f5r7OlkkDW9TeIJRsyFqfrtjh28AQJbFvl8xqTh6yLHmllmK8iLQFaLlVlimLF4R8GQlG8CJrIynhoCSmegyJuVqGip9V8KJdamqFoB3pliAKiim-8ppaypTTFmGLABqF2KuQhaujZ2HAA_GazoKUIw-h4z8WqnjDKipKt2UGGKVqzUiGutpFUjGcBUZ5GiWyeVaABzEgzXy8hyta9gmDzpoapkmby48ADAWm5GizolxiUqKazm8gSmbzqgvACg-9zEoggyUlye8GEW4uErCxiWCGWKdhFDyag8E5ai5EsKuummfA-5FUKQVod9FUN16vzUkxyu1pHAwBx2qibG4Ujz9E98kggxx28jwmU2FK9xfwhoS5u5k4qN08HwBhk12xC1obwtCbv9bPztEW4zYpfG2S48B4Gb9vQbBqwwxKi4o5258qK0PE6G-1HBzooyUyCl0kF8564ozw8C2CaggGsSAuH4F7-pyfgtxG1iwCx60AUpyo4v94wDg6S6rG0wECV8sx-akLoaUG6UuAg5oPAFyk6EybwUU8JwQx11m6kaQexW1lz4qP1ucwvF2uUihXm6oHHgyqcyUCzGaEEOfxq8SF2wKQrWG9xi3ym4ohweW021i0pe0dBPe0oK1Bw1x61bxTw5-grg1H9ox0Hz205Xw1kEjsEEk2a2mp02mEG01ytw1FcpRgGF81Ao0cWogw9aXS1Nwba0zE2Qwf22a1Mg6WN1k8VU4Ci1HwcK24w1hoy0FU7tk1Dg0JG5q-0CQ0Jo1U83xw2neawyyoownFU2WwdZ3p85mXwro1CU5Zw2tE2WxW4p8aEtg4mfxx6DjAJkh16ayolDzo0Ku0EucQqp052w2kywiE3xP0WweO0k-u1nwbC0la09Jxl0ZGi0Mo1081y60meEp80keA07uUCmE3yyE0yD83C0bKg30wiU722K0BE2Yw3koC22aEM0pgG0c5wuUyaDw
__comet_req=15
fb_dtsg=NAcOtFRKw6zQRwNAUjIu7CIvARckxjesDrz2WQmLRQvuNjEIlcfFtVA:38:1722255951
jazoest=25692
lsd=iGcxqlLgqDVEPRltdYG3KX
__spin_r=1019959221
__spin_b=trunk
__spin_t=1739028258
fb_api_caller_class=RelayModern
fb_api_req_friendly_name=CometMarketplaceSearchContentPaginationQuery
variables={"count":24,"cursor":"__CURSOR__","params":{"bqf":{"callsite":"COMMERCE_MKTPLACE_WWW","query":"convertible"},"browse_request_params":{"commerce_enable_local_pickup":true,"commerce_enable_shipping":true,"commerce_search_and_rp_available":true,"commerce_search_and_rp_category_id":[],"commerce_search_and_rp_condition":null,"commerce_search_and_rp_ctime_days":null,"filter_location_latitude":34.675,"filter_location_longitude":33.0333,"filter_price_lower_bound":0,"filter_price_upper_bound":214748364700,"filter_radius_km":100},"custom_request_params":{"browse_context":null,"contextual_filters":[],"referral_code":null,"saved_search_strid":null,"search_vertical":"C2C","seo_url":null,"surface":"SEARCH","virtual_contextual_filters":[]}},"scale":2}
server_timestamps=true
doc_id=9423540494371697'''
    import urllib

    result = []
    for line in data_str.replace("__CURSOR__", cursor.replace('"', r'\"')).split("\n"):
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
            yield scrapy.Request(url=url, callback=self.parse_start_page, priority=10, headers=dict(html_headers), errback=self.error_handler)
    
    def parse_start_page(self, response: Response):
        """
        Parse the initial page to find the maximum page number.
        """
        text = response.text
        start_pos = text.find('{"data":{"marketplace_search')
        end_pos = text.find(',"sequence_number"', start_pos)
        data = json.loads(text[start_pos:end_pos])
        cursor = get_cursor(data)

        self.logger.info(f"{cursor=}")
        yield scrapy.Request(url="https://www.facebook.com/api/graphql/", callback=self.parse_list_page, priority=10, headers=json_headers, data=get_request_body(cursor))
            
    def parse_list_page(self, response):
        text = response.text
        pos = text.find(',"extensions')
        data = json.loads(text[:pos] + "}")
        for edge in data["data"]["marketplace_search"]["feed_units"]["edges"]:
            yield dict(id=edge["node"]["story_key"])

        cursor = get_cursor(data)
        yield scrapy.Request(url="https://www.facebook.com/api/graphql/", callback=self.parse_list_page, priority=10, headers=json_headers, data=get_request_body(cursor))
        
    def parse_page(self, response):
        """
        Parse a single page for property listings.
        """
        data = {
            "url": response.url,
            "title": get(response, "h1::text"),
            "price": get(response, "meta[itemprop='price']::attr(content)", type=float),
            "original_price": get(response, ".announcement-price__discount-start::text", type=int, replace="/m² € ."),
            "price_per_sqm": get(response, ".announcement-price__per-meter::text", type=int, replace="/m² € ."),
            "location": get(response, "span[itemprop='address']::text"),
            "posted": get(response, "span[class='date-meta']::text", replace="Posted: Today"),
            "ad_id": get(response, "span[itemprop='sku']::text"),
            "reference_number": get(response, "span.reference-number::text"),
            "views": get(response, "span[class='counter-views']::text", replace="Views:", type=int),
            "lat": get(response, "div[id='geoMap']::attr(data-default-lat)"),
            "lng": get(response, "div[id='geoMap']::attr(data-default-lng)"),
            "sold": bool(get(response, ".phone-author--sold")),
        }
        
        categories = getall(response, "span[itemprop='name']::text")
        categories_map = {f"cat{i}": cat for i, cat in enumerate(categories[1:])}
        data.update(categories_map)
            
        keys = getall(response, "div[class='announcement-characteristics clearfix'] [class='key-chars']::text", replace=":")
        values = getall(response, "div[class='announcement-characteristics clearfix'] [class='value-chars']::text", replace="m²")
        data.update(zip(keys, values))
        
        long_data = {
            "images": getall(response, "img[class='announcement__thumbnails-item js-select-image']::attr(src)"),
            "description": "\n".join(getall(response, "div.js-description > *::text"))
        }
        data.update(long_data)
        
        self.pb.update(1)
        return data
    
    def closed(self, reason):  
        # Close the progress bar when the spider finishes  
        if self.pb:  
            self.pb.close()     
            
    def error_handler(self, failure):
        self.logger.error(f"Request failed: {failure.value}")            