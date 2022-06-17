import json, requests, gzip, os, re
from datetime import datetime
from urllib.parse import urlparse


def download(token, bucketName, domain, date):
    file_downloaded = []
    print("token:" + token)
    headers = {"Authorization": "Bearer " + token}
    url = "https://api.upyun.com/analysis/archives?bucket_name=%s&domain=%s&date=%s&useSsl=true"
    result = json.loads(requests.get(url % (bucketName, domain, date), headers=headers).text)
    print(result)
    for item in result["data"]:
        gz_fileName = "data/" + item["file"]
        gz_url = item["url"]
        # 下载日志 gz 包
        with open(gz_fileName, "wb") as file:
            file.write(requests.get(gz_url).content)
        # 解压日志 gz 包
        g_log = gzip.GzipFile(gz_fileName)
        open(gz_fileName.replace(".gz", ".log"), "wb+").write(g_log.read())
        g_log.close()
        print(gz_fileName + " 日志下载成功")
        # 删除 gz 包
        os.remove(gz_fileName)
        file_downloaded.append(gz_fileName.replace(".gz", ".log"))
    print("File downloaded: " + str(file_downloaded))
    return file_downloaded


def EscapeLog(fileName):
    result = []
    for line in open(fileName):
        split = line.split(' ')
        # The length of split2 is more stable (len == 13)
        split2 = line.split('"')

        RemoteAddr = split[0]
        RemoteUser = split[1] + " " + split[2]
        TimeLocal = split[3].replace("[", "")
        TimeLocal = str(datetime.strptime(TimeLocal, "%d/%b/%Y:%H:%M:%S"))
        TimeZone = split[4].replace("]", "")
        RequestMethod = split[5].replace('"', "")

        url_path = urlparse(split[6])
        Scheme = url_path.scheme
        HTTPHost = url_path.hostname
        Uri = url_path.path
        QueryString = url_path.query
        try:
            QueryString2 = re.search(r"(\?|\!)(.)+$", Uri).group()
            Uri = Uri.replace(QueryString2, "")
        except:
            QueryString2 = ""
        QueryString = QueryString + QueryString2

        ServerProtocol = split[7].replace('"', '')
        HTTPStatus = split[8]
        BodyBytesSent = split[9]
        HTTPReferer = split[10].replace('"', '')

        EdgeServerIP = split[-1].replace("\n", "")
        RequestTime = split[-2]
        CacheControl = split2[-2]
        IsDynamic = split2[-3].replace(" ", "")
        SourceCode = split2[-4]
        if "hit" in split2[-5].lower():
            CacheHit = "HIT"
            RequestContentLength = split2[-5].replace("Hit", "").replace(" ","")
        elif "miss" in split2[-5].lower():
            CacheHit = "MISS"
            RequestContentLength = split2[-5].replace("Miss", "").replace(" ", "")
        else:
            # Should not happen
            CacheHit = "UNKNOWN"
            RequestContentLength = split2[-5].replace(" ", "")
        ContentType = split2[-6]
        HTTPUserAgent = split2[-8]

        this_log = {
            "RemoteAddr": RemoteAddr,
            "RemoteUser": RemoteUser,
            "TimeLocal": TimeLocal,
            "TimeZone": TimeZone,
            "RequestMethod": RequestMethod,
            "Scheme": Scheme,
            "HTTPHost": str(HTTPHost),
            "QueryString": QueryString,
            "Uri": Uri,
            "ServerProtocol":ServerProtocol,
            "HTTPStatus": HTTPStatus,
            "BodyBytesSent": BodyBytesSent,
            "HTTPReferer": HTTPReferer,
            "HTTPUserAgent": HTTPUserAgent,
            "ContentType": ContentType,
            "RequestContentLength": RequestContentLength,
            "CacheHit": CacheHit,
            "SourceCode": SourceCode,
            "IsDynamic": IsDynamic,
            "CacheControl": CacheControl,
            "RequestTime": RequestTime,
            "EdgeServerIP": EdgeServerIP
        }
        result.append(this_log)
    return result


def SaveSQL(fileList):
    for file in fileList:
        print(file)


EscapeLog("../data/17_00-blogpic.irain.in-8420802881497378793.log")
