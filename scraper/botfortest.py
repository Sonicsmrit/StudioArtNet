##scrape for validation and testing datasets
from camoufox.async_api import AsyncCamoufox
import asyncio, base64
from pathlib import Path

root_dir = Path(__file__).resolve().parent.parent

New_Data_dir = root_dir / "Validation Data"

anime_dict = {
    "MAPPA": ["Dorohedoro"],
    "ufotable": ["God Eater"],
    "Trigger": ["Space Patrol Luluco"],
    "Wit Studio": ["Kabaneri of the Iron Fortress"],
    "Bones": ["Noragami"],
    "Madhouse":["Parasyte -the maxim-"],
    "Kyoto Animation": ["Love, Chunibyo & Other Delusions!"]

}

studio_and_img = {}

async def scrape_stuff(page):

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


async def download_image(page, studio, url, sem):
    async with sem:
        try:
            b64_data = await page.evaluate(
                """async (url) => {
                    const res = await fetch(url);
                    if (!res.ok) return null;
                    const buf = await res.arrayBuffer();
                    let binary = '';
                    const bytes = new Uint8Array(buf);
                    for (let i = 0; i < bytes.length; i++) {
                        binary += String.fromCharCode(bytes[i]);
                    }
                    return btoa(binary);
                }""",
                url,
            )

            if b64_data is None:
                print(f"FAILED: {url}")
                return

            
            data = base64.b64decode(b64_data)

            filename = url.split("/")[-1].split("?")[0]

            with open(studio / filename, "wb") as f:
                f.write(data)

        except Exception as e:
            print(f"Exception on {url}: {e}")


async def download_images(page):

    sem = asyncio.Semaphore(6)
    tasks = []

    for key_studio, val_urls in studio_and_img.items():

        STUDIO_DIR = New_Data_dir / key_studio

        STUDIO_DIR.mkdir(parents=True, exist_ok=True)

        for url in val_urls:
            tasks.append(asyncio.create_task(download_image(page, STUDIO_DIR, url, sem)))

    await asyncio.gather(*tasks)


async def main():

    async with AsyncCamoufox() as browser:
        page = await browser.new_page()

        await scrape_stuff(page)

        await download_images(page)



if __name__ == "__main__":
    asyncio.run(main())