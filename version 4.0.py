from pygame import *
from random import*
import math #import relavant modules for future use

init() #initialization of the pygame engine
SIZE=SCREENWIDTH,SCREENHEIGHT=(1000,700) #with size var of 1000,700
screen=display.set_mode(SIZE) #def our surface with respective size variable

RED= (255,0,0)
BLACK=(0,0,0)
WHITE= (255,255,255)
GREEN= (0,255,0)
BLUE= (0,0,255)
SKYBLUE=(122,214,245)
BEIGE= (186,111,26)
PINK=(255,0,238)
ORANGE=(255,165,0)
PEACH= (232, 135, 78)
LIGHTGREEN= (177,233,111)
GREY= (52, 54, 58)
BROWN=(86,62,38)  #Color Constants

turretSprite=image.load("turretSprite.png")
HUD=image.load("HUD.png")
turretGround=image.load("turretsquare.png")
enemyGround=image.load("enemyPath.png")
fontSans=font.SysFont("Comic Sans MS", 20)
move_1right=image.load("move_1 right.png")
move_2right=image.load("move_2 right.png")
move_1front=image.load("move_1 front.png")
move_2front=image.load("move_2 front.png")
move_1left=image.load("move_1 left.png")
move_2left=image.load("move_2 left.png")
move_1back=image.load("move_1 back.png")
move_2back=image.load("move_2 back.png")
smoke_1=image.load("smoke_1.png")
smoke_2=image.load("smoke_2.png")
smoke_3=image.load("smoke_3.png")
explosion=image.load("explosion.png")
pew=mixer.Sound("pew.wav")
mainSong=mixer.Sound("music.ogg")
ded=mixer.Sound("ded.wav")
pew.set_volume(0.2) #20% volume for shooting sounds
boom=mixer.Sound("boom.wav")
instruction=image.load("instructions.png")
instruction2=image.load("instruction2.png")
mainmenu=image.load("mainMenu.png")
diary=image.load("diary.png")
intro=mixer.Sound("intro.wav")
difficulty=image.load("difficulty.png")
#compilation of loading of images, music, fontdeclarations


def clearSelections(): #func clear selections clears the HUD and map block active selections
    global selectedHUDAction, selectedBlock #global these variables so can be called on all levels of modular programming
    selectedHUDAction="" #hud button is null weapon
    selectedBlock=() #block selection is null 
    
def counterMarkTrueFalse(millisecondsUntilTrue, lastTimeLocal): #func that uses perfered interval and pygame time to determine a true return
    if time.get_ticks()-lastTimeLocal > millisecondsUntilTrue: #if current time at this line minus sent time is more than specified interval
        lastTimeLocal=time.get_ticks() #update to new sent time as current time (mark) so difference is reset
        hit=True #return a True hit
    else: #if not reached interval
        lastTimeLocal=lastTimeLocal #lastTimeLocal stays the same
        hit=False #return a false hit
    return hit, lastTimeLocal #returns whether counter has been reached, updated lasttime

def createGrid(): #func that creates a 2d array for our map grid
    rectListTopDownLeftRight=[] #empty list to avoid declaration errors
    for x in range (0,10): #for 10 squares across
        for y in range (0,6): #for 6 squares down for each square across
            currentXY=(x*100,y*100, 100, 100) #def our pos Rect for that square
            rectListTopDownLeftRight.append(currentXY) #append to our empty list
    return rectListTopDownLeftRight #return full list

def createPathway():  #func that creates our pathway array and takes away those squares as valid collisions
    collideList=createGrid() #create a new list from scratch to be used a valid collision 
    rectPathway=[] #create a pathway list (empty)
    rectPathwayList=[0,1,2,8,13,14,19,25,26,27,28,34,40,44,45,46,50,56] #all these squares (position relative to master grid list)
    counter=0 #0 to avoid declaration errors
    for x in rectPathwayList: #for all positional pathway integers
        rectPathway.append(collideList[x-counter]) #append the respective rects from master into pathway list
        del collideList[x-counter] #delete that respective rect from valid collision list
        counter+=1 #add one for next operation
    return rectPathway, collideList #return these lists to be used globally

