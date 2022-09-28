# Propreturns_assignment

Run the python file webscraper.py to scrap the table of a locality from e-Search (delhigovt.nic.in).

We need to bypass the captcha to click the submit. I tried using image processing techniques and tesseract OCR to convert the captcha image to string. However, the results were not satisfactory. I have added the function for your reference.

Hence, I have created a semi-automated process. The script will enter the details itself and then wait for 7 seconds for the user to enter the captcha manually. It will then scrape the tables present on the next page.
