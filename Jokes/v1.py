import random
import time

jokes = ["What does Arnold Schwarzenegger say at the beginning of a game of chess?... I'll be black!",
         "Why are americans bad at chess?... Because they already lost 2 towers!", 
         "I like rooks. They're straightforward.",
         "Do you mind if I make a move on you? <3",
         "Why wouldn't the chess player eat the bread?... It was stale, mate."]

insults = ["A Random generator would be harder to beat!", 
           "I'm going to alpha prune the s*** out of you!", 
           "You just made me realize what the opposite of Artificial Intelligence is... Real Stupid!",
           "I'll win in less then 4 moves!"]

excuses = ["I play worse against lower-rated AI's",
           "I play better as your color",
           "I couldn't remember...was I playing black or white?"]

Anouncement = "Shallow Blue: "

probability = 0.5


def tellJoke():
    if random.random() < probability:
        print("info string " + Anouncement + random.choice(jokes));
        return True
    else:
        return False

def insult():
    if random.random() < 0.5:
        print("info string " + Anouncement + random.choice(insults));
        return True
    return False

def badExcuse():
    if random.random() < 0.5:
        print("info string " + Anouncement + random.choice(excuses));
        return True
    return False

def connectToAmazonWebServices():
    if random.random() < probability:
        print("info string " + Anouncement + "Connecting to Amazon Web Services for additional processing power ...");
        print("info string " + Anouncement + "Connection successful!");
        time.sleep(5)
        
