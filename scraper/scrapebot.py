from playwright.sync_api import sync_playwright

anime_dict = {
    "MAPPA": ["Jujutsu Kaisen", "Chainsaw Man", "Attack on Titan Final Season"],
    "ufotable": ["Demon Slayer","Fate/Stay Night: Unlimited Blade Works", "Fate/Zero", "Fate/Zero S2"],
    "Trigger": ["Kill la Kill","Little Witch Academia", "Cyberpunk Edgerunners"],
    "Wit Studio": ["Attack on Titan","Attack on Titan season 2", "Vinland Saga","Ranking of Kings"],
    "Bones": ["My Hero Academia","Mob Psycho 100","Mob Psycho 100 II", "Fullmetal Alchemist: Brotherhood"],
    "Madhouse":["One Punch Man","Hunter x Hunter","Overlord","Overlord II"],
    "Kyoto Animation": ["Violet Evergarden","Hyouka", "Miss Kobayashi's Dragon Maid", "Miss Kobayashi's Dragon Maid S"]
}

def scrape_stuff():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)

        page = browser.new_page()
        page.goto("https://fancaps.net/search.php")
        page.click("#accept-btn")
        page.locator(".form-control").press_sequentially("Demon Slayer")
        page.wait_for_timeout(3000)
        page.click("#submit")
        
        page.wait_for_timeout(100000)

scrape_stuff()