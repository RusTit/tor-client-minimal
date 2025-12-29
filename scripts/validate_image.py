import logging
import tarfile
import io
import requests
from typing import Final, Optional

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

INDEX_URL: Final[str] = "https://dl-cdn.alpinelinux.org/alpine/edge/community/x86_64/APKINDEX.tar.gz"

def get_index():
    url = INDEX_URL
    logger.debug(f"Fetching index from {url}")

    resp = requests.get(url)
    resp.raise_for_status()

    logger.debug("Index fetched successfully")

    logger.debug("Parsing index")
    with tarfile.open(fileobj=io.BytesIO(resp.content), mode="r:gz") as tar:
        index = tar.extractfile("APKINDEX").read().decode()
    return index

def get_version(pkg_name, blocks) -> Optional[str]:
    for b in blocks:
        if f"P:{pkg_name}\n" in b:
            for line in b.splitlines():
                if line.startswith("V:"):
                    return line[2:]
    return None

def get_readme_content() -> list[str]:
    result: list[str] = []
    is_packages_block = False
    with open("README.md", "r") as fh:
        line = fh.readline()

    return result

def main() -> None:
    logger.info("Starting validation")
    index = get_index()
    blocks = index.split("\n\n")
    tor_version = get_version("tor", blocks)
    lyrebird_version = get_version("lyrebird", blocks)
    logger.info("Validation finished")


if __name__ == "__main__":
    main()