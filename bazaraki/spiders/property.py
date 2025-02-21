import email
import json
import re
import scrapy
from tqdm import tqdm
from scrapy.http import Response
from bs4 import BeautifulSoup
import re
import urllib


HIGH_PRIO = 10


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
X-FB-LSD: SVynp8scZMIVjJvvjM9HlR
X-ASBD-ID: 359341
Content-Length: 5000
Origin: https://www.facebook.com
Connection: keep-alive
Referer: https://www.facebook.com/marketplace/108107325884650/search?query=mini
Cookie: datr=JIqnZow5qnkGa9qpV94F4WyT; sb=ToqnZlhdH_aVuvzChhoREzZY; ps_l=1; ps_n=1; wd=824x1013; usida=eyJ2ZXIiOjEsImlkIjoiQXNramEyYzFjYjV0M28iLCJ0aW1lIjoxNzI3NTQ1NjQ0fQ%3D%3D; c_user=100001857951275; fr=0JE0Hxi2jNkOyl97Y.AWWHh9q3kMeuCS4eu6eqKhGT9DeuXqpfRT1pkA.BnuLO5..AAA.0.0.BnuLO5.AWXx0N9_HeY; xs=13%3AaLs4XucKM0cS_Q%3A2%3A1740157882%3A-1%3A14496; presence=C%7B%22t3%22%3A%5B%7B%22o%22%3A0%2C%22i%22%3A%22u.24052952154294604%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8198290400276938%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8479708578816243%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8647792911909990%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22sc.7250117433385889937%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.27390201170593783%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8280212772075879%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8643388819107455%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8536117643093004%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.27498303063116923%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8574592289283638%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.7970065553094064%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22u.8481826755233958%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22sc.7250117433383252638%22%7D%2C%7B%22o%22%3A0%2C%22i%22%3A%22sc.8179238638870654%22%7D%5D%2C%22utc3%22%3A1740159004737%2C%22v%22%3A1%7D
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
__req=z
__hs=20140.HYP:comet_pkg.2.1...1
dpr=2
__ccg=EXCELLENT
__rev=1020291413
__s=u778lz:g2shdo:kx2i9w
__hsi=7473925991077884072
__dyn=7xeXzWK2l2o8ong569yaxG4Qih0noeEb8nwgUaofUjyUW3qi7UK360CEboG4E2vwpUe8hw8u2a0Z82_CxS320qa321Rwwwg8a8462mcw8a0XohwGxu782lwj8bU9kbxS2617wc61awkovwRwlE-U2exi4UaEW4UmwkUtxGm2SU4i5o6Kexfxmu3W3y2616DBx_wHwfC2-awLyESE2KwkQ0z8c84u2ubwHwKG4UrwFg2fwxyo6J0qo4e16wWzUfHDzUiBG2OUqwjVqwLwHwea1ww
__csr=gT4hAI8NAG4gLb25T7jYvax299kyPN7YObcBsrkTfQXvS-QWiSmy77teiSQmpbTHbq9SAjuyHJX4JGiGjGRJ7CVp6XABl4A_8F8DBQFvXFybGQGGDgGGyvyKmBV-EKRiCvUjDG-m5kiUyRWW-dG_KmVqACUKmUy8ACBQUnGaDKmXBjhm8Cz-aJrxKibK599GDkEpxy9zUyGy8yUlgO9yeuqqdzoCay8jBx6dyF8CaDCWK7HypEe8aoKdABWK5mQ2a8XAy4u8m4EW8AokyUB2oO5EgyumrhooGF89EF2oOcxqicwLzEmzV7wgA8DzUB0zDK9x24_UsG6KqEkzo-3iEqCxG2OcyUky8y6pWBVoy8UiDGQjz8d8G1AxOcABwLwKyU666ouBp8b82kgqzp8eE4p1G9zum2eE9o88-p7UGawj4azm0xU6Dz82rGimawlHzt0Bg6Vy8V1u7432u5i0Ixe2ibDzBUvy42O3u4Eb8bEbk4pbwn88qK0Irw9e2e3u2e2R1i3q3a5Vp41jwIyEhxpUSfGbmqEx0xzVUfUKi-fzXVF7VongG26Q5e3e1swsV8c5h8OUsyEe8hDWFaaK1cBwj9UdES3aawh41rQl90Dxe1jxedxvx-2m2u2h03D80sTwnGw6LzC7Uy0hy16ha8jADzK05u81-Q0f3w16-OG4kaDsCx0vQ01VLw35U2zwdKA48aA2R8Yg024a07Mo1e202h81I8uwG83O4824g2xIK320-9K0mulQ0w83XCDWws80wi0jClwdK3W2O0Vm0Xo881dU2sw43wiEigk5ojy8bo3YxF1q5t02ho4t5u04g8S8wBg2KAUf88tdk4SagCl0a6IYWx9czJcXN05a6k6AUjAx6U3GDgGiE18QeGlU13ocSdxi6o9U1R8jwjo2I8FQaIE5a0VaU2Qwfa04tE0wfwdp0UXG06mE0g9w9ME4O0WUdoeU7W481L409Kw6zBo0RW8gGgw1ao3L7d2FmVZwRw64wzwVw4Ow
__comet_req=15
fb_dtsg=NAcMTyD1-Cu7mVbqqGackcwtYvE178s25Bcu6uilkozjKRHv44NYQiw:13:1740157882
jazoest=25580
lsd=SVynp8scZMIVjJvvjM9HlR
__spin_r=1020291413
__spin_b=trunk
__spin_t=1740158999
fb_api_caller_class=RelayModern
fb_api_req_friendly_name=CometMarketplaceSearchContentPaginationQuery
variables={"count":24,"cursor":"{\"pg\":0,\"b2c\":{\"br\":\"\",\"it\":0,\"hmsr\":false,\"tbi\":0},\"c2c\":{\"br\":\"AbrP6RgjiTpfdTQgk5pJwofjcCurhghA1gAWmPTWWLytb_7_htpE2KsBEuKFuyXRPrTmvpZ3O6i7OvN7npdrsL76YAZ3R7VjR3OO3VvBgjEcpkySQp7p7vuMtcPTLnJKKou6YMsJTQoFF6Nu9rdgBsCqzM7zxYMVOMcyL5Rzz-Pkk4_xZR7rvlzVZjzg_qFH88zXOEZBnBbM9Em_HvDtc7AUFvuorom2qOnOcMteqYFdAPWEBvET6PbEo8uRqNPa7V-SZbOJULV-ROf6Au_5UMDeQ_f9ZNb4Outth6rssUFrkL0GXLPRxiXMQVZUyw2UNVbal35pTjo6XnjZRX9XtOkhbz_Ke_E0sFCeO0DIbIJV6LTqeTlXQKTC-VAEGxCxHjJonwBu9zh_jThAO4283OWeMg1aGVzi3xUs9DdJYR03wX3QtMncHby1cpFuyzx_-5o-q4kN_VjoNPgw6zHwqXeaJej6_eVyGlXJKTjPmqvpW0mOQ-nGEJ2BKFvIYCopk7goEx4tlXb3k1GJNZcsUQJpIImgSKvfINQZgpNw20C67A\",\"it\":24,\"rpbr\":\"\",\"rphr\":false,\"rmhr\":false},\"ads\":{\"items_since_last_ad\":24,\"items_retrieved\":24,\"ad_index\":0,\"ad_slot\":0,\"dynamic_gap_rule\":0,\"counted_organic_items\":0,\"average_organic_score\":0,\"is_dynamic_gap_rule_set\":false,\"first_organic_score\":0,\"is_dynamic_initial_gap_set\":false,\"iterated_organic_items\":0,\"top_organic_score\":0,\"feed_slice_number\":0,\"feed_retrieved_items\":0,\"ad_req_id\":0,\"refresh_ts\":0,\"cursor_id\":20083,\"mc_id\":0,\"ad_index_e2e\":0,\"seen_ads\":{\"ad_ids\":[],\"page_ids\":[],\"campaign_ids\":[]},\"has_ad_index_been_reset\":false,\"is_reconsideration_ads_dropped\":false},\"irr\":false,\"serp_cta\":false,\"rui\":[],\"mpid\":[],\"ubp\":null,\"ncrnd\":0,\"irsr\":false,\"bmpr\":[],\"bmpeid\":[],\"nmbmp\":false,\"skrr\":false,\"ioour\":false,\"ise\":false}","params":{"bqf":{"callsite":"COMMERCE_MKTPLACE_WWW","query":"mini"},"browse_request_params":{"commerce_enable_local_pickup":true,"commerce_enable_shipping":true,"commerce_search_and_rp_available":true,"commerce_search_and_rp_category_id":[],"commerce_search_and_rp_condition":null,"commerce_search_and_rp_ctime_days":null,"filter_location_latitude":34.675,"filter_location_longitude":33.0333,"filter_price_lower_bound":0,"filter_price_upper_bound":214748364700,"filter_radius_km":100},"custom_request_params":{"browse_context":null,"contextual_filters":[],"referral_code":null,"saved_search_strid":null,"search_vertical":"C2C","seo_url":null,"surface":"SEARCH","virtual_contextual_filters":[]}},"scale":2}
server_timestamps=true
doc_id=9423540494371697'''

    result = []
    for line in data_str.split("\n"):
        key, value = line.split("=")
        if key == "variables" and cursor is not None:
            variables = json.loads(value)
            variables["cursor"] = cursor
            value = json.dumps(variables)
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
        # self.logger.info(f"Requesting list page with {cursor=}")
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
                    self.logger.debug(f"Skipping edge without listing: {edge}")
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