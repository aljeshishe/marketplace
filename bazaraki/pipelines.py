from datetime import datetime, timezone
from pathlib import Path
import re
import json
from urllib.parse import urlparse
from itemadapter import ItemAdapter
from loguru import logger

def escape(s):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', s)

class BazarakiPipeline:
    def open_spider(self, spider):
        path = "_".join(urlparse(url).path.replace("/", "") for url in spider.start_urls)
        now = datetime.now(tz=timezone.utc)
        fast_prefix = "fast_" if spider.fast else ""
        file_name = f"output/{now:%Y%m%d_%H%M%S}_{fast_prefix}{escape(path)}.jsonl"
        self.file_path = Path(file_name)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        logger.info(f"Writing to {self.file_path}")
        self.file = self.file_path.open("w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item