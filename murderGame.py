import pygame
import random
import sys
import time

pygame.init()

character_names = ["Vera","Philip","Dr.Edward","William","Emily","General John"]
characters_left = character_names.copy()
font = pygame.font.Font(None, 32)
current_screen = "starting"
rooms = ["hallway1","mainRoom","hallway2"]
size = width, height = 1000, 1000
bg_Color = 0,0,0
black = 0,0,0
transparent = (0,0,0,0)
darkYellow = 225,173,1
steps = 0
guessTxt = ""
wrongTextStatus = False

enteredLeftRoom = False
enteredRightRoom = False
enteredBottomRoom = False
lastMurderCharacterSolved = True
lastMurderedCharacter = None
character1X,character1Y = 350,300
character2X,character2Y = 700,450
character3X,character3Y = 200,275
character4X,character4Y = 800,275
character5X,character5Y = 200,275
character6X,character6Y = 800,275
character1MurderType = "knife"
character2MurderType = "hanging"
character3MurderType = "poison"
character4MurderType = "knife"
character5MurderType = "poison"
character6MurderType = "knife"

welcome_place = 300, 410
welcome = font.render("This is the gothic murder mystery game", True, "white")
start_place = 400,465
start = font.render("Press here to start",True, "black")
screen = pygame.display.set_mode(size)

mainRoom = pygame.image.load("Mansion_main.png")
hallway1 = pygame.image.load("Hallway_1.png")
hallway2 = pygame.image.load("Hallway_2.png")
under_room = pygame.image.load("under_room.png")
mainRoomSize = (710*1.41,570*1.41)
seperateRoomSize = (742*1.3,392*1.3)
under_roomSize = (115*8,75*8)
mainRoom = pygame.transform.scale(mainRoom,mainRoomSize)
hallway1 = pygame.transform.scale(hallway1,seperateRoomSize)
hallway2 = pygame.transform.scale(hallway2,seperateRoomSize)
under_room = pygame.transform.scale(under_room,mainRoomSize)

main1 = pygame.image.load("main_character1.png")
main2 = pygame.image.load("main_character2.png")
main3 = pygame.image.load("main_character3.png")
characterV = [main1,main2,main3]

character1 = pygame.transform.scale(pygame.image.load("character1.png"),(89/2,198/2))
character2 = pygame.transform.scale(pygame.image.load("character2.png"),(89/2,198/2))
character3 = pygame.transform.scale(pygame.image.load("character3.png"),(89/2,198/2))
character4 = pygame.transform.scale(pygame.image.load("character4.png"),(89/2,198/2))
character5 = pygame.transform.scale(pygame.image.load("character5.png"),(89/2,198/2))
character6 = pygame.transform.scale(pygame.image.load("character6.png"),(89/2,198/2))

speechBubble = pygame.transform.scale(pygame.image.load("speech_bubble.png"),(89,89))

character1Status = True
character2Status = True
character3Status = True
character4Status = True
character5Status = True
character6Status = True
yesButtonStatus = False
noButtonStatus = False
murdererChosen = random.choice(character_names)
print(murdererChosen)

def getCharacterV():
    if steps %3 == 0:
        return main1
    elif steps %3 == 1:
        return main2
    elif steps %3 == 2:
        return main3

mainCharacter = getCharacterV()
mainCharacter = pygame.transform.scale(mainCharacter,(89/2,198/2))
mainCharacterX = 500
mainCharacterY = 400
murderer = random.choice(character_names)

eventList = [pygame.K_a,pygame.K_b,pygame.K_c,pygame.K_d,pygame.K_e,pygame.K_f,pygame.K_g,pygame.K_h,pygame.K_i,pygame.K_j,pygame.K_k,pygame.K_l,pygame.K_m,pygame.K_n,pygame.K_o,pygame.K_p,pygame.K_q,pygame.K_r,pygame.K_s,pygame.K_t,pygame.K_u,pygame.K_v,pygame.K_w,pygame.K_x,pygame.K_y,pygame.K_z,pygame.K_PERIOD]

