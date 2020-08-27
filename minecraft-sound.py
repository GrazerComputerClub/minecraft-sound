# www.stuffaboutcode.com & GC2.at
# Raspberry Pi, GC2's Minecraft Pi Music, Sound and TNT- Add some sound effects and features to Minecraft Pi
# unchanged music by http://www.nosoapradio.us/, see LICENCE https://gamesounds.xyz/No%20soap%20radio/LICENSE
# Version 0.3 Beta

from time import time
from mcpi import minecraft
from mcpi import block
import time
#import pygame to play sound files
import pygame

# constants
STOPPED = 1
WALKING = 2
FALLING = 3
FLYING  = 4
SWIMING = 5


def run():
    try:
        #Connect to minecraft by creating the minecraft object
        # - minecraft needs to be running and in a game
        mc = minecraft.Minecraft.create()
        mc.postToChat("GC2's Minecraft Pi Music, Sound and TNT")
        mc.postToChat(" based upon project from Martin O'Hanlon")
        mc.postToChat("music by http://www.nosoapradio.us/")
        pygame.mixer.music.play(-1)
        mc.postToChat("sound sfx by http://soundbible.com/ (public domain)")

        # setup variables
        lastPlayersState = STOPPED
        lastBlock_beneath = 0
        playersState = STOPPED
        playerJumped = False
        playerLastJumpTime = 0
        playerFalling = False
        playerFallDistance = 0

        #get players position
        lastPlayerPos = mc.player.getPos()
        # loop until CTRL+C
        try:
            while(True):

                # get players position
                currentPlayerPos = mc.player.getPos()

                #print("player x=%d y=%d, z=%d" % (currentPlayerPos.x, currentPlayerPos.y, currentPlayerPos.z))
                Block_beneath = mc.getBlock(lastPlayerPos.x, lastPlayerPos.y-1, lastPlayerPos.z)  # block ID
                if Block_beneath == block.WATER_FLOWING or Block_beneath == block.WATER_STATIONARY:
                  Block_beneath = block.WATER
                  print("water")

                # has the player moved in either X or Z (are they WALKING?)
                if lastPlayerPos.x != currentPlayerPos.x or lastPlayerPos.z != currentPlayerPos.z:
                    # if player is FALLING they cant be WALKING
                
                    if playersState != FALLING:
                        if Block_beneath == block.AIR and lastBlock_beneath == block.AIR and playerJumped == False:
                          playersState = FLYING
                          print("flying")
                        elif Block_beneath == block.WATER:
                          playersState = SWIMING
                          print("swiming")
                        else:
                          playersState = WALKING
                          print("walking")
                    else:
                          print("not falling status %d" % playersState)


                # has the player moved in positive Y (have they jumped?)
                if int(lastPlayerPos.y) < int(currentPlayerPos.y):
                    playerJumped = True

                # has the player moved in negative Y (are they FALLING?)
                if int(lastPlayerPos.y) > int(currentPlayerPos.y):
                    print("falling state")
                    playersState = FALLING

                # is the player still falling?
                if playersState == FALLING and lastPlayersState == FALLING:
                    # increase the distance they have fallen
                    playerFallDistance = playerFallDistance + (lastPlayerPos.y - currentPlayerPos.y)

                # has the player STOPPED
                if playersState == WALKING and lastPlayerPos.x == currentPlayerPos.x and lastPlayerPos.z == currentPlayerPos.z:
                    print("state stopped x,z")
                    playersState = STOPPED

                # if the player is FALLING but has stopped moving down
                # (have they STOPPED FALLING?)
                if playersState == FALLING and int(lastPlayerPos.y) == int(currentPlayerPos.y):
                    print("state stopped y")
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
                    print("falling")
                    if playerFalling == False:
                        soundFalling.play()
                        playerFalling = True
                    else:
                      if lastBlock_beneath != block.WATER and Block_beneath == block.WATER:
                        print("hit water")
                        soundSplash.play()     

                # if last players state = falling and the players state != falling
                # player has stopped falling
                if lastPlayersState == FALLING and playersState != FALLING and playerFalling == True:
                    print("falling stopped, hit ground")
                    soundFalling.stop()
                    soundLanding.play()
                    playerFallDistance = 0
                    playerFalling = False
            
                # if player has jumped and the jump sound is not playing
                if playerJumped == True and playersState == WALKING:
                    elapsed = time.time()-playerLastJumpTime
                    if elapsed>0.5:
                      print("jump %f %d" % (elapsed, playersState))
                      soundJump.play()
                    else:
                      print("double jump")
                    playerLastJumpTime = time.time()
                    playerJumped = False

                lastPlayerPos = currentPlayerPos
                lastPlayersState = playersState
                lastBlock_beneath = Block_beneath

                #Get the block hit events
                blockHits = mc.events.pollBlockHits()
                # block has been hit by right-mouse click
                for hit in blockHits:
                  print("Hits: " , blockHits)
                  soundSword.play()
                  Block_Hit = mc.getBlockWithData(hit.pos.x, hit.pos.y, hit.pos.z)
                  # turn inactive TNT into explosive TNT
                  print("block = %d, data = %d" %  (Block_Hit.id,  Block_Hit.data))
                  if Block_Hit.id == block.TNT.id:
                    if Block_Hit.data == 0:
                      print("set TNT explosive %d" % (block.TNT.id))
                      mc.setBlock(hit.pos.x, hit.pos.y, hit.pos.z, block.TNT.id, 1)
                      mc.postToChat("turned into explosive TNT- hit for detonation")
                    if Block_Hit.data == 1:
                      mc.postToChat("hit TNT for detonation (left mouse)")
                  if Block_Hit.id == 247: #block.NETHER_REACTOR_CORE.id
                    if Block_Hit.data == 0 or Block_Hit.data == 2:
                      mc.setBlock(hit.pos.x, hit.pos.y, hit.pos.z, 247, 1)
                      mc.postToChat("reactor activated")
                      print("reactor activated")
                    if Block_Hit.data == 1:
                      mc.setBlock(hit.pos.x, hit.pos.y, hit.pos.z, 247, 2)
                      mc.postToChat("reactor stopped")
                      print("reactor stopped")
            
                # sleep to meet 20 Hz update
                time.sleep(0.05) 

        except KeyboardInterrupt:
          print("stopped")
          return 0

    except:
        print("No connetion to mcpi ...")
        pygame.mixer.music.stop()
        return -1

