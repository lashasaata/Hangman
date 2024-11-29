def Hangman():
    global guessed_words
    guessed_words = 0

    print("Wellcome to Hangman game!")
    print("Choose the difficulty level...\n==============================\n || Hard || Medium || Easy ||\n------------------------------")
    
    game_lvl = input("Set the level: ").lower()
    while game_lvl not in ("hard", "medium", "easy"):
        game_lvl = input("Choose the level from the menu!: ").lower()
    print()

    with open("Hangman_Game/words.json", mode="r", encoding="utf-8") as file:
        import json, random
        data = json.load(file)

    def guessing(data, lvl):
        words = data[lvl]
        word_index = random.randint(0, len(words)-1)
        guessing_word = words[word_index]["word"].lower()

        lifes = 10
        guessed_alpabets = []
        printing = []

        # making "_"s for the letters
        for _ in range(0,len(guessing_word)):
            printing.append("_ ")

        def guess(lifes):
            global guessed_words
            life = lifes

            #if player has less than 4 lives, it will give a hint
            if life > 3:
                print(f"You have {life} lives.")
            else:
                print(f"Because you have left {life} lives, we have a hint for you.\n")
                print(f"The hint: {words[word_index]["hint"]}")
            print("The word: "+"".join(printing)+"\n")

            user_guess = input("Enter your guess: ")
            print()

            #this part makes sure that user will input only unique guesses
            if not user_guess.isalpha():
                while not user_guess.isalpha():
                    user_guess = input("You must input only alpabets!: ")
            elif len(user_guess) == 1 or len(user_guess) == len(guessing_word):
                while user_guess in guessed_alpabets:
                    user_guess = input("You have already guessed that!\nEnter your other guess: ")
                    print()
            else:
                while len(user_guess) not in (1,len(guessing_word)):
                    user_guess = input(f"Your guessing must contain only one letter or the full word with {len(guessing_word)} letters!\nTry again:  ")
                    print()

            #and saves already tried letters and words
            guessed_alpabets.append(user_guess)

            if user_guess == guessing_word:
                print("Amazing! You guessed the word!")
                guessed_words += 1
                return 
            elif user_guess in guessing_word:
                #it gaves indexes for guessed letters
                indices = [i for i, char in enumerate(guessing_word) if char == user_guess]

                #changes printing text's guessed letters
                for x in indices:
                    printing[x] = f"{guessing_word[x]} "
                exc_word = "".join(printing)

                #if user guess the word by letters he will win
                if exc_word.replace(" ", "") == guessing_word:
                    print("You guessed the word!")
                    guessed_words += 1
                    return 
                else:
                    print("You guessed the letter, keep continue.")  
            else:
                print(f"There is not \"{user_guess}\" in the word.")
                life -= 1

            if life > 0:
                return guess(life)
            else:
                return print(f"You ran out of lives! The word was {guessing_word}. Game over...\n")

        guess(lifes)

        #after user guess the word or run out of lives, we show the menu and the score
        print(f"====================================\n|| Exit || Continue || Difficulty ||\n------------------------------------")
        print(f"Your score: {guessed_words}\n")

        next = input("Choose next move from the bar!: ")
        while next.lower() not in ("exit", "continue", "difficulty"):
            next = input("Choose next move only from the bar!: ")
        
        if next == "exit":
            print(f"Game over, you have guessed {guessed_words} words. Good luck.")
            return
        elif next == "continue":
            print("\nGuess the new word...")
            return guessing(data, lvl)
        else:
            #if user choose dificulty section we will let him change game's difficulty and then continue it
            print("The difficulty menu:\n==============================\n || Hard || Medium || Easy ||\n------------------------------")
            
            new_lvl = ""
            while new_lvl not in ("hard", "medium", "easy"):
                new_lvl = input("Choose the level from the menu!: ").lower()

            print("Guess the new word...")
            return guessing(data, new_lvl)

    guessing(data, game_lvl)

Hangman()