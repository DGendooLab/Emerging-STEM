from bs4 import BeautifulSoup
import requests
import pandas as pd
from multiprocessing import Pool
from functools import partial


class scrape():

    # Create base URL for all further scraping
    def create_url(parameters):
        # create base url for all further searches
        academic_discipline = parameters['academic_discipline']
        hours_type = parameters['hours_type']
        funding_type = parameters['funding_type']
        base_url = f"https://www.jobs.ac.uk/search/?activeFacet=hoursTypeFacet&sortOrder=1&pageSize=25&startIndex=1&academicDisciplineFacet%5B0%5D={academic_discipline}&jobTypeFacet%5B0%5D=phds&hoursTypeFacet%5B0%5D={hours_type}&fundingTypeFacet%5B0%5D={funding_type}"
        return base_url

    # Rate phd based on parameters given
    def rate_phd(p_title, p_soup, parameters):
        # rate by keywords
        # description = p_soup.select_one("#job-description.row-8").get_text()
        title_keywords = parameters['ordered_keywords']
        exclude_keywords = parameters['exclude_keywords']
        total_keywords = len(title_keywords)
        title_keywords_present = []
        rating = 0

        # Check for title keywords
        for index, keyword in enumerate(title_keywords):
            if keyword in p_title:
                rating += total_keywords - index
                title_keywords_present.append(keyword)

        # Normalise rating
        rating = rating / sum(range(1, total_keywords + 1))

        # Check for excluded keywords
        for keyword in exclude_keywords:
            if keyword in p_title:
                rating = 0
                break

        return rating, title_keywords_present

    # Obtain details of the job (company, title, description etc.)
    def get_phd_details(job, parameters):
        pass

    # Primary function for obtaining scraped data
    def get_scrape(self, parameters):
        pass

        # For outputting to excel locally
    def output_excel(df):
        pass