if __name__ == "__main__":
    print("")
    print("================================================") 
    print("| GC2's Minecraft Pi Music, Sound and TNT      |") 
    print("================================================")
    print("                      | |                       ") 
    print("                      | |                       ") 
    print("")

    #Initialise pygame and the mixer
    print("Initialise music and sound") 
    pygame.init()
    pygame.mixer.init()

    #MP3 background music from  http://www.nosoapradio.us/
    print("music by http://www.nosoapradio.us/")
    pygame.mixer.music.load("music/DST-BattleLands.mp3")

    #load WAVS files
    print("sound effects by http://soundbible.com/ (public domain)")
    soundWalking = pygame.mixer.Sound("sounds/walking.wav") #http://soundbible.com/2057-Footsteps-On-Cement.html
    soundJump = pygame.mixer.Sound("sounds/jump.wav") #http://soundbible.com/1953-Neck-Snap.html
    soundFalling = pygame.mixer.Sound("sounds/falling.wav") #http://soundbible.com/1247-Wind.html
    soundLanding = pygame.mixer.Sound("sounds/landing.wav") #http://soundbible.com/1952-Punch-Or-Whack.html
    soundSword = pygame.mixer.Sound("sounds/sword.wav") #http://soundbible.com/1898-Spin-Jump.html
    soundFlying = pygame.mixer.Sound("sounds/flying.wav") #http://soundbible.com/1036-Propeller.html
    soundSwiming = pygame.mixer.Sound("sounds/swiming.wav") #http://soundbible.com/2032-Water.html
    soundSplash = pygame.mixer.Sound("sounds/splash.wav")   #http://soundbible.com/2100-Splash-Rock-In-Lake.html

    while run() != 0:
        time.sleep(10) # seconds before retry
    print("Exit")

