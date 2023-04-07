from alert.gmailalert import GmailAlert
from binance.listings import BinanceListings
import yaml
import time
import os

class IEOMoon:
    def __init__(self, config_file=os.path.join('alert', 'config.yaml')):
        with open(config_file) as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)
            self.email_alerter = None

        if 'gmail' in self.config.keys():
            self.email_alerter = GmailAlert(**self.config['gmail'])
 
    def purchase_new_listings(self):
        print('Starting purchase_new_listings')
        print('--------------------------------')
        print()
        bl = BinanceListings()
        cc_listings = bl.future_cc_listing_releases()
        print(cc_listings)

        if self.email_alerter != None:
            for url, cc_listing in cc_listings.items():
                self.email_alerter.notify(cc_listing['tokens'], cc_listing['release_date'])
        
        time.sleep(60*10)

if __name__ == '__main__':
    abspath = os.path.abspath(__file__)
    dirname = os.path.dirname(abspath)
    os.chdir(dirname)
    while True:
        ieo = IEOMoon()
        ieo.purchase_new_listings()