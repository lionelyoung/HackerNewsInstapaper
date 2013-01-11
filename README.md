Setup
=====

Recommend using virtualenv and virtualenvwrapper to manage your environment

1. mkvirtualenv HackerNewsInstapaper
2. pip install -r pip-requirements.txt
3. Edit and rename scrapyhacker/instapaper.ini.sample to scrapyhacker/instapaper.ini
4. Edit the helper scripts to add your environment in `scrapyhacker/cron_hackernews_scrape.sh` and `scrapyhacker/cron_hackernews_instapaper.sh`

Usage
=====

Use scrapy to crawl Hacker News (http://news.ycombinator.com/best) and store
into articles.db, then run `submitinstapaper.py`:

1. `scrapy crawl hackernews`
2. `python submitinstapaper.py`


Examples
========

Two example scripts are provided, but needs editing depending on your virtualenv location:

1. `scrapyhacker/cron_hackernews_scrape.sh`: Sets the environment and runs the crawler
2. `scrapyhacker/cron_hackernews_instapaper.sh`: Submits the unsent articles in articles.db to Instapaper

Example lines to add to your crontab:
  `0 3 * * * cron_hackernews_scrape.sh > /dev/null 2>&1
   15 3 * * 1 cron_hackernews_instapaper.sh`
