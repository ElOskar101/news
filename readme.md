# News scraper bot

This bot browses through https://apnews.com and retrieves information from the news such as the title, description, publication date, among others, in order to create a report as an output of the news published in an estimated date range

## Description
This project generates a report in ```/outputs/results.xlsx.``` In that folder you will also find the downloaded images

## Getting Started

### Inputs

* Work-Items
```
{
    "months": 0 ~ 1 | 2 | 3 | 4 ...,
    "search_phrase": "any"
    "category": "stories, videos, subsections"
}
```
This is an example. Categories must be in lower case. Highly recommended to use a short search phrase in order to get
more precise results

## Authors

Contributors names and contact info

Oscar Gonzalez  
oscaresga22@gmail.com

