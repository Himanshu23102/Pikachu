import random

def buildDeck():
    deck = []
    colours = ["Red","Green","Yellow","Blue"]
    values = [0,1,2,3,4,5,6,7,8,9,"Draw Two", "Skip", "Reverse"]
    wilds = ["Wild","Wild Draw Four"]
    for colour in colours:
        for value in values:
            cardVal = "{} {}".format(colour, value)
            deck.append(cardVal)
            if value != 0:
                deck.append(cardVal)
    for i in range(4):
        deck.append(wilds[0])
        deck.append(wilds[1])
    return deck


def shuffleDeck(deck):
    random.shuffle(deck)
    return deck

def drawCards(numCards):
    cardsDrawn = []
    for x in range(numCards):
        cardsDrawn.append(unoDeck.pop(0))
    return cardsDrawn

def showHand(player, playerHand):
    print("Player {}'s Turn".format(player+1))
    print("Your Hand")
    print("------------------")
    y = 1
    for card in playerHand:
        print("{}) {}".format(y,card))
        y+=1
    print("")


def canPlay(colour, value, playerHand):
    for card in playerHand:
        if "Wild" in card:
            return True
        elif colour in card or value in card:
            return True
    return False

def aiMove(currentColour, cardVal, playerHand):
    valid_moves = []
    for idx, card in enumerate(playerHand):
        if "Wild" in card or currentColour in card or cardVal in card:
            valid_moves.append(idx)
    if valid_moves:
        return random.choice(valid_moves)
    else:
        return -1

unoDeck = buildDeck()
unoDeck = shuffleDeck(unoDeck)
unoDeck = shuffleDeck(unoDeck)
discards = []

players = []
colours = ["Red","Green","Yellow","Blue"]
numPlayers = int(input("How many human players? "))
while numPlayers<1 or numPlayers>3:
    numPlayers = int(input("Invalid. Please enter a number between 1-3. How many human players? "))
for player in range(numPlayers):
    players.append(drawCards(5))

players.append(drawCards(5))

playerTurn = 0
playDirection = 1
playing = True
discards.append(unoDeck.pop(0))
splitCard = discards[0].split(" ", 1)
currentColour = splitCard[0]
if currentColour != "Wild":
    cardVal = splitCard[1]
else:
    cardVal = "Any"

while playing:
    showHand(playerTurn, players[playerTurn])
    print("Card on top: {}".format(discards[-1]))

    if playerTurn < numPlayers:  
        if canPlay(currentColour, cardVal, players[playerTurn]):
            cardChosen = int(input("Which card do you want to play? "))
            while not canPlay(currentColour, cardVal, [players[playerTurn][cardChosen-1]]):
                cardChosen = int(input("Not a valid Choice. Which card do you want to play? "))
            print("You played {}".format(players[playerTurn][cardChosen-1]))
            discards.append(players[playerTurn].pop(cardChosen-1))
            if len(players[playerTurn])==0:
                playing = False
                winner = "Player {}".format(playerTurn+1)
            else:
                splitCard = discards[-1].split(" ", 1)
                currentColour = splitCard[0]
                if len(splitCard) == 1:
                    cardVal = "Any"
                else:
                    cardVal = splitCard[1]
                if currentColour == "Wild":
                    for x in range(len(colours)):
                        print("{}) {}".format(x+1, colours[x]))
                    newColour = int(input("What colour would you like to choose? "))
                    while newColour < 1 or newColour > 4:
                        newColour = int(input("Invalid option. What colour would you like to choose? "))
                    currentColour = colours[newColour-1]
                if cardVal == "Reverse":
                    playDirection = playDirection * -1
                elif cardVal == "Skip":
                    playerTurn += playDirection
                    if playerTurn >= numPlayers:
                        playerTurn = 0
                    elif playerTurn < 0:
                        playerTurn = numPlayers-1
                elif cardVal == "Draw Two":
                    playerDraw = playerTurn+playDirection
                    if playerDraw == numPlayers:
                        playerDraw = 0
                    elif playerDraw < 0:
                        playerDraw = numPlayers-1
                    players[playerDraw].extend(drawCards(2))
                elif cardVal == "Draw Four":
                    playerDraw = playerTurn+playDirection
                    if playerDraw == numPlayers:
                        playerDraw = 0
                    elif playerDraw < 0:
                        playerDraw = numPlayers-1
                    players[playerDraw].extend(drawCards(4))
                print("")
        else:
            print("You can't play. You have to draw a card.")
            players[playerTurn].extend(drawCards(1))
    else:
        print("AI Player's Turn")
        ai_choice = aiMove(currentColour, cardVal, players[playerTurn])
        if ai_choice != -1:
            print("AI played {}".format(players[playerTurn][ai_choice]))
            discards.append(players[playerTurn].pop(ai_choice))
            if len(players[playerTurn]) == 0:
                playing = False
                winner = "AI Player"
            else:
                splitCard = discards[-1].split(" ", 1)
                currentColour = splitCard[0]
                if len(splitCard) == 1:
                    cardVal = "Any"
                else:
                    cardVal = splitCard[1]
                if currentColour == "Wild":
                    currentColour = random.choice(colours)
                if cardVal == "Reverse":
                    playDirection = playDirection * -1
                elif cardVal == "Skip":
                    playerTurn += playDirection
                    if playerTurn >= numPlayers:
                        playerTurn = 0
                    elif playerTurn < 0:
                        playerTurn = numPlayers-1
                elif cardVal == "Draw Two":
                    playerDraw = playerTurn+playDirection
                    if playerDraw == numPlayers:
                        playerDraw = 0
                    elif playerDraw < 0:
                        playerDraw = numPlayers-1
                    players[playerDraw].extend(drawCards(2))
                elif cardVal == "Draw Four":
                    playerDraw = playerTurn+playDirection
                    if playerDraw == numPlayers:
                        playerDraw = 0
                    elif playerDraw < 0:
                        playerDraw = numPlayers-1
                    players[playerDraw].extend(drawCards(4))
            print("")

    playerTurn += playDirection
    if playerTurn >= numPlayers + 1:
        playerTurn = 0
    elif playerTurn < 0:
        playerTurn = numPlayers

print("Game Over")
print("{} is the Winner!".format(winner))