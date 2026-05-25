import os
import re
import json
import requests
import psycopg2
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse

DB_CONFIG = {
    "host": os.getenv("DB_HOST", "postgres-ai"),
    "port": int(os.getenv("DB_PORT", "5432")),
    "dbname": os.getenv("DB_NAME", "aidacha"),
    "user": os.getenv("DB_USER", "change_me"),
    "password": os.getenv("DB_PASSWORD", "change_me")
}


KEYWORDS = [
    "роза",
    "розы",
    "rose",
    "roses",
    "catalog",
    "каталог",
    "саженцы",
    "plants"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 AI-Dacha-Rose-Agent/0.1"
}

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://ollama:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "gemma3:1b")
AI_LIMIT_PER_RUN = int(os.getenv("AI_LIMIT_PER_RUN", "5"))

def looks_like_rose_page(url: str, text: str) -> bool:
    value = f"{url} {text}".lower()

    rose_url_markers = [
        "/rozy",
        "/roses",
        "/rose",
        "/roza",
        "rozy/",
        "roses/",
        "roza-",
        "rozy-",
        "rose-",
        "роза",
        "розы",
    ]

    bad_markers = [
        "delivery",
        "contact",
        "contacts",
        "payment",
        "return",
        "policy",
        "about",
        "cart",
        "wishlist",
        "compare",
        "gift",
        "dok",
        "job",
        "team",
        "review",
        "peonies",
        "hydrangeas",
        "clematis",
        "gortenziya",
        "piony",
        "klubnika",
    ]

    if any(bad in value for bad in bad_markers):
        return False

    return any(marker in value for marker in rose_url_markers)


def normalize_url(base_url: str, href: str) -> str | None:
    if not href:
        return None

    href = href.strip()

    if href.startswith("#"):
        return None

    if href.startswith("mailto:") or href.startswith("tel:") or href.startswith("javascript:"):
        return None

    full_url = urljoin(base_url, href)
    parsed = urlparse(full_url)

    if parsed.scheme not in ("http", "https"):
        return None

    clean_url = parsed._replace(fragment="").geturl()
    return clean_url


def same_domain(base_url: str, target_url: str) -> bool:
    base_host = urlparse(base_url).netloc.replace("www.", "")
    target_host = urlparse(target_url).netloc.replace("www.", "")
    return base_host == target_host

def classify_page(url: str) -> str:
    value = url.lower()

    product_markers = [
        "/product/",
        "/item/",
    ]

    if any(marker in value for marker in product_markers):
        return "product_card"

    return "category"
    
def normalize_name(name: str) -> str:
    value = name.lower()

    garbage_patterns = [
        r"саженцы",
        r"роза",
        r"розы",
        r"шт",
        r"фото и описание",
        r"описание",
        r"комплект\s*\d*",
        r"чайно-гибридной",
        r"чайно-гибридная",
        r"шраб",
        r"плетистой",
        r"плетистая",
        r"почвопокровной",
        r"почвопокровная",
        r"флорибунда",
        r"английская",
    ]

    for pattern in garbage_patterns:
        value = re.sub(pattern, " ", value)

    value = re.sub(r"\([^)]*\)", " ", value)

    value = re.sub(r"[-–—]\s*\d+\s*$", " ", value)
    value = re.sub(r"\b\d+\b", " ", value)
    value = re.sub(r"[^a-zа-яё0-9\s-]", " ", value)

    value = re.sub(r"\s+", " ", value)

    value = re.sub(r"\s*[-–—]\s*$", " ", value)
    value = re.sub(r"\s+", " ", value)

    return value.strip().title()

def detect_type_from_text(text: str) -> str | None:
    value = text.lower()

    mapping = {
        "чайно-гибрид": "Чайно-гибридная",
        "chayno-gibrid": "Чайно-гибридная",
        "floribunda": "Флорибунда",
        "флорибунд": "Флорибунда",
        "pletist": "Плетистая",
        "плетист": "Плетистая",
        "shrab": "Шраб",
        "шраб": "Шраб",
        "pochvopokrov": "Почвопокровная",
        "почвопокров": "Почвопокровная",
        "angliysk": "Английская",
        "англий": "Английская",
        "park": "Парковая",
        "парков": "Парковая",
        "mini": "Миниатюрная",
        "мини": "Миниатюрная",
    }

    for marker, rose_type in reversed(list(mapping.items())):
        if marker in value:
            return rose_type

    return None


