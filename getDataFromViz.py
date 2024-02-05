import json
import datetime
import time
import requests
import argparse
import calendar
import sys
    

def setupArgs(parser):
    
    parser.add_argument("fromDate", help="Format: YYYY-MM-DD, the begining of the date range (includes that whole day) from which to retrieve records")
    parser.add_argument("toDate", help="Format: YYYY-MM-DD, The ending date range (includes that whole day) from which to retrieve records")
    parser.add_argument("queryPath", help="path/filename of query text copied from kibana visualization")
    # get arguments and make dates out of them, starts at 0:00 for from and ends at 23:59 for end
    args = parser.parse_args()
    return args

def processDate(args):

    try:
        datetime.date.fromisoformat(args.fromDate)
        datetime.date.fromisoformat(args.toDate)
    except ValueError:
            print("\nError! Invalid date, both dates must be in ISO format: YYYY-MM-DD", file=sys.stderr)
            sys.exit(1)

    year, month, day = args.fromDate.split('-')
    fromDate = datetime.datetime(int(year), int(month), int(day), 0, 0)

    year, month, day = args.toDate.split('-')
    toDate = datetime.datetime(int(year), int(month), int(day), 23, 59)

    fromDate = calendar.timegm(fromDate.utctimetuple())
    toDate = calendar.timegm(toDate.utctimetuple())

    if toDate < fromDate:
        print("\nError! Invalid date, end is before begining", file=sys.stderr)
        sys.exit(1)

    if time.time() < fromDate:
        print("\nWarning! From date is in the future (according to system time).")

    if time.time() < toDate:
        print("\nWarning! To date is in the future (according to system time).")

    return fromDate,toDate

def getDataFromVisualization():
    parser = argparse.ArgumentParser()
    args = setupArgs(parser)
    
    fromDate, toDate = processDate(args)
    queryObject = processQuery(args)

    # set time frame --- https://www.elastic.co/guide/en/elasticsearch/reference/current/query-dsl-range-query.html
    queryObject["query"]["bool"]["must"][2]["range"]["@timestamp"]["gte"] = fromDate
    queryObject["query"]["bool"]["must"][2]["range"]["@timestamp"]["lte"] = toDate

    sendQuery(queryObject)
    
def sendQuery(queryObject):

    try:
        req = requests.post('https://fifemon-es.fnal.gov/fifebatch-history-*/_search', json=queryObject)
    except Exception:
        print("Error! Couldn't connect to server, check URL and connection")
        sys.exit(1)
    
    if req.status_code != 200:
        print("Error! http status code: ", req.status_code, "are you connected to the VPN?")
        sys.exit(1)

    result = req.json()
    fromDate = datetime.datetime.utcfromtimestamp(queryObject["query"]["bool"]["must"][2]["range"]["@timestamp"]["gte"])
    toDate = datetime.datetime.utcfromtimestamp(queryObject["query"]["bool"]["must"][2]["range"]["@timestamp"]["lte"])

    if result["hits"]["total"] == 0:
        print("\nNo results found for date range from: ", fromDate, " to: ", toDate, " UTC")
        sys.exit(0)

    outputToFile(result, fromDate, toDate)

def outputToFile(result, fromDate, toDate):
    niceToDate = str(toDate.year) + "-" + str(toDate.month) + "-" + str(toDate.day)
    niceFromDate = str(fromDate.year) + "-" + str(fromDate.month) + "-" + str(fromDate.day)
    filename = "records_" + niceFromDate + "_to_" + niceToDate + ".json"
    with open(filename, "w") as outfile: 
        json.dump(result, outfile)

def processQuery(args):

    filePath = args.queryPath
    queryFile = open(filePath, "r")
    query = queryFile.read()
    queryObject = json.loads(query)
    queryFile.close()

    return queryObject

getDataFromVisualization()