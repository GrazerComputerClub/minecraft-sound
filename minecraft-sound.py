#www.stuffaboutcode.com & GC2.at
#Raspberry Pi, Minecraft Sound - Add some sound effects to minecraft
# unchanged music by http://www.nosoapradio.us/, see LICENCE https://gamesounds.xyz/No%20soap%20radio/LICENSE

from mcpi import minecraft
from mcpi import block
import time
#import pygame to use the mixer to play wav file
import pygame

# constants
STOPPED = 1
WALKING = 2
FALLING = 3
FLYING  = 4
SWIMING = 5

if __name__ == "__main__":



    #Connect to minecraft by creating the minecraft object
    # - minecraft needs to be running and in a game
    mc = minecraft.Minecraft.create()
    mc.postToChat("Minecraft Sound Effects ")
    mc.postToChat(" by www.stuffaboutcode.com and gc2.at")

    #Initialise pygame and the mixer
    pygame.init()
    pygame.mixer.init()
    
    #MP3 background music from  http://www.nosoapradio.us/
    pygame.mixer.music.load("music/DST-BattleLands.mp3")
    pygame.mixer.music.play(-1)
    
    mc.postToChat("music by http://www.nosoapradio.us/")

    #load WAVS files
    soundWalking = pygame.mixer.Sound("sounds/walking.wav") #http://soundbible.com/2057-Footsteps-On-Cement.html
    soundJump = pygame.mixer.Sound("sounds/jump.wav") #http://soundbible.com/1953-Neck-Snap.html
    soundFalling = pygame.mixer.Sound("sounds/falling.wav") #http://soundbible.com/1247-Wind.html
    soundLanding = pygame.mixer.Sound("sounds/landing.wav") #http://soundbible.com/1952-Punch-Or-Whack.html
    soundSword = pygame.mixer.Sound("sounds/sword.wav") #http://soundbible.com/1898-Spin-Jump.html - public domain 
    soundFlying = pygame.mixer.Sound("sounds/flying.wav") #http://soundbible.com/1036-Propeller.html - public domain 
    soundSwiming = pygame.mixer.Sound("sounds/swiming.wav") #http://soundbible.com/2032-Water.html - public domai
    soundSplash = pygame.mixer.Sound("sounds/splash.wav")   #http://soundbible.com/2100-Splash-Rock-In-Lake.html

    
    mc.postToChat("sound sfx by http://soundbible.com/ (public domain)")

    # setup variables
    lastPlayersState = STOPPED
    playersState = STOPPED
    playerJumped = False
    playerFalling = False
    playerFallDistance = 0

    #get players position
    lastPlayerPos = mc.player.getPos()
    
    
    # loop until CTRL+C
    try:
        while(True):
            
            # get players position
            currentPlayerPos = mc.player.getPos()
            block_beneath = mc.getBlock(lastPlayerPos.x, lastPlayerPos.y-1, lastPlayerPos.z)  # block ID

            # has the player moved in either X or Z (are they WALKING?)
            if lastPlayerPos.x != currentPlayerPos.x or lastPlayerPos.z != currentPlayerPos.z:
                # if player is FALLING they cant be WALKING
                
                if playersState != FALLING:
                    if block_beneath == block.AIR:
                      playersState = FLYING
                    elif block_beneath == block.WATER_FLOWING or block_beneath == block.WATER_STATIONARY:                      
                      playersState = SWIMING
                    else:
                      playersState = WALKING

            # has the player moved in positive Y (have they jumped?)
            if int(lastPlayerPos.y) < int(currentPlayerPos.y):
                playerJumped = True

            # has the player moved in negative Y (are they FALLING?)
            if int(lastPlayerPos.y) > int(currentPlayerPos.y):
                playersState = FALLING

            # is the player still falling?
            if playersState == FALLING and lastPlayersState == FALLING:
                # increase the distance they have fallen
                playerFallDistance = playerFallDistance + (lastPlayerPos.y - currentPlayerPos.y)

            # if the player is FALLING but has stopped moving down
            # (have they STOPPED FALLING?)
            if playersState == FALLING and int(lastPlayerPos.y) == int(currentPlayerPos.y):
                playersState = STOPPED

            # has the player STOPPED
            if lastPlayerPos.x == currentPlayerPos.x and lastPlayerPos.z == currentPlayerPos.z:
                playersState = STOPPED

            # if last players state != walking and players state = walking
            # player has started WALKING
            if lastPlayersState != WALKING and playersState == WALKING:
                soundWalking.play(-1)

            # if last players state = walking and players state != walking
            # player has stopped WALKING
            if lastPlayersState == WALKING and playersState != WALKING:
                soundWalking.stop()
                
             # player has started FLYING
            if lastPlayersState != FLYING and playersState == FLYING:
                soundFlying.play(-1)      
                
            # player has stopped FLYING
            if lastPlayersState == FLYING and playersState != FLYING:
                soundFlying.stop()                              

             # player has started SWIMING
            if lastPlayersState != SWIMING and playersState == SWIMING:
                soundSwiming.play(-1)      
                
            # player has stopped SWIMING
            if lastPlayersState == SWIMING and playersState != SWIMING:
                soundSwiming.stop()                              


            # if the players state = falling and the distance they have fell is greater than 3
            # player has started FALLING
            if playersState == FALLING and playerFallDistance > 3:
                if playerFalling == False:
                    soundFalling.play()
                    playerFalling = True

            # if last players state = falling and the players state != falling
            # player has stopped falling
            if lastPlayersState == FALLING and playersState != FALLING and playerFalling == True:
                soundFalling.stop()
                print("landing")
                soundLanding.play()
                playerFallDistance = 0
                playerFalling = False
            
            # if player has jumped and the jump sound is not playing
            if playerJumped == True:
                soundJump.play()
                playerJumped = False

            lastPlayerPos = currentPlayerPos
            lastPlayersState = playersState

            #Get the block hit events
            blockHits = mc.events.pollBlockHits()
            # block has been hit by right-mouse click
            #if blockHits:
            for hit in blockHits:
                print("Hits: " , blockHits)
                soundSword.play()
            
            # sleep to meet 20 Hz update
            time.sleep(0.05) 

    except KeyboardInterrupt:
        print("stopped")