def moveEnemy(enemyQueue, pixelSpeed): #compensating for blit size rn
    for index in range (len(enemyQueue)-1, -1, -1): #for all enemies in enemyQueue
        x=enemyQueue[index][0] #x as x element in 4 element tuple rect
        y=enemyQueue[index][1] #y as y element in 4 element tuple rect
        if x==0 and y <200: #if in first straightaway
            enemyQueue[index][1] += pixelSpeed # move down by pixelspeed
        elif x <= 200 and y >= 200: #if in second straight away
            enemyQueue[index][0]+= pixelSpeed #move right by pixelspeed 
        elif x<=250 and y >= 100: #if in third straightaway
            enemyQueue[index][1]-=pixelSpeed #move up by pixelspeed
        elif y<=100 and x<400: #if in fourth straight away 
            enemyQueue[index][0]+=pixelSpeed #move right by pixelspeed
        elif y < 400 and x<=500: #if in fifth straight away
            enemyQueue[index][1]+=pixelSpeed #move down by pixelspeed 
        elif y < 450 and x < 700: #if in sixth straight away
            enemyQueue[index][0]+=pixelSpeed #move right by pixelspeed
        elif y > 200 and x <800: #if in seventh straight away
            enemyQueue[index][1]-=pixelSpeed #move up by pixelspeed
        elif y <=200 and x < 1000: #if in seventh straight away
            enemyQueue[index][0]+=pixelSpeed #move right by pixelspeed
            
    return enemyQueue #return these values to global state to be reused 

def outsideCheck(enemyList, healthList, stateListLocal): #check if any enemies have finished their journy, save memory and used to diminish hp
    for element in enemyList: #for all enemies in enemylist
        pos=enemyList.index(element) #index as for corrosponding lists
        if element[0] > 999: #if enemy has past the 1000 pixel limit for x of the screen
            del enemyList[pos]
            del healthList[pos]
            del stateListLocal[pos] #delete its corrosponding data from lists
            diminishGlobalHealth() #diminish player health by 10
    return enemyList, healthList, stateListLocal #return these new lists to global to be used in other operations
def drawEnemies(enemyList, stateListLocal): #draws the sprites of enemies 
    for enemy in enemyList: #for all enemies in enemylist
        x=enemy[0] #let x be x enemy pos 
        y=enemy[1] #let y be y enemy pos
        pos=enemyList.index(enemy) #let pos be the index of all corosponding lists
        if x==0 and y <200: #if in straight away 1
            if stateListLocal[pos]==1: #and in animation state 1
                temp=Rect (enemy[0], enemy[1], 50,50) #temp be coordinates of blit for that enemy
                screen.blit(move_1front,temp) #blit the first sprite onto temp
                stateListLocal[pos]=0 #change the list element to animation state 0
            else:  #else in animation state 0
                temp=Rect (enemy[0], enemy[1], 50,50)#temp be coordinates of blit for that enemy
                screen.blit(move_2front,temp)#blit the first sprite onto temp
                stateListLocal[pos]=1#change the list element to animation state 1
        elif x <= 200 and y >= 200: #if in straight away 2
            if stateListLocal[pos]==1:#and in animation state 1
                temp=Rect (enemy[0], enemy[1], 50,50) #temp be coordinates of blit for that enemy
                screen.blit(move_1right,temp)#blit the first sprite onto temp
                stateListLocal[pos]=0#change the list element to animation state 0
            else:#else in animation state 0
                temp=Rect (enemy[0], enemy[1], 50,50) #temp be coordinates of blit for that enemy
                screen.blit(move_2right,temp)#blit the first sprite onto temp
                stateListLocal[pos]=1#change the list element to animation state 0
        elif x<=250 and y >= 100:                                       #repeated for respective directions
            if stateListLocal[pos]==1:
                temp=Rect (enemy[0], enemy[1], 50,50)
                screen.blit(move_1back,temp)
                stateListLocal[pos]=0
            else:
                temp=Rect (enemy[0], enemy[1], 50,50)
                screen.blit(move_2back,temp)
                stateListLocal[pos]=1          
        elif y<=100 and x<400:                                     #repeated for respective directions
            if stateListLocal[pos]==1:
                temp=Rect (enemy[0], enemy[1], 50,50)
                screen.blit(move_1right,temp)
                stateListLocal[pos]=0
            else:
                temp=Rect (enemy[0], enemy[1], 50,50)
                screen.blit(move_2right,temp)
                stateListLocal[pos]=1
        elif y < 400 and x<=500:                               #repeated for respective directions
            if stateListLocal[pos]==1:
                temp=Rect (enemy[0], enemy[1], 50,50)
                screen.blit(move_1front,temp)
                stateListLocal[pos]=0
            else:
                temp=Rect (enemy[0], enemy[1], 50,50)
                screen.blit(move_2front,temp)
                stateListLocal[pos]=1
        elif y < 450 and x < 700:#repeated for respective directions
            if stateListLocal[pos]==1:
                temp=Rect (enemy[0], enemy[1], 50,50)
                screen.blit(move_1right,temp)
                stateListLocal[pos]=0
            else:
                temp=Rect (enemy[0], enemy[1], 50,50)
                screen.blit(move_2right,temp)
                stateListLocal[pos]=1
        elif y > 200 and x <800:#repeated for respective directions
            if stateListLocal[pos]==1:
                temp=Rect (enemy[0], enemy[1], 50,50)
                screen.blit(move_1back,temp)
                stateListLocal[pos]=0
            else:
                temp=Rect (enemy[0], enemy[1], 50,50)
                screen.blit(move_2back,temp)
                stateListLocal[pos]=1
        elif y <=200 and x < 1000:#repeated for respective directions
            if stateListLocal[pos]==1:
                temp=Rect (enemy[0], enemy[1], 50,50)
                screen.blit(move_1right,temp)
                stateListLocal[pos]=0
            else:
                temp=Rect (enemy[0], enemy[1], 50,50)
                screen.blit(move_2right,temp)
                stateListLocal[pos]=1            
            
            
