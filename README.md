# hometest

## Pytest Python Selenium for Web automation testing
A framework to test mobile and desktop applications

## Project setup:
uv init --python 3.14
uv venv
.venv\Scripts\activate or source ./.venv/bin/activate.sh
uv add pytest
uv add allure-pytest
uv add selenium
uv add webdriver-manager

## Folders structure


## How to run:
for mobile devices use the marker 'responsive'
pytest -m responsive --device=iPad -v
pytest -m responsive --device='iPhone 12 Pro' -v
pytest -m responsive --device="Samsung Galaxy S21" -v

for desktop computers use the marker 'desktop'
pytest -m desktop -v --browser=chrome
pytest -m desktop -v --browser=firefox
pytest -m desktop -v --browser=edge

To create Allure reports:
pytest -m responsive -v --device="iPhone 12 Pro" --browser=chrome --alluredir=allure-results
allure serve allure-results
