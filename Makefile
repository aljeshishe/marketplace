.PHONY: crawl
crawl:
	scrapy crawl spider -a  urls="https://www.facebook.com/marketplace/108107325884650/search/"
	# scrapy crawl spider -a  urls='https://www.facebook.com/marketplace/108107325884650/search/?query=mini'


.PHONY: fast
fast:
	scrapy crawl spider -a  urls='https://www.facebook.com/marketplace/108107325884650/vehicles' -a fast=1
	scrapy crawl spider -a  urls='https://www.facebook.com/marketplace/108107325884650/search/?query=mini' -a fast=1

.PHONY: sync
sync:
	aws s3 sync output s3://ab-users/grachev/marketplace/output

.PHONY: syncback
syncback:
	aws s3 sync s3://ab-users/grachev/marketplace/output output 