def healthCheck (healthList, enemyQueue, stateListLocal): #func for checking if enemy has died
    for x in range (0, len(healthList)): #for x in range of all enemies
        if x !=0: #preventing index errors, if x is not ==0
            x=x-1 # minus 1 as we start from 0 in lists
        if healthList[x] < 1: #if health is 0 or below
            del healthList[x] 
            del enemyQueue[x]
            del stateListLocal[x] #delete respective enemy data
            ded.play() #play death sound
    return healthList, enemyQueue, stateListLocal #retuen these data as global to be used in other operations

def spawnSniper(x,y,gunPlaceList,gunTypeList, validCollisionList,stateListGunsLocal):  #func adds all neessary starter data for a functioning sniper
    place=(x,y,100,100) #format  rect as using x and y coordinates of selection squares
    gunPlaceList.append(place) #append that to a master weapon list (coor)
    gunTypeList.append("Sniper") #append a coorosponding list for a weapon id "sniper"
    validCollisionList.remove(place) #remove that square from valid collisions list so it may not be used again
    stateListGunsLocal.append(0) #append animation state to 0
    
    return gunPlaceList, gunTypeList, validCollisionList,stateListGunsLocal #return these to global so they may be used in other operations

def mapCollisions(x,y, validCollisionList, mouseEvent, selectedBlockLocal,): #catching collisions for the main map
    mouseHit=Rect(x,y,1,1) #def a rect for our mouse so it may be list checked
    rectRank=mouseHit.collidelist(validCollisionList) #list checkin our mouse with valid collisions on the map
    if button==1 and rectRank != -1: #if left click and a match was found in our list
        temp=validCollisionList[rectRank] 
        selectedBlockLocal=temp #selected block is the coordinate (or list element) mathced
    elif button==3: #if right click
        selectedBlockLocal=() #return selected block to null
    return selectedBlockLocal #return selected blocks vars to be used globally

def hudCollisions(x, y, mouseButton, selectedHUDLocal): #catching collisions for the lowe hud
    hudListRect=[(0,600,100,100),(900,600,100,100),(300,600,100,100)] #respective collide rects
    hudListType=["Sniper","", "Bomb"] #item ids for each of the respective rects
    mouseHit=Rect(x,y,1,1) #def mouse hit as rect to be used for collidelist
    collide=mouseHit.collidelist(hudListRect) #def our returned collidelist with mouse as collide 
    if collide != -1 and mouseButton==1: #if left click and match
        selectedHUDLocal=hudListType[collide] #hud local var is that match
    return selectedHUDLocal #return to global scale

def diminishHealth(weaponListType, weaponListPlace, healthList, enemyList, stateGunLocal): #func to slowly diminish health if in range of a weapon
    for x in range (0,len(weaponListPlace)):     #for all weapons in weaponlistcoordinates
        if weaponListType[x]=="Sniper": #if respective id is sniper
            rangeCapacity=400 #define our range in all directions as 400
            damage=1 #diminish rate per operation
            enemyPlaceX=enemyList[0][0] #
            enemyPlaceY=enemyList[0][1]
            weaponPlaceX=weaponListPlace[x][0]
            weaponPlaceY=weaponListPlace[x][1] #formatting from 4 element tuples into single variables for x and ys of weapon and enemy places 
            rangeActual=(math.sqrt ((enemyPlaceX-weaponPlaceX)**2+(enemyPlaceY-weaponPlaceY)**2)) #distance of two points for weapon and enemy place
            if abs (rangeActual)<rangeCapacity: #if in range
                healthList[0]-=damage #diminish the enemy's health
                pew.play() #play the shoot sound
                if stateGunLocal[x]==0:
                    temp=Rect(weaponPlaceX-25, weaponPlaceY-25, 150,150)
                    screen.blit (smoke_1,temp)
                    stateGunLocal[x]+=1
                elif stateGunLocal[x]==1:
                    temp=Rect(weaponPlaceX-25, weaponPlaceY-25, 150,150)
                    screen.blit (smoke_2,temp)
                    stateGunLocal[x]+=1
                elif stateGunLocal[x]==2: 
                    temp=Rect(weaponPlaceX-25, weaponPlaceY-25, 150,150)    #if a certain animation stage, play that respective sprite animation around the gun
                    screen.blit (smoke_3,temp)
                    stateGunLocal[x]=0
                
    return weaponListType, weaponListPlace, healthList, stateGunLocal #return all manipulated data for use in other operations

