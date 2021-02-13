from venmo_api import Client
import pickle
from datetime import date

class House():
    """
    This class is responsible for maintaining profile information as well as interacting with venmo API
    """
    version = 1.0
    def __init__(self, access_token = ''):
        """
        Initializes object and creates profile attributes
        Returns None
        """
        self.token = access_token
        self.members = {}
        self.totalrent = 0
        self.rent = {}
        self.operatorrent = 0.00
        self.balance = 0
        self.venmo = {}
        self.transactions = []
    def startclient(self):
        """
        Starts venmo API client after token has been either entered or loaded from imported profile.
        Returns True if process is successful.
        """
        self.session = Client(self.token)
        return True
    def delmembers(self, uid):
        """
        Removes member from all associated attributes.
        Returns True if process is successful.
        """
        del self.rent[uid]
        del self.venmo[uid]
        del self.members[uid]
        return True
    def addmembers(self, uid, name, rent, venmo):
        """
        Adds new member information to all associated attributes.
        Returns True if process is successful.
        """
        if uid in self.members.keys():
          return False
        self.members[uid] = name
        self.getuser(uid, venmo)
        self.rent = rent
        return True
    def chargerent(self, message = "Rent"):
        """
        Sends venmo requests of self.rent[uid] to all members of the profile excluding operator.
        Returns True if process is successful.
        """
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
        """
        Sends venmo requests of custom amounts and splitting methods to specified members of the profile excluding operator.
        Returns True if process is successful.
        """
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
        """
        Retrieves Venmo API's User object containing user information from venmo username.
        Returns True if successful.
        """
        self.venmo[uid] = self.session.user.get_user_by_username(username)
        return True

    def export(self, filepath):
        """
        Exports active profile.
        Returns None
        """
        with open(filepath, 'wb') as f:
            pickle.dump([self.version, self.token, self.totalrent, self.balance, self.rent, self.venmo, self.members, self.transactions, self.operatorrent], f)
    def importf(self, filepath):
        """
        Imports previously saved profile.
        Returns None
        """
        with open(filepath, 'rb') as f:
            self.version, self.token, self.totalrent, self.balance, self.rent, self.venmo, self.members, self.transactions, self.operatorrent = pickle.load(f)