import httpx, itertools, ctypes, uuid, threading
from colorama import Fore

amountthread = int(input("[>] Amount Of threads --> "))
proxyless = input("[>] Proxy or Proxy-less (yes or no): ")
channel_id = input("[>] Channel ID: ")
message = input("[>] Message: ")

class Spammer:
    def __init__(self):
        with open("data/proxies.txt", encoding="utf-8") as f:
            self.proxies = itertools.cycle([i.strip() for i in f if i])
        with open("data/cookies.txt", encoding="utf-8") as f:
            self.cookies = itertools.cycle([i.strip() for i in f if i])
        self.amount = 0


    def spammer(self):
        ctypes.windll.kernel32.SetConsoleTitleW(f"Guilded Channel Spammer: Amount Spammed: {self.amount}")
        self.proxy = {
            "http://": "http://" + next(self.proxies),
            "https://": "http://" + next(self.proxies),
        }

        if proxyless == "yes":
            self.client = httpx.Client()
        elif proxyless == "no":
            self.client = httpx.Client(proxies = self.proxy)
        self.client.cookies.set('hmac_signed_session', next(self.cookies))

        self.headers = {
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'fr-FR,fr;q=0.9',
            'content-type': 'application/json',
            'guilded-device-type': 'desktop',
            'origin': 'https://www.guilded.gg',
            'referer': 'https://www.guilded.gg/',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/97.0.4692.99 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'dnt': '1',
            "Sec-Ch-Ua": '" Not;A Brand";v="99", "Google Chrome";v="97", "Chromium";v="97"',
            "Sec-Ch-Ua-Mobile": '?0',
            "Sec-Ch-Ua-Platform": "macOS",
        }
        self.json = {
            "messageId": str(uuid.uuid4()),
            "content": {
                "object": "value",
                "document": {
                "object": "document",
                "data": {},
                "nodes": [
                    {
                    "object": "block",
                    "type": "paragraph",
                    "data": {},
                    "nodes": [
                        {
                        "object": "text",
                        "leaves": [
                            {
                            "object": "leaf",
                            "text": message,
                            "marks": []
                            }
                        ]
                        }
                    ]
                    }
                ]
                }
            },
            "repliesToIds": [],
            "confirmed": False,
            "isSilent": False,
            "isPrivate": False
        }
        try:
            self.response = self.client.post(f"https://www.guilded.gg/api/channels/{channel_id}/messages", headers=self.headers, json=self.json)
            self.amount += 1 
            print(f'({Fore.GREEN}!{Fore.RESET}) Sent message: {self.response.json()["message"]["id"]} ({Fore.LIGHTCYAN_EX}{self.amount}{Fore.RESET})')
        except Exception as e:
            pass
    
    def run(self):
        while True:
                if threading.active_count() <= amountthread:
                    threading.Thread(target=self.spammer).start()


Spammer().run()