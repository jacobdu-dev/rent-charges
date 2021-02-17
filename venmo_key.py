from venmo_api import Client
import time
username = str(input("Please enter your venmo username and press enter: "))
password = str(input("Please enter your venmo password and press enter: "))
access_token = Client.get_access_token(username=username, password=password)
print("Your Access Token is ", access_token + ". Ensure this is used when creating a new profile!")
time.sleep(600)