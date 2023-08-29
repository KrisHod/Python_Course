from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes

user_data = {}

def ask_credentials():
    username = input("Enter your username: ")
    password = input("Enter your password: ")
    return username, password

def save_user_data(username, salt, hashed_password):
    # Save the username, salt, and hashed password to the user_data dictionary
    user_data[username] = {
        'salt': salt,
        'hashed_password': hashed_password
    }

def retrieve_user_data(username):
    # Retrieve the salt and hashed password from the user_data dictionary
    user = user_data.get(username)
    if user:
        salt = user['salt']
        hashed_password = user['hashed_password']
        return salt, hashed_password
    else:
        return None, None

def register_user(username, password):
    # Generate a random salt
    salt = get_random_bytes(16)

    # Add the salt to the password
    salted_password = password.encode() + salt

    # Create a SHA-256 hash object
    hash_object = SHA256.new()
    hash_object.update(salted_password)

    # Get the hashed password as a hexadecimal string
    hashed_password = hash_object.hexdigest()

    # Save the username, salt, and hashed password to a database or file
    save_user_data(username, salt, hashed_password)
    print("User", username, "registered successfully.")

def login_user(username, password):
    # Retrieve the salt and hashed password from the database or file
    salt, hashed_password = retrieve_user_data(username)

    if salt is None or hashed_password is None:
        print("Login failed. User not found.")
        return

    # Add the salt to the provided password
    salted_password = password.encode() + salt

    # Create a SHA-256 hash object
    hash_object = SHA256.new()
    hash_object.update(salted_password)

    # Get the hashed password for comparison
    input_hashed_password = hash_object.hexdigest()

    # Compare the input hashed password with the stored hashed password
    if input_hashed_password == hashed_password:
        print("Login successful. Welcome back,", username + "!")
    else:
        print("Login failed. Invalid credentials.")

    # Example usage
register_user("myuser", "password123")
register_user("carson", "Str0ng!Password")
register_user("fred", "111111")

for user in user_data:
    print(user + " " + str(user_data[user]))

username, password = ask_credentials()
login_user(username, password)