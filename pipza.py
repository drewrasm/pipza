import pizzapi
import json
import sys

print('Welcome to the best way to order your Domino\'s pizza')
print('_________________________')

try: 
    f =  open('config.json')
except: 
    print('you do not have a settings file set up, if you would like one, please make a file called config.json, an example is provided.' + '\n')
    print('_________________________')

def getCustomer(mode): 
    #check for each of the needed variables if it exists inside of the config file, if not just use the custom ones
    try: 
        with open('config.json') as json_file:
            customer = json.load(json_file).get('customer')
    except: 
        customer = ''

    if(customer != '' and mode !='custom'):
        firstName = customer.get('first_name')
        lastName = customer.get('last_name')
        email = customer.get('email')
        phone = customer.get('phone')
    else: 
        print('Your customer info: ')
        fullName = input('Enter your first and last name (ex: Babe Ruth): ')
        firstName = fullName.split(' ')[0]
        lastName = fullName.split(' ')[1]
        email = input('Please enter your email: ')
        phone = input('Please enter your phone number: ')
    return pizzapi.Customer(firstName, lastName, email, phone)

def getAddress(mode):
    #check for each of the needed variables if it exists inside of the config file, if not just use the custom ones
    try: 
        with open('config.json') as json_file:
            address = json.load(json_file).get('address')
    except: 
        address = ''

    if(address != '' and mode !='custom'):
        street = address.get('street')
        city = address.get('city')
        state = address.get('state')
        zipCode = address.get('zip_code')
    else: 
        print('Your address: ')
        street = input('Please enter your street (ex: 299 east example way): ')
        city = input('Please enter your city: ')
        state = input('Please enter your state (ex: \'UT\' for Utah): ')
        zipCode = input('Please enter your zip code: ')
    return pizzapi.Address(street, city, state, zipCode)
    
def getStore(address):
    return address.closest_store()

mode = ''
for i in range(len(sys.argv)):
    if(sys.argv[i] == '-default'):
        #use all the available file values
        mode = 'default'
        break
    if(sys.argv[i] == '-custom'): 
        #use inputs
        mode = 'custom'
        break
    if(sys.argv[i] == '-help'):
        print('*only one command is valid at a time*')
        print('here are the available commands: ' + '\n' + '-help (displays the available arguments)' + '\n' + '-default (reads available values from config file to the program)' + '\n' + '-custom (allows for full custom inputs for order)' )
        break

customer = getCustomer(mode)
address = getAddress(mode)
store = getStore(address)

print('Hello, ' + customer.first_name + ' ' + customer.last_name)
print('Your store is : ', store)






    