veraHints = ["Key Fob","oil residue","socket wrench","nail","Hammer"]
philipHints = ["Blueprints","USB drive","Ruler","nail","Hammer"]
dredwardHints = ["Stethoscope","Needle","Pills","Sedatives","Gloves"]
williamHints = ["Globe","Gps","Pen","Compass","Map"]
emilyHints = ["Dog Hair","Needle","Pills","Sedatives","Gloves"]
generaljohnHints = ["Military Hat","Purple Heart","Binoculars","Dog tags","Map"]

def listPlayersLeft():
    pygame.draw.rect(screen, darkYellow, (850, 0, 150, 190))
    font3 = pygame.font.Font(None, 20)
    titleText = font3.render('Players Left:', True, "white")
    titleText_place = 860,10
    screen.blit(titleText,titleText_place)
    placeX = 860
    placeY = 35
    for x in characters_left:
        if x == "Vera":
            x = x + "(Mechanic)"
        elif x == "Philip":
            x = x + "(Engineer)"
        elif x == "Dr.Edward":
            x = x + "(Doctor)"
        elif x == "William":
            x = x + "(Cartographer)"
        elif x == "Emily":
            x = x + "(Veterinarian)"
        elif x == "General John":
            x = x + "(General)"
        screen.blit(font3.render(x,True,"white"),(placeX,placeY))
        placeY += 25

def nextRoom(status):
    current = rooms.index(current_screen)
    if status == "foward":
        current += 1
        return rooms[current]
    if status == "backward":
        current -= 1
        return rooms[current]

def solveMurder():
    global lastMurderCharacterSolved
    characterScreen = None

    if lastMurderedCharacter == "character1" or lastMurderedCharacter == "character2":
        characterScreen = "under_room"
    elif lastMurderedCharacter == "character3" or lastMurderedCharacter == "character4":
        characterScreen = "hallway1"
    elif lastMurderedCharacter == "character5" or lastMurderedCharacter == "character6":
        characterScreen = "hallway2"
    
    if current_screen == characterScreen:
        characterX = eval(lastMurderedCharacter + "X")
        characterY = eval(lastMurderedCharacter + "Y")
        
        if (abs(mainCharacterX - characterX)) < 50 and (abs(mainCharacterY - characterY)) < 50:
            lastMurderCharacterSolved = True
            return True
    else:
        return False

def getRandomCharacterNotInRoom(room):
    character = random.choice(characters_left)
    while character == murdererChosen:
        character = random.choice(characters_left)
    return character

def murderCharacter(room): 
    global character1, character2, character3,character4,character5,character6
    global character1Status, character2Status, character3Status, character4Status,character5Status, character6Status
    global lastMurderedCharacter, lastMurderCharacterSolved
    global character3Y,character4Y,character5Y,character6Y
    global yesButtonStatus, noButtonStatus, wrongTextStatus

    currentRoom = room
    deadMan = getRandomCharacterNotInRoom(currentRoom)
    characters_left.remove(deadMan)
    index = character_names.index(deadMan) +1
    deadMan = "character" + str(index)
    deadManSkin = pygame.transform.scale(pygame.image.load(deadMan + "dead.png"),(89/2,198/2))
    
    if deadMan == "character1":
        character1 = deadManSkin
        character1Status = False
    elif deadMan == "character2":
        character2 = deadManSkin
        character2Status = False
    elif deadMan == "character3":
        character3 = deadManSkin
        character3Status = False
        character3Y += 50
    elif deadMan == "character4":
        character4 = deadManSkin
        character4Status = False
        character4Y += 50
    elif deadMan == "character5":
        character5 = deadManSkin
        character5Status = False
        character5Y += 50
    elif deadMan == "character6":
        character6 = deadManSkin
        character6Status = False
        character6Y += 50
    
    lastMurderedCharacter = deadMan
    lastMurderCharacterSolved = False
    yesButtonStatus = False
    noButtonStatus = False


def getHint(murderer):

    if murderer == "Vera":
        index = len(characters_left) -2
        hint = veraHints[index]
        return hint
    elif murderer == "Philip":
        index = len(characters_left) -2
        hint = philipHints[index]
        return hint
    elif murderer == "Dr.Edward":
        index = len(characters_left) -2
        hint = dredwardHints[index]
        return hint
    elif murderer == "William":
        index = len(characters_left) -2
        hint = williamHints[index]
        return hint
    elif murderer == "Emily":
        index = len(characters_left) -2
        hint = emilyHints[index]
        return hint
    elif murderer == "General John":
        index = len(characters_left) -2
        hint = generaljohnHints[index]
        return hint
