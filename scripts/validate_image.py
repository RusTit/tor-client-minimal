import logging
import tarfile
import io
import re
from re import Match
import requests
from typing import Final, Optional

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

INDEX_URL: Final[str] = (
    "https://dl-cdn.alpinelinux.org/alpine/edge/community/x86_64/APKINDEX.tar.gz"
)


def get_index() -> str:
    url = INDEX_URL
    logger.debug(f"Fetching index from {url}")

    resp = requests.get(url)
    resp.raise_for_status()

    logger.debug("Index fetched successfully")

    logger.debug("Parsing index")
    with tarfile.open(fileobj=io.BytesIO(resp.content), mode="r:gz") as tar:
        index = tar.extractfile("APKINDEX").read().decode()
    return index


def get_version(pkg_name: str, blocks: list[str]) -> Optional[str]:
    logger.debug(f"Looking up package {pkg_name}")
    for b in blocks:
        if f"P:{pkg_name}\n" in b:
            for line in b.splitlines():
                if line.startswith("V:"):
                    return line[2:]
    logger.warning(f"No version found for {pkg_name}")
    return None


README_FILENAME: Final[str] = "README.md"


def create_package_version_line(m: Match[str], index_blocks: list[str]) -> str:
    package_name = m.group("name")
    package_version = m.group("version")
    logger.info(f"Package {package_name} version {package_version}")
    package_version_in_index = get_version(package_name, index_blocks)
    if package_version_in_index is None:
        raise RuntimeError(f"package version {package_name} not found!")
    if package_version != package_version_in_index:
        logger.info(
            f"Version {package_version} does not match version {package_version_in_index}"
        )
        package_version = package_version_in_index
    return f"- **{package_name}:** `{package_version}`\n"


def get_processed_readme_lines(index_blocks: list[str]) -> list[str]:
    result: list[str] = []
    line_re = re.compile(
        r"^- \*\*(?P<name>[a-zA-Z0-9._+-]+):\*\*\s+`(?P<version>[^`]+)`$"
    )
    is_packages_block = False
    with open(README_FILENAME, "r", encoding="utf-8", newline="") as fh:
        for line in fh:
            if "Versions" in line:
                is_packages_block = True
            elif is_packages_block and "---" in line:
                is_packages_block = False

            if not is_packages_block:
                result.append(line)
            else:
                m = line_re.match(line)
                if m:
                    line = create_package_version_line(m, index_blocks)
                result.append(line)

    return result


def save_readme_lines(readme_lines: list[str]) -> None:
    with open(README_FILENAME, "w", encoding="utf-8", newline="") as fh:
        fh.writelines(readme_lines)


def main() -> None:
    logger.info("Starting validation")
    index = get_index()
    blocks = index.split("\n\n")
    readme_lines = get_processed_readme_lines(blocks)
    save_readme_lines(readme_lines)
    logger.info("Validation finished")


if __name__ == "__main__":
    main()
