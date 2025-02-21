from selenium import webdriver 
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait 
from selenium.webdriver.support import expected_conditions as EC 
import time 
import csv

# Setup Selenium WebDriver (Chrome) 
options = webdriver.ChromeOptions() 
options.add_argument("--headless")  # Run without opening browser 
options.add_argument("--disable-blink-features=AutomationControlled")  # Avoid detection 
driver = webdriver.Chrome(options=options)

# Output CSV file
output_file = "zameen_agents.csv"

# Write headers to CSV file
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.writer(f)
    writer.writerow(["Name", "Category", "Company", "Phone Number", "Mobile Number", "Sales Properties", "Rental Properties", "Profile Link"])

# Loop through all pages (Adjust range as needed)
for page in range(1, 121):  # Scraping 120 pages (~1,200 agents)
    print(f"Scraping Page {page}...")  
    url = f"https://www.zameen.com/agents/Lahore-1/?page={page}"
    driver.get(url)
    time.sleep(5)  # Allow page to load

    # Find all agent profile links
    agent_links = driver.find_elements(By.CLASS_NAME, "agent-listing-card_cardListingItem__aX-UY")
    profile_urls = [agent.get_attribute("href") for agent in agent_links]

    for profile_url in profile_urls:
        driver.get(profile_url)
        time.sleep(5)  # Let profile page load

        try:
            # Extract Name
            name = driver.find_element(By.CLASS_NAME, "heading_h5__3K7ad").text.strip()
        except:
            name = "NA"

        try:
            # Extract Category (Titanium Plus, etc.)
            category = driver.find_element(By.XPATH, '//span[@class="fw-700"]').text.strip()
        except:
            category = "NA"

        try:
            # Extract Company Name
            company = driver.find_element(By.CLASS_NAME, "heading_h1__KZ8SV").text.strip()
        except:
            company = "NA"

        try:
            # Click the "Call" button to reveal numbers
            call_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "staff-card_callBtn__188RX"))
            )
            call_button.click()
            time.sleep(3)  # Give some time for number popup

            # Extract Mobile Number
            mobile_number = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "contact-popup_numberchip__24E__"))
            ).text.strip()
        except:
            mobile_number = "NA"

        try:
            # Extract Phone Number (if available)
            phone_number = driver.find_elements(By.CLASS_NAME, "contact-popup_numberchip__24E__")
            phone_number = phone_number[1].text.strip() if len(phone_number) > 1 else "NA"
        except:
            phone_number = "NA"

        try:
            # Extract Sales Properties (View All link)
            sales_properties_link = driver.find_element(By.XPATH, '//a[contains(text(), "View All") and contains(@href, "Homes")]')
            sales_properties = sales_properties_link.get_attribute("href")
        except:
            sales_properties = "NA"

        try:
            # Extract Rental Properties (View All link)
            rental_properties_link = driver.find_element(By.XPATH, '//a[contains(text(), "View All") and contains(@href, "Rentals")]')
            rental_properties = rental_properties_link.get_attribute("href")
        except:
            rental_properties = "NA"

        # Save data to CSV
        with open(output_file, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([name, category, company, phone_number, mobile_number, sales_properties, rental_properties, profile_url])

        print(f"✅ Scraped: {name} | {category} | {company} | {mobile_number} | {phone_number} | {sales_properties} | {rental_properties}")

# Close WebDriver
driver.quit()

print("✅ Scraping completed! Data saved in 'zameen_agents.csv'.")
