from gmailalert import GmailAlert
from listings import BinanceListings
import yaml
import time

class IEOMoon:
    def __init__(self, config_file='config.yaml'):
        with open(config_file) as file:
            self.config = yaml.load(file, Loader=yaml.FullLoader)
            self.email_alerter = None

        if 'gmail' in self.config.keys():
            self.email_alerter = GmailAlert(**self.config['gmail'])
 
    def purchase_new_listings(self):
        bl = BinanceListings()
        cc_listings = bl.future_cc_listing_releases()
        print(cc_listings)

        if self.email_alerter != None:
            for url, cc_listing in cc_listings.items():
                self.email_alerter.notify(cc_listing['tokens'], cc_listing['release_date'])
        
        time.sleep(60*10)

if __name__ == '__main__':
    while True:
        ieo = IEOMoon()
        ieo.purchase_new_listings()