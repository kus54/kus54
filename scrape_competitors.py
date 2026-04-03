#!/usr/bin/env python3
"""
Scraping competitors in Sochi/Adler: menu + business details → Excel
Uses Firecrawl for scraping, Claude for structured extraction.
"""

import os
import re
import json
import time
import anthropic
from firecrawl import FirecrawlApp
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment
from openpyxl.utils import get_column_letter

FIRECRAWL_API_KEY = "fc-db3cb07605954ae1b10de5c484265779"
ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")

SITES = [
    "https://familygarden.su/prohinkalisochi/",
    "https://santorinisochi.ru",
    "https://midiynoe-mesto.ru",
    "https://hinkali-tancevali.ru",
    "https://fabrikavkysarest.ru",
    "https://kebab-king.ru",
    "https://big-roll-sochi.ru",
    "https://ysebya.ru",
    "https://fedinadacha.ru",
    "https://parusanamore.ru",
    "https://guri-rest.com",
    "https://sapotliner.ru",
    "https://adler.rvbar.ru",
    "https://ainos-sochi.ru",
    "https://khinkalinaprichale.ru",
    "https://sarmatcafe.ru",
    "https://umi-kitchen.ru",
    "https://torobowling-sochi.ru",
    "https://sochi.nebar.ru",
    "https://hooknrolla.ru",
    "https://malinabar.taplink.ws",
    "https://chaihona-sochi.ru",
    "https://kumkumaadler.online",
    "https://sushilka.online",
    "https://veranda-adler.ru",
    "https://hansyfamily.ru",
    "https://chachapuri23.ru",
    "https://vkusmorya-sochi.ru",
    "https://surfcoffee.ru",
    "https://giorgiosuluguni.ru",
    "https://dragonkp.ru",
    "https://travelers-coffee.com",
    "https://farfor.ru",
    "https://mybox.ru",
    "https://semga.su",
    "https://sushicafe.ru",
    "https://achmabar.ru",
    "https://sochi.cosmosgroup.ru",
    "https://rancho.qr-cafe.ru",
    "https://prichalgroup.ru",
]

firecrawl = FirecrawlApp(api_key=FIRECRAWL_API_KEY)
claude = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None


def scrape_url(url, timeout=30):
    """Scrape a URL via Firecrawl, return markdown text or None."""
    try:
        result = firecrawl.scrape_url(url, formats=["markdown"])
        if result and hasattr(result, 'markdown') and result.markdown:
            return result.markdown
        if result and isinstance(result, dict) and result.get('markdown'):
            return result['markdown']
        return None
    except Exception as e:
        print(f"  [scrape error] {url}: {e}")
        return None


def crawl_site(url, limit=8):
    """Crawl up to `limit` pages of a site via Firecrawl."""
    try:
        result = firecrawl.crawl_url(
            url,
            limit=limit,
            scrape_options={"formats": ["markdown"]}
        )
        pages = []
        if result and hasattr(result, 'data'):
            for page in result.data:
                md = page.markdown if hasattr(page, 'markdown') else page.get('markdown', '')
                src = page.metadata.url if hasattr(page, 'metadata') and hasattr(page.metadata, 'url') else page.get('metadata', {}).get('url', url)
                if md:
                    pages.append({'url': src, 'markdown': md})
        return pages
    except Exception as e:
        print(f"  [crawl error] {url}: {e}")
        # Fall back to single page scrape
        md = scrape_url(url)
        if md:
            return [{'url': url, 'markdown': md}]
        return []


