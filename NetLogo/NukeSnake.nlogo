; Nuke Snake 1.0  by Jim Lyons
; January 6, 2005

__extensions [ "sound.jar" ]

globals [ bg-color  fg-color  score ]
breeds [ snakes  bullets ]
patches-own [ mem ]
snakes-own [ armed? ]

;=== OBSERVER ===

to startup
  set bg-color brown + 2 ; <-------- SET BACKGROUND COLOR --------
  set fg-color bg-color - 4 ; <-------- SET FOREGROUND COLOR --------
  set-default-shape snakes "snake eyes"
  set-default-shape bullets "line"
  set score [0 0]
  new-game
end

to new-game
  clear-turtles
  ask patches [ set pcolor bg-color ]
  if rocks?
  [ ask random-n-of num-rocks patches with [abs pxcor > 5 or abs pycor > 5] [ make-rock ] ]
  if walls? [ ask borders [ set pcolor fg-color ] ]
  create-custom-snakes 2
  [ setxy (2 * who - 1) (1 - 2 * who) ; start 0 at (-1,1) and 1 at (1,-1)
    set color item who [orange sky] ; <-------- SET SNAKE COLORS --------
    stamp color
    set armed? false ; don't arm until first move
  ]
end

to-report borders
  report patches with [abs pxcor = screen-edge-x or abs pycor = screen-edge-y]
end

to go
  if count snakes < 2 [ ask snakes [ add-win  celebrate ]  stop ]
  every 1 / (5 * speed) [ ask bullets [ streak ] ]
  every 1 / speed [ ask snakes [ move ] ]
end

;=== PATCHES ===

to make-rock
  set pcolor fg-color
  ask random-n-of 6 neighbors [ set pcolor fg-color + random-float 2 ]
end

to blast
  set mem pcolor  set pcolor yellow  wait .2  set pcolor mem
  ask snakes-here [ sfx-blasted  depart ]
end

;=== SNAKES ===

to move
  if pcolor-of patch-ahead 1 != bg-color [ sfx-crash  depart ]
  if not trails? [ stamp bg-color ]
  forward 1
  stamp color
  if any? other-snakes-here [ ask snakes [ sfx-crash  depart ] ]
  set armed? true
end

to fire
  if armed?
  [ sfx-fire
    hatch-bullets 1 [ set color white  streak ]
    set armed? false ; until next move
  ]
end

to add-win
  let n item who score ; my number of wins
  set score replace-item who score (n + 1)
end

to celebrate
  sfx-celebrate
  ask patches in-radius-nowrap 4
  [ set mem pcolor  set pcolor color-of myself  wait random-float .75  set pcolor mem ]
end

to depart
  stamp black
  die
end

;=== BULLETS ===

to streak
  forward 1
  if pcolor != bg-color
  [ stamp white
    sfx-hit
    ask neighbors [ blast ]
    stamp bg-color
    ask snakes-here [ sfx-kill  depart ]
    die
  ] 
end

;=== SOUND EFFECTS ===

to sfx-crash ;snake hits something
  if sound? [ play-note "orchestra hit" 55 120 1 ]
end

to sfx-fire ;fire bullet
  if sound? [ play-note "gunshot" 114 120 1 ]
end

to sfx-hit ;bullet hits wall, rock, or trail
  if sound? [ play-drum "long guiro" 120 ]
end

to sfx-kill ;bullet hits snake
  if sound? [ play-drum "crash cymbal 2" 120 ]
end

to sfx-blasted ;blast hits snake
  if sound? [ play-drum "vibraslap" 120 ]
end

to sfx-celebrate
  if sound? [ play-note "applause" 60 120 1 ]
end
@#$#@#$#@
GRAPHICS-WINDOW
227
10
710
514
21
21
11.0
1
12
0
0
0
0

CC-WINDOW
5
528
719
623
Command Center

BUTTON
114
144
212
243
Go
go
T
1
T
OBSERVER
T
G

BUTTON
114
85
211
135
New Game
new-game
NIL
1
T
OBSERVER
T
N

BUTTON
127
329
182
362
Right
if turtle 0 != nobody [ ask turtle 0 [right 90] ]
NIL
1
T
OBSERVER
T
D

