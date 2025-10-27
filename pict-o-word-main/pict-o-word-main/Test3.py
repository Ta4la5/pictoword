#Higher, lower, same, infinite lives
# num range: 1-500
#Guess between 1- 500
#Computer chooses number and hides
#Checks through with yours.
#Higher, lower, and checks till how long you get same number.

import random
comp_num = random.randint(1, 500)
trials = 0
n = 0


while n == 0:
    choice = int(input("Enter a number between 1 and 500."))
    if choice == comp_num:
        print("Same, you've printed the right number")
        trials += 1
        n = 1
    elif choice > comp_num:
        print("Higher")
        trials += 1
    elif choice < comp_num:
        print("Lower")
        trials += 1

