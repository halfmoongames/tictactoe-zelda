$$\textbf{Project 1 - TicTacToe via MinMax Algorithm}$$

$\textbf{Minimax}$ is a decision-making strategy used in two-player games where one player aims to maximize their score (often called the "maximizer") and the other player aims to minimize the score of the maximizer (often called the "minimizer"). The goal is to find the best move for the maximizer, assuming that the minimizer will make optimal moves.

$\textbf{Case Of TicTacToe :}$ We +1 for any favorable move that the player makes and -1 for any unfavorable move that the player makes. The Artificial Intelligence role is the "minimizer" in which it tries to minimize the score of the "maximizer" which is the player.

```
function  minimax(node, depth, maximizingPlayer)  is
    if  depth = 0  or  node is a terminal node  then 
         return  the heuristic value of node
    if  maximizingPlayer  then 
        value := −∞
         for each  child of node  do 
            value := max(value, minimax(child, depth − 1, FALSE))
         return  value
    else  _(* minimizing player *)_
        value := +∞
         for each  child of node  do 
            value := min(value, minimax(child, depth − 1, TRUE))
         return  value
```

$\textbf{Alpha–beta pruning}$ is a search algorithm that seeks to decrease the number of nodes that are evaluated by the minimax algorithm in its search tree. It is an adversarial search algorithm used commonly for machine playing of two-player combinatorial games (Tic-tac-toe, Chess, Connect 4, etc.). It stops evaluating a move when at least one possibility has been found that proves the move to be worse than a previously examined move. Such moves need not be evaluated further. When applied to a standard minimax tree, it returns the same move as minimax would, but prunes away branches that cannot possibly influence the final decision.

$\textbf{Fail-Hard Version:}$

```
  function   alphabeta(node, depth, α, β, maximizingPlayer)   is  
      if   depth == 0   or   node is terminal   then  
          return   the heuristic value of node
      if   maximizingPlayer   then  
        value := −∞
          for each   child of node   do  
            value := max(value, alphabeta(child, depth − 1, α, β, FALSE))
              if   value > β   then  
                  break   _(* β cutoff *)_
            α := max(α, value)
          return   value
      else  
        value := +∞
          for each   child of node   do  
            value := min(value, alphabeta(child, depth − 1, α, β, TRUE))
              if   value < α   then  
                  break   _(* α cutoff *)_
            β := min(β, value)
          return   value
```

$\textbf{Fail-Soft Version: }$

```
  function   alphabeta(node, depth, α, β, maximizingPlayer)   is  
      if   depth == 0   or   node is terminal   then  
          return   the heuristic value of node
      if   maximizingPlayer   then  
        value := −∞
          for each   child of node   do  
            value := max(value, alphabeta(child, depth − 1, α, β, FALSE))
            α := max(α, value)
              if   value ≥ β   then  
                  break   _(* β cutoff *)_
          return   value
      else  
        value := +∞
          for each   child of node   do  
            value := min(value, alphabeta(child, depth − 1, α, β, TRUE))
            β := min(β, value)
              if   value ≤ α   then  
                  break   _(* α cutoff *)_
          return   value
```

$\textbf{Difference Between Fail-Hard and Fail-Soft Part 1:}$ In the fail-hard version, if a move is found that proves the current node to be worse than the alpha value (for a maximizing node) or better than the beta value (for a minimizing node), the search immediately terminates. This is called "fail-hard" because it's strict and doesn't explore further down that branch of the search tree. In the fail-soft version, if a move is found that proves the current node to be worse than the alpha value (for a maximizing node) or better than the beta value (for a minimizing node), the search doesn't immediately terminate. Instead, it keeps exploring other branches of the tree to confirm if there's a better move. If a better move is found, it can update the alpha or beta values accordingly. 

$\textbf{Difference Between Fail-Hard and Fail-Soft Part 2:}$ Fail-hard pruning guarantees that the final result will be the same as if you had explored the entire search tree, assuming that the alpha and beta values are initialized correctly. It's both optimal (in terms of finding the best move) and complete (in terms of exploring all necessary nodes). Fail-soft pruning does not guarantee optimality or completeness on its own. It might miss the best move if it stops too early, or it might explore unnecessary nodes if it doesn't stop when it should. However, it can still be effective in practice when used in combination with move ordering and other heuristic techniques.

