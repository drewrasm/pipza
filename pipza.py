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

def getCustomer(mode, configFile): 
    customer = configFile.get('customer')

    if(customer != None and mode !='custom'):
        firstName = customer.get('first_name')
        lastName = customer.get('last_name')
        if(firstName == '' or lastName == ''):
            fullName = input('Enter your first and last name (ex: Babe Ruth): ')
            firstName = fullName.split(' ')[0]
            lastName = fullName.split(' ')[1]
        email = customer.get('email')
        if(email == ''):
            email = input('Please enter your email: ')
        phone = customer.get('phone')
        if phone == '':
            phone = input('Please enter your phone number: ')

    else: 
        print('Your customer info: ')
        fullName = input('Enter your first and last name (ex: Babe Ruth): ')
        firstName = fullName.split(' ')[0]
        lastName = fullName.split(' ')[1]
        email = input('Please enter your email: ')
        phone = input('Please enter your phone number: ')
    return pizzapi.Customer(firstName, lastName, email, phone)

def getAddress(mode, configFile):
    address = configFile.get('address')
    if(address != None and mode !='custom'):
        street = address.get('street')
        if street == '':
            street = input('Please enter your street (ex: 299 east example way): ')
        city = address.get('city')
        if city == '':
            city = input('Please enter your city: ')
        state = address.get('state')
        if state == '':
            state = input('Please enter your state (ex: \'UT\' for Utah): ')
        zipCode = address.get('zip_code')
        if zipCode == '':
            zipCode = input('Please enter your zip code: ')
    else: 
        print('Your address: ')
        street = input('Please enter your street (ex: 299 east example way): ')
        city = input('Please enter your city: ')
        state = input('Please enter your state (ex: \'UT\' for Utah): ')
        zipCode = input('Please enter your zip code: ')
    return pizzapi.Address(street, city, state, zipCode)
    
def getStore(address):
    return address.closest_store()

def displayStoreData(store):
    details = store.get_details()
    storeId = details['StoreID']
    streetName = details['StreetName']
    city = details['City']
    region = details['Region']
    phone = details['Phone']
    print(f'Your store is :  ID: { storeId }, ADDRESS: {streetName}, {city}, {region}')
    print(f'Their phone number is: {phone}')

def getCard(configFile):
    card = configFile.get('card')
    if(card != None and mode !='custom'):
        cardNumber = card.get('card_number')
        if(cardNumber == ''):
            cardNumber = input('Please enter your card number: ')
        pin = card.get('pin')
        if(cardNumber == ''):
            pin = input('Please enter your pin: ')
        zipCode = card.get('zip')
        if(zipCode == ''):
            zipCode = input('Please enter the zip code: ')
        expiration = card.get('expiration')
        if(expiration == ''):
            expiration = input('Please enter the expiration date: ')
    else: 
        print('Your card: ')
        cardNumber = input('Please enter your card number: ')
        pin = input('Please enter your pin: ')
        zipCode = input('Please enter the zip code: ')
        expiration = input('Please enter the expiration date: ')
    return pizzapi.PaymentObject(cardNumber, expiration, pin, zipCode)

def displayOrder(orderData):
    products = orderData['Products']
    print('+++++++++++++')
    print('YOUR ORDER: ')
    if len(products) == 0:
        print('your order is empty!')
        exit()
    for product in products:
        price = product['Price']
        name = product['Name']
        print(f'\t - {name} : {price}')
    
mode = ''
defaultOrder = False
for i in range(len(sys.argv)):
    if(sys.argv[i] == '-default'):
        #use all the available file values
        mode = 'default'
        default = print('would you like to user your default order? (y/n): ')
        if default == 'y' or default == 'yes':
            defaultOrder = True
        break
    if(sys.argv[i] == '-custom'): 
        #use inputs
        mode = 'custom'
        break
    if(sys.argv[i] == '-help'):
        print('*only one command is valid at a time*')
        print('here are the available commands: ' + '\n' + '-help (displays the available arguments)' + '\n' + '-default (reads available values from config file to the program)' + '\n' + '-custom (allows for full custom inputs for order)' )
        break

try: 
    with open('config.json') as json_file:
        configFile = json.load(json_file)
except: 
    configFile = ''

customer = getCustomer(mode, configFile)
address = getAddress(mode, configFile)
store = getStore(address)
card = getCard(configFile)

print('Hello, ' + customer.first_name + ' ' + customer.last_name)
displayStoreData(store)

if(not store.data['IsOpen']):
    print('warning, the closest store to you is closed, you may want to call them')

menu = store.get_menu()
order = pizzapi.Order(store, customer, address)


if defaultOrder == False: 
    print('Let\'s build your order!')
    print('--------------------------')

    print('Here is the menu along with the item codes')
    codes = menu.menu_by_code
    for code in codes:
        currentData = codes[code].menu_data
        if 'ReferencedProductCode' in currentData.keys() and 'Size' in currentData.keys():
            print('___________________' + '\n')
            print(currentData['ReferencedProductCode'])
            print(currentData['Size'])
            print(currentData['Name'])

    ordering = True
    while ordering:
        print()
        item = input('Please enter an order item (enter c to cancel): ')
        if item != 'c' and item != 'cancel': 
            try:
                order.add_item(item)
            except:
                print('oops looks like a bad code, try again')
                continue
        if item == 'c':
            print('it did equal c')
        
        keepGoing = input('Would you like to add another? (y/n): ')
        if keepGoing == '' or keepGoing == 'n' or keepGoing == 'no':
            ordering = False
else: 
    try: 
        with open('config.json') as json_file:
            orderData = json.load(json_file).get('default_order')
    except: 
        orderData = ''
    for item in orderData:
        try:
            order.add_item(item)
        except:
            print('there seems to be a bad item in your default order, check your config.json file')

displayOrder(order.data)


#COMMENT THIS OUT IF YOU DO NOT WANT TO RISK MAKING AN ACTUAL PURCHASE
isRealPurchase = (input('+++ WOULD YOU LIKE TO ACTUALLY CHARGE YOUR CARD? (y/n) +++: ') == 'y')
if isRealPurchase: 
    paymentData = order.pay_with(card)
else: 
    paymentData = order.place(card)

#COMMENT THIS OUT ONCE YOU ARE SET ON MAKING A PURCHASE
# paymentData = order.pay_with(card)


for data in paymentData['Order']['AmountsBreakdown'].keys():
    print(data, ': ', paymentData['Order']['AmountsBreakdown'][data])

# desiredData = ['Customer', 'Surcharge', 'Tax']
# for data in desiredData:
#     if data in paymentData['Order']['AmountsBreakdown']:
#         print(data, ': ', paymentData['Order']['AmountsBreakdown'][data])

#TODO: find out how to see if it was a successful order





    

