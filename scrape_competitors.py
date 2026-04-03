#!/usr/bin/env python3
"""
Scraping competitors in Sochi/Adler: menu + business details → Excel

ЗАПУСК ЛОКАЛЬНО:
  pip install firecrawl-py openpyxl anthropic
  export ANTHROPIC_API_KEY=sk-ant-...
  python3 scrape_competitors.py

Требует открытого интернета (api.firecrawl.dev + сайты конкурентов).
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


def scrape_url(url):
    """Scrape a single URL via Firecrawl, return markdown or None."""
    try:
        result = firecrawl.scrape(url, formats=["markdown"])
        if hasattr(result, 'markdown') and result.markdown:
            return result.markdown
        if isinstance(result, dict) and result.get('markdown'):
            return result['markdown']
        return None
    except Exception as e:
        print(f"  [scrape error] {url}: {e}")
        return None


def crawl_site(url, limit=8):
    """Crawl up to `limit` pages of a site, return list of {url, markdown}."""
    try:
        result = firecrawl.crawl(
            url,
            limit=limit,
            scrape_options={"formats": ["markdown"]}
        )
        pages = []
        data = getattr(result, 'data', None) or (result.get('data') if isinstance(result, dict) else [])
        if data:
            for page in data:
                md = getattr(page, 'markdown', None) or (page.get('markdown', '') if isinstance(page, dict) else '')
                meta = getattr(page, 'metadata', None) or (page.get('metadata', {}) if isinstance(page, dict) else {})
                src = getattr(meta, 'url', None) or (meta.get('url', url) if isinstance(meta, dict) else url)
                if md:
                    pages.append({'url': src, 'markdown': md})
        return pages
    except Exception as e:
        print(f"  [crawl error] {url}: {e}")
        # Fallback to single-page scrape
        md = scrape_url(url)
        if md:
            return [{'url': url, 'markdown': md}]
        return []


def extract_with_claude(content, site_url):
    """Use Claude Haiku to extract menu + business details from scraped text."""
    if not claude:
        print("  [warn] ANTHROPIC_API_KEY not set, skipping Claude extraction")
        return None

    prompt = f"""Ты извлекаешь данные из текста сайта ресторана/кафе.

Сайт: {site_url}

Текст (markdown):
{content[:8000]}

Извлеки ТОЛЬКО то, что явно указано в тексте:

1. РЕКВИЗИТЫ (если есть):
   - Наименование компании (официальное: ООО "...", ИП Иванов и т.д.)
   - Форма: ООО / ИП / АО / ПАО / ЗАО (или пустая строка)
   - ИНН (10 или 12 цифр, или пустая строка)
   - ОГРН (13 или 15 цифр, или пустая строка)

2. МЕНЮ (все позиции с ценами):
   - Категория (Горячее, Пицца, Салаты, Напитки, Десерты, Суши, Роллы и т.д.)
   - Название блюда
   - Вес/объём (например: 350г, 0.5л) или пустая строка
   - Цена (только число без руб/₽)

Если меню не найдено — верни {{"no_menu": true}}.
Если реквизиты не найдены — оставь поля пустыми.

