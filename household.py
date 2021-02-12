from venmo_api import Client
import pickle
from datetime import date

class House():
    version = 1.0
    def __init__(self, access_token = ''):
        self.token = access_token
        self.members = {}
        self.totalrent = 0
        self.rent = {}
        self.operatorrent = 0.00
        self.balance = 0
        self.venmo = {}
        self.transactions = []
    def startclient(self):
        self.session = Client(self.token)
        return True
    def delmembers(self, uid):
        del self.rent[uid]
        del self.venmo[uid]
        del self.members[uid]
        return True
    def addmembers(self, uid, name, rent, venmo):
        if uid in self.members.keys():
          return False
        self.members[uid] = name
        self.getuser(uid, venmo)
        self.rent = rent
        return True
    def chargerent(self, message = "Rent"):
        if (sum(list(self.rent.values())) + self.operatorrent) < self.totalrent:
            while True:
                re = input("Amount to be charged (${:.2f}) does not cover the total rent burden (${:.2f}). Would you like to continue? (y/n)".format(sum(list(self.rent.values())), self.totalrent))
                if re == 'y':
                    break
                elif re == 'n':
                    return False
                else:
                    print("Invalid response!")
        for uid in list(self.rent.keys()):
            amount = self.rent[uid]
            charge = self.session.payment.request_money(amount=amount, note=message, target_user_id=int(self.venmo[uid].id))
            if charge != True:
                print("Error: ", charge)
            else:
                self.transactions.append((date.today().strftime("%b-%d-%Y"), "Request", amount, message, self.members[uid]))
        return True

    def chargeothers(self, amount, uids, message = "Utility", splitbyrent = False):
        icharges = {i: amount/len(uids) for i in self.members.keys()}
        chargeop = True
        for i in uids:
            if i not in self.members.keys(): chargeop = False
        if splitbyrent == True:
            totalratiorent = sum([self.rent[i] for i in uids]) if chargeop == False else sum([self.rent[i] for i in uids]) + self.operatorrent
            for i in uids:
                icharges[i] = (self.rent[i] / totalratiorent) * amount
        for uid, totcharge in icharges.items():
            if totcharge == 0:
                continue
            charge = self.session.payment.request_money(amount=icharges[uid], note=message, target_user_id=int(self.venmo[uid].id))
            if charge != True:
                print("Error: ", charge)
            else:
                self.transactions.append((date.today().strftime("%b-%d-%Y"), "Request", amount, message, self.members[uid]))
        return True

        pass
    def getuser(self, uid, username):
        self.venmo[uid] = self.session.user.get_user_by_username(username)
        return True

    def export(self, filepath):
        with open(filepath, 'wb') as f:
            pickle.dump([self.version, self.token, self.totalrent, self.balance, self.rent, self.venmo, self.members, self.transactions, self.operatorrent], f)
    def importf(self, filepath):
        with open(filepath, 'rb') as f:
            self.version, self.token, self.totalrent, self.balance, self.rent, self.venmo, self.members, self.transactions, self.operatorrent = pickle.load(f)