import requests
import sys

DUMP_URL = "https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-pages-articles.xml.bz2"
BZ2_FILE = "enwiki-latest-pages-articles.xml.bz2"

# Download the latest dump of the English Wikipedia
def download_dump(url, filename):
    """Download the latest dump of the English Wikipedia"""

    response = requests.get(url, stream=True)

    # Get the total size in bytes for progress bar
    total_length = int(response.headers.get('Content-Length', 0))
    block_size = 1024
    written = 0

    with open(filename, "wb") as file:
        for data in response.iter_content(block_size):
            # Update progress bar
            written += len(data)
            # Write data to file
            file.write(data)
            # Print progress
            done = int(50 * written / total_length)
            sys.stdout.write("\r[{}{}] {:.1f}%".format(
                '=' * done, ' ' * (50-done), 100 * written / total_length))
            sys.stdout.flush()
    print()

if __name__ == "__main__":
    download_dump(DUMP_URL, BZ2_FILE)

    # Hacky way to run WikiExtractor
    os.system('python -m wikiextractor.WikiExtractor --no-templates --json --output "json" enwiki-latest-pages-articles.xml.bz2')