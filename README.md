# ![](jungle-py/assets/icon.png) Jungle Chess (Dou Shou Qi) ![](jungle-py/assets/icon.png)
_University of Porto · Master In Data Science and Engineering · Artificial Intelligence Project_

<br>

Python app developed for tinkering with AI concepts using [_Dou Shou Qi (Jungle Chess)_](https://en.wikipedia.org/wiki/Jungle_(board_game)) as the playground. Implementing several search algorithms (**minimax**, **alpha-beta**, **pruning**) and developing custom **evaluation functions**.

[Code](jungle-py/) and [PDF](MECD06%20-%20Dou%20Shou%20QI%20-%20AndreAfonso_NunoVasconcelos.pdf) available. 

A more in-depth guide for the **app architecture**, **game strategy** and each **search algorithm** & **evaluation function** developed can be seen in the [PDF](MECD06%20-%20Dou%20Shou%20QI%20-%20AndreAfonso_NunoVasconcelos.pdf).

**Code structure:**
* [main.py](jungle-py/main.py): runs the game
* [Assets](jungle-py/assets/): stores all assets (images, sound, buttons) used to improve UX 
* [Jungle](jungle-py/jungle/): controls the board game logic 
* [Minimax](jungle-py/minimax/): stores all search algorithms implemented
  * [minimax](jungle-py/minimax/algorithm.py?plain=1#L7)
  * [alpha-beta](jungle-py/minimax/algorithm.py?plain=1#L52)
  * [alpha-beta w/ pruning](jungle-py/minimax/algorithm.py?plain=1#L105)
  * the [iterative deepening](jungle-py/minimax/algorithm.py?plain=1#156) versions of these

<br>
<p align="center">
  <img src="https://github.com/nunobv/jungle-chess_dou-shou-qi_AI/blob/main/jungle-py/assets/home_screen.png?raw=true" alt="Game home screen image"/>
</p>
