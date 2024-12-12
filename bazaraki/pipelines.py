from datetime import datetime, timezone
from pathlib import Path
import re
import json
from urllib.parse import urlparse
from itemadapter import ItemAdapter

# escape string to make filename
def escape(s):
    return re.sub(r'[^a-zA-Z0-9_-]', '_', s)

class BazarakiPipeline:
    def open_spider(self, spider):
        path = urlparse(spider.start_url).path
        now = datetime.now(tz=timezone.utc)
        debug_prefix = "debug_" if spider.debug else ""
        file_name = f"output/{debug_prefix}{escape(path)}_{now:%Y%m%d_%H%M%S}.jsonl"
        self.file_path = Path(file_name)
        self.file_path.parent.mkdir(parents=True, exist_ok=True)
        self.file = self.file_path.open("w")

    def close_spider(self, spider):
        self.file.close()

    def process_item(self, item, spider):
        line = json.dumps(ItemAdapter(item).asdict()) + "\n"
        self.file.write(line)
        return item