Ответь ТОЛЬКО валидным JSON:
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
"""

    try:
        response = claude.messages.create(
            model="claude-haiku-4-5-20251001",
            max_tokens=4000,
            messages=[{"role": "user", "content": prompt}]
        )
        text = response.content[0].text.strip()
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if json_match:
            return json.loads(json_match.group())
    except Exception as e:
        print(f"  [claude error]: {e}")
    return None


def search_vk(site_url):
    """Try to find the restaurant on VK and extract menu."""
    domain = re.sub(r'https?://', '', site_url).split('/')[0]
    search_term = re.sub(r'\.(ru|com|su|online|ws)$', '', domain).replace('-', ' ').replace('.', ' ')

    vk_search_url = f"https://vk.com/search?c[q]={search_term}+сочи&c[section]=communities"
    print(f"  VK search: {vk_search_url}")

    md = scrape_url(vk_search_url)
    if not md:
        return None

    # Find VK community slugs in search results
    vk_links = re.findall(r'(?:vk\.com/|href=["\']/)([a-zA-Z0-9._-]{3,40})', md)
    skip = {'search', 'login', 'feed', 'im', 'photo', 'video', 'music', 'market',
            'away', 'wall', 'topic', 'note', 'doc', 'poll', 'app', 'link'}
    vk_links = [l for l in dict.fromkeys(vk_links) if l not in skip and not l.startswith('id')]

    for slug in vk_links[:3]:
        vk_url = f"https://vk.com/{slug}"
        print(f"  Trying VK: {vk_url}")
        md2 = scrape_url(vk_url)
        if md2 and len(md2) > 300:
            data = extract_with_claude(md2, vk_url)
            if data and not data.get('no_menu') and data.get('menu'):
                data['source_url'] = vk_url
                return data
        time.sleep(1)

    return None


def process_site(site_url):
    """
    Full pipeline for one site:
      1. Crawl website → extract
      2. If no menu → VK fallback
      3. If still no menu → return None (skip)
    """
    print(f"\n{'='*60}")
    print(f"Processing: {site_url}")

    # Step 1: Crawl main site
    pages = crawl_site(site_url, limit=8)

    if pages:
        # Prioritise pages whose URL contains menu-related keywords
        menu_pages = [p for p in pages if any(
            kw in p['url'].lower() for kw in ['menu', 'меню', 'food', 'блюд', 'catalog', 'dish', 'eda']
        )]
        other_pages = [p for p in pages if p not in menu_pages]
        ordered = menu_pages + other_pages

        combined = "\n\n---PAGE---\n\n".join(
            f"URL: {p['url']}\n{p['markdown'][:3000]}" for p in ordered[:5]
        )
        data = extract_with_claude(combined, site_url)
        if data and not data.get('no_menu') and data.get('menu'):
            print(f"  ✓ {len(data['menu'])} menu items from website")
            data['source_url'] = site_url
            return data

    # Step 2: VK fallback
    print("  No menu on website → trying VK...")
    vk_data = search_vk(site_url)
    if vk_data and vk_data.get('menu'):
        print(f"  ✓ {len(vk_data['menu'])} menu items from VK")
        return vk_data

    print("  ✗ No menu found, skipping.")
    return None


def style_header_row(ws):
    fill = PatternFill(start_color="2B5591", end_color="2B5591", fill_type="solid")
    font = Font(color="FFFFFF", bold=True)
    for cell in ws[1]:
        cell.fill = fill
        cell.font = font
        cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)


def create_excel(results, output_path):
    wb = Workbook()

    # Sheet 1: Реквизиты
    ws1 = wb.active
    ws1.title = "Реквизиты"
    ws1.append(["Сайт", "Наименование", "Форма (ООО/ИП)", "ИНН", "ОГРН"])
    style_header_row(ws1)
    for r in results:
        ws1.append([
            r.get('source_url', ''),
            r.get('company_name', ''),
            r.get('legal_form', ''),
            r.get('inn', ''),
            r.get('ogrn', ''),
        ])
    for i, w in enumerate([40, 35, 16, 14, 18], 1):
        ws1.column_dimensions[get_column_letter(i)].width = w
    ws1.row_dimensions[1].height = 30
    ws1.freeze_panes = "A2"

    # Sheet 2: Меню
    ws2 = wb.create_sheet("Меню")
    ws2.append(["Сайт", "Наименование компании", "Категория", "Позиция", "Вес/объём", "Цена"])
    style_header_row(ws2)
    for r in results:
        company = r.get('company_name', '') or r.get('source_url', '')
        source = r.get('source_url', '')
        for item in r.get('menu', []):
            price = item.get('price', '')
            if price:
                try:
                    price = float(str(price).replace(' ', '').replace(',', '.'))
                    price = int(price) if price == int(price) else price
                except Exception:
                    pass
            ws2.append([source, company,
                        item.get('category', ''),
                        item.get('name', ''),
                        item.get('weight', ''),
                        price])
    for i, w in enumerate([40, 35, 20, 40, 12, 10], 1):
        ws2.column_dimensions[get_column_letter(i)].width = w
    ws2.row_dimensions[1].height = 30
    ws2.freeze_panes = "A2"

    wb.save(output_path)
    menu_count = sum(len(r.get('menu', [])) for r in results)
    print(f"\nExcel saved: {output_path}")
    print(f"  Реквизиты: {len(results)} компаний")
    print(f"  Меню: {menu_count} позиций")


def main():
    if not ANTHROPIC_API_KEY:
        print("ВНИМАНИЕ: ANTHROPIC_API_KEY не задан — извлечение данных работать не будет.")
        print("Задайте: export ANTHROPIC_API_KEY=sk-ant-...\n")

    results = []
    failed = []

    for i, site in enumerate(SITES, 1):
        print(f"\n[{i}/{len(SITES)}]")
        try:
            data = process_site(site)
            if data and data.get('menu'):
                results.append(data)
            else:
                failed.append(site)
        except Exception as e:
            print(f"  ERROR: {e}")
            failed.append(site)
        time.sleep(2)  # вежливая пауза между сайтами

    print(f"\n{'='*60}")
    print(f"Итог: данные собраны с {len(results)}/{len(SITES)} сайтов")
    if failed:
        print(f"Пропущено ({len(failed)}):")
        for s in failed:
            print(f"  - {s}")

    if results:
        create_excel(results, "sochi_competitors.xlsx")
    else:
        print("Данные не собраны — проверь ключи API и доступ к интернету.")


if __name__ == "__main__":
    main()