def drawSnipers(gunPlaceList, gunTypeList, enemyList): #func to visually rotate and draw all snipers
    if len(enemyList)!=0: #if there are enemies
        for x in range (0,len(gunPlaceList)): #for all guns
            current=turretSprite #current var is now turret sprite surface
            if gunTypeList[x]=="Sniper": #if respective index has an id of sniper
                xLength=(gunPlaceList[x][0]+50)-enemyList[0][0] #difference of x and x
                yLength=(gunPlaceList[x][1]+50)-enemyList[0][1] #difference of y and y 
                if xLength < 0 and yLength <0: #if in top left quad
                    tangentRatio=yLength/xLength #tangent ratio is opposite over adj
                    angle=math.atan(tangentRatio) #angle of that tri is tangent of that ratio
                    angle=math.degrees(angle) #conversion to degrees
                    current=transform.rotate(current, -(angle+90)) #current turret object is rotated by that many degrees+compensation
                elif xLength > 0 and yLength <0: #quad top right
                    tangentRatio=yLength/xLength
                    angle=math.atan(tangentRatio)
                    angle=math.degrees(angle)
                    current=transform.rotate(current, -(angle+270)) #repeated
                elif xLength > 0 and yLength >0: #quad bottom right
                    tangentRatio=yLength/xLength
                    angle=math.atan(tangentRatio)
                    angle=math.degrees(angle)
                    current=transform.rotate(current, -(angle+270)) #repeated
                elif xLength < 0 and yLength >0: #bottom left
                    tangentRatio=yLength/xLength
                    angle=math.atan(tangentRatio)
                    angle=math.degrees(angle)       
                    current=transform.rotate(current, -(angle+90)) #repeated
                elif xLength == 0 and yLength > 0: #if directly above:
                    current=transform.rotate(current, 0) #rotate up (nothing as is default pos)
                elif xLength==0 and yLength <0:#if directly below
                    current=transform.rotate(current, 180) #Point down
                elif xLength < 0 and yLength==0: #if directly right
                    current=transform.rotate(current, 270) #point right
                elif xLength > 0 and yLength==0: #if directly left
                    current=transform.rotate(current,90) #point left
                    
                temp=gunPlaceList[x] #temp is the rect coor for the gun in question
                screen.blit(current, temp) #blit the newly rotated object in that pos.
    else: #otherwise if there are no enemies
        for x in range (0,len(gunPlaceList)):
            current=turretSprite
            temp=gunPlaceList[x]
            screen.blit(current, temp) #reset and draw all snipers to default ready position
            
def drawScene(HUDSelection, plotSelection, playerMoneyLocal, healthList, enemyList, stateListLocal, globalPlayerHealthLocal): #drawscene to order and be called for in main game loop 
    hitList=["Sniper", "Bomb"] #respective ids for hud collisions
    posList=[(0,600,100,100), (300,600,100,100)] #respective coordinates for hud colisons
    for x in allSquares: #for all squares on the map
        screen.blit(turretGround, x)      #blit surface turret ground 
    for x in pathwaySquares: #for all pathway squares
        screen.blit(enemyGround, x) #blut surface enemy ground
    screen.blit(HUD, (0,600)) #blit the hud @ 0,600
    drawSnipers(activeWeaponPlaces, activeWeaponTypes, enemyQueue1) #call our rotate and draw sniper funcs
    drawHealthEnemies(healthList, enemyList)#draw the health of our enemies 
    drawEnemies(enemyQueue1, stateListLocal) #draw our actual enemeis
    if selectedBlock != (): #if there is a selected block
        draw.rect(screen, BLACK, selectedBlock,4) #outline around it in black
    if HUDSelection != "": #if there is a hud selection
        pos=hitList.index(HUDSelection)
        draw.rect(screen, BLACK, posList[pos], 4) #outline that in reference to our hitlist and poslist
    moneyString=fontSans.render("$%s" %playerMoneyLocal, True, (BLACK)) #render a string for our global money count
    screen.blit(moneyString,(760,610,100,100)) #blit that money on the screen 
    drawGlobalPlayerHealth(globalPlayerHealthLocal) #draw our main player health bar
    
        
