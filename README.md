Just trying to find some interesting stuff about Formula 1, partly for iROZHLAS.cz and partly for fun.

Notebooks published before October 2023 can be found in the "archive" folder. Sorry for the confusion and broken links but some major refactoring of the whole project was needed. (It was my first adventure in Python / pandas and some practices were suboptimal.)

The primary source of data is [Ergast API](http://ergast.com/mrd/) (RIP in 2024). Some additional CSVs were scraped from Wikipedia.

Notebooks from #001 to #099 cover downloading, scraping and cleaning of data, notebooks from #101 to #899 cover data exporation and notebooks from #901 on contain calculations and charts I've used in my articles at iROZHLAS.cz.

To-do:

- The notebooks for scraping Wikipedia / Wikidata are way too redundant and send far more requests than necessary. I was coding faster than thinking. This will be resolved by 1/ joining the notebooks for acquring Wikidata IDs and downloading Wikipedia pages, 2/ keeping a list of the drivers that have been already scraped.