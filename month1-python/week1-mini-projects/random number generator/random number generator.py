import random

class player():
    def __init__(self):
        self.name = input("enter your name: ")
        self.score = 0
        self.best_score = 0
        self.attempts_taken = 0

    def calculate_score(self, attempts_taken, max_attempts):
        if attempts_taken == 0:
            return 0
        score = int((max_attempts - attempts_taken + 1) / max_attempts * 1000)
        return max(score, 100) 

    def update_best_score(self):
        if self.score > self.best_score:
            self.best_score = self.score

class game():
    def __init__(self, player):           
        self.player = player               
        self.range_ = None
        self.random_number = None
        self.attempt = 0
        self.hint = 0
        self.limit = None
        self.difficulty = None
        self.max_attempts = 10

    def choose_difficulty(self):
        print("\n" + "-" * 50)
        print("1 - easy   (1–50,  unlimited or 10 attempts)")
        print("2 - medium (1–100, unlimited or 7 attempts)")
        print("3 - hard   (1–300, unlimited or 5 attempts)")
        print("4 - set range yourself")
        print("5 - exit")
        while True:
            try:
                self.difficulty = int(input("choose one of the option number from above: "))
                if self.difficulty in range(1, 5):
                    break
                elif self.difficulty == 5:
                    quit()
                else:
                    print("you must choose only the option number [1-5]")
                    continue
            except ValueError:
                print("you must choose only the option number [1-5]")
                continue

        while True:
            self.limit = input("do you want unlimited attempts till you get correct? [Y/N]: ").strip().upper()
            if self.limit == 'Y' or self.limit == 'N':
                break
            else:
                print("you must only enter 'Y' or 'N'")
                continue

    def set_range(self):
        if self.difficulty == 1:
            self.range_ = range(1, 50)
            self.max_attempts = 10
        elif self.difficulty == 2:
            self.range_ = range(1, 100)
            self.max_attempts = 7
        elif self.difficulty == 3:
            self.range_ = range(1, 300)
            self.max_attempts = 5            
        else:
            while True:
                try:
                    min_range = int(input("enter the minimum number: "))
                    if min_range < 0:
                        print("minimum number should be greater than or equal to zero")
                        continue
                    while True:
                        try:
                            max_range = int(input("enter the maximum number: "))
                            if max_range <= 0 or max_range <= min_range:
                                print("maximum number must be greater than minimum number")
                                continue
                            else:
                                break
                        except ValueError:
                            print("you must enter a number greater than zero")
                            continue
                    break
                except ValueError:
                    print("you must enter only numbers")
                    continue
            self.range_ = range(min_range, max_range)
            self.max_attempts = 10

    def get_hint(self):                             
        difference = abs(self.player_input - self.random_number)
        if difference <= 5:
            proximity = "🔥 burning hot"
        elif difference <= 15:
            proximity = "♨️  hot"
        elif difference <= 30:
            proximity = "🌤️  warm"
        elif difference <= 50:
            proximity = "❄️  cold"
        else:
            proximity = "🧊 freezing"

        if self.player_input < self.random_number:
            direction = "go higher ⬆️"
        else:
            direction = "go lower ⬇️"

        print(f"{proximity} — {direction}")

    def set_number_and_ask_input(self):
        self.random_number = random.randint(self.range_.start, self.range_.stop)
        self.attempt = 0

        if self.limit == 'Y':
            self.hint = 0
            while True:
                while True:
                    try:
                        self.player_input = int(input(f"\nattempt {self.attempt + 1} — guess a number between {self.range_.start} and {self.range_.stop}: "))
                        if self.player_input in self.range_:
                            self.attempt += 1
                            break
                        else:
                            print(f"you must only choose number in range {self.range_.start} to {self.range_.stop}")
                            continue
                    except ValueError:
                        print(f"you must only choose number in range {self.range_.start} to {self.range_.stop}")
                        continue

                if self.player_input == self.random_number:
                    print(f"\n🎯 you got it right in {self.attempt} attempts!")
                    break
                else:
                    hint_option = input("do you want a hint? [Y/N]: ").upper().strip()
                    if hint_option == 'Y':
                        self.hint += 1
                        self.get_hint()         # 🔥 calling the method cleanly
                    else:
                        continue
                    
        else:
            self.hint = 3
            while self.attempt < self.max_attempts:
                while True:
                    try:
                        self.player_input = int(input(f"\nattempt {self.attempt + 1}/{self.max_attempts} — guess a number between {self.range_.start} and {self.range_.stop}: "))
                        if self.player_input in self.range_:
                            self.attempt += 1
                            break
                        else:
                            print(f"you must only choose number in range {self.range_.start} to {self.range_.stop}")
                            continue
                    except ValueError:
                        print(f"you must only choose number in range {self.range_.start} to {self.range_.stop}")
                        continue

                if self.player_input == self.random_number:
                    print(f"\n🎯 you got it right in {self.attempt} attempts!")
                    break
                else:
                    if self.hint > 0:
                        hint_option = input(f"do you want to use one of your remaining {self.hint} hints? [Y/N]: ").upper().strip()
                        if hint_option == 'Y':
                            self.hint -= 1
                            self.get_hint()     
                        else:
                            continue
                    else:
                        print("you have no remaining hints")
                        self.get_hint()        
            else:
                print(f"\n💀 out of attempts! the number was {self.random_number}")
                return                         
            
        self.player.attempts_taken = self.attempt
        self.player.score = self.player.calculate_score(self.attempt, self.max_attempts)
        self.player.update_best_score()

    def display_result(self):
        print("\n" + "=" * 50)
        print(f"  🏆 {self.player.name}'s result")
        print("=" * 50)
        print(f"  attempts taken : {self.player.attempts_taken}")
        print(f"  hints used     : {self.hint}")
        print(f"  score          : {self.player.score}")
        print(f"  best score     : {self.player.best_score}")
        print("=" * 50)


def main():
    print("-" * 70)
    print("welcome to the number guessing game")
    print("-" * 70)

    p = player()                   

    while True:
        g = game(p)                
        g.choose_difficulty()
        g.set_range()
        g.set_number_and_ask_input()
        g.display_result()

        while True:
            play_again = input("\nplay again? [Y/N]: ").upper().strip()
            if play_again in ['Y', 'N']:
                break
            print("enter only Y or N")

        if play_again == 'N':
            print(f"\nthanks for playing {p.name}! your best score was {p.best_score} 🏆")
            break

if __name__ == "__main__":
    main()
