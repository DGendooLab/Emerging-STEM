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
        description = p_soup.select_one("#job-description.row-8").get_text()
        keywords = parameters['ordered_keywords']
        title_keywords = parameters['title_keywords']
        exclude_keywords = parameters['exclude_keywords']
        total_keywords = len(keywords) + len(title_keywords)
        keywords_present = []
        title_keywords_present = []
        rating = 0

        # Check for keyword, add value to rating depending on ranking
        for index, keyword in enumerate(keywords):
            if keyword in description:
                rating += len(keywords) - index
                keywords_present.append(keyword)

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

        return description, rating, keywords_present, title_keywords_present

    # Obtain details of the job (company, title, description etc.)
    def get_phd_details(job, parameters):
        pass

    # Primary function for obtaining scraped data
    def get_scrape(self, parameters):

        # Create base url for all further searches
        base_url = scrape.create_url(parameters)

        # Output list and frame
        output = []

        # Create dataframe from list of jobs
        df_output_frame = pd.DataFrame(
            output,
            columns=['Rating', 'Job Title', 'Company', 'Description', 'Job URL', 'Keywords Present', 'Title Keywords',
                     'Page Found']).sort_values(
            by='Rating', ascending=False).reset_index(drop=True)

        # Sort df by rating
        df_output_frame['Rating'] = df_output_frame['Rating'].round(decimals=3)
        df_output_frame = df_output_frame.drop_duplicates(
            subset=['Rating', 'Job Title', 'Company'])
        self.loading = False

        # For outputting to excel locally
    def output_excel(df):
        pass