def extract_with_claude(content, site_url):
    """Use Claude to extract menu items and business details from scraped content."""
    if not claude:
        return None

    prompt = f"""Ты извлекаешь данные из текста сайта ресторана/кафе.

Сайт: {site_url}

Текст (markdown):
{content[:8000]}

Извлеки ТОЛЬКО то, что явно указано в тексте:

1. РЕКВИЗИТЫ (если есть):
   - Наименование компании (официальное, как ООО "...", ИП Иванов и т.д.)
   - Форма: ООО / ИП / АО / ПАО / ЗАО (или пустая строка если не найдено)
   - ИНН (10 или 12 цифр, или пустая строка)
   - ОГРН (13 или 15 цифр, или пустая строка)

2. МЕНЮ (все позиции с ценами):
   - Категория (Горячее, Пицца, Салаты, Напитки, Десерты, Суши, Роллы и т.д.)
   - Название блюда
   - Вес/объём (например: 350г, 0.5л, 500мл) или пустая строка
   - Цена (только число, без руб/₽)

Если меню не найдено вообще - верни "NO_MENU".
Если реквизиты не найдены - оставь поля пустыми.

Ответь ТОЛЬКО JSON в формате:
{{
  "company_name": "ООО Пицца Плюс",
  "legal_form": "ООО",
  "inn": "7701234567",
  "ogrn": "",
  "menu": [
    {{"category": "Горячее", "name": "Пицца Маргарита", "weight": "400г", "price": 590}},
    {{"category": "Напитки", "name": "Coca-Cola", "weight": "0.5л", "price": 120}}
  ]
}}

Или если нет меню:
{{"no_menu": true}}
"""

    try:
        response = claude.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        text = response.content[0].text.strip()
        # Extract JSON from response
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception as e:
        print(f"  [claude error]: {e}")
    return None


def search_vk(company_name, site_url):
    """Try to find restaurant on VK and extract menu."""
    # Build search query from domain name
    domain = re.sub(r'https?://', '', site_url).split('/')[0]
    search_terms = domain.replace('-', ' ').replace('.ru', '').replace('.com', '').replace('.su', '').replace('.online', '')

    vk_search_url = f"https://vk.com/search?c[q]={search_terms}+сочи&c[section]=communities"
    print(f"  Searching VK: {vk_search_url}")

    md = scrape_url(vk_search_url)
    if not md:
        return None

    # Extract VK community URLs from search results
    vk_links = re.findall(r'vk\.com/([\w._-]+)', md)
    vk_links = [l for l in vk_links if not l.startswith(('search', 'login', 'feed', 'im', 'photo', 'video', 'music', 'market'))]

    if not vk_links:
        return None

    # Try first few community links
    for link in vk_links[:3]:
        vk_page_url = f"https://vk.com/{link}"
        print(f"  Trying VK page: {vk_page_url}")
        md2 = scrape_url(vk_page_url)
        if md2 and len(md2) > 200:
            data = extract_with_claude(md2, vk_page_url)
            if data and not data.get('no_menu') and data.get('menu'):
                data['source_url'] = vk_page_url
                return data
        time.sleep(1)

    return None


def process_site(site_url):
    """
    Process one site: scrape → extract → VK fallback.
    Returns dict with extracted data or None if no menu found.
    """
    print(f"\n{'='*60}")
    print(f"Processing: {site_url}")

    # Step 1: Crawl the main site
    pages = crawl_site(site_url, limit=8)

    if not pages:
        print("  No pages scraped, trying VK...")
        return search_vk("", site_url)

    # Combine content from all pages, prioritizing menu-related pages
    menu_pages = []
    other_pages = []
    for p in pages:
        url_lower = p['url'].lower()
        if any(kw in url_lower for kw in ['menu', 'меню', 'food', 'блюда', 'catalog', 'dish']):
            menu_pages.append(p)
        else:
            other_pages.append(p)

    # Build combined content: menu pages first, then others
    all_pages = menu_pages + other_pages
    combined = "\n\n---PAGE---\n\n".join(
        f"URL: {p['url']}\n{p['markdown'][:3000]}" for p in all_pages[:5]
    )

    # Step 2: Extract with Claude
    data = extract_with_claude(combined, site_url)

    if data and not data.get('no_menu') and data.get('menu'):
        print(f"  Found {len(data['menu'])} menu items")
        data['source_url'] = site_url
        return data

    # Step 3: VK fallback
    print("  No menu on website, trying VK...")
    vk_data = search_vk("", site_url)
    if vk_data and vk_data.get('menu'):
        print(f"  Found {len(vk_data['menu'])} menu items on VK")
        return vk_data

    print("  No menu found anywhere, skipping.")
    return None


