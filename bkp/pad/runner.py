import os

from edgar import SECDownloader


class FileManager:
    def __init__(self, save_dir="sec_filings_index"):
        self.save_dir = save_dir
        self._ensure_save_directory()

    def _ensure_save_directory(self):
        if not os.path.exists(self.save_dir):
            os.makedirs(self.save_dir)

    def build_local_path(self, index_type, year, quarter, extension=".idx"):
        return os.path.join(
            self.save_dir, f"{index_type}_{year}_QTR{quarter}{extension}"
        )

    def save_data(self, data, local_path):
        with open(local_path, "wb") as f:
            f.write(data)
        print(f"Data saved to: {local_path}")


class SECRunner:
    def __init__(self, save_dir="sec_filings_index"):
        self.sec_downloader = SECDownloader()
        self.file_manager = FileManager(save_dir)

    def download_sec_file(self, url, index_type, year, quarter):
        try:
            data = self.sec_downloader.download(url)
            extension = ".json" if url.endswith(".json") else ".idx"
            local_path = self.file_manager.build_local_path(
                index_type, year, quarter, extension
            )
            self.file_manager.save_data(data, local_path)
            print(f"Successfully processed {index_type} for {year} Q{quarter}")
            return local_path
        except Exception as e:
            print(f"Failed to download and save file: {e}")
            return None


def download_sec_index_file(
    year, quarter, index_type="companies", save_dir="sec_filings_index"
):
    runner = SECRunner(save_dir)
    url = "https://data.sec.gov/submissions/CIK0001318605.json"
    return runner.download_sec_file(url, index_type, year, quarter)


def main():
    runner = SECRunner()
    url = "https://data.sec.gov/submissions/CIK0001318605.json"
    result = runner.download_sec_file(url, "companies", 2025, 1)

    if result:
        print(f"\nDownload process complete. File saved to: {result}")
    else:
        print("\nDownload process failed.")


if __name__ == "__main__":
    main()