$\textbf{Case Of Zero Sum Game: }$For every two-person, zero-sum game with finitely many strategies, there exists a value V and a mixed strategy for each player, such that:

* Given Player 2's strategy, the best payoff possible for Player 1 is V
* Given Player 1's strategy, the best payoff possible for Player 2 is −V

$\textbf{Choice of web server:}$ The web server came down to two choices, as suggested by the assignment. Flask, a backend python server that hosts and delivers HTML templates with static files (JavaScript, CSS), or a frontend app development tool called Streamlit. Originally, the team considered using Streamlit. Benefits of Streamlit such the free and easy hosting alongside not needing to develop a seperate frontend were enticing. However, when the team started to implement the application in Streamlit, two issues sprang up: Front end customization was limited, and the tic-tac-toe game would need to be remade from scratch. The Streamlit server loop did not work well with our current implementation and so we pivoted into Flask. Flask proved to be much more inclined to integrate with our current tic-tac-toe implementation. Our own HTML, JavaScript, and CSS could be used on the frontend, which puts no limits on design. Additionally, the backend implementation only required some modification to the original design. The biggest issue with Flask, is that there would be no free or provided host for the server. We would need to host it ourselves.

$\textbf{Flask web server implementation:}$ Implementing the python game for Flask required some specific but trivial modifications to the game loop and user input-output. Most importantly, the game needs to be able to communicate with the user. Flask has some basic features to server HTML, JS, and CSS, but we will also need to send and retrieve the board state and the players move respectivly. To do this, we can send variables via GET and POST methods supplied by Flask. As an important mesure to differentiate users, before a new game is played, the server creates a session ID for a new user. Trivialy, because the Flask server allows us to host our own front-end data, the liberty was taken to customize the design further, including sound effects and particles.

$\textbf{Report}$

Team: Yurixander Ricardo Silva, Zee Fisher, and Kenneth Nguyen

Above is the information gathered to better understand the various aspect of the project gathered through sources such as Wikipedia, GeeksForGeeks, Artificial Intelligence: A Modern Approach, and Grokking Artificial Intelligence Algorithms. We also consulted the official documentation for Python, Streamlit, and Flask.

!["Original TicTacToe game"](https://raw.githubusercontent.com/KennNguyen/CAP4630-Project1-TicTacToe/web-extra-credit/screenshots/tic1.png)

In the beginning, Zee first developed the basics of the TicTacToe game in which it includes basic functionality of the TicTacToe game. Yurixander reviewed Zee's code for the basic TicTacToe game as well as implement the minimax algorithm into the Zee's basic TicTacToe game in which it performs as it should. Now continuing onto the Alpha-Beta Pruning aspect of the project, several pathways open up. As research from Kenneth shows that there is a Fail-Soft and Fail-Hard approach. We all agreed on going with the Fail Soft approach, despite being a computationally intensive approach, the implementation is just a 3x3 grid and possibilities don't branch out as much than other turn-base games such as Chess in which Fail-Soft might not be viable. Yurixander set his work on creating the Alpha Beta Pruning with Fail Soft approach as well as a benchmarking system that measures the recursion calls in each algorithm.

!["Benchmark Of Minimax and Alpha Beta"](https://raw.githubusercontent.com/KennNguyen/CAP4630-Project1-TicTacToe/blob/web-extra-credit/screenshots/benchmark.png)

!["Improved TicTacToe game"](https://raw.githubusercontent.com/KennNguyen/CAP4630-Project1-TicTacToe/web-extra-credit/screenshots/tic2.png)

For the web base portion of the assignment, Kenneth created the basic function and design of the TicTacToe website that didn't have AI implementation yet. Zee researched technologies such as Flask to learn how to implement the algorithms into the website. Yurixander using information that Zee gathered began creating a web server in which it a user when opening a page requests the backend of the website for a new session ID in which the backend of the website generates an ID via random int which then converts into hex and returning a hex string for the session ID. An empty board object is then assigned to that session ID which then has the clients makes requests to provide the session ID. Data is then sent between the user and server via GET and POST request generated by the user and by Flask. They contain game data and allow the server to communicate the computer's move and the game result. Yurixander also furnished the frontend with a Legend of Zelda inspired theme, complete with sound effects and particles.

!["Final TicTac Toe"](https://raw.githubusercontent.com/KennNguyen/CAP4630-Project1-TicTacToe/web-extra-credit/screenshots/tic3.png)

