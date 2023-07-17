from bs4 import BeautifulSoup
import requests
import pandas as pd
import re


class Scrape_Job:
    @staticmethod
    def create_url(parameters):
        search_keywords = parameters['search_keywords'].replace(' ', '+')
        academic_discipline = parameters['academic_discipline']
        base_url = f'https://www.jobs.ac.uk/search/?keywords={search_keywords}&activeFacet=academicDisciplineFacet&sortOrder=0&pageSize=25&startIndex=1&academicDisciplineFacet%5B0%5D={academic_discipline}'

        return base_url

    @staticmethod
    def rate_job(data, parameters):
        title_keywords = parameters['ordered_keywords']
        exclude_keywords = parameters['exclude_keywords']
        total_keywords = len(title_keywords)
        title_keywords_present = []
        rating = 0

        for index, keyword in enumerate(title_keywords):
            if keyword in data['title']:
                rating += total_keywords - index
                title_keywords_present.append(keyword)

        rating = rating / sum(range(1, total_keywords + 1))
        rating = round(rating, 3)  # Round up

        for keyword in exclude_keywords:
            if keyword in data['title']:
                rating = -1
                break

        # Convert title_keywords_present to string representation
        title_keywords_present_str = ", ".join(title_keywords_present)

        return rating, title_keywords_present_str

    @staticmethod
    def get_job_details(url):
        data = pd.DataFrame()

        total_job_number_text = BeautifulSoup(requests.get(url).content, "html.parser")\
            .select_one("#job-count h2.j-search-content__count").get_text(strip=True)
        total_job_number = int(re.sub(r'\D', '', total_job_number_text))

        print(f"[Collection] Job data size: {total_job_number}, collecting...")

        total_page_number = (total_job_number + 24) // 25

        for i in range(1, total_page_number + 1):
            index_start = (i - 1) * 25 + 1
            page_url = f"{url}&startIndex={index_start}"
            page = BeautifulSoup(requests.get(page_url).content, "html.parser")

            # Extract data from the page
            titles = [title.get_text(strip=True) for title in page.select(
                "div.j-search-result__text a")]
            urls = ["https://www.jobs.ac.uk" + url["href"]
                    for url in page.select("div.j-search-result__text a")]
            departments = [department.get_text(
                strip=True) for department in page.select("div.j-search-result__department")]
            departments = departments if departments else [None]
            employers = [employer.get_text(strip=True) for employer in page.select(
                "div.j-search-result__employer b")]
            employers = employers if employers else [None]
            locations = [location.get_text(strip=True).replace("Locations:", "").strip(
            ) for location in page.select("div.j-search-result__text div:nth-child(4)")]
            salary = [re.sub(r'\s+', ' ', salary.get_text(strip=True).replace("Salary:", "").strip())
                      for salary in page.select("div.j-search-result__text div:nth-child(5)")]
            post_dates = [post_date.get_text(strip=True).replace("Date Placed:", "").strip(
            ) for post_date in page.select("div.j-search-result__text div:nth-child(6)")]
            close_dates = [close_date.get_text(strip=True) for close_date in page.select(
                "div.j-search-result__date-logos span.j-search-result__date--blue")]

            page_data = pd.DataFrame({
                "title": titles,
                "employer": employers,
                "department": departments,
                "salary": salary,
                "location": locations,
                "post_date": post_dates,
                "close_date": close_dates,
                "url": urls
            })

            data = pd.concat([data, page_data], ignore_index=True)
            print("Collection Done")
            return data

    def get_scrape(self, parameters):
        base_url = self.create_url(parameters)
        job_data = self.get_job_details(base_url)
        rating_data = job_data.apply(lambda row: self.rate_job(
            row, parameters), axis=1, result_type="expand")
        rating_data = rating_data.rename(
            columns={0: 'rating', 1: 'title_keywords_present'})
        output_data = pd.concat([job_data, rating_data], axis=1)

        # Sort df by rating
        output_data = output_data.sort_values(
            by='rating', ascending=False).reset_index(drop=True)

        return output_data
