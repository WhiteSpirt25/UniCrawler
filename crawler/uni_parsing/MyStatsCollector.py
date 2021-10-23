from scrapy.statscollectors import StatsCollector
from scrapy.utils.serialize import ScrapyJSONEncoder

class MyStatsCollector(StatsCollector):
    def _persist_stats(self, stats, spider):
        encoder = ScrapyJSONEncoder(sort_keys=True)
        with open("stats.json", "w") as file:
            data = encoder.encode(stats)
            file.write(data)