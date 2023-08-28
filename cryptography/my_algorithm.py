# methodology of algorithm:
# key: not fixed
# Blocks: Bytes (per ASCII character)
# ex.:
# key = xyz (3 character)
# text = abc

# key calculation: 120+121+122/3 = 121

# encryption:
# a:97+121=218 -> Ú
# b:98+121=219 -> Û
# c:99+121=220 -> Ü

# decryption:
# Ú: 218-121=97 -> a
# Û: 219-121=98 -> b
# Ü: 220-121=99 -> c


def save_file(results, file_path):
    with open(file_path, 'w') as f:
        f.write(results)

def open_file(file_path):
    #create file object
    with open(file_path, 'r') as f:  # Using 'with' to automatically close the file
    #read file contents
        file_contents = f.read()

    return file_contents

def calculate_key(key):
    results = 0
    counter = 0
    #convert each character into INT and added to results
    for char in key:
        counter += 1
        results += ord (char)

    #return the results divided by the number of characters in the key
    return int (results/counter)

def decrypt(file_path, key):
    #Get encrypted text data
    file_contents = open_file (file_path)
    #Calculate the key
    key_calc = calculate_key (key)
    dec_res = ''

    for line in file_contents.split('\n'):  # Split the contents into lines
        for wrd in line.split(' '):  # Split the line into words
            for char in wrd:
                #Subtract from the key results
                #The ord() function returns the number representing the unicode code of a specified character
                int_char = ord (char) - key_calc
                #append results
                dec_res += chr (int_char)
            dec_res += ' '  # Add space between words
        dec_res += '\n'  # Add newline at the end of the line

    save_file (dec_res, file_path)
    print ('Finished dencryption')

def encrypt(file_path, key):
    #Get clear text data
    file_contents = open_file (file_path)
    #Calculate the key
    key_calc = calculate_key (key)
    enc_result = ''

    for char in file_contents:
        int_char = ord(char) + key_calc
        enc_result += chr(int_char)

    save_file (enc_result, file_path)
    print ('Finished encryption')

def main():
    print ('Please choose one of the following:\n 1]Encrypt\n 2]Decrypt')
    choice = input('>')
    print ('Enter the file path')
    file_path = input('>')
    print('Enter the secret key')
    key = input('>')

    #Encrypt
    if choice == '1':
        encrypt (file_path, key)
    #Decrypt
    elif choice == '2':
        decrypt (file_path, key)
    else:
        print ('Invalid choice')

main()