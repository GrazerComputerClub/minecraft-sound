## GC2's Minecraft Pi Music, Sound and TNT


### Installation

   - Download latest release version and unzip to /home/pi/minecraft-sound
   - edit '/usr/bin/minecraft-pi' and add sound process start and stop:
   ```
   cd /opt/minecraft-pi || exit
   
   cd /home/pi/minecraft-sound
python3 minecraft-sound.py &
PID=$!
echo Minecraft Sound process PID is $PID

cd /opt/minecraft-pi

if grep -q okay /proc/device-tree/soc/v3d@7ec00000/status \
        /proc/device-tree/soc/firmwarekms@7e600000/status 2> /dev/null; then
        export LD_PRELOAD=libbcm_host.so.1.0
        export LD_LIBRARY_PATH=lib/mesa
else
        export LD_LIBRARY_PATH=lib/brcm
fi

./minecraft-pi
echo stopping Minecraft Sound process
kill -KILL $PID
   ```
   

------------------------------------------------------------------------------

### Version history 
  0.3 - GC2 version
   - Program stays active after closing map or Minecraft Pi
   - Automatic reconnect
   
  0.2 - GC2 version 
   - Port to Python 3
   - Replaced Sound with Public Domain sounds
   - New sounds (splash, flying)
   - Background music
   - Optimizations (double jump for flying)
   - Activation of explosive TNT block (by simply hit it with sword)
   
  0.1 - first beta release by Martin O'Hanlon (martin@ohanlonweb.com) - http://www.stuffaboutcode.com

-------------------------------------------------------------------------------
### Martin O'Hanlon:
I got bored of Minecraft on the Pi not having any sound, so I made my own!
http://www.stuffaboutcode.com/2013/06/raspberry-pi-minecraft-sounds-effects.html

-------------------------------------------------------------------------------
