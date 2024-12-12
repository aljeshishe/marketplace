.PHONY: rent
rent:
	scrapy crawl property_spider -a  url=https://www.bazaraki.com/real-estate-to-rent/apartments-flats/

.PHONY: buy
buy:
	scrapy crawl property_spider -a  url=https://www.bazaraki.com/real-estate-for-sale/apartments-flats/


.PHONY: rent_house
rent_house:
	scrapy crawl property_spider -a  url=https://www.bazaraki.com/real-estate-to-rent/houses/

.PHONY: buy_house
buy_house:
	scrapy crawl property_spider -a  url=https://www.bazaraki.com/real-estate-for-sale/houses/



.PHONY: test
test:
	scrapy crawl property_spider -a debug=1 -a url=https://www.bazaraki.com/real-estate-to-rent/apartments-flats/