def randomMoneyGeneration(playerMoneyLocal): #randomly adds a cash amount to our global player cash
    """Much like real life, jobs are unstable and the market is screwed. Therefore, we have unstable incomes!"""
    income=randint(0,200) #income defined as a randint from 0-200
    playerMoneyLocal+=income #variable sent over (orig global) gets added with income
    return playerMoneyLocal #new total is returned 

def deductPlayerMoney(playerMoneyLocal, amount): #func that deducts global player cash by an amount
    playerMoneyLocal=playerMoneyLocal-amount #sent var becomes deducted by amout
    return playerMoneyLocal #that new amount is returned o

def drawHealthEnemies(healthList, enemyList): #func to draw the healthbars of enemies
    for x in range (len(healthList)-1, -1, -1): #for all enemies
        percentage=healthList[x] #their percentage out of 100 is their list element
        blitX=enemyList[x][0]+20  
        blitY=enemyList[x][1]+100    #health bar coordinates are +20x and +100y relative to their enemy list element
        draw.rect(screen, RED, (blitX, blitY, 100,10)) #draw a red max (normal) bar at these locations
        draw.rect (screen, GREEN,(blitX, blitY, percentage, 10)) #draw the same but green relative to the health as its length
        
def spawnEnemy(healthList, enemyList, stateListLocal, health, positionX, positionY): #func to spawn an enemy
    healthList.append(health) #append to health list recieved health value var
    enemyList.append([positionX, positionY]) #append to positional enemy list the x and y vars recieved
    stateListLocal.append(0) #append animation state 0 to animation list
    return healthList, enemyList, stateListLocal #return all these data to be used globally

def diminishGlobalHealth(): #func to diminish global player health
    global globalPlayerHealth #global this var so it may be called on all levels
    globalPlayerHealth=globalPlayerHealth-10 #diminish that value by 10
    
def playerLoseHPCheck(stateLocal, playerHealth): #check if player has died
    if playerHealth <=0: #if yes
        stateLocal="GAMEOVER" #state becomes gameover
    return stateLocal #return state to be used globally

def drawGlobalPlayerHealth(mainPlayerHealth): #func to draw the HUD healthbar
    draw.rect (screen, RED, (750,650,100,30)) #draw a static 100 wide red bar @ rect specified
    draw.rect (screen, GREEN, (750,650,mainPlayerHealth,30)) #do the same but relative to player health
    mainPlayerHealth=str(mainPlayerHealth) #turning into string so it is blittable
    textHealth=fontSans.render(mainPlayerHealth, True, BLACK) #render the main player's health value into var texthealth
    screen.blit (textHealth, (785, 652)) #blit onto coor (785,652)

def AOEBombBackEnd(enemyList, healthList, stateListLocal, bombListLocalX, bombListLocalY): #func to call when a explosion is triggered
    tempRect=Rect(bombListLocalX-25, bombListLocalY-25, 150,150) #coordinate to blit the explosion sprite is top left (25 pixel diff) of x and y sent through fun
    screen.blit(explosion, tempRect) #blit the explosion surface at those coordinates
    display.flip() #flip drawings onto screen
    boom.play() #play the explosion sound
    time.wait(50) #wait 50 milliseconds
    for x in range (len (enemyList)-1,-1,-1): #for all enemies
        
        if abs(math.sqrt(((bombListLocalX-enemyList[x][0])**2)+((bombListLocalY-enemyList[x][1])**2))) <= 200: #if they were within 200 pixels of the blast
            del enemyList[x]
            del healthList[x]
            del stateListLocal[x] #delete data corrosponding to those enemies
            ded.play() #play the death sound
    return enemyList, healthList, stateListLocal #return all data to be used globally
            
def mainMenuCollisions(stateLocal, x, y, mouseButton): #func to change states based on main menu collisions
    mouseHit=Rect(x,y,1,1) #use mouse x and y data to make a rect usable in collisionlist func
    collisionList=[(200,200,600,150),(200,400,600,150)] #make a collision rect list that has valid collisoons
    stateList=["PRE1","INSTRUCTION"] #create respective ids (states) for those 
    collide=mouseHit.collidelist(collisionList) #compare them and use math into var collide
    if collide != -1 and mouseButton==1: #if matched and left click
        stateLocal=stateList[collide] #new statelocal is that match id 
    return stateLocal #return to be used globally

