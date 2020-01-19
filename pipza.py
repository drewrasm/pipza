import pizzapi


print('Welcome to the best way to order your Domino\'s pizza')
print('_____________________________________________________')

def getCustomer(): 
    print('Your customer info: ')
    fullName = input('Enter your first and last name (ex: Babe Ruth): ')
    firstName = fullName.split(' ')[0]
    lastName = fullName.split(' ')[1]
    email = input('Please enter your email: ')
    phone = input('Please enter your phone number: ')
    return pizzapi.Customer(firstName, lastName, email, phone)

def getAddress():
    print('Your address: ')
    street = input('Please enter your street (ex: 299 east example way): ')
    city = input('Please enter your city: ')
    state = input('Please enter your state (ex: \'UT\' for Utah): ')
    zipCode = input('Please enter your zip code: ')
    return pizzapi.Address(street, city, state, zipCode)
    
def getStore():
    return getAddress().closest_store()

customer = getCustomer()
store = getStore()

print('Hello, ' + customer.first_name + ' ' + customer.last_name)
print('Your closest store is: ' + store)

