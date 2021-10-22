import json
import subprocess
import re

from mamba import description, context, it
from expects import expect, equal

with description('Crawler') as self:
    with before.all:
        subprocess.run(['rm', '-f', 'stats.json'])
        subprocess.run(['scrapy', 'crawl', 'uni_crawl', '--nolog'])

        with open('stats.json') as json_data:
            self.stats = json.load(json_data)

    with it('counts links quantity correctly w/o duplicates'):
        expect(self.stats.get('scheduler/enqueued', 0) +
            self.stats.get('offsite/filtered', 0) -
            self.stats.get('retry/count', 0)
        ).to(equal(1029))

    with it('counts inner pages correctly'):
        expect(self.stats.get('my_pages_downloaded', 0)).to(equal(1006))

    with it('counts inner subdomain urls correctly'):
        expect(self.stats.get('my_subdomain_urls', 0)).to(equal(3))

    with it('counts inner subdomains correctly'):
        expect(self.stats.get('my_subdomain_count', 0)).to(equal(2))

    with it('counts links to redirected pages correctly'):
        expect(
            sum({k: v for k, v in self.stats.items() if re.match("downloader/response_status_count/3", k)}.values())
        ).to(equal(5))

    with it('counts not working links correctly'):
        expect(
            sum({k: v for k, v in self.stats.items() if re.match("downloader/response_status_count/[45]", k)}.values()) -
            sum({k: v for k, v in self.stats.items() if re.match("retry/reason_count/[45]", k)}.values())
        ).to(equal(2))

    with it('counts links to absent pages correctly'):
        expect(self.stats.get('downloader/response_status_count/404', 0)).to(equal(1))

    with it('counts links to server errors pages correctly'):
        expect(
            sum({k: v for k, v in self.stats.items() if re.match("downloader/response_status_count/5", k)}.values()) -
            sum({k: v for k, v in self.stats.items() if re.match("retry/reason_count/5", k)}.values())
        ).to(equal(1))

    with it('counts offsite pages correctly'):
        expect(self.stats.get('offsite/filtered', 0)).to(equal(4))

    with it('counts offsite domains correctly'):
        expect(self.stats.get('offsite/domains', 0)).to(equal(3))

    with it('correctly counts PDF links'):
        expect(self.stats['my_pdf_files_met']).to(equal(2))

    with it('correctly counts DOC links'):
        expect(self.stats['my_doc_files_met']).to(equal(3))

    with it('correctly counts DOCX links'):
        expect(self.stats['my_docx_files_met']).to(equal(4))
