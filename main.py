import json
import os
import time
from datetime import datetime, timedelta
import schedule
from schedule import every, repeat, run_pending

from UpyunTools import tokenAPI, logAPI
from db_pool.mysqlhelper import MySqLHelper


@repeat(every().day.at('03:00'))
def logger():
    try:
        # Create DB Connection
        db = MySqLHelper()

        # Load config file
        with open("config.json", 'r') as config:
            config_dict = json.load(config)
        UPYUN_Token = config_dict["UPYUN_Token"]
        UPYUN_Username = config_dict["UPYUN_Username"]
        UPYUN_Password = config_dict["UPYUN_Password"]
        CDN_Resource = config_dict["CDN_Resource"]
        LogOperation = config_dict["LogOperation"]

        yesterday = (datetime.now() - timedelta(days=1)).strftime("%Y-%m-%d")
        if UPYUN_Token == "":
            UPYUN_Token = tokenAPI.get(UPYUN_Username, UPYUN_Password)
        else:
            pass
        for CDN in CDN_Resource:
            bucket_name = CDN[0]
            domain = CDN[1]
            fileList = logAPI.download(UPYUN_Token, bucket_name, domain, yesterday)
            for file in fileList:
                logList = logAPI.EscapeLog(file)
                for logDict in logList:
                    logAPI.SaveSQL(logDict, db)
                if LogOperation == "move":
                    os.replace(file, file.replace("data/", "data/archive/"))
                elif LogOperation == "delete":
                    os.remove(file)
                else:
                    pass
        print("Finished Task at " + str(datetime.now()))
    except Exception as err:
        print("Task error at " + str(datetime.now()))
        print(err)


if __name__ == "__main__":
    while True:
        schedule.run_pending()
        time.sleep(1)
