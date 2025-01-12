.PHONY: crawl
crawl:
	scrapy crawl property_spider -a  urls=https://www.bazaraki.com/real-estate-to-rent,https://www.bazaraki.com/real-estate-for-sale


.PHONY: fast
fast:
	scrapy crawl property_spider -a fast=1 -a urls=https://www.bazaraki.com/real-estate-to-rent,https://www.bazaraki.com/real-estate-for-sale

.PHONY: sync
sync:
	aws s3 sync output s3://ab-users/grachev/bazaraki/output

.PHONY: syncback
syncback:
	aws s3 sync s3://ab-users/grachev/bazaraki/output output 

