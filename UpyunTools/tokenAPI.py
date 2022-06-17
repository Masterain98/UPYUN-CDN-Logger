import requests, random, string, time, json


def get(username, password):
    url = "https://api.upyun.com/oauth/tokens/"
    code = "".join(random.choice(string.ascii_lowercase + string.ascii_uppercase +
                                 string.digits) for i in range(32))
    post_form = {
        "username": username,
        "password": password,
        "code": code,
        "name": "UPYUN_MYSQL_LOGGER",
        "scope": "log",
    }
    req = requests.post(url, data=post_form)
    try:
        token = json.loads(req.text)["access_token"]
        return token
    except Exception as e:
        print("error when gathering token")
        print(e)
        return None


def delete(tokenName, token):
    headers = {"Authorization": "Bearer " + token}
    url = "https://api.upyun.com/oauth/tokens?name=%s"
    result = json.loads(requests.delete(url % tokenName, headers=headers).text)
    print(result)