BUTTON
17
329
72
362
Left
if turtle 0 != nobody [ ask turtle 0 [left 90] ]
NIL
1
T
OBSERVER
T
A

BUTTON
47
480
102
513
Left
if turtle 1 != nobody [ ask turtle 1 [left 90] ]
NIL
1
T
OBSERVER
T
L

BUTTON
157
480
212
513
Right
if turtle 1 != nobody [ ask turtle 1 [right 90] ]
NIL
1
T
OBSERVER
T
'

TEXTBOX
37
276
201
304
(Click outside of buttons to enable keyboard control.)

SLIDER
17
210
114
243
speed
speed
1
10
5
1
1
NIL

BUTTON
72
329
127
362
Fire
if turtle 0 != nobody [ ask turtle 0 [fire] ]
NIL
1
T
OBSERVER
T
S

BUTTON
102
480
157
513
Fire
if turtle 1 != nobody [ ask turtle 1 [fire] ]
NIL
1
T
OBSERVER
T
;

TEXTBOX
64
367
160
385
Snake Zero

TEXTBOX
115
462
213
480
Snake One

SWITCH
17
36
114
69
walls?
walls?
1
1
-1000

MONITOR
64
384
114
433
Wins
item 0 score
3
1

MONITOR
114
410
164
459
Wins
item 1 score
3
1

SWITCH
17
177
114
210
trails?
trails?
0
1
-1000

SWITCH
17
69
114
102
rocks?
rocks?
0
1
-1000

SWITCH
17
144
114
177
sound?
sound?
0
1
-1000

SLIDER
17
102
114
135
num-rocks
num-rocks
5
35
17
1
1
NIL

TEXTBOX
75
10
205
28
NUKE SNAKE  1.0

BUTTON
114
36
211
85
New Match
set score [0 0]\nnew-game
NIL
1
T
OBSERVER
T
NIL

@#$#@#$#@
NUKE SNAKE 1.0
--------------
This two-player arcade game is a cross between "snake" and "tank" games, and is named after the popular Macintosh shareware game by David Riggle that inspired it. It requires NetLogo version 2.1 or higher since it uses keyboard input for the controls.

It is a game of survival -- the one who doesn't die wins. Each player controls the constantly moving head of a growing trail. If you run into one of the trails, or into the walls or rocks, you die.

In Nuke Snake, you also have the ability to shoot. If you shoot the other snake's head, it dies and you win. You can also shoot your way through the trails, rocks, and walls, but be careful -- if anything blows up within one patch of your head, you die.

HOW TO PLAY
-----------
This version of Nuke Snake requires two players. (If you want a real challenge though, try steering both snakes, one with each hand, and see how long you can keep them from crashing into the rocks.) Notice that in order to use the keyboard controls for the buttons when starting up, or after using the Command Center or going to another Tab, you have to click in the panel outside of any buttons or text; you will see a difference in the buttons when the keyboard is enabled. (To change a keyboard control, edit its button in the Interface and change its Action Key field.)

The Trails? switch, the Sound? switch, and the speed control can be changed while playing. The Walls? switch, the Rocks? switch, and the num-rocks slider must be set before pressing the New Game button. Be sure to try all combinations of trails, rocks, and walls.

A match is a series of games that continues until one player reaches a predetermined number of wins, usually 10. The New Match button resets the Wins score for the two players.

The two snakes are called Snake Zero and Snake One to avoid using colors as the names (so they can be whatever colors you want) and also to remind you about numbering things starting with zero in NetLogo. There are comments in the Procedures to show you where to set the colors for the model if you want to change them.

HOW IT WORKS
------------
The snakes (actually just the heads) are a breed of turtles. A snake's "body" -- the trail -- is really just colored patches showing where the head has been. In order to make the head look exactly like the rest of its body, the patch the head is on is stamped with its color. The turtle shape used for the snake's head is actually just the eyes.

Patch color is the key to operation of the game. If a patch is the background color, that means it is clear and the snakes can move there. If a patch is any other color, that means it is a trail, wall, or rock. The move command in the Snakes section of the Procedures just has to check the color of the patch-ahead 1. If it's the background color, go forward 1; if it's not, crash and die. The move script also checks for the special case of the snakes running into each other.