while 1:
    screen.fill(bg_Color)
    if current_screen == "starting":
        screen.blit(welcome, welcome_place)
        playButton = pygame.draw.rect(screen, "white", pygame.Rect(350, 450, 300, 50))
        screen.blit(start,start_place)
        directionText0 = "Directions: The main goal of the game is to guess the murderer."
        directionText1 = "-When you first enter the game you have to explore every room first before the murdering" 
        directionText2 = "starts happening so you know what the characters look like.(USE ARROW KEYS TO MOVE)"
        directionText3 = "-You will know someone is murdered when someone gets knocked off the players left list"
        directionText4 = "-Then you will have to explore the map to find who got murdered."
        directionText5 = "-Once when you find them you have to go up them and it will show you what was left at the"
        directionText6 = "scene of the crime and use that hint to determine if you want to guess who murdered them"
        directionText7 = "To guess, click yes then type the name of the person you think is the murderer and hit enter"
        directionText8 = "-If you guess wrong then someone gets murdered instantly so choose when to guess carefully!"
        directionText9 = "-You get 10 points for evey person left when you guess correctly"

        for x in range(8):
            directionTextRender = font.render(eval("directionText"+ str(x)),True, "white")
            screen.blit(directionTextRender, (5,(x*25)))
    elif current_screen == "mainRoom":
        roomPlace = 0,0#1000-(eval(current_screen).get_height())
        screen.blit(mainRoom,roomPlace)
        screen.blit(mainCharacter, (mainCharacterX,mainCharacterY))
        listPlayersLeft()
    elif current_screen == "hallway1":
        roomPlace = 0+(1000-(eval(current_screen).get_width())),0#1000-(eval(current_screen).get_height())
        screen.blit(hallway1,roomPlace)
        screen.blit(character3, (character3X,character3Y))
        screen.blit(character4, (character4X,character4Y))
        screen.blit(mainCharacter, (mainCharacterX,mainCharacterY))
        listPlayersLeft()
    elif current_screen == "hallway2":
        roomPlace = 0,0#1000-(eval(current_screen).get_height())
        screen.blit(hallway2,roomPlace)
        screen.blit(character5, (character5X,character5Y))
        screen.blit(character6, (character6X,character6Y))
        screen.blit(mainCharacter, (mainCharacterX,mainCharacterY))
        listPlayersLeft()
    elif current_screen == "under_room":
        roomPlace = -100,0
        screen.blit(under_room,roomPlace)
        screen.blit(character1, (character1X,character1Y))
        screen.blit(character2, (character2X,character2Y))
        screen.blit(mainCharacter, (mainCharacterX,mainCharacterY))
        listPlayersLeft()
    elif current_screen == "win_screen":
        screen.fill(bg_Color)
        font5 = pygame.font.Font(None, 60)
        winText = font5.render("YOU WIN!",True, "white")
        screen.blit(winText, (200,200))
        pointText = font.render("Points: " + str(len(characters_left)*10),True,"white")
        screen.blit(pointText,(200,240))
    elif current_screen == "wrong_screen":
        screen.fill(bg_Color)
        font5 = pygame.font.Font(None, 60)
        wrongText = font5.render("Wrong",True, "white")
        screen.blit(wrongText, (200,200))

    if solveMurder() == True:
        characterX = eval(lastMurderedCharacter + "X")
        characterY = eval(lastMurderedCharacter + "Y")
        screen.blit(speechBubble, (characterX + (eval(lastMurderedCharacter).get_width()), characterY - 60))
        font4 = pygame.font.Font(None, 20)
        txt1 = font4.render('Murdered By:', True, "black")
        txt2 = font4.render((eval(lastMurderedCharacter+ "MurderType")),True,"black")
        txt3 = font4.render('Left at Crime: ', True, "black")
        txt4 = font4.render(getHint(murdererChosen), True, "black")
        interChangeText = "Would you like to guess?"
        txt5 = font4.render(interChangeText, True, "white")
        yestxt = font4.render('YES', True, "black")
        notxt = font4.render('NO', True, "black")
        inputtxt = font4.render("Type Answer(Hit Enter When Done):", True,"white")
        screen.blit(txt1,(characterX + (eval(lastMurderedCharacter).get_width())+5, characterY - 49))
        screen.blit(txt2,(characterX + (eval(lastMurderedCharacter).get_width())+5, characterY - 36))
        screen.blit(txt3,(characterX + (eval(lastMurderedCharacter).get_width())+5, characterY - 23))
        screen.blit(txt4,(characterX + (eval(lastMurderedCharacter).get_width())+5, characterY - 10))
        yesButton = pygame.Rect(characterX + (eval(lastMurderedCharacter).get_width())+25 ,characterY +55, 30,20)
        noButton = pygame.Rect(characterX + (eval(lastMurderedCharacter).get_width())+75 ,characterY +55, 30,20)
        inputSpace = pygame.Rect(characterX + (eval(lastMurderedCharacter).get_width())+25 ,characterY +40, 80,40)
        if yesButtonStatus == False and noButtonStatus == False:
            screen.blit(txt5,(characterX + (eval(lastMurderedCharacter).get_width())+5, characterY +40))
            pygame.draw.rect(screen,"green",yesButton)
            pygame.draw.rect(screen,"red",noButton)
            screen.blit(yestxt,(characterX + (eval(lastMurderedCharacter).get_width())+25, characterY +55))
            screen.blit(notxt,(characterX + (eval(lastMurderedCharacter).get_width())+75, characterY +55))
        elif yesButtonStatus == True:
            screen.blit(inputtxt,(characterX + (eval(lastMurderedCharacter).get_width())+5, characterY +25))
            pygame.draw.rect(screen,"white",inputSpace)
            guessTxtType = font4.render(guessTxt, True, "black")
            screen.blit(guessTxtType,((eval(lastMurderedCharacter + "X")) + (eval(lastMurderedCharacter).get_width())+25,characterY +40))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONUP:
            mouse_pos = pygame.mouse.get_pos()
            if playButton.collidepoint(mouse_pos):
                current_screen = "mainRoom"
            if solveMurder() == True:
                if yesButton.collidepoint(mouse_pos):
                    yesButtonStatus = True
                elif noButton.collidepoint(mouse_pos):
                    noButtonStatus = True
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                solveMurder()
                wrongTextStatus = False
                mainCharacterY -= 20
                steps +=1
                mainCharacter = getCharacterV()
                mainCharacter = pygame.transform.scale(mainCharacter,(89/2,198/2))
                if mainCharacterY < 0:
                    current_screen = "mainRoom"
                    mainCharacterY = (eval(current_screen)).get_height() - mainCharacter.get_height()
            elif event.key == pygame.K_DOWN:
                solveMurder()
                wrongTextStatus = False
                mainCharacterY += 20
                steps +=1
                mainCharacter = getCharacterV()
                mainCharacter = pygame.transform.scale(mainCharacter,(89/2,198/2))
                if mainCharacterY > (eval(current_screen)).get_height() - mainCharacter.get_height() and (current_screen == "under_room" or current_screen == "hallway1" or current_screen == "hallway2"):
                    mainCharacterY -= 20
                elif mainCharacterY > (eval(current_screen)).get_height() - mainCharacter.get_height():
                    current_screen = "under_room"
                    mainCharacterY = mainCharacter.get_height()
                    enteredBottomRoom = True
                    if lastMurderCharacterSolved == True and (enteredLeftRoom == True and enteredRightRoom == True and enteredBottomRoom == True):
                        murderCharacter(current_screen)
                

            elif event.key == pygame.K_LEFT:
                solveMurder()
                wrongTextStatus = False
                mainCharacterX -= 20
                steps +=1
                mainCharacter = getCharacterV()
                mainCharacter = pygame.transform.scale(mainCharacter,(89/2,198/2))
                if mainCharacterX < 0:
                    current_screen = nextRoom("backward")
                    mainCharacterX = eval(current_screen).get_width() - mainCharacter.get_width()
                    if current_screen == "hallway1":
                        enteredLeftRoom = True
                    elif current_screen == "hallway2":
                        enteredRightRoom = True
                    if lastMurderCharacterSolved == True and (enteredLeftRoom == True and enteredRightRoom == True and enteredBottomRoom == True):
                        murderCharacter(current_screen)
                if mainCharacterX < 460 and (mainCharacterY + mainCharacter.get_height()) > 679 and (current_screen == "under_room"):
                    mainCharacterX +=20
                elif ((1000- eval(current_screen).get_width() > mainCharacterX)) and (current_screen == "under_room" or current_screen == "hallway1"):
                    mainCharacterX +=20
                
                    
            elif event.key == pygame.K_RIGHT:
                solveMurder()
                wrongTextStatus = False
                if mainCharacterX > (eval(current_screen).get_width() - mainCharacter.get_width() ):
                    if current_screen != "hallway2":
                        current_screen = nextRoom("foward")
                        mainCharacterX = 5
                    else:
                        mainCharacterX -=20
                    if current_screen == "hallway1":
                        enteredLeftRoom = True
                    elif current_screen == "hallway2":
                        enteredRightRoom = True
                    if lastMurderCharacterSolved == True and (enteredLeftRoom == True and enteredRightRoom == True and enteredBottomRoom == True):
                        murderCharacter(current_screen)
                if  (mainCharacterX > (eval(current_screen).get_width() - mainCharacter.get_width())) and (current_screen == "under_room" or current_screen == "hallway2"):
                    mainCharacterX -=20
                else:
                    mainCharacterX +=20
                    steps +=1
                    mainCharacter = getCharacterV()
                    mainCharacter = pygame.transform.scale(mainCharacter,(89/2,198/2))
                    if mainCharacterX > 560 and (mainCharacterY + mainCharacter.get_height()) > 559 and current_screen == "under_room":
                        mainCharacterX -=20
                    if mainCharacterX > 850 and current_screen == "under_room":
                        mainCharacterX -= 20
            else:
                
                if event.key == pygame.K_a:
                    guessTxt += "a"
                elif event.key == pygame.K_b:
                    guessTxt += "b"
                elif event.key == pygame.K_c:
                    guessTxt += "c"
                elif event.key == pygame.K_d:
                    guessTxt += "d"
                elif event.key == pygame.K_e:
                    guessTxt += "e"
                elif event.key == pygame.K_f:
                    guessTxt += "f"
                elif event.key == pygame.K_g:
                    guessTxt += "g"
                elif event.key == pygame.K_h:
                    guessTxt += "h"
                elif event.key == pygame.K_i:
                    guessTxt += "i"
                elif event.key == pygame.K_j:
                    guessTxt += "j"
                elif event.key == pygame.K_k:
                    guessTxt += "k"
                elif event.key == pygame.K_l:
                    guessTxt += "l"
                elif event.key == pygame.K_m:
                    guessTxt += "m"
                elif event.key == pygame.K_n:
                    guessTxt += "n"
                elif event.key == pygame.K_o:
                    guessTxt += "o"
                elif event.key == pygame.K_p:
                    guessTxt += "p"
                elif event.key == pygame.K_q:
                    guessTxt += "q"
                elif event.key == pygame.K_r:
                    guessTxt += "r"
                elif event.key == pygame.K_s:
                    guessTxt += "s"
                elif event.key == pygame.K_t:
                    guessTxt += "t"
                elif event.key == pygame.K_u:
                    guessTxt += "u"
                elif event.key == pygame.K_v:
                    guessTxt += "v"
                elif event.key == pygame.K_w:
                    guessTxt += "w"
                elif event.key == pygame.K_x:
                    guessTxt += "x"
                elif event.key == pygame.K_y:
                    guessTxt += "y"
                elif event.key == pygame.K_z:
                    guessTxt += "z"
                elif event.key == pygame.K_PERIOD:
                    guessTxt += "."
                elif event.key == pygame.K_SPACE:
                    guessTxt += " "
                elif event.key == pygame.K_BACKSPACE:
                    guessTxt = guessTxt[:-1]
                guessTxtType = font4.render(guessTxt, True, "black")
                screen.blit(guessTxtType,((eval(lastMurderedCharacter + "X")) + (eval(lastMurderedCharacter).get_width())+25,characterY +40))
                
                if event.key == pygame.K_RETURN:
                    if murdererChosen.lower() == guessTxt:
                        current_screen = "win_screen"
                    else:
                        guessTxt = ""
                        murderCharacter(current_screen)
                        


    pygame.display.flip()