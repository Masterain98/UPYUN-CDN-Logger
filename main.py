import json
import os
from datetime import datetime, timedelta

from UpyunTools import tokenAPI, logAPI
from db_pool.mysqlhelper import MySqLHelper

# Load config file
with open("config.json", 'r') as config:
    config_dict = json.load(config)
UPYUN_Token = config_dict["UPYUN_Token"]
UPYUN_Username = config_dict["UPYUN_Username"]
UPYUN_Password = config_dict["UPYUN_Password"]
CDN_Resource = config_dict["CDN_Resource"]
LogOperation = config_dict["LogOperation"]

if __name__ == "__main__":
    db = MySqLHelper()

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
