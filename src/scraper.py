import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from .models import Pokemon
from .database import SessionLocal

class PokemonScraper:
    def __init__(self):

        # Initialize WebDriver
        chromedriver = os.getenv("CHROMEDRIVER_PATH", "/usr/lib/chromium-browser/chromedriver")
        service = Service(chromedriver)  # Update with your chromedriver path
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
                "prefs", {
                    # block image loading
                    "profile.managed_default_content_settings.images": 2,
                }
            )
        options.add_argument('--headless')  # Run in headless mode
        options.add_argument("--no-sandbox")
        options.add_argument('--disable-gpu')
        options.add_argument('--disable-extensions')
        options.add_argument("--disable-dev-shm-usage")

        self.base_url = "https://pokemondb.net/pokedex/national"
        self.session = SessionLocal()
        self.driver = webdriver.Chrome(service=service, options=options)

    def scrape_pokemon(self, limit=10):
        try:
            # Navigate to the Pokédex page
            self.driver.set_page_load_timeout(60)
            self.driver.get(self.base_url)

            # After loading all desired Pokémon, find all Pokémon card elements
            # Wait up to 10 seconds for the elements to be present
            pokemon_cards = WebDriverWait(self.driver, 10).until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "infocard"))
            )
            print(f"Found {len(pokemon_cards)} Pokémon cards.")

            # Limit to first 10 Pokémon for demonstration purposes
            pokemon_cards = pokemon_cards[:limit]

            # Extract Pokémon data
            for card in pokemon_cards:
                name = card.find_element(By.CLASS_NAME, "ent-name").text

                types = card.find_elements(By.CLASS_NAME, "itype")
                types = [t.text for t in types]

                element = card.find_element(By.XPATH, ".//a[contains(@href, '/pokedex/')]")
                link = element.get_attribute("href")

                self.driver.get(link)

                vital = WebDriverWait(self.driver, 10).until(
                    EC.presence_of_all_elements_located((By.CLASS_NAME, "vitals-table"))
                )

                weight = vital[0].find_element(By.XPATH, ".//tr[th[text()='Weight']]/td").text
                height = vital[0].find_element(By.XPATH, ".//tr[th[text()='Height']]/td").text
                number = vital[0].find_element(By.XPATH, ".//tr[th[text()='National №']]/td").text

                abilities_td = vital[0].find_element(By.XPATH, ".//tr[th[text()='Abilities']]/td")
                abilities = [a.text for a in abilities_td.find_elements(By.TAG_NAME, "a")]

                pokemon_entry = Pokemon(
                    id=number,
                    name=name,
                    types=','.join(types),
                    height=height,
                    weight=weight,
                    abilities=','.join(abilities)
                )
                self.session.merge(pokemon_entry)
                self.driver.back()

        finally:
            self.session.commit()
            self.driver.quit()