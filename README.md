# PyFingers

The 2P Finger Dance Dance Revolution music game in Python (**PYQT5**) 

This project is one of my school project which is done in a hurry week, it still needs much improvement. See [TODO](#todo).
However, in the current version, you can already have some fun with creating your own music sheet and play it (with your friend, it's 2P).

![Phase](https://img.shields.io/badge/Phase-Need%20Enhansed%20But%20Not%20In%20Developing-orange.svg) <br/>

# Table of contents

- [FEATURES](#features)
- [HOW-TO-PLAY](#how-to-play)
- [TODO](#todo)
- [DEMO](#demo)
- [BUILD](#Build)

FEATURES
===

- Create and Edit your **own music sheet** of a music. (Defines arrows)
- Play any music sheet and prepare your fingers 
- Java Style code, I'm as Java as Fk...

HOW TO PLAY
===

**Make your own music sheet first then play it.**

1. To make your own music sheet
    1. Go to the Music Sheet Arrangement Page.
    2. Open the music file you want to arrange for.
    3. Click the start button to start the arrangement, then the music will be played.
    4. While the music playing, push **←↑↓→** on the keyboard to arrange the arrows, the **arrangement system is watching all the arrows you push, when they are hit and in which directions**, and then it will record them into the sheet file which is placed **\resources\sheets** prefixed by the music file name. 

2. Play your own music
    1. Go to the homepage, select your music name and hit the start game button.
    2. The sheet loading engine will load your premade sheet in with all arrows arranged, so you can start enjoying your DDR game with your own music.
    3. Further, you can share your music to your friend by giving him the sheeet file placed in **\resources\sheets** and the corresponding music file placed in **\resources\sheets\musics**. He should place them under the same place then he can play it.
    
TODO
===

- **Improve Dance Dance Revolution engine** (The current implementation was done in just a week with full of haste..)
    - Use another tailored format to better describe a music sheet.
    - Use some scheduler pools to arrange tempo finger and update game sprites more punctually rather than creating threads extravagantly. 
    - Improve the sheet editor. (Make it into English)
        - Make GUI into English
        - Improve accuracy and performance
    - Calculating the player scores and show it during the end of a game.
    
- More detailed documents if you wished
- Apply machine learning to create music sheets. (Seriously?) (Yes so this is why it's in python)

DEMO
===

[Youtube Demo Video](https://www.youtube.com/watch?v=cCnGRNj_92g)


BUILD
===

1. Use Pycharm open it and pull the dependencies. Or use `pip`. (It depends **pyqt5**)

2. Type commands
```
cd PyFingers
python MyMainView.py
```

3. The repository ignores all music components in sheets and musics directories but includes only a Demo music which you can play by choosing the music **king_boss_op.mp3** on the homepage panel.


