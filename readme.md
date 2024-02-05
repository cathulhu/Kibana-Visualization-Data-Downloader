# Kibana Visualization Data Downloader

getDataFromViz.py allows you to download JSON data from your Kibana visualizations.

## Requirements

Python 3+

## Installation

clone this repository with git clone.

## Usage

```python

# Gets data from Kibana visualization query in file 'esQuery' for the date range from 2023-02-06 to 2023-02-07 

python3 getDataFromViz.py 2023-02-06 2023-02-07 esQuery

# Outputs to file in following format: 'records_2023-2-6_to_2023-2-7.json'

```

## Changing the Kibana data source

Currently to change the URL for the querry you must edit line 65 of getDataFromViz.py

```python
req = requests.post('https://fifemon-es.fnal.gov/fifebatch-history-*/_search', json=queryObject)
```

If there is sufficient interest I can add an argument or a config file to specify that

## Changing the Kibana query

1) Open [your visualization](https://fifemon.fnal.gov/kibana/goto/0433f4c6c83913846dc3a63c2872cb23) in Kibana 
2) Click Inspect from the menu bar, then go over to view drop down on the right hand side of the pop over window and select "View: Requests" then in the main area of the inspect window select the tab labeled "Request". Copy the complete content of the Request tab into a file. This file will be supplied as the third argument after the from and to date when you run getDataFromViz.py. In the above example that file is called esquery.
3) ![IMAGE]()
4) run getDataFromViz.py with the following arguments [from date YYYY-MM-DD UTC] [to date YYYY-MM-DD UTC] [path to file with saved Kibana query from step 2]

4a) If successful and matches were found no messages will be output, the found data will be saved in the same directory getDataFromViz.py resides in.

4b) If there were no matches or there was an error in syntax, or a connectivity issue, the appropriate error message will be displayed.

## License

[MIT](https://choosealicense.com/licenses/mit/)