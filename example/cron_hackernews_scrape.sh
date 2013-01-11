#!/usr/bin/bash

VENVDIR=/PATH/TO/VENV/
source $VENVDIR/bin/activate
cd /PATH/TO/WORKING/DIR/scrapyhacker

scrapy crawl hackernews
