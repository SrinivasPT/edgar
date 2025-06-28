import gzip
import os
import time
import urllib.error
import urllib.request


def download_sec_index_file(
    year, quarter, index_type="companies", save_dir="sec_filings_index"
):
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # url = "https://www.sec.gov/Archives/edgar/full-index"
    url = "https://data.sec.gov/submissions/CIK0001318605.json"

    headers = {
        "User-Agent": "Company Name Application/1.0 srinivaspt@gmail.com",
        "Accept-Encoding": "gzip, deflate",
        "host": url.split("//")[1].split("/")[0],
    }

    file_name = f"{index_type}.idx"
    local_path = os.path.join(save_dir, f"{index_type}_{year}_QTR{quarter}.idx")

    print(f"Attempting to download: {url}")
    try:
        # Create request with headers
        req = urllib.request.Request(url, headers=headers)

        # Create OpenerDirector with default handlers
        opener = urllib.request.build_opener()

        with opener.open(req) as response:
            # Check if response is gzip compressed
            content_encoding = response.getheader("Content-Encoding", "")

            if content_encoding == "gzip":
                # Handle gzip compressed response
                compressed_data = response.read()
                data = gzip.decompress(compressed_data)
                with open(local_path, "wb") as f:
                    f.write(data)
            else:
                # Handle uncompressed response
                with open(local_path, "wb") as f:
                    while True:
                        chunk = response.read(8192)
                        if not chunk:
                            break
                        f.write(chunk)

        print(
            f"Successfully downloaded {file_name} for {year} Q{quarter} to: {local_path}"
        )

    except urllib.error.HTTPError as e:
        if e.code == 403:
            print(
                f"Error 403 Forbidden: The SEC may be blocking your request. "
                f"Ensure your User-Agent is properly set and you are not making too many requests too quickly. "
                f"URL: {url}"
            )
        else:
            print(f"HTTP Error {e.code}: {e.reason}")
    except urllib.error.URLError as e:
        print(
            f"URL Error: Could not connect to the SEC server. Check your internet connection. {e.reason}"
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

    # Be polite to the SEC servers to avoid getting blocked.
    # The SEC recommends not to make more than 10 requests per second.
    time.sleep(0.1)


if __name__ == "__main__":
    download_sec_index_file(2025, 1, index_type="companies")

    print("\nDownload process complete.")