def get_rose_type_id(cur, type_name: str | None):
    if not type_name:
        return None

    cur.execute("""
        SELECT id
        FROM garden_catalog.rose_types
        WHERE name = %s;
    """, (type_name,))

    row = cur.fetchone()
    return row[0] if row else None

def extract_latin_name(title: str) -> str | None:
    matches = re.findall(r"\(([^)]*[A-Za-z][^)]*)\)", title)

    if not matches:
        return None

    return matches[-1].strip()

def extract_rose_from_product_page(url: str) -> dict | None:
    print(f"Extract product: {url}")

    try:
        response = requests.get(url, headers=HEADERS, timeout=60)
        response.raise_for_status()
    except Exception as e:
        print(f"Product fetch error: {e}")
        return None

    soup = BeautifulSoup(response.text, "lxml")

    h1 = soup.find("h1")
    title = h1.get_text(" ", strip=True) if h1 else None

    if not title:
        title_tag = soup.find("title")
        title = title_tag.get_text(" ", strip=True) if title_tag else None

    if not title:
        return None

    img = soup.find("img")
    photo_url = None

    if img and img.get("src"):
        photo_url = normalize_url(url, img.get("src"))

    latin_name = extract_latin_name(title)
    clean_name_ru = normalize_name(title)
    rose_type = detect_type_from_text(f"{title} {url}")

    return {
            "name": title,
            "normalized_name": clean_name_ru.lower(),
            "clean_name_ru": clean_name_ru,
            "latin_name": latin_name,
            "rose_type": rose_type,
            "source_url": url,
            "photo_url": photo_url,
            "description": None,
            "raw_title": title,
            }

def enrich_with_ollama(rose: dict) -> dict:
    prompt = f"""
Ты извлекаешь структурированные данные о сорте розы.

Верни только JSON без пояснений.

Исходные данные:
raw_title: {rose.get("raw_title")}
clean_name_ru: {rose.get("clean_name_ru")}
latin_name: {rose.get("latin_name")}
rose_type: {rose.get("rose_type")}

Формат JSON:
{{
  "clean_name_ru": "...",
  "latin_name": "...",
  "color_text": "...",
  "rose_type": "..."
}}
"""

    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": OLLAMA_MODEL,
                "prompt": prompt,
                "format": "json",
                "stream": False
            },
            timeout=60
        )
        response.raise_for_status()

        data = response.json()
        raw_json = data.get("response")
        print("OLLAMA RAW RESPONSE:")
        print(raw_json)

        if not raw_json:
            return rose

        ai_data = json.loads(raw_json)
        print("OLLAMA PARSED JSON:")
        print(ai_data)

        rose["clean_name_ru"] = ai_data.get("clean_name_ru") or rose.get("clean_name_ru")
        rose["latin_name"] = ai_data.get("latin_name") or rose.get("latin_name")
        rose["color_text"] = ai_data.get("color_text")
        rose["rose_type"] = ai_data.get("rose_type") or rose.get("rose_type")
        rose["normalized_name"] = rose["clean_name_ru"].lower()

        return rose

    except Exception as e:
        print(f"Ollama enrichment error: {e}")
        return rose

