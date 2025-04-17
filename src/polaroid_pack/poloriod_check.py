from playwright.async_api import async_playwright
import json
import os
import asyncio

# ==== CONFIGURATION ====
PRODUCT_URL = "https://item.taobao.com/item.htm?id=790218356106"
STATE_FILE = "taobao_state.json"

# ==== MAIN FUNCTION ====
async def check_taobao_stock():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)

        try:
            # First-time login: no storage state yet
            context = await browser.new_context()
            page = await context.new_page()
            print("[!] Please log in to Taobao manually...")
            await page.goto("https://login.taobao.com")
            await page.wait_for_timeout(30000)  # give you 30 seconds to log in manually

            print("[*] Saving login state...")
            await context.storage_state(path=STATE_FILE)
        finally:
            await browser.close()


async def extract_stock_info(page):
    items = await page.query_selector_all("div[class*='valueItem']")

    stock_info = []
    for item in items:
        class_name = await item.get_attribute("class")
        span = await item.query_selector("span")
        if not span:
            continue
        style_name = await span.get_attribute("title") or await span.inner_text()
        
        if "预计" in style_name:
            continue
            
        disabled = 'isDisabled' in class_name if class_name else False

        stock_info.append({
            "style": style_name,
            "in_stock": not disabled
        })

    return stock_info


async def fetch_stock_data():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        try:
            context = await browser.new_context(storage_state=STATE_FILE)
            page = await context.new_page()

            print("[*] Navigating to product page...")
            await page.goto(PRODUCT_URL)
            await page.wait_for_timeout(5000)

            stock_info = await extract_stock_info(page)
            return stock_info
        finally:
            await browser.close()


def display_stock_info(stock_info):
    if not stock_info:
        print("[!] No stock information available.")
        return

    print("\n[+] Stock status:")
    for entry in stock_info:
        print(f"- {entry['style']}: {'有貨' if entry['in_stock'] else '缺貨'}")


def register_polaroid_check_commands(bot):
    @bot.hybrid_command()
    async def check_stock(ctx):
        '''
        Check stock for Taobao
        '''
        await ctx.send("Checking stock...")
        try:
            stock_data = await fetch_stock_data()
            
            if isinstance(stock_data, list) and stock_data:
                stock_list = []
                for item in stock_data:
                    style = item.get("style", "Unknown Style")
                    in_stock = item.get("in_stock", False)
                    stock_list.append(f"{style}: {'有貨' if in_stock else '缺貨'}")
                stock_message = "\n".join(stock_list)
                await ctx.send(f"Stock List:\n```\n{stock_message}\n```")
            else:
                await ctx.send("No stock data available.")
        except Exception as e:
            await ctx.send(f"Error: {e}")
            print(f"Error during stock check: {e}")


if __name__ == "__main__":
    async def main():
        if not os.path.exists(STATE_FILE):
            await check_taobao_stock()

        stock_info = await fetch_stock_data()
        display_stock_info(stock_info)

    asyncio.run(main())