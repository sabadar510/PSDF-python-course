import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

def scrape_customer_reviews(airline_name, total_pages=5):
    # Skytrax par har airline ka URL format lowercase mein hota hai
    airline_slug = airline_name.lower().replace(" ", "-")
    
    # User-Agent lagana zaroori hai taake website request block na kare
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    
    reviews_data = []
    
    print(f"--- {airline_name} ke Customer Reviews ki Scraping Shuru Ho Rahi Hai ---")
    
    for page in range(1, total_pages + 1):
        # Pagination handle karne ke liye URL mein page number add kiya
        url = f"https://www.airlinequality.com/airline-reviews/{airline_slug}/page/{page}/"
        print(f"Scraping Page {page}: {url}")
        
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"Page {page} load nahi ho saka. Error Code: {response.status_code}")
            continue
            
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Har review aik <article> tag mein hota hai jiski class 'review-layout' hoti hai
        review_cards = soup.find_all('article', itemprop='review')
        
        for card in review_cards:
            try:
                # 1. Overall Rating (Out of 10)
                rating_badge = card.find('div', itemprop='reviewRating')
                rating = rating_badge.find('span', itemprop='ratingValue').text.strip() if rating_badge else "N/A"
                
                # 2. Review Title (Heading)
                title = card.find('h2', class_='text_header').text.strip().replace('"', '')
                
                # 3. Customer Review Text
                review_div = card.find('div', class_='text_content')
                review_text = review_div.text.strip() if review_div else "N/A"
                
                # Agar review text mein Verification tag ho (e.g., "Trip Verified |"), usko clean karna
                if " | " in review_text:
                    review_text = review_text.split(" | ", 1)[1]
                
                # 4. Review Date
                date_meta = card.find('time', itemprop='datePublished')
                review_date = date_meta.text.strip() if date_meta else "N/A"
                
                # 5. Detailed Breakdown Table (Seat Comfort, Staff, Food, etc.)
                # Skytrax har extra metric ko aik table row (tr) mein rakhta hai
                stats_table = card.find('table', class_='review-ratings')
                
                # Default values for sub-ratings
                seat_comfort = "N/A"
                cabin_staff = "N/A"
                food_beverages = "N/A"
                inflight_entertainment = "N/A"
                value_for_money = "N/A"
                recommended = "N/A"
                
                if stats_table:
                    rows = stats_table.find_all('tr')
                    for row in rows:
                        header = row.find('td', class_='review-rating-header').text.strip()
                        
                        # Star ratings check karne ke liye stars count karna
                        stars = row.find_all('span', class_='star fill')
                        star_count = len(stars) if stars else "N/A"
                        
                        # Recommendation text form mein hoti hai (Yes/No)
                        value_td = row.find('td', class_='review-value')
                        text_value = value_td.text.strip() if value_td else "N/A"
                        
                        if header == "Seat Comfort": seat_comfort = star_count
                        elif header == "Cabin Staff Service": cabin_staff = star_count
                        elif header == "Food & Beverages": food_beverages = star_count
                        elif header == "Inflight Entertainment": inflight_entertainment = star_count
                        elif header == "Value For Money": value_for_money = star_count
                        elif header == "Recommended": recommended = text_value
                
                # Har review ka complete data dictionary mein store karein
                reviews_data.append({
                    "Airline": airline_name,
                    "Review_Date": review_date,
                    "Overall_Rating": rating,
                    "Review_Title": title,
                    "Review_Text": review_text,
                    "Seat_Comfort": seat_comfort,
                    "Cabin_Staff_Service": cabin_staff,
                    "Food_Beverages": food_beverages,
                    "Inflight_Entertainment": inflight_entertainment,
                    "Value_For_Money": value_for_money,
                    "Recommended": recommended
                })
                
            except Exception as e:
                # Agar kisi specific card mein error aaye to baaki script na ruke
                continue
                
        # Server par load na daalne ke liye 2 seconds ka delay
        time.sleep(2)
        
    # Data Frame mein convert karke CSV file save karna
    if reviews_data:
        df = pd.DataFrame(reviews_data)
        file_name = f"{airline_slug}_customer_trends.csv"
        df.to_csv(file_name, index=False)
        print(f"\nMukammal Data successfully save ho gaya hai file name: '{file_name}'")
        print(f"Total reviews scraped: {len(df)}")
    else:
        print("Koi data extract nahi ho saka. HTML layout check karein.")

# Function run karne ka tareeqa
if __name__ == "__main__":
    # Aap "Pakistan International Airlines", "Emirates", ya kisi bhi airline ka naam likh sakte hain
    scrape_customer_reviews("British Airways", total_pages=3)
