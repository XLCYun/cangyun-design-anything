import argparse
import json
import unicodedata
from urllib.parse import urljoin
from urllib.request import urlopen


CATALOG_URL = "https://xlcyun.github.io/cangyun-design-anything-examples/catalog/"
CATEGORIES = ("ppt", "ui", "paper")
SEARCH_FIELDS = ("title", "style", "description")


def normalize(text):
    return unicodedata.normalize("NFKC", text).lower()


def search_catalog(entries, terms, limit, catalog_url):
    matches = []
    for example in entries:
        text = normalize(" ".join(example[field] for field in SEARCH_FIELDS))
        score = sum(term in text for term in terms)
        if score:
            matches.append((score, example))
    matches.sort(key=lambda match: match[0], reverse=True)

    results = []
    for _, example in matches[:limit]:
        description = " ".join(example["description"].split())
        if len(description) > 240:
            description = description[:240].rstrip() + "…"
        results.append({
            "title": example["title"],
            "style": example["style"],
            "description": description,
            "cover": urljoin(catalog_url, example["cover"]),
            "detail": urljoin(catalog_url, example["detail"]),
            "page": urljoin(catalog_url, example["page"]),
        })
    return results


def main():
    parser = argparse.ArgumentParser(description="按类别和关键词检索 Design Anything 风格示例")
    parser.add_argument("--category", required=True, choices=CATEGORIES)
    parser.add_argument("--query", required=True, help="用空格分隔关键词")
    parser.add_argument("--limit", type=int, default=3, help="最多返回的示例数，默认为 3")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit 必须是正整数")
    terms = set(normalize(args.query).split())
    if not terms:
        parser.error("--query 至少需要一个关键词")

    try:
        with urlopen(f"{CATALOG_URL}{args.category}.json", timeout=15) as response:
            entries = json.load(response)
            catalog_url = response.geturl()
        if not isinstance(entries, list):
            raise ValueError("索引应为 JSON 数组")
        results = search_catalog(entries, terms, args.limit, catalog_url)
    except (OSError, ValueError, TypeError, KeyError) as error:
        parser.exit(1, f"无法检索 {args.category} 示例。{error}\n")

    print(json.dumps(results, ensure_ascii=False, separators=(",", ":")))


if __name__ == "__main__":
    main()