def style_header_row(ws, row=1):
    """Apply header styling to the first row."""
    header_fill = PatternFill(start_color="2B5591", end_color="2B5591", fill_type="solid")
    header_font = Font(color="FFFFFF", bold=True)
    for cell in ws[row]:
        cell.fill = header_fill
        cell.font = header_font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)


def create_excel(results, output_path):
    """Create Excel with 2 sheets: Реквизиты and Меню."""
    wb = Workbook()

    # ── Sheet 1: Реквизиты ──
    ws1 = wb.active
    ws1.title = "Реквизиты"
    headers1 = ["Сайт", "Наименование", "Форма (ООО/ИП)", "ИНН", "ОГРН"]
    ws1.append(headers1)
    style_header_row(ws1)

    for r in results:
        ws1.append([
            r.get('source_url', ''),
            r.get('company_name', ''),
            r.get('legal_form', ''),
            r.get('inn', ''),
            r.get('ogrn', ''),
        ])

    # Auto-width
    col_widths1 = [40, 35, 16, 14, 18]
    for i, w in enumerate(col_widths1, 1):
        ws1.column_dimensions[get_column_letter(i)].width = w
    ws1.row_dimensions[1].height = 30

    # ── Sheet 2: Меню ──
    ws2 = wb.create_sheet("Меню")
    headers2 = ["Сайт", "Наименование компании", "Категория", "Позиция", "Вес/объём", "Цена"]
    ws2.append(headers2)
    style_header_row(ws2)

    for r in results:
        company = r.get('company_name', '') or r.get('source_url', '')
        source = r.get('source_url', '')
        for item in r.get('menu', []):
            price = item.get('price', '')
            # Ensure price is a number
            if price:
                try:
                    price = float(str(price).replace(' ', '').replace(',', '.'))
                    price = int(price) if price == int(price) else price
                except:
                    pass
            ws2.append([
                source,
                company,
                item.get('category', ''),
                item.get('name', ''),
                item.get('weight', ''),
                price,
            ])

    col_widths2 = [40, 35, 20, 40, 12, 10]
    for i, w in enumerate(col_widths2, 1):
        ws2.column_dimensions[get_column_letter(i)].width = w
    ws2.row_dimensions[1].height = 30

    # Freeze header rows
    ws1.freeze_panes = "A2"
    ws2.freeze_panes = "A2"

    wb.save(output_path)
    print(f"\nExcel saved: {output_path}")
    print(f"  Реквизиты: {len(results)} rows")
    print(f"  Меню: {sum(len(r.get('menu',[])) for r in results)} rows")


def main():
    results = []
    failed = []

    for i, site in enumerate(SITES, 1):
        print(f"\n[{i}/{len(SITES)}] {site}")
        try:
            data = process_site(site)
            if data and data.get('menu'):
                results.append(data)
                print(f"  ✓ Added: {data.get('company_name', 'N/A')} — {len(data['menu'])} items")
            else:
                failed.append(site)
                print(f"  ✗ Skipped (no menu)")
        except Exception as e:
            print(f"  ERROR: {e}")
            failed.append(site)

        # Be polite to APIs
        time.sleep(2)

    print(f"\n{'='*60}")
    print(f"Done! Collected data from {len(results)}/{len(SITES)} sites")
    print(f"Skipped: {len(failed)}")
    if failed:
        print("Skipped sites:")
        for s in failed:
            print(f"  - {s}")

    if results:
        create_excel(results, "/home/user/kus54/sochi_competitors.xlsx")
    else:
        print("No data collected!")


if __name__ == "__main__":
    main()
