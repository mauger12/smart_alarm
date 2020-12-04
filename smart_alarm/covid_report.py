"""The covid_report module uses the Government's COVID-19 API to get the latest
   data and processes the information to be used in the __main__ module"""
import requests


def weekly_cases_update(city):
    """Takes a city input and returns new cases over the past week"""
    base_url = "https://api.coronavirus.data.gov.uk/v1/data?"
    filters = 'areaName=' + city
    structure = '{"newCases":"newCasesBySpecimenDate"}'
    complete_url = base_url + "filters=" + filters + "&structure=" + structure
    response = requests.get(complete_url)
    covid_dict = response.json()
    total_cases = 0
    for day in range(0,6):
        total_cases += covid_dict['data'][day]['newCases']
    return total_cases


def total_cases_update(city):
    """Takes a city and returns the latest figure for total cases of covid 19"""
    base_url = "https://api.coronavirus.data.gov.uk/v1/data?"
    filters = 'areaName=' + city
    structure = '{"newCases":"cumCasesBySpecimenDate"}'
    complete_url = base_url + "filters=" + filters + "&structure=" + structure
    response = requests.get(complete_url)
    covid_dict = response.json()
    return str(covid_dict['data'][0]['newCases'])
