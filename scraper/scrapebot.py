from playwright.sync_api import sync_playwright
from camoufox.async_api import AsyncCamoufox
import asyncio

anime_dict = {
    "MAPPA": ["Jujutsu Kaisen", "Chainsaw Man", "Attack on Titan The Final Season"],
    "ufotable": ["Demon Slayer","Fate/Stay Night: Unlimited Blade Works", "Fate/Zero", "Fate/Zero S2"],
    "Trigger": ["Kill la Kill","Little Witch Academia", "Cyberpunk: Edgerunners"],
    "Wit Studio": ["Attack on Titan","Attack on Titan Season 2", "Vinland Saga","Ranking of Kings"],
    "Bones": ["My Hero Academia","Mob Psycho 100","Mob Psycho 100 II", "Fullmetal Alchemist: Brotherhood"],
    "Madhouse":["One Punch Man","Hunter x Hunter (2011)","Overlord","Overlord II"],
    "Kyoto Animation": ["Violet Evergarden","Hyouka", "Miss Kobayashi's Dragon Maid", "Miss Kobayashi's Dragon Maid S"]
}

async def scrape_stuff():
    
    async with AsyncCamoufox() as browser:

        page = await browser.new_page()

        for keys, val in anime_dict.items():
            for i in range(len(val)):
                await page.goto("https://fancaps.net/search.php")

                await page.wait_for_timeout(3000)

                accept_cookie = page.locator("#accept-btn")

                if await accept_cookie.is_visible():
                    await accept_cookie.click()

                await page.click("#MoviesCB")

                await page.click("#TVCB")

                await page.locator(".form-control").press_sequentially(anime_dict[keys][i])
                
                await page.click("#submit")

                await page.get_by_role("link", name=anime_dict[keys][i], exact=True).click()



asyncio.run(scrape_stuff())