def instructionOneCollisions(stateLocal, x, y, mouseButton): #func to change states based on int 1 collisions
    mouseHit=Rect(x,y,1,1)#use mouse x and y data to make a rect usable in collisionlist func
    collisionList=[(0,610,274,90),(280,610,274,90)]#make a collision rect list that has valid collisoons
    stateList=["MAINMENU","INSTRUCTION2"]#create respective ids (states) for those 
    collide=mouseHit.collidelist(collisionList)#compare them and use math into var collide
    if collide != -1 and mouseButton==1:#if matched and left click
        stateLocal=stateList[collide]#new statelocal is that match id 
    return stateLocal#return to be used globally

def instructionTwoCollisions(stateLocal, x,y, mouseButton): #func to change states based on int2 collisions
    mouseHit=Rect(x,y,1,1)#use mouse x and y data to make a rect usable in collisionlist func
    collisionList=[(600,600,180,100),(800,600,180,100)]#make a collision rect list that has valid collisoons
    stateList=["INSTRUCTION","MAINMENU"]#create respective ids (states) for those 
    collide=mouseHit.collidelist(collisionList)#compare them and use math into var collide
    if collide != -1 and mouseButton==1:#if matched and left click
        stateLocal=stateList[collide]#new statelocal is that match id 
    return stateLocal  #return to be used globally

def difficultyCollisions(stateLocal, x, y, mouseButton): #collisions for difficulty
    moveRate=0 #reference before assignment
    mouseHit=Rect(x,y,1,1) #mouse rect to test collidelist
    collisionList=[(0,0,333,700), (333,0,333,700), (666,0,333,700)] #respective regions to establish difficulty
    speedList=[2,5,10] #speed list to use as pixel movement once returned (respective to collisions)
    collide=mouseHit.collidelist(collisionList)  #collide test with mouse
    if collide != -1 and mouseButton==1: #if collide test matched and mousebutton ==1
        stateLocal="PRE" #change the state to pregane
        moveRate=speedList[collide] #moverate (later used globally as pixelspeed) is respective list to collisions
    return stateLocal, moveRate #return these data to be used globally
    
    
    
        
            
    
    


        
        
        
    
    
        
