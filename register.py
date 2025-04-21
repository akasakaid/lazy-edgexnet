import os
import httpx
from datetime import datetime
from colorama import Fore, Style
import random
import string
import json
import sys
import asyncio
hitam = Fore.LIGHTBLACK_EX
reset = Style.RESET_ALL


def log(msg):
    now = datetime.now().isoformat(" ").split(".")[0]
    print(f"{hitam}[{now}] {reset}{msg}{reset}")


async def http(ses: httpx.AsyncClient, url, data=None):
    attemp = 0
    while True:
        try:
            if attemp == 5:
                return None
            if data is None:
                res = await ses.get(url=url)
            elif data == "":
                res = await ses.post(url=url)
            else:
                res = await ses.post(url=url, data=data)
            if (
                not os.path.exists("http.log")
                or os.path.getsize("http.log") / 1024 > 1024
            ):
                open("http.log", "w").write("")
            open("http.log", "a", encoding="utf-8").write(
                f"{res.status_code} - {res.text}\n"
            )
            return res
        except httpx.NetworkError as e:
            log(f"http request error : network error {e.request.url} !")
            attemp += 1
            continue
        except httpx.ProxyError:
            log("http request error : proxy error !")
            attemp += 1
            continue
        except httpx.TimeoutException as e:
            log(f"http request error : request timeout {e.request.url} !")
            attemp += 1
            continue
        except httpx.RemoteProtocolError:
            log("http request error : server disconnected without response !")
            attemp += 1
            continue
        except Exception as e:
            log(e)
            attemp += 1
            continue


async def ipinfo(ses):
    url = "https://directory.cookieyes.com/api/v1/ip"
    res = await http(ses=ses, url=url)
    if res is None:
        return None
    ip = res.json().get("ip")
    log(f"ip : {ip}")
    return ip


class MailTM:
    def __init__(self, proxy=None, password="useruser@123"):
        headers = {
            "accept": "application/json",
            "accept-language": "en-US,en;q=0.9",
            "cache-control": "no-cache",
            "content-type": "application/json",
            "origin": "https://mail.tm",
            "pragma": "no-cache",
            "priority": "u=1, i",
            "referer": "https://mail.tm/",
            "sec-ch-ua": '"Not(A:Brand";v="99", "Microsoft Edge";v="133", "Chromium";v="133"',
            "sec-ch-ua-mobile": "?0",
            "sec-ch-ua-platform": '"Windows"',
            "sec-fetch-dest": "empty",
            "sec-fetch-mode": "cors",
            "sec-fetch-site": "same-site",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36 Edg/133.0.0.0",
        }
        self.ses = httpx.AsyncClient(headers=headers, proxy=proxy)

        self.password = password

    async def get_domains(self):
        url = "https://api.mail.tm/domains"
        res = await http(ses=self.ses, url=url)
        return res.json()

    async def create_account(self):
        url = "https://api.mail.tm/accounts"
        domains = await self.get_domains()
        domain = random.choice(domains).get("domain")
        username = await self.get_randomuserme()
        email = f"{username}@{domain}"
        data = {"address": email, "password": self.password}
        res = await http(ses=self.ses, url=url, data=json.dumps(data))
        if res is None:
            return None, None
        if res.status_code == 201:
            return 201, email

    async def get_randomuserme(self):
        username = "".join([
            random.choice(list(string.ascii_lowercase)) for _ in range(10)
        ])
        nrn = random.randint(1000, 9999)
        uname = f"{username}{nrn}".lower()
        return uname

    async def get_token(self, email):
        url = "https://api.mail.tm/token"
        data = {"address": email, "password": self.password}
        # data = {"address": email, "password": self.password}
        res = await http(ses=self.ses, url=url, data=json.dumps(data))
        if res.status_code != 200:
            return None, None
        token = res.json().get("token")
        return 200, token

    def set_token(self, token):
        self.ses.headers.update({"authorization": f"Bearer {token}"})

    async def get_mails(self):
        url = "https://api.mail.tm/messages"
        while True:
            res = await http(ses=self.ses, url=url)
            if res.status_code != 200:
                return None, []
            if len(res.json()) <= 0:
                await asyncio.sleep(3)
                continue
            mails = res.json()
            if len(mails) == 0:
                await asyncio.sleep(3)
                continue
            return 200, mails

    async def get_text_mail(self, mail_id):
        url = f"https://api.mail.tm/messages/{mail_id}"
        res = await http(ses=self.ses, url=url)
        if res.status_code != 200:
            return None, None
        text = res.json().get("text")
        return 200, text


