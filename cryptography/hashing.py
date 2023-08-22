from Crypto.Hash import SHA256

def calculate_hash(password):
    h = SHA256.new()
    # Encode the password string into bytes before updating the hash
    h.update(password.encode('utf-8'))
    return h.hexdigest()

def subscribe(user_name, password):
    account = user_name + ':' + calculate_hash(password)
    f = open('accounts.txt', 'w')
    f.write(account)
    f.close()
    print ('You are registered now!')
    

def login(user_name, password):
    f = open('accounts.txt', 'r')
    account_file = f.read()
    s = account_file.split(':')
    user_name_file = s[0]
    password_file = s[1]
    hashed_password = calculate_hash(password)

    if user_name == user_name_file and hashed_password == password_file:
        print ('You are Authenticated :)')
    else:
        print ('Invalid password')


def main():
    chioce = input("Enter\n 1] to subscribe\n 2] to login\n Choice>")

    if chioce == '1':
        user_name = input("Enter a username: ")
        password = input("Enter a password: ")
        subscribe(user_name, password)
    elif chioce == '2':
        user_name = input("Enter a username: ")
        password = input("Enter a password: ")
        login(user_name, password)
    else:
        print ("Invalid choice")


main()

