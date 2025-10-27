#rock paper scissors and shoe
#randomized 2 user choose
#Shoe can win only against, everyone else can beat shoe
import random
while True:
    num = random.randint(0, 3)
    mm = ["rock", "paper", "scissors", "shoe"]

    comp_choice = mm[num]
    choice = input("Type 'rock', 'paper', 'scissors' or 'shoe'").lower()

    if choice == comp_choice:
        print(f"Comp chose {comp_choice}. It's a tie")
    elif choice == mm[0] and comp_choice == mm[1]:
        print(f"Comp wins!")
    elif choice == mm[0] and comp_choice == mm[2]:
        print(f"You win!")
    elif choice == mm[0] and comp_choice == mm[3]:
        print(f"Comp wins!")
    elif choice == mm[1] and comp_choice == mm[0]:
        print(f"You win!")
    elif choice == mm[1] and comp_choice == mm[2]:
        print(f"Comp wins!")
    elif choice == mm[1] and comp_choice == mm[3]:
        print(f"You win!")
    elif choice == mm[2] and comp_choice == mm[0]:
        print(f"Comp wins!")
    elif choice == mm[2] and comp_choice == mm[1]:
        print(f"You win!")
    elif choice == mm[2] and comp_choice == mm[3]:
        print(f"You win!")
    elif choice == mm[3] and comp_choice == mm[0]:
        print(f"You win!")
    elif choice == mm[3] and comp_choice == mm[1]:
        print(f"Comp wins!")
    elif choice == mm[3] and comp_choice == mm[2]:
        print(f"Comp wins!")


