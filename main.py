from venmo_api import Client
from household import House
import easygui

def printinfo(house):
    print("Monthly Rent Burden: ${:.2f}".format(house.totalrent))
    print("Member Rent Breakdown: ")
    for uid, amount in house.rent.items():
        print("{:<15}    ${:<}".format(house.members[uid], amount))
    print("Total Monthly Collection: ${:.2f}".format(sum(list(house.rent.values())) + house.operatorrent))
    print("Recent Transactions: ")
    for date, transtype, message, name in [("Date", "Transaction Type", "Request Message", "Name")] + house.transactions[::-1]:
        print("{}     {:<}    {:<}    {:<}".format(date, transtype, message, name))
    print("\n\n")


def main():
    house = House()
    print('Welcome! Please ensure you exit the program using commandline to ensure active profiles are saved!')
    while True:
        action = str(input("Enter n for new profile, i to import existing profile, or q to quit. (n/i/q)"))
        if action == 'n':
            username = str(input("Please enter your venmo username and press enter."))
            password = str(input("Please enter your venmo password and press enter."))
            access_token = Client.get_access_token(username=username, password=password)
            house.token = access_token
            break
        elif action == 'i':
            file_path = easygui.fileopenbox(msg="Select profile to import.", title="Import Profile", filetypes=["*.prex", "*.PREX"])
            if file_path == '':
                print("Error! You must select a profile to import.")
                continue
            else:
                print("importing....\n")
                house.importf(file_path)
                break
        elif action == 'q':
            quit()
        else:
            print("Invalid command!\n")
    house.startclient()
    while True:
        print("Please note for all charges where all members are charged, you are included in the calculation but won't be charged (can't venmo request yourself)!\n")
        action = str(input("Enter r to charge rent, e to edit/set up profile information such as rent burden, c to charge for utility/fine, or sq to save and exit. (r/e/c/sq)"))
        if action == 'r':
            message = str(input("Enter a message for the Venmo request. If left empty, 'Rent' will be used"))
            a = house.chargerent(message) if message != '' else house.chargerent()
            if a == True:
                print("Venmo requests sent!\n")
            else:
                print("An unknown error has occured. Please save and exit prior to reattempting.\n")
        elif action == 'e':
            while True:
                printinfo(house)
                action = str(input("Enter r to edit rent breakdown, d to remove a member, a to add a new member, or e to return to main menu. (r/d/a/e)"))
                if action == 'r':
                    print("UID    Name      Monthly Rent")
                    for uid, amount in house.rent.items():
                        print("{}     {:<}    ${:<}".format(uid, house.members[uid], amount))
                    while True:
                        action = str(input("Please enter the UID of the member you would like to modify, enter s to modify operator rent (your rent, not collected through venmo), or e to return to previous menu."))
                        if action == 'e': 
                            print()
                            break
                        elif action == 's': 
                            house.operatorrent = float(input("Please enter the new monthly rent for the operator in numeric form (eg. 400 or 400.00). "))
                            print("Rent updated successsfully!\n")
                            break
                        elif action not in list(house.members.keys()):
                            print("Error: Invalid uid\n")
                        else:
                            newrent = float(input("Please enter the new monthly rent for {} in numeric form (eg. 400 or 400.00). ".format(house.members[action])))
                            a = house.rent[action] = newrent
                            if a == True: 
                                print("Rent updated successsfully!\n")
                            else:
                                print("An unknown error has occured.\n")
                            break
                elif action == 'd':
                    print("UID    Name")
                    for uid, name in house.members.items(): print("{}      {}".format(uid, name))
                    while True:
                        action = int(input("Please enter the UID of the member to be removed or enter e to return to previous menu."))
                        if action == 'e':
                            print()
                            break
                        elif action in house.members.keys():
                            a = house.delmembers(action)
                            if a == True: 
                                print("Member removed successfully!\n")
                            else:
                                print("An unknown error has occured.\n")
                            break
                        else:
                            print("Error: Invalid input!")
                elif action == 'a':
                    print("UID    Name")
                    for uid, name in house.members.items(): print("{}      {}".format(uid, name))
                    name = str(input("Please enter the name of the new member to-be added."))
                    uid = 1
                    while True:
                        if uid in house.members.keys():
                            uid += 1
                        else:
                            break
                    newrent = float(input("Please enter the new monthly rent for the new member in numeric form (eg. 400 or 400.00). "))
                    venmo = str(input("Please enter the venmo username of the new member (username, not display name)."))
                    a = house.addmembers(uid, name, newrent, venmo)
                    if a ==  True:
                        print("New user added successfully!\n")
                    else: 
                        print("An unknown error has occured!\n")
                elif action == 'e':
                    break
        elif action == 'c':
            print("UID    Name")
            for uid, name in house.members.items(): print("{}      {}".format(uid, name))
            uids = str(input("\n\nPlease enter the UIDs of those to be charged (separated by a space), a to charge all users (you will be included in the calculation but will not be charged), or e to exit to main menu."))
            if uids == 'e': continue
            elif uids == 'a':
                uids = list(house.members.keys())
            else:
                uids = uids.split(" ")
            chargeamount = float(input("Please enter the total charge amount in numeric form."))
            message = str(input("Please enter a messsage for the Venmo request (eg. fine for not doing dishes). If left blank the default 'Utility' will be used"))
            splitbyrent = str(input("Please enter y if you would like to split the request by rent paid (if the member pays 15% of the rent they will pay 15% of the total amount), else type n. (y/n)"))
            if splitbyrent not in ['y', 'n']:
                print("Invalid Input!")
                continue
            if message == '':
                a = house.chargeothers(chargeamount, uids) if splitbyrent == 'n' else house.chargeothers(chargeamount, uids, splitbyrent=True)
            else:
                a = house.chargeothers(chargeamount, uids, message) if splitbyrent == 'n' else house.chargeothers(chargeamount, uids, message, splitbyrent=True)
            if a != True:
                print("An unknown error has occured.\n")
            else:
                print("Charge request sent successfully!\n")
        elif action == 'sq':
            while True: 
                file_path = easygui.fileopenbox(msg="Choose a location and filename to save the current profile.", title="Export Profile", filetypes=["*.prex", "*.PREX"])
                if file_path == '':
                    print("Error! You must provide a valid filename to save to.")
                    continue
                else:
                    print("Exporting....")
                    house.export(file_path)
                    quit()


main()
