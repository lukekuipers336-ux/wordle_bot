word_list = {"a":0, "b":0, "c":0, "d":0, "e":0, "f":0, "g":0, "h":0, 
            "i":0, "j":0, "k":0, "l":0, "m":0, "n":0, "o":0, "p":0, "q":0, 
            "r":0, "s":0, "t":0, "u":0, "v":0, "w":0, "x":0, "y":0, "z":0}
with open("words.txt", "r") as f:
    words = f.readlines()
wordss = []
for word in words:
    wordss.append(word.strip())
words = wordss

for word in words:
    for letter in word:
        word_list[letter] += 1
        
letters_used = []
words_used = []
green_letters = ["_", "_", "_", "_", "_"]
yellow_letters = [[], [], [], [], []]
gray_letters = []
turn = 0

def get_yellow_letters():
    letters = []
    for box in yellow_letters:
        for letter in box:
            if letter not in letters:
                letters.append(letter)
    return letters

def get_letter_pos(letter, pos):
    score = 0
    for word in words:
        if word[pos] == letter:
            score += 1
    return score

def clear_yellow(letter=None):
    global yellow_letters
    if letter == None:
        yellow_letters = [[], [], [], [], []]
    for group in yellow_letters:
        try:
            group.remove(letter)
        except:
            pass
        
def clear():
    global green_letters, yellow_letters, gray_letters, letters_used, words_used, turn
    letters_used = []
    words_used = []
    green_letters = ["_", "_", "_", "_", "_"]
    yellow_letters = [[], [], [], [], []]
    gray_letters = []
    turn = 0
    
def get_first_move(quickShot=False):
  global letters_used, words_used
  if quickShot:
      return ['stare', 'login', 'duchy', 'swamp', 'brake', 'froze'][len(words_used)], None
  best_score = -999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999
  best_guess = None
  for word in words:
    if word in words_used:
      continue
    score = 0
    repeated = []
    for i in range(len(word)):
      letter = word[i]
      if letter in letters_used:
        score -= 999999999999999999999999999999999999999999999999999
      if letter in repeated:
        score -= 999999999999999999999999999999999999999999999999999
      score += word_list[letter]
      score += get_letter_pos(letter, i)
      repeated.append(letter)
    if score >= best_score:
      best_score = score
      best_guess = word
  return best_guess, best_score
  
  
def words_available():
    valid_words = []
    yellow = get_yellow_letters()
    for word in words:
        if word in words_used:
            continue
        valid = True
        for i in range(len(word)):
            letter = word[i]
            if letter in gray_letters and letter not in green_letters and letter not in get_yellow_letters():
                valid = False
                break
            elif green_letters[i] != "_":
                if green_letters[i] != letter:
                    valid = False
                    break
            elif letter in yellow_letters[i]:
                valid = False
                break
        for letter in yellow:
            if letter not in word:
                valid = False
        if valid == True:
            valid_words.append(word)
        continue
    return valid_words
    
def get_all_found_letters():
    letters_found = []
    for i in range(len(green_letters)):
        if green_letters[i] != "_":
            letters_found.append(green_letters[i])
    for box in yellow_letters:
        for letter in box:
            if letter not in letters_found:
                letters_found.append(letter)
    return letters_found

def get_best_eliminate(letters):
    best_word = None
    best_score = float('-inf')
    for word in words:
        score = 0
        already_used = []
        for letter in word:
            if letter in letters and letter not in already_used:
                already_used.append(letter)
                if letter in letters_used:
                    continue
                else:
                    score += word_list[letter]
        if score >= best_score:
            best_score = score
            best_word = word
    return best_word
    
def get_best_move():
    possible = words_available()
    best_word = None
    best_score = float('-inf')
    if green_letters.count("_") == 1 and len(words_used) <= 4 and len(possible) > 2:
        letters = []
        location = green_letters.index("_")
        for word in possible:
            letters.append(word[location])
        best_eliminate = get_best_eliminate(letters)
        return best_eliminate, None
    
    elif green_letters.count("_") == 2 and yellow_letters == [[], [], [], [], []] and len(words_used) <=4 and len(possible) > 2:
        letters = []
        locations = []
        for x in range(5):
            if green_letters[x] == "_":
                locations.append(x)
        for word in possible:
            for loc in locations:
                if word[loc] not in letters:
                    letters.append(word[loc])
        best_eliminate = get_best_eliminate(letters)
        return best_eliminate, None
        
    for word in possible:
        score = 0
        letters_used = []
        for i in range(len(word)):
            letter = word[i]
            if letter not in letters_used:
                score += get_letter_pos(letter, i)
            else:
                score += 1
            letters_used.append(letter)
        if score >= best_score:
            best_score = score
            best_word = word
    return best_word, best_score

