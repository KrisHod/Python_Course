str = ' PYTHON '
print('>' + str + '<')
str = str.strip()
print('>' + str + '<')

print('>' + str[1:3] + '<')

""""""
log_file = "2022/01/01 04:12:05 MikeW 200 success login.aspx"
parts = log_file.split()

date = parts[0]
time = parts[1]
user = parts[2]
status = parts[3]
result = parts[4]
page = parts[5]

print("On {}, User {} had {} on page: {}".format(date, user, result, page))