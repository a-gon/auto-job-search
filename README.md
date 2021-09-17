# Job Search Bot for LinkedIn

This is a scraper bot that collects unique job postings that correspond to your preferences and outputs them into a .csv file.

This could also be used as a tutorial on how to set up and run a small app with Docker and use persistent storage with it.


## How it works

The bot takes in a URL of a page with your search results on LinkedIn (for now, just copy and paste it in **linkedinbot.py**).  
It looks through search results (using Selenium) and finds the ones that should be accepted into its shortlist by applying filters defined in **job_filter.py**.  E.g. you can filter out all job postings that contain "principal" in them and include only job postings that contain "software engineer".  
All jobs postings ever seen are stored in a SQLite database and duplicates are not allowed. To avoid duplicates, a unique hash is calculated based on job description text.  
What is stored in the database: hash, title, company, location, description, link to apply, date found, senioirity level, accepted or not (whether it corresponds to what you're looking for).

## Installation and launch

At the moment, to run the bot on your machine you need to do the following:

- make sure you have python 3.7 (to check `python --version`)
- install all dependencies: `pip install -r requirements.txt`
- install chromedriver: cd into /src, `brew install chromedriver`
  - if you have Google Chrome browser on your machine make sure it's updated to the latest version
- alter filters to make them relevant to your search in **job_filters.py**
- execute **linkedinbot.py** with your own search parameters (this will take a few minutes)
  - `$ python3 linkedinbot.py <"Software Engineer"> <"California, United States">`
  - or without search parameters, then you'll need to paste the search url into **linkedinbot.py** (main method)

Using Docker:

- Get Docker: <https://docs.docker.com/get-docker/>
- Build an image: `docker build -t job-bot .`
- Start a container with persistent storage: `docker run -v datavolume:/data --name mybot job-bot`
  - Here, 'job-bot' is an image name.
  - 'datavolume' is the name of volume, when run for the first time, it will be created automatically. '/data' is the location of database within the container.
  - The database will persist between container launches.
  - 'mybot' is the container name, so if you're starting a new container with the same command, first, remove the old container with `docker rm mybot`
- To get the resulting csv files from the container to your local machine: `docker cp mybot:/data/csv ./data` after the container finishes, where 'mybot' is the container name.
- Tip: for getting inside your container: `docker run --entrypoint /bin/bash -it -v datavolume:/data job-bot` where 'job-bot' is image name. This is helpful for exploring the file system of the container.

Updates introduced:

- [x] Handling search parameters as key arguments.
- [x] Containerization with Docker
- [x] Persistent storage (locally)
