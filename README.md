# Times Rich List 2020 Python Scraper

This repo provides Python-Selenium code to scrape the data from the Times [website](https://www.thetimes.co.uk/sunday-times-rich-list).

Pretty hard coded so the data is [included](https://github.com/harveydevereux/TimesRichList2020)

## Setup

The code requires a working python installation with [Selenium installed](https://selenium-python.readthedocs.io/installation.html) (+ the [driver](https://selenium-python.readthedocs.io/installation.html#drivers) for you browser)

Code works with the webpage on 30 May 2020, with Python 3.6.9, Selenium (Python) 3.141.0, and numpy 1.18.1 for the ceil function only

## Running/Options
run with
```Python
python ScrapeData.py
```
or 
```Bash
./run.sh
```

Both support the options ```--csv [string]``` and ```--headless```, the first takes the name of the csv you
want to save the data as, and the sceond will launch Selenium without openning a browser (otherwise you'll watch the
scraper in action)

## Caveats

- Sometimes the webpage bugs or takes to long to load and so Selenium does not find the "I Agree [to cookies]" button. This will show as ```selenium.common.exceptions.ElementNotInteractableException: Message: Element <button class="message-component message-button no-children"> could not be scrolled into view``` re-running usually works
- If the webtext changes it will likely break 

## Data Analysis

Example [Notebook](https://github.com/harveydevereux/TimesRichList2020/blob/master/resources/DataExploration.ipynb) to get started 

### The Wealth Distribution

![alt text](https://github.com/harveydevereux/TimesRichList2020/blob/master/resources/WealthDist.png)

### Top 10 Sectors by Median Wealth

![alt text](https://github.com/harveydevereux/TimesRichList2020/blob/master/resources/HighestMedianWealth.png)

### Top 10 Sectors By Total Wealth 

![alt text](https://github.com/harveydevereux/TimesRichList2020/blob/master/resources/HighestWealth.png)
