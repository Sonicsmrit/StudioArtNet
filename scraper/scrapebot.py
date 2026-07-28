from camoufox.async_api import AsyncCamoufox
import asyncio, aiohttp
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent

New_Data_dir = root_dir / "Images"


anime_dict = {
    "MAPPA": ["Jujutsu Kaisen", "Chainsaw Man", "Attack on Titan The Final Season"],
    "ufotable": ["Demon Slayer","Fate/Stay Night: Unlimited Blade Works", "Fate/Zero", "Fate/Zero S2"],
    "Trigger": ["Kill la Kill","Little Witch Academia", "Cyberpunk: Edgerunners"],
    "Wit Studio": ["Attack on Titan","Attack on Titan Season 2", "Vinland Saga","Ranking of Kings"],
    "Bones": ["My Hero Academia","Mob Psycho 100","Mob Psycho 100 II", "Fullmetal Alchemist: Brotherhood"],
    "Madhouse":["One Punch Man","Hunter x Hunter (2011)","Overlord","Overlord II"],
    "Kyoto Animation": ["Violet Evergarden","Hyouka", "Miss Kobayashi's Dragon Maid", "Miss Kobayashi's Dragon Maid S"]
}

studio_and_img = {}

async def scrape_stuff():
    
    async with AsyncCamoufox() as browser:

        page = await browser.new_page()

        for keys, val in anime_dict.items():
            all_images = set()

            for i in range(len(val)):

                await page.goto("https://fancaps.net/search.php")

                await page.wait_for_load_state("networkidle")

                accept_cookie = page.locator("#accept-btn")

                if await accept_cookie.is_visible():
                    await accept_cookie.click()

                await page.click("#MoviesCB")

                await page.click("#TVCB")

                await page.locator(".form-control").press_sequentially(anime_dict[keys][i])
                
                await page.click("#submit")

                await page.get_by_role("link", name=anime_dict[keys][i], exact=True).click()

                while True:

                    images = await page.locator(".imageFade").evaluate_all(
                        "imgs => imgs.map(img => img.src)"
                    )

                    all_images.update(images)

                    old = page.url.split("#")[0]

                    await page.get_by_role("link", name="Next").click()

                    await page.wait_for_load_state("networkidle")

                    new = page.url.split("#")[0]

                    if old == new:
                        break

            print(all_images)
            studio_and_img[keys] = list(all_images)


HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Referer": "https://fancaps.net/",
}

async def download_image(session, studio, url):
    try:
        async with session.get(url, headers=HEADERS) as response:

            if response.status != 200:
                print(f"FAILED ({response.status}): {url}")
                return

            data = await response.read()
            filename = url.split("/")[-1].split("?")[0]  # strip query params too

            with open(studio / filename, "wb") as f:
                f.write(data)

    except Exception as e:
        print(f"Exception on {url}: {e}")

async def download_images(session):

    tasks = []

    for key_studio, val_urls in studio_and_img.items():
        STUDIO_DIR = New_Data_dir / key_studio

        STUDIO_DIR.mkdir(parents=True, exist_ok=True)

        for url in val_urls:

            tasks.append(
                asyncio.create_task(download_image(session, STUDIO_DIR, url))
            )

    await asyncio.gather(*tasks)


async def main():

    await scrape_stuff()

    async with aiohttp.ClientSession() as session:
        await download_images(session)


if __name__ == "__main__":
    asyncio.run(main())