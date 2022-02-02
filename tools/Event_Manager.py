import threading, time
import tkinter as tk
from .Entry_Parse import Parse_Entry
from .Test import Test
from .Checker import Checker


class Submission():
    def __init__(self, status, combos, popup_obj, proxies:tuple, output, threads, timeout, working, failed, proxies_count, remaining, proxyless):
        self.status = status
        self.combos = combos
        self.popup_obj = popup_obj
        self.proxies = proxies
        self.output = output
        self.threads = threads
        self.timeout = timeout
        self.working = working
        self.failed = failed
        self.proxies_count = proxies_count
        self.remaining = remaining
        self.proxyless = proxyless

    def on_submit(self):
        entry_parser = Parse_Entry(popup_obj=self.popup_obj, proxyless_option=self.proxyless.is_proxyless.get())
        entry_valid = entry_parser.check_entries(self.combos.text.get('0.0', 'end'), (self.proxies[0].text.get('0.0', 'end'), self.proxies[1].text.get('0.0', 'end')))
        if entry_valid == True:
            # try:
            self.failed.start()
            self.working.start()
            combos_list = entry_parser.parse_combos(entry=self.combos.text.get('0.0', 'end'))
            proxies_list = entry_parser.parse_proxies(https=self.proxies[0].text.get('0.0', 'end'), socks4=self.proxies[1].text.get('0.0', 'end'))
            checker = Checker(combos=combos_list, proxies=proxies_list, output=self.output, threads=self.threads, timeout=self.timeout, status=self.status, failed=self.failed, working=self.working, popup=self.popup_obj, proxies_count=self.proxies_count, remaining=self.remaining, proxyless=self.proxyless.is_proxyless.get())
            self.status.in_progress()
            self.status.update_status_display()
            checker.iteration()
            while threading.active_count() > 2:
                pass
            self.status.deactivate()
            self.status.update_status_display()
            # except Exception as e:
            #     print(str(e))
            #     self.popup_obj((500, 50), 'There Was An Unknown Error!')
        else:
            self.popup_obj((500, 50), 'Either Combos, HTTPS, Or SOCKS4 List Is Empty!')

class Finish():
    def __init__(self, status):
        self.status = status

    def on_submit(self):
        if self.status.status_var.get() == 'In Progress':
            self.status.finishing()
            self.status.update_status_display()