async def register(referral_code="", proxy=None):
    headers = {
        "accept-encoding": "gzip",
        "host": "ope.edgex.one",
        "user-agent": "Dart/3.5 (dart:io)",
        "x-access-token": "",
    }
    ses = httpx.AsyncClient(proxy=proxy)
    ip = await ipinfo(ses=ses)
    if ip is None:
        return "bad_proxy"
    ses.headers.update(headers)
    sendotp_url = "https://ope.edgex.one/api/front/login/sendCode"
    login_url = "https://ope.edgex.one/api/front/login/login"
    mail = MailTM(proxy=proxy)
    code, email = await mail.create_account()
    code, token = await mail.get_token(email=email)
    mail.set_token(token=token)
    log(f"email : {email}")
    sendotp_data = {
        "email": email,
    }
    res = await http(ses=ses, url=sendotp_url, data=sendotp_data)
    if res is None:
        return "bad_proxy"
    code, mails = await mail.get_mails()
    code, mail_text = await mail.get_text_mail(mail_id=mails[0]["id"])
    otp = "".join(mail_text.split("Code\n\n")[1].split("\n\n")[0].split(" "))
    log(f"otp : {otp}")
    login_data = {"email": email, "captcha": otp}
    ses.headers.update({"content-type": "application/json"})
    res = await http(ses=ses, url=login_url, data=json.dumps(login_data))
    if res is None:
        return "bad_proxy"
    token = res.json().get("data", {}).get("token")
    if token is None:
        log("failed to login !")
        return False
    ses.headers.update({"x-access-token": token})
    log("success login !")
    open("accounts.txt","a+").write(f"{email}|{mail.password}\n")
    bind_invitation_url = f"https://ope.edgex.one/api/front/login/bindInvitationCode?invitationCode={referral_code}"
    res = await http(ses=ses, url=bind_invitation_url)
    if res is None:
        return "bad_proxy"
    if res.json().get("info") == "success":
        log("success bind invitation code !")

    checkin_url = "https://ope.edgex.one/api/front/integral/task/finish?taskId=1"
    res = await http(ses=ses, url=checkin_url)
    if res is None:
        return "bad_proxy"
    if res.json().get("info") != "success":
        log("failed to daily check in !")
    else:
        log("success daily check in !")
    welcomegift_url = "https://ope.edgex.one/api/front/integral/task/finish?taskId=2"
    res = await http(ses=ses, url=welcomegift_url)
    if res is None:
        return "bad_proxy"
    if res.json().get("info") != "success":
        log("failed to claim welcome gift !")
    else:
        log("success claim welcome gift !")
    info_url = "https://ope.edgex.one/api/front/user/info"
    res = await http(ses=ses, url=info_url)
    if res is None:
        return "bad_proxy"
    user_referral_code = res.json().get("data", {}).get("invitationCode")
    balance = res.json().get("data", {}).get("integralBalance")
    log(f"referral code : {user_referral_code}")
    log(f"balance : {balance}")
    return True


async def main():
    print("""
>
> Auto Register EdgeX network !
> Join @sdsproject
>

        """)
    proxies = open("proxies.txt").read().splitlines()
    referral_code = open("referral_code.txt").read().splitlines()
    if len(referral_code) <= 0:
        print("you haven't set referral code !")
        sys.exit()
    referral_code = referral_code[0]
    print(f"total proxy : {len(proxies)}")
    print(f"referral code : {referral_code}")
    print()
    referrals = input("how many referral : ")
    print()
    p = 0
    n = 0
    while True:
        print("~" * 50)
        log(f"account {n}/{referrals}")
        proxy = None if len(proxies) <= 0 else proxies[p % len(proxies)]
        result = await register(referral_code=referral_code, proxy=proxy)
        if result == "bad_proxy":
            p += 1
            continue
        if result:
            p += 1
            n += 1
            continue
        p += 1
        if n == int(referrals):
            sys.exit()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, EOFError):
        sys.exit()