Bullets are another breed of turtles. To fire, a snake simply "hatches" a bullet with the same heading as itself and the main loop (see below) will make it "streak" along until it hits something. The streak command in the Bullets section of the Procedures just moves the bullet and checks the patch color. If it's the background color the bullet keeps going. If not, whatever was there is blown away and the neighboring patches are blasted. If a snake's head is hit or blasted, it dies.

The main loop of this game is the go command in the Observer section of the Procedures. It is called by a "forever" button in the Interface and is just three lines long. The first line checks to see if both snakes are still alive and if not, ends the game:

  if count snakes < 2 [ ask snakes [ add-win  celebrate ]  stop ]

Notice that this covers the situations where both snakes die; the "ask snakes" just refers to the surviving snake, if any.

The other two lines make the bullets streak and the snakes move:

  every 1 / (5 * speed) [ ask bullets [ streak ] ]
  every 1 / speed [ ask snakes [ move ] ]

"speed" is the value of the slider in the Interface, which goes from 1 to 10. The bullets move five times as fast as the snakes and the snakes move every 1 to 1/10 second. The streak and move scripts take care of all collision detection. (The slider at the top of the Graphics area controls the speed of the NetLogo engine and should stay all the way to the right for best results.) Look up "every" in the Primitives Dictionary of the NetLogo manual for more information.

To create the visual effect when something is blasted, each patch has its own memory variable, mem, to store its color while the blast is shown. See the Patches section of the Procedures for the blast command. Also notice the other patch command, make-rock. When the Rocks? switch is on, the new-game command asks a number of patches, set by the num-rocks slider, to make the rocks.

The sound effects are written in the form of individual commands for convenience. This separates the details of creating the sounds from the logic of the procedures that use them, which has two benefits: It makes the logic easier to follow and it collects all the sound effects in one place so it is easier to experiment with them. Look at the Sound section of the NetLogo manual and try creating your own sound design for the game with the available drum and instrument sounds.


COPYRIGHT AND TERMS OF USE
--------------------------
This NetLogo model is copyright 2005 by Jim Lyons. All rights reserved. 

Permission to use, modify or redistribute this model is hereby granted, provided that this copyright notice is included. This model may not be redistributed for profit without permission of the author. Contact Jim Lyons, jimlyons@earthlink.net.
@#$#@#$#@
default
true
0
Polygon -7566196 true true 150 5 40 250 150 205 260 250

airplane
true
0
Polygon -7566196 true true 150 0 135 15 120 60 120 105 15 165 15 195 120 180 135 240 105 270 120 285 150 270 180 285 210 270 165 240 180 180 285 195 285 165 180 105 180 60 165 15

arrow
true
0
Polygon -7566196 true true 150 0 0 150 105 150 105 293 195 293 195 150 300 150

box
false
0
Polygon -7566196 true true 150 285 285 225 285 75 150 135
Polygon -7566196 true true 150 135 15 75 150 15 285 75
Polygon -7566196 true true 15 75 15 225 150 285 150 135
Line -16777216 false 150 285 150 135
Line -16777216 false 150 135 15 75
Line -16777216 false 150 135 285 75

bug
true
0
Circle -7566196 true true 96 182 108
Circle -7566196 true true 110 127 80
Circle -7566196 true true 110 75 80
Line -7566196 true 150 100 80 30
Line -7566196 true 150 100 220 30

butterfly
true
0
Polygon -7566196 true true 150 165 209 199 225 225 225 255 195 270 165 255 150 240
Polygon -7566196 true true 150 165 89 198 75 225 75 255 105 270 135 255 150 240
Polygon -7566196 true true 139 148 100 105 55 90 25 90 10 105 10 135 25 180 40 195 85 194 139 163
Polygon -7566196 true true 162 150 200 105 245 90 275 90 290 105 290 135 275 180 260 195 215 195 162 165
Polygon -16777216 true false 150 255 135 225 120 150 135 120 150 105 165 120 180 150 165 225
Circle -16777216 true false 135 90 30
Line -16777216 false 150 105 195 60
Line -16777216 false 150 105 105 60

