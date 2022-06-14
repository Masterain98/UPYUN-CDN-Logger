import json, requests, gzip, os


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