def evaluate_word(word, code):
    global words_used, green_letters, yellow_letters, gray_letters, letters_used
    code = code.lower()
    for i in range(len(code)):
        letter = code[i]
        if letter == 'l':
            clear_yellow(letter=word[i])
            green_letters[i] = word[i]
        elif letter == 'y':
            yellow_letters[i].append(word[i])
        elif letter == 'g':
            gray_letters.append(word[i])
    words_used.append(word)
    for letter in word:
        if letter not in letters_used:
            letters_used.append(letter)
            
            
def original():
    print("Welcome to the original! You know the deal...\n")
    won = False
    for turns in range(6):
        if len(get_all_found_letters()) <= 2 and turns < 3:
            word = get_first_move(quickShot=True)
            print(word)
        else:
            word = get_best_move()
            print(get_best_move())
        code = input(f"Code for the word '{word[0]}':\n")
        if code == "lllll":
            won = True
            break
        evaluate_word(word[0], code)
        turn = turns
    if won:
        print("Congrats! You won!")
    else:
        print("Aww, better luck next time!")

def eliminate_major():
    print("Welcome! This mode is very similar to the original except for the fact that every move is trying to eliminate words.\nThis is best used in situations where you just want to get the answer right even if it takes many attempts.\n")
    won = False
    for turns in range(6):
        possible = words_available()
        if len(possible) == 1:
            best_eliminate = possible[0]
            print(possible[0])
        elif turns == 4:
            best_eliminate = get_best_move()
            print(word)
        else:
            letters = []
            locations = []
            for x in range(5):
                if green_letters[x] == "_":
                    locations.append(x)
            for word in possible:
                for loc in locations:
                    if word[loc] not in letters:
                        letters.append(word[loc])
            best_eliminate = get_best_eliminate(letters)
            print(best_eliminate)
        code = input(f"Code for the word '{best_eliminate}':\n")
        if code == "lllll":
            won = True
            break
        evaluate_word(best_eliminate, code)
        turn = turns
    if won:
        print("Congrats! You won!")
    else:
        print("Aww, better luck next time!")

def off_current_board():
    print("Welcome! This mode makes it easy to get the best wordle guess based off your current board.\nJust enter your words and codes and I will generate a word for you!\n")
    words = []
    while True:
        word = input("Current word(write 'done' to move on): ")
        if word.lower() == 'done':
            break
        words.append(word)
        code = input(f"Code for the word '{word}': ")
        evaluate_word(word, code)
    if len(get_all_found_letters()) <= 2 and len(words) < 4:
            word = get_first_move(quickShot=False)
            print(word)
    else:
        word = get_best_move()
        print(get_best_move())
         
if __name__ == "__main__":
    print("Welcome to Lukes Wordle bot!\nHeres how it works:\n  First: Open the wordle website\n    Second: I will provide you with a word for you to put in the wordle website as a guess.\n   Third: You will come back and give me the code of the wordle via prompt.\n\nHow To Use Wordle Code:\n   Once wordle gives you the colors for the guessed word you will decode it like this:\n   Green Box = 'l'\n   Yellow Box = 'y'\n  Gray Box = 'g'\n\nMake sure to use all lower case and only the code in the prompt anything else will return an error.\n\nExample of the code: 🟩  🟩  ⬛  🟨  🟨  = llgyy")
    print("-------------------------------------------------------------------------------")
    while True:
        mode = input("Please enter the name of the wordle mode you would like to try(Current, Original, Eliminate):\n")
        mode = mode.strip().lower()
        if mode == 'original':
            original()
        elif mode == 'eliminate':
            eliminate_major()
        else:
            off_current_board()
        again = input('\n\nPlay again?("yes" to play again, "no" to quit)\n')
        if again.strip().lower() == 'yes':
            clear()
            continue
        else:
            print("Okay! Until we meet again!")
            break