car
false
0
Polygon -7566196 true true 300 180 279 164 261 144 240 135 226 132 213 106 203 84 185 63 159 50 135 50 75 60 0 150 0 165 0 225 300 225 300 180
Circle -16777216 true false 180 180 90
Circle -16777216 true false 30 180 90
Polygon -16777216 true false 162 80 132 78 134 135 209 135 194 105 189 96 180 89
Circle -7566196 true true 47 195 58
Circle -7566196 true true 195 195 58

circle
false
0
Circle -7566196 true true 30 30 240

circle 2
false
0
Circle -7566196 true true 16 16 270
Circle -16777216 true false 46 46 210

cow
false
0
Polygon -7566196 true true 200 193 197 249 179 249 177 196 166 187 140 189 93 191 78 179 72 211 49 209 48 181 37 149 25 120 25 89 45 72 103 84 179 75 198 76 252 64 272 81 293 103 285 121 255 121 242 118 224 167
Polygon -7566196 true true 73 210 86 251 62 249 48 208
Polygon -7566196 true true 25 114 16 195 9 204 23 213 25 200 39 123

face happy
false
0
Circle -7566196 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 255 90 239 62 213 47 191 67 179 90 203 109 218 150 225 192 218 210 203 227 181 251 194 236 217 212 240

face neutral
false
0
Circle -7566196 true true 8 7 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Rectangle -16777216 true false 60 195 240 225

face sad
false
0
Circle -7566196 true true 8 8 285
Circle -16777216 true false 60 75 60
Circle -16777216 true false 180 75 60
Polygon -16777216 true false 150 168 90 184 62 210 47 232 67 244 90 220 109 205 150 198 192 205 210 220 227 242 251 229 236 206 212 183

fish
false
0
Polygon -1 true false 44 131 21 87 15 86 0 120 15 150 0 180 13 214 20 212 45 166
Polygon -1 true false 135 195 119 235 95 218 76 210 46 204 60 165
Polygon -1 true false 75 45 83 77 71 103 86 114 166 78 135 60
Polygon -7566196 true true 30 136 151 77 226 81 280 119 292 146 292 160 287 170 270 195 195 210 151 212 30 166
Circle -16777216 true false 215 106 30

flag
false
0
Rectangle -7566196 true true 60 15 75 300
Polygon -7566196 true true 90 150 270 90 90 30
Line -7566196 true 75 135 90 135
Line -7566196 true 75 45 90 45

flower
false
0
Polygon -11352576 true false 135 120 165 165 180 210 180 240 150 300 165 300 195 240 195 195 165 135
Circle -7566196 true true 85 132 38
Circle -7566196 true true 130 147 38
Circle -7566196 true true 192 85 38
Circle -7566196 true true 85 40 38
Circle -7566196 true true 177 40 38
Circle -7566196 true true 177 132 38
Circle -7566196 true true 70 85 38
Circle -7566196 true true 130 25 38
Circle -7566196 true true 96 51 108
Circle -16777216 true false 113 68 74
Polygon -11352576 true false 189 233 219 188 249 173 279 188 234 218
Polygon -11352576 true false 180 255 150 210 105 210 75 240 135 240

house
false
0
Rectangle -7566196 true true 45 120 255 285
Rectangle -16777216 true false 120 210 180 285
Polygon -7566196 true true 15 120 150 15 285 120
Line -16777216 false 30 120 270 120

leaf
false
0
Polygon -7566196 true true 150 210 135 195 120 210 60 210 30 195 60 180 60 165 15 135 30 120 15 105 40 104 45 90 60 90 90 105 105 120 120 120 105 60 120 60 135 30 150 15 165 30 180 60 195 60 180 120 195 120 210 105 240 90 255 90 263 104 285 105 270 120 285 135 240 165 240 180 270 195 240 210 180 210 165 195
Polygon -7566196 true true 135 195 135 240 120 255 105 255 105 285 135 285 165 240 165 195

line
true
0
Line -7566196 true 150 0 150 300

pentagon
false
0
Polygon -7566196 true true 150 15 15 120 60 285 240 285 285 120

