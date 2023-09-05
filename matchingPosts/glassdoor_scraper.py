# -*- coding: utf-8 -*-
"""
Updated on Wed Jul  5 09:32:36 2023 by Ilef

author: HenloIlef
author: Ilef
url: https://github.com/arapfaik/scraping-glassdoor-selenium
"""

from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException
from selenium import webdriver
import time
import pandas as pd
def get_jobs(keyword, num_jobs, verbose, path, slp_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    #Initializing the webdriver
    options = webdriver.ChromeOptions()
    
    #Uncomment the line below if you'd like to scrape without a new Chrome window every time.
    #options.add_argument('headless')
    
    #Change the path to where chromedriver is in your home folder.
    options.binary_location = "C:/Users/henloIlef/AppData/Local/Programs/Opera/opera.exe"
    driver = webdriver.Opera(executable_path=path,options=options)
    driver.set_window_size(1120, 1000)

    url = 'https://www.glassdoor.com/Job/jobs.htm?sc.keyword="' + keyword + '"&locT=C&locId=1147401&locKeyword=San%20Francisco,%20CA&jobType=all&fromAge=-1&minSalary=0&includeNoSalaryJobs=true&radius=100&cityId=-1&minRating=0.0&industryId=-1&sgocId=-1&seniorityType=all&companyId=-1&employerSizes=0&applicationType=0&remoteWorkType=0'
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  #If true, should be still looking for new jobs.

        #Let the page load. Change this number based on your internet speed.
        #Or, wait until the webpage is loaded, instead of hardcoding it.
        time.sleep(slp_time)

        #Test for the "Sign Up" prompt and get rid of it.
        try:
            driver.find_element_by_class_name("selected").click()
        except ElementClickInterceptedException:
            pass

        time.sleep(.1)

        try:
          driver.find_element_by_css_selector('button.e1q8sty40').click()
          print("***********************************************done")
        except NoSuchElementException:
            print("**********************************************************************fail")
            pass
    

        
        #Going through each job in this page
        job_buttons = driver.find_elements_by_class_name("css-3x5mv1")  #jl for Job Listing. These are the buttons we're going to click.
        for job_button in job_buttons:  
            print("accessing buttons")
            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break

            job_button.click()  #You might 
            time.sleep(1)
            collected_successfully = False
            company_name = ""
            location = ""
            job_title = ""
            job_description = ""
            size = -1 
            founded = -1
            type_of_ownership = -1
            industry = -1
            sector = -1
            revenue = -1
            while not collected_successfully:
                try:
                    company_name = driver.find_element_by_xpath('.//div[@data-test="employerName"]').text
                    location = driver.find_element_by_xpath('.//div[@data-test="location"]').text
                    job_title = driver.find_element_by_xpath('.//div[@data-test="jobTitle"]').text
                    job_description_element = driver.find_element_by_xpath('//div[@class="jobDescriptionContent desc"]')
                    job_description = job_description_element.text
                    company_info_element = driver.find_element_by_id("EmpBasicInfo")
                    try:
                        size = company_info_element.find_element_by_xpath('.//div[contains(span, "Size")]//span[contains(@class, "css-i9gxme")]').text
                    except NoSuchElementException:
                        size = -1
                    try:
                        founded = company_info_element.find_element_by_xpath('.//div[contains(span, "Founded")]//span[contains(@class, "css-i9gxme")]').text
                    except NoSuchElementException:
                        founded = -1
                    try:
                        type_of_ownership = company_info_element.find_element_by_xpath('.//div[contains(span, "Type")]//span[contains(@class, "css-i9gxme")]').text
                    except NoSuchElementException:
                        type_of_ownership = -1
                    try:
                        industry = company_info_element.find_element_by_xpath('.//div[contains(span, "Industry")]//span[contains(@class, "css-i9gxme")]').text
                    except NoSuchElementException:
                        industry = -1
                    try:
                        sector = company_info_element.find_element_by_xpath('.//div[contains(span, "Sector")]//span[contains(@class, "css-i9gxme")]').text
                    except NoSuchElementException:
                        sector = -1
                    try:
                        revenue = company_info_element.find_element_by_xpath('.//div[contains(span, "Revenue")]//span[contains(@class, "css-i9gxme")]').text
                    except NoSuchElementException:
                        revenue = -1
                    


                    collected_successfully = True
                except:
                    time.sleep(5) 
                    print("collection failed**************")
                    break
                if not collected_successfully:
                    continue
            try:
                salary_estimate = driver.find_element_by_xpath('.//div[@class="salary-estimate"]').text
            except NoSuchElementException:
                salary_estimate = -1 #You need to set a "not found value. It's important."
            
            try:
                rating = driver.find_element_by_xpath('.//span[@data-test="detailRating"]').text
            except NoSuchElementException:
                rating = -1 #You need to set a "not found value. It's important."

            #Printing for debugging
            if verbose:
                print("Job Title: {}".format(job_title))
                print("Salary Estimate: {}".format(salary_estimate))
                print("Job Description: {}".format(job_description[:500]))
                print("Rating: {}".format(rating))
                print("Company Name: {}".format(company_name))
                print("Location: {}".format(location))
                print("Size: {}".format(size))
                print("Founded: {}".format(founded))
                print("Type of ownership: {}".format(type_of_ownership))
                print("Industry: {}".format(industry))
                print("Sector: {}".format(sector))
                print("Revenue: {}".format(revenue))
                print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

            #Going to the Company tab...
            #clicking on this:
            #<div class="tab" data-tab-type="overview"><span>Company</span></div>

            jobs.append({"Job Title" : job_title,
            "Salary Estimate" : salary_estimate,
            "Job Description" : job_description,
            "Rating" : rating,
            "Company Name" : company_name,
            "Location" : location,
            "Size" : size,
            "Founded" : founded,
            "Type of ownership" : type_of_ownership,
            "Industry" : industry,
            "Sector" : sector,
            "Revenue" : revenue})
            #add job to jobs

        #Clicking on the "next page" button
        try:
            next_button = driver.find_element_by_css_selector('button.nextButton.job-search-opoz2d.e13qs2072')
            next_button.click()
        except NoSuchElementException:
            print("Scraping terminated before reaching target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    return pd.DataFrame(jobs)  #This line converts the dictionary object into a pandas DataFrame.
