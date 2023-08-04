current_movies = {'The Grinch' : "11:00am",
                  'Rudolph' : "1:00pm",
                  'Frosty the Snowman' : "3:00pm",
                  'Christmas Vacation' : "5:00pm"}

print("We're shoowing the following movies:")
for key in current_movies:
    print(key)

movie = input("What movie would you like  the showtime for?\n")

showtime = current_movies.get(movie) 

#if showtime = none -> false
if showtime: 
    print(movie, 'is playing at', showtime)
else:
    print("Requested movie isn't playing")