person
false
0
Circle -7566196 true true 110 5 80
Polygon -7566196 true true 105 90 120 195 90 285 105 300 135 300 150 225 165 300 195 300 210 285 180 195 195 90
Rectangle -7566196 true true 127 79 172 94
Polygon -7566196 true true 195 90 240 150 225 180 165 105
Polygon -7566196 true true 105 90 60 150 75 180 135 105

plant
false
0
Rectangle -7566196 true true 135 90 165 300
Polygon -7566196 true true 135 255 90 210 45 195 75 255 135 285
Polygon -7566196 true true 165 255 210 210 255 195 225 255 165 285
Polygon -7566196 true true 135 180 90 135 45 120 75 180 135 210
Polygon -7566196 true true 165 180 165 210 225 180 255 120 210 135
Polygon -7566196 true true 135 105 90 60 45 45 75 105 135 135
Polygon -7566196 true true 165 105 165 135 225 105 255 45 210 60
Polygon -7566196 true true 135 90 120 45 150 15 180 45 165 90

snake eyes
true
0
Polygon -16777216 true false 180 60 240 45 255 150
Polygon -16777216 true false 120 60 60 45 45 150

square
false
0
Rectangle -7566196 true true 30 30 270 270

square 2
false
0
Rectangle -7566196 true true 30 30 270 270
Rectangle -16777216 true false 60 60 240 240

star
false
0
Polygon -7566196 true true 60 270 150 0 240 270 15 105 285 105
Polygon -7566196 true true 75 120 105 210 195 210 225 120 150 75

target
false
0
Circle -7566196 true true 0 0 300
Circle -16777216 true false 30 30 240
Circle -7566196 true true 60 60 180
Circle -16777216 true false 90 90 120
Circle -7566196 true true 120 120 60

tree
false
0
Circle -7566196 true true 118 3 94
Rectangle -6524078 true false 120 195 180 300
Circle -7566196 true true 65 21 108
Circle -7566196 true true 116 41 127
Circle -7566196 true true 45 90 120
Circle -7566196 true true 104 74 152

triangle
false
0
Polygon -7566196 true true 150 30 15 255 285 255

triangle 2
false
0
Polygon -7566196 true true 150 30 15 255 285 255
Polygon -16777216 true false 151 99 225 223 75 224

truck
false
0
Rectangle -7566196 true true 4 45 195 187
Polygon -7566196 true true 296 193 296 150 259 134 244 104 208 104 207 194
Rectangle -1 true false 195 60 195 105
Polygon -16777216 true false 238 112 252 141 219 141 218 112
Circle -16777216 true false 234 174 42
Rectangle -7566196 true true 181 185 214 194
Circle -16777216 true false 144 174 42
Circle -16777216 true false 24 174 42
Circle -7566196 false true 24 174 42
Circle -7566196 false true 144 174 42
Circle -7566196 false true 234 174 42

turtle
true
0
Polygon -11352576 true false 215 204 240 233 246 254 228 266 215 252 193 210
Polygon -11352576 true false 195 90 225 75 245 75 260 89 269 108 261 124 240 105 225 105 210 105
Polygon -11352576 true false 105 90 75 75 55 75 40 89 31 108 39 124 60 105 75 105 90 105
Polygon -11352576 true false 132 85 134 64 107 51 108 17 150 2 192 18 192 52 169 65 172 87
Polygon -11352576 true false 85 204 60 233 54 254 72 266 85 252 107 210
Polygon -7566196 true true 119 75 179 75 209 101 224 135 220 225 175 261 128 261 81 224 74 135 88 99

wheel
false
0
Circle -7566196 true true 3 3 294
Circle -16777216 true false 30 30 240
Line -7566196 true 150 285 150 15
Line -7566196 true 15 150 285 150
Circle -7566196 true true 120 120 60
Line -7566196 true 216 40 79 269
Line -7566196 true 40 84 269 221
Line -7566196 true 40 216 269 79
Line -7566196 true 84 40 221 269

x
false
0
Polygon -7566196 true true 270 75 225 30 30 225 75 270
Polygon -7566196 true true 30 75 75 30 270 225 225 270

@#$#@#$#@
NetLogo 2.1.0
@#$#@#$#@
@#$#@#$#@
@#$#@#$#@
