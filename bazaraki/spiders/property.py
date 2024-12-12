import re
import scrapy

# todo remote m2 from Property area                                                                                                     100 m²

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

class PropertySpider(scrapy.Spider):
    name = "property_spider"

    def __init__(self, url=None, debug=False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.start_url = url
        self.debug = int(debug)

    
    def start_requests(self):
        yield scrapy.Request(self.start_url, self.parse)
    
    
    def parse(self, response):
        """
        Parse the initial page to find the maximum page number.
        """
        # Extract the maximum page number
        pages = response.css("a.page-number::attr(data-page)").getall()
        max_page_number = max(map(int, pages)) + 1 if pages else 1
        if self.debug:
            max_page_number = 2
        for page_number in range(1, max_page_number):
            url = f"{self.start_url}?page={page_number}"
            yield scrapy.Request(url=url, callback=self.parse_list_page)
       
        yield from self.parse_list_page(response)

    
    def parse_list_page(self, response):
        for url in response.css("a[class='mask']::attr(href)").getall():
            yield response.follow(url, callback=self.parse_page)
            # yield scrapy.Request(url=f"{self.prefix}/{url}", callback=self.parse_page)

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
            "description": "\n".join(getall(response, "div.js-description > *::text")),
            "images": getall(response, "img[class='announcement__thumbnails-item js-select-image']::attr(src)"),
        }
        
        keys = getall(response, "div[class='announcement-characteristics clearfix'] [class='key-chars']::text", replace=":")
        values = getall(response, "div[class='announcement-characteristics clearfix'] [class='value-chars']::text")
        data.update(zip(keys, values))
        return data