def save_rose(cur, rose: dict, source_site: str):
    rose_type_id = get_rose_type_id(cur, rose.get("rose_type"))

    cur.execute("""
        INSERT INTO garden_catalog.roses (
            name,
            normalized_name,
            rose_type_id,
            description,
            source_url,
            source_site,
            photo_url,
            clean_name_ru,
            latin_name,
            color_text,
            raw_title,
            ai_enriched_at,
            updated_at
        )
        VALUES (
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now(), now()
        )
        ON CONFLICT (normalized_name)
        DO UPDATE SET
            updated_at = now(),
            source_url = EXCLUDED.source_url,
            source_site = EXCLUDED.source_site,
            photo_url = COALESCE(garden_catalog.roses.photo_url, EXCLUDED.photo_url),
            clean_name_ru = EXCLUDED.clean_name_ru,
            latin_name = EXCLUDED.latin_name,
            color_text = EXCLUDED.color_text,
            raw_title = EXCLUDED.raw_title,
            ai_enriched_at = now();
    """, (
        rose["name"],
        rose["normalized_name"],
        rose_type_id,
        rose.get("description"),
        rose.get("source_url"),
        source_site,
        rose.get("photo_url"),
        rose.get("clean_name_ru"),
        rose.get("latin_name"),
        rose.get("color_text"),
        rose.get("raw_title"),
    ))

def fetch_links(base_url: str) -> list[str]:
    print(f"Fetching: {base_url}")

    try:
        response = requests.get(
            base_url,
            headers=HEADERS,
            timeout=60
        )
        response.raise_for_status()
    except Exception as e:
        print(f"Fetch error for {base_url}: {e}")
        return []

    soup = BeautifulSoup(response.text, "lxml")

    found_urls = set()

    for a in soup.find_all("a"):
        href = a.get("href")
        text = a.get_text(" ", strip=True)

        full_url = normalize_url(base_url, href)

        if not full_url:
            continue

        if not same_domain(base_url, full_url):
            continue

        if looks_like_rose_page(full_url, text):
            found_urls.add(full_url)

    return sorted(found_urls)


def save_page(cur, source_id: int, url: str, page_type: str = "candidate"):
    cur.execute("""
        INSERT INTO garden_catalog.rose_source_pages (
            source_id,
            url,
            page_type,
            last_seen_at
        )
        VALUES (
            %s,
            %s,
            %s,
            now()
        )
        ON CONFLICT (url)
        DO UPDATE SET
            last_seen_at = now(),
            page_type = EXCLUDED.page_type;
    """, (source_id, url, page_type))


def main():
    print("Rose agent started")

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO garden_catalog.rose_agent_runs (
            started_at,
            status
        )
        VALUES (
            now(),
            'running'
        )
        RETURNING id;
    """)

    run_id = cur.fetchone()[0]
    conn.commit()

    found_count = 0
    ai_count = 0

    try:
        cur.execute("""
            SELECT id, site_name, base_url
            FROM garden_catalog.rose_sources
            WHERE is_active = true;
        """)

        sources = cur.fetchall()

        print(f"Found {len(sources)} sources")

        for source_id, site_name, base_url in sources:
            print("--------------")
            print(f"Source: {site_name} | {base_url}")

            urls = fetch_links(base_url)

            print(f"Candidate pages found: {len(urls)}")

            for url in urls:
                page_type = classify_page(url)
                print(f"  + [{page_type}] {url}")
                save_page(cur, source_id, url, page_type)
                found_count += 1

                if page_type == "product_card":
                    rose = extract_rose_from_product_page(url)
                    if rose:
                        if ai_count < AI_LIMIT_PER_RUN:
                            rose = enrich_with_ollama(rose)
                            ai_count += 1

                        save_rose(cur, rose, site_name)

            cur.execute("""
                UPDATE garden_catalog.rose_sources
                SET last_crawled_at = now()
                WHERE id = %s;
            """, (source_id,))

            conn.commit()

        cur.execute("""
            UPDATE garden_catalog.rose_agent_runs
            SET
                finished_at = now(),
                status = 'success',
                found_count = %s
            WHERE id = %s;
        """, (found_count, run_id))

        conn.commit()

    except Exception as e:
        conn.rollback()

        cur.execute("""
            UPDATE garden_catalog.rose_agent_runs
            SET
                finished_at = now(),
                status = 'error',
                error_message = %s
            WHERE id = %s;
        """, (str(e), run_id))

        conn.commit()

        print(f"Agent error: {e}")

    finally:
        cur.close()
        conn.close()

    print(f"Rose agent finished. Found pages: {found_count}")


if __name__ == "__main__":
    main()

