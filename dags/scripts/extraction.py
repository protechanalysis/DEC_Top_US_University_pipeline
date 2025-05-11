import json
import logging
import time

import pandas as pd
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent

from scripts.config import (output_score_card, output_unirank, params,
                            scorecard_url, unirank_url)

logging.basicConfig(level=logging.INFO)

agent = UserAgent().random


def scrape_universities():
    """
    Scrapes the top 1,000 universities from the uniRank website and saves 
    the data to a CSV file.

    This function makes an HTTP GET request to the uniRank website, parses
    the HTML using BeautifulSoup, and extracts the university rankings, names, 
    and locations.
    The scraped data is stored in a DataFrame and saved as a CSV file.

    Returns:
        list: A list of tuples containing the rank, university name, and 
        location.

    Raises:
        Exception: If an error occurs during the scraping process or saving 
        the data.
    """
    try:
        response = requests.get(unirank_url, headers={"User-Agent": agent})
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        # Find the university list in the table
        uni_table = soup.find("table", {"class": "table"})
        universities = []

        if uni_table:
            rows = uni_table.find_all("tr")[1:]
            for rank, row in enumerate(rows[:1000], start=1):
                columns = row.find_all("td")
                if columns:
                    uni_name = columns[1].text.strip()
                    location = columns[2].text.strip()
                    universities.append((rank, uni_name, location))
        uni = pd.DataFrame(universities,
                           columns=["Rank", "University", "Location"])
        uni.to_csv(output_unirank, index=False)
        logging.info("Scraped and saved university data successfully.")
        return universities
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


def fetch_page():
    """
    Fetches school details from the College Scorecard API and writes them to a
    JSON file.

    This function makes multiple requests to the College Scorecard API,
    fetching data for a given page range, and appends the results to a list.
    The collected data is saved to a local JSON file.

    Args:
        page (int): The starting page number for the API request.

    Raises:
        Exception: If an error occurs during the API request or while writing
        to the file.
    """
    try:
        score_data = []
        for i in range(0, 69):
            params["page"] = i
            logging.info(f"Fetching page {i}...")
            response = requests.get(scorecard_url, params=params)
            response.raise_for_status()
            data = response.json()
            data_score = data["results"]
            if data_score is None or len(data_score) == 0:
                logging.info("No more data available.")
                break
            score_data.extend(data_score)
            time.sleep(3)

        with open(output_score_card, "w", encoding='utf-8') as f:
            json.dump(score_data, f, indent=4)

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
