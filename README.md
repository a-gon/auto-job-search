# Job Search Bot for LinkedIn

Looking through endless job postings can be daunting, and even if you apply several filters they may filter out the jobs that may be intetesting to you or not be strict enough.

This bot collects job postings that correspond to your preferences and outputs them into a .csv file so you can spend more time on applications that you are actually interested in.

___
**NOTE**

This is a small personal project for automating a repetitive task for time saving purposes and is not intended for large-scale web scraping.  
Anyone is welcome to use it.
___

## How it works

The bot takes in a URL of a page with your search results on LinkedIn (for now, just copy and paste it in **linkedinbot.py**).  
It looks through search results (using Selenium) and finds the ones that should be accepted into its shortlist by applying filters defined in **job_filter.py**.  E.g. you can filter out all job postings that contain "principal" in them and include only job postings that contain "software engineer".  
All jobs postings ever seen are stored in a SQLite database and duplicates are not allowed. To avoid duplicates, a unique hash is calculated based on job description text.  
What is stored in the database: hash, title, company, location, description, link to apply, date found, senioirity level, accepted or not (whether it corresponds to what you're looking for).

## Installation and launch

At the moment, to run the bot on your machine you need to do the following:

- make sure you have python 3.7 (to check `python --version`)
- install all dependencies: `pip install -r requirements.txt`
- install chromedriver: `brew install chromedriver`
  - if you have Google Chrome browser on your machine make sure it's updated to the latest version
- alter filters to make them relevant to your search in **job_filters.py**
- execute **linkedinbot.py** with your own search parameters (this will take a few minutes)
  - `$ python3 linkedinbot.py <"Software Engineer"> <"California, United States">`

Upcoming updates will include:

- [x] Handling search parameters as key arguments.
- [x] Containerization with Docker
- [ ] Extraction of data from a container
- [ ] Setting up a schedule to run the bot