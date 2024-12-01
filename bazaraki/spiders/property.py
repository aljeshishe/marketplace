import scrapy


class PropertySpider(scrapy.Spider):
    name = "property_spider"
    start_urls = ["https://www.bazaraki.com/real-estate-for-sale/apartments-flats/lemesos-district-limassol/"]  # Replace with the path to `pages.html`
    prefix = "https://www.bazaraki.com/"

    def parse(self, response):
        """
        Parse the initial page to find the maximum page number.
        """
        # Extract the maximum page number
        pages = response.css("a.page-number::attr(data-page)").getall()
        max_page_number = max(map(int, pages)) if pages else 1
        max_page_number = 1
        # Generate requests for all pages up to the maximum page
        for page_number in range(1, max_page_number + 1):
            url = f"{self.start_urls[0]}?page={page_number}"  # Replace with the correct URL structure
            yield scrapy.Request(url=url, callback=self.parse_list_page)

    def parse_list_page(self, response):
        for url in response.css("a[class='mask']::attr(href)").getall():
            yield scrapy.Request(url=f"{self.prefix}/{url}", callback=self.parse_page)

    def parse_page(self, response):
        """
        Parse a single page for property listings.
        """
        keys = map(str.strip, response.css("div[class='announcement-characteristics clearfix'] [class='key-chars']::text").getall())
        values = map(str.strip, response.css("div[class='announcement-characteristics clearfix'] [class='value-chars']::text").getall())
        properties = dict(zip(keys, values))
        data = {
            "url": response.url,
            "title": response.css("h1::text").get().strip(),
            "price": int(response.css("meta[itemprop='price']::attr(content)").get().replace(".", "")),
            "price_per_sqm": int(response.css(".announcement-price__per-meter::text").get().strip().replace("/m²", "").replace("€", "").replace(".", "")),
            "location": response.css("div.location::text").get(),
            "posted": response.css("span[class='date-meta']::text").get().replace("Posted: ", "").replace("Today ", ""),
            "ad_id": response.css("span[itemprop='sku']::text").get(),
            "reference_number": response.css("span.reference-number::text").get(),
            "views": int(response.css("span[class='counter-views']::text").get().replace("Views: ", "")),
            "lat": response.css("div[id='geoMap']::attr(data-default-lat)").get(),
            "lng": response.css("div[id='geoMap']::attr(data-default-lng)").get(),
            "description": "\n".join(response.css("div.js-description > *::text").getall()),
            "images": response.css("img[class='announcement__thumbnails-item js-select-image']::attr(src)").getall(),
        }
        
        properties.update(data)
        return properties