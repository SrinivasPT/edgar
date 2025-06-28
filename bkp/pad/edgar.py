import gzip
import time
import urllib.request


class SECDownloader:
    DEFAULT_HEADERS = {
        "User-Agent": "Company Name Application/1.0 srinivaspt@gmail.com",
        "Accept-Encoding": "gzip, deflate",
    }

    def __init__(self, rate_limit_delay=0.1):
        self.rate_limit_delay = rate_limit_delay

    def _build_headers(self, url):
        headers = self.DEFAULT_HEADERS.copy()
        headers["host"] = url.split("//")[1].split("/")[0]
        return headers

    def download(self, url):
        headers = self._build_headers(url)

        try:
            req = urllib.request.Request(url, headers=headers)
            opener = urllib.request.build_opener()

            with opener.open(req) as response:
                content_encoding = response.getheader("Content-Encoding", "")

                if content_encoding == "gzip":
                    compressed_data = response.read()
                    return gzip.decompress(compressed_data)
                else:
                    return response.read()

        finally:
            time.sleep(self.rate_limit_delay)
