class Parse_Entry():
    def __init__(self, popup_obj, proxyless_option):
        self.popup_obj = popup_obj
        self.proxyless = proxyless_option

    def check_entries(self, combos, proxies:tuple):
        if len(combos) < 1:
            return False
        elif len(proxies[0]) < 2 and self.proxyless == 0 and len(proxies[1]) < 2 and self.proxyless == 0:
            return False
        else:
            return True

    def parse_combos(self, entry:str):
        combo_list = entry.strip().split('\n')
        return combo_list

    def parse_proxies(self, https:str, socks4:str):
        https = https.strip().split('\n')
        https = list(dict.fromkeys(https))
        for h in https:
            if len(h.strip()) <= 1:
                del h

        socks4 = socks4.strip().split('\n')
        socks4 = list(dict.fromkeys(socks4))
        for s in socks4:
            if len(s) <= 1:
                del s

        parsed_proxies = []
        for p in https:
            p_dict = {
                'type':'https',
                'proxy': p
            }
            if len(p.strip()) > 0:
                parsed_proxies.append(p_dict)
        
        for i in socks4:
            i_dict = {
                'type':'socks4',
                'proxy': i
            }
            if len(i.strip()) > 0:
                parsed_proxies.append(i_dict)
        
        return parsed_proxies