running=True #for our while loop, to be false upon exit
myClock=time.Clock() #used for our loop frequency per second
state="MAINMENU" #defining our initial state to main menu
speed=30 #speed to be running our program
enemySpeed=0
#GameLoop
while running: #while true
    button=0
    mx=-1
    my=-1 #failsafe button and x and y pos to prevent accidental triggering
    for evnt in event.get(): #for all pygame events
        if evnt.type==QUIT: #if x button is hit
            running=False #True loop becomes false
        if evnt.type==MOUSEBUTTONDOWN: #if event is mousebutton down
            mx,my=evnt.pos #mx and my is the coor of the event
            button=evnt.button #button of the event in var button
            eventCurrent="MOUSEBUTTONDOWN" #current event = "MOUSEBUTTONDOWN"  for additional comparisons outside of evnt loop
        if evnt.type==MOUSEMOTION: #if event is mousemotion
            mx, my=evnt.pos #mx and my is the coor of the event
            eventCurrent="MOUSEMOTION" #current event = "MOUSEMOTION" for additional comparisons outside of evnt loop
            
    if state=="MAINMENU": #if state is mainmenu
        menuRect=Rect(0,0,1000,700) #def rect surface for entire screen
        screen.blit(mainmenu, menuRect) #fill the entire screen with the main menu surface
        state=mainMenuCollisions(state, mx, my, button) #check for main menu collisions, change state depending on return of func
    elif state=="PRE1": #if state is pre1
        mainRect=Rect(0,0,1000,700) #main rect to blit screen 
        screen.blit(difficulty, mainRect) #blit the difficulty screen at mainrect
        state, enemySpeed=difficultyCollisions(state, mx, my, button) #dyanmically update state and enemy speed when a selection is made
        
    elif state=="INSTRUCTION":#if state is instruction
        menuRect=Rect(0,0,1000,700)#def rect surface for entire screen
        screen.blit(instruction,menuRect)#fill the entire screen with the instruction1 surface
        state=instructionOneCollisions(state, mx, my, button)#check for instruction collisions, change state depending on return of func
    elif state=="INSTRUCTION2":#if state is instruction2
        menuRect=Rect(0,0,1000,700)#def rect surface for entire screen
        screen.blit(instruction2, menuRect)#fill the entire screen with the instruction2surface
        state=instructionTwoCollisions(state, mx,my,button)#check for instruction2 collisions, change state depending on return of func
        
        
        
        
    elif state=="PRE": #if state is pre
        screen.blit(diary, (0,0,1000,700)) #blit diary screen
        intro.play() #play story soundtrack
        display.flip() #flip onto screen
        time.wait(37000) #allow 37 seconds for all to finish
        intro.stop() #failsafe stop
        mainSong.play() #start playing main song
        allSquares=createGrid()
        pathwaySquares, validCollisions=createPathway()
        selectedHUDAction=""
        selectedBlock=()
        place=()
        playerMoney=400
        globalPlayerHealth=100
        stateList=[0]
        stateListGuns=[]
        subState="BABY"
        hit1Counter=0
        bombList=[]
        lastTime=time.get_ticks() #0
        lastTime2=time.get_ticks()
        enemyQueue1=[[0,0]]
        HPList=[100]
        activeWeaponPlaces=[]
        activeWeaponTypes=[]         #reset all respective global data for game start, run all necessary funcs for arrays etc.
        state="GAMESTART"
        
    elif state=="GAMESTART": #if state is gamestart
        if subState=="BABY": #substate defining as the current wave structure, there are two. Active and waits. "BABY" is active where enemies are spawned. Waits are redirectors to an active loop after a time period.
            hit1, lastTime2=counterMarkTrueFalse(14000, lastTime2) #every 14 seconds, return a true hit1
            if hit1==True: #if a true hit1
                spawnEnemy(HPList, enemyQueue1, stateList, 100,0,0) #spawn an enemy with 100 hp at 0,0
                hit1Counter+=1 #add one to hitcountermemory
                if hit1Counter>1: #if over 1 occurances
                    subState="WAVE2" #change the substate
                    hit1Counter=0 #reset the counter for the next loop
                    lastTime2=time.get_ticks() # reset the lasttime for the next loop interval
        elif subState=="WAVE2": #active loop @ 14 times, every 500 milliseconds @ 100 hp
            hit1, lastTime2=counterMarkTrueFalse(500,lastTime2)
            if hit1==True:
                spawnEnemy(HPList, enemyQueue1, stateList, 100,0,0)
                hit1Counter+=1
                if hit1Counter > 14:
                    subState="THEYRECOMING"
                    lastTime2=time.get_ticks()
                    hit1Counter=0
                    
        elif subState=="THEYRECOMING": #wait loop
            hit1, lastTime2=counterMarkTrueFalse(10000, lastTime2) #once 10 seconds is achieved, return a true hit
            if hit1==True: #if a true hit is returned
                subState="RAPIDFIRE" #change the substate
                lastTime2=time.get_ticks() #reset time
        elif subState=="RAPIDFIRE": #active loop @ 50 milliseonds 15 times @ 100 hp
            hit1, lastTime2=counterMarkTrueFalse(50,lastTime2)
            if hit1==True:
                spawnEnemy(HPList, enemyQueue1, stateList, 100,0,0)
                hit1Counter+=1
                if hit1Counter > 15:
                    subState="THEYREADAPTING"
                    lastTime2=time.get_ticks()
                    hit1Counter=0 
        elif subState=="THEYREADAPTING": #wait loop for 20 seconds
            hit1, lastTime2=counterMarkTrueFalse(20000, lastTime2)
            if hit1==True:
                subState="ADAPTATIONISAMONGUS"
                lastTime2=time.get_ticks()
                    
        elif subState=="ADAPTATIONISAMONGUS":  #700 milliseoncds each 10 times @ 200 hp
            hit1, lastTime2=counterMarkTrueFalse(700,lastTime2)
            if hit1==True:
                spawnEnemy(HPList, enemyQueue1, stateList, 200,0,0)
                hit1Counter+=1
                if hit1Counter>10:
                    subState="GETREADYBUDDY"
                    lastTime2=time.get_ticks()
                    hit1Counter=0
        elif subState=="GETREADYBUDDY": #wait loop for 10000 milliseoncd
            hit1, lastTime2=counterMarkTrueFalse(10000, lastTime2)
            if hit1==True:
                subState="BOSS1"
                lastTime2=time.get_ticks()
            
        elif subState=="BOSS1": #active loop at 1, no timer, 1400 hp
            spawnEnemy(HPList, enemyQueue1, stateList, 1400,0,0)
            subState="HUGEWAVE"
        elif subState=="HUGEWAVE": #wait loop for 10 sec
            hit1, lastTime2=counterMarkTrueFalse(10000, lastTime2)
            if hit1==True:
                subState="WAVEX"
                lastTime2=time.get_ticks()
                
        elif subState=="WAVEX": #active loop @ 100 milliseonds, 40 times, 150 hp
            hit1, lastTime2=counterMarkTrueFalse(100,lastTime2)
            if hit1==True:
                spawnEnemy(HPList, enemyQueue1, stateList, 150,0,0)
                hit1Counter+=1
                if hit1Counter>40:
                    subState="BRACEYOURSELF"
                    lastTime2=time.get_ticks()
                    hit1Counter=0
        elif subState=="BRACEYOURSELF": #wait loop for 7 seonds
            hit1, lastTime2=counterMarkTrueFalse(7000, lastTime2)
            if hit1==True:
                subState="FINALBOSS10000HP"
                lastTime2=time.get_ticks()            
            
        elif subState=="FINALBOSS10000HP": #active loop of 1, after 7 seconds, 10000hp
            hit1, lastTime2=counterMarkTrueFalse(7000,lastTime2)
            if hit1==True:
                spawnEnemy(HPList, enemyQueue1, stateList,10000,0,0)
                subState="WINCHECK"
                
        elif subState=="WINCHECK": #if substate wincheck
            if globalPlayerHealth > 0 and len (enemyQueue1)==0: #once player has defeated all and survived
                state="PLAYERWIN" #change main state into playerwin
        #stateloop always on
        selectedBlock=mapCollisions(mx,my, validCollisions, eventCurrent, selectedBlock) #check for map collisions, return any into selectedBlock var
        selectedHUDAction=hudCollisions(mx, my, button, selectedHUDAction) #check for hud collisions, return any into selectedhudaction var
        if selectedBlock != (): #if a block is selected
            if selectedHUDAction=="Sniper" and playerMoney >= 400: #if a hud weapon is selected (sniper) and player can afford @ 400 dollars
                activeWeaponPlaces, activeWeaponTypes, validCollisions, stateListGuns=spawnSniper(selectedBlock[0], selectedBlock[1], activeWeaponPlaces,activeWeaponTypes, validCollisions,stateListGuns) #spawn the sniper at selected block
                clearSelections() #clear selections
                playerMoney=deductPlayerMoney(playerMoney, 400) #deduct player money of 400
            elif selectedHUDAction=="Bomb" and playerMoney >800: # if hud weapon is selected (checmical bomb) and player can afford @ 800 dollars
                playerMoney=deductPlayerMoney(playerMoney, 800) #deduct player money of 800
                enemyQueue1, HPList, stateList=AOEBombBackEnd(enemyQueue1, HPList, stateList, selectedBlock[0], selectedBlock[1]) #perform aoe actions
                clearSelections() #clear selections
        drawScene(selectedHUDAction, selectedBlock, playerMoney, HPList, enemyQueue1, stateList, globalPlayerHealth) #drawscene, draw all relevant game objects
        if len (enemyQueue1) != 0: #if enemies exist
            moveEnemy(enemyQueue1,enemySpeed) #move enemies at enemySpeed pixels a second
            HPList,enemyQueue1, stateList=healthCheck(HPList, enemyQueue1, stateList) #check if any are dead and remove any that are
            if len(activeWeaponPlaces) != 0 and len(enemyQueue1) !=0 : #if there are weapons and there are enemies
                activeWeaponTypes, activeWeaponPlaces, HPList,stateListGuns=diminishHealth( activeWeaponTypes, activeWeaponPlaces, HPList, enemyQueue1,stateListGuns) #check for in range and shoot 
        makeMoneyBool, lastTime=counterMarkTrueFalse(2000, lastTime) #generate random income for player every 2 sec (this func just returns a bool, timer)
        if makeMoneyBool==True: #if func returned true bool
            playerMoney=randomMoneyGeneration(playerMoney) #generate random income for player
        enemyQueue1, HPList, stateList=outsideCheck(enemyQueue1, HPList, stateList) #check if any enemies have gotten through, and deduct accordingly
        state=playerLoseHPCheck(state, globalPlayerHealth) #check if player is dead, and dynamically update state if it is
    elif state=="GAMEOVER": #if state is gameover
        draw.rect(screen, WHITE, (100,200,800,400)) #draw rect for blit objects
        textLose=fontSans.render("You lose. Congrats. Computers continue to be destroyed as the world goes to crap.", True, BLACK) #render loser text
        screen.blit(textLose, (100,200,800,400)) #blit at coor 100,200
        display.flip() #flip the drawings onto screen
        time.wait(5000) #wait 5 sec
        mainSong.stop() #stop playing songs
        state="MAINMENU" #return to main menu
    elif state=="PLAYERWIN": #if state is player win
        draw.rect(screen, WHITE, (200,300,500,400))#draw rect for blit objects
        textWin=fontSans.render ("Congratulations! You won and delivered your key!", True, BLACK) #render winner text
        screen.blit(textWin, (200,300,700,400)) #blit at coor 200,300
        display.flip() #flip onto screen
        time.wait(5000) #wait for 5 seco
        mainSong.stop() #stop the sond 
        state="MAINMENU" #return to main menu
    myClock.tick(speed) #run main loop speed times a second where speed is an int
    display.flip() #flip onto memory any drawing operations
    
quit() #quit if loop is exited