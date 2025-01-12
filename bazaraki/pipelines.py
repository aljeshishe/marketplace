from datetime import datetime, timezone
from pathlib import Path
import re
import json
from urllib.parse import urlparse
from itemadapter import ItemAdapter


def escape(s):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', s)

class BazarakiPipeline:
    def open_spider(self, spider):
        path = "_".join(urlparse(url).path.replace("/", "") for url in spider.start_urls)
        now_str = datetime.now().isoformat(sep=" ", timespec="seconds")
        fast_prefix = "fast_" if spider.fast else ""
        self.file_path = Path(f"output/{now_str} {fast_prefix}{escape(path)}.jsonl_")
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.file = self.file_path.open("w")
        spider.logger.info(f"Writing to {self.file_path}")

    def close_spider(self, spider):
        self.file.close()
        self.file_path.rename(self.file_path.with_suffix(".jsonl"))
        

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item