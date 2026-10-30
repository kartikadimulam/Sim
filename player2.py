from itertools import combinations
import random

from consts import Board, Color, Edge, NUM_NODES


class Player2:
    """
    Implements a winning strategy for the second player in a game of Sim.
    """

    @staticmethod
    def get_move(board: list[list[Color]]) -> Edge:
        """
        Return a move for Player 2 following the optimal strategy.
        """

        miniboard = Player2.get_miniboard(board)

        if miniboard is None:
            raise ValueError("No miniboard found.")

        allowed_moves = Player2.get_allowed_moves(Color.P2, miniboard)

        if not allowed_moves:
            raise ValueError("No P2-allowed moves available.")

        if len(allowed_moves) == 1:
            return allowed_moves[0]

   
        p2_maximal_sets = Player2.get_maximal_allowed_sets(
            Color.P2, miniboard
        )

   
        p2_move_counts = {
            move: sum(move in allowed_set for allowed_set in p2_maximal_sets)
            for move in allowed_moves
        }

        max_p2_count = max(p2_move_counts.values())

        best_p2_moves = {
            move for move, count in p2_move_counts.items()
            if count == max_p2_count
        }

        if len(best_p2_moves) == 1:
            return next(iter(best_p2_moves))

    
        p1_maximal_sets = Player2.get_maximal_allowed_sets(
            Color.P1, miniboard
        )

        p1_move_counts = {
            move: sum(move in allowed_set for allowed_set in p1_maximal_sets)
            for move in best_p2_moves
        }

        max_p1_count = max(p1_move_counts.values())

        best_moves = [
            move for move, count in p1_move_counts.items()
            if count == max_p1_count
        ]

        return random.choice(best_moves)

    @staticmethod
    def get_miniboard(board: list[list[Color]]) -> list[list[Color]] | None:
        """
        Return a minimal miniboard from the input adjacency matrix.
        """

       
        mandatory_nodes = set()

        for u in range(NUM_NODES):
            for v in range(u + 1, NUM_NODES):
                if board[u][v] in (Color.P1, Color.P2):
                    mandatory_nodes.add(u)
                    mandatory_nodes.add(v)

      
        optional_nodes = set(range(NUM_NODES)) - mandatory_nodes

  
        for size in range(len(optional_nodes) + 1):
            for extra_nodes in combinations(optional_nodes, size):

                nodes = mandatory_nodes | set(extra_nodes)

      
                complete = True

                for u, v in combinations(nodes, 2):
                    if board[u][v] == Color.NONE:
                        complete = False
                        break

                if not complete:
                    continue

       
                p2_moves = []

                for u, v in combinations(nodes, 2):

                    if board[u][v] != Color.UNCOLORED:
                        continue

                    creates_triangle = False

                    for w in nodes:
                        if w == u or w == v:
                            continue

                        if (board[u][w] == Color.P2
                                and board[v][w] == Color.P2):
                            creates_triangle = True
                            break

                    if not creates_triangle:
                        p2_moves.append((u, v))

                if not p2_moves:
                    continue

          
                miniboard = [
                    [
                        board[u][v] if u in nodes and v in nodes
                        else Color.NONE
                        for v in range(NUM_NODES)
                    ]
                    for u in range(NUM_NODES)
                ]

                return miniboard

        return None

    @staticmethod
    def get_allowed_moves(
        player: Color, board: list[list[Color]]
    ) -> list[Edge]:
        """
        Return all distinct valid moves for the given player.
        """

        allowed_moves = []

        for u in range(NUM_NODES):
            for v in range(u + 1, NUM_NODES):

             
                if board[u][v] != Color.UNCOLORED:
                    continue

              
                creates_triangle = False

                for w in range(NUM_NODES):

                    if w == u or w == v:
                        continue

                    if (board[u][w] == player
                            and board[v][w] == player):
                        creates_triangle = True
                        break

                if not creates_triangle:
                    allowed_moves.append((u, v))

        return allowed_moves

    @staticmethod
    def get_maximal_allowed_sets(
            player: Color, board: list[list[Color]]
    ) -> set[frozenset[Edge]]:
        """
        Return all distinct maximum-cardinality allowed sets
        for the given player.
        """

        allowed_moves = Player2.get_allowed_moves(player, board)

        valid_sets = set()
        max_size = -1

 
        for size in range(len(allowed_moves) + 1):

            for moves in combinations(allowed_moves, size):

               
                temp_board = [row[:] for row in board]

         
                for u, v in moves:
                    temp_board[u][v] = player
                    temp_board[v][u] = player

       
                creates_triangle = False

                for u, v, w in combinations(range(len(board)), 3):

                    if (temp_board[u][v] == player
                            and temp_board[u][w] == player
                            and temp_board[v][w] == player):
                        creates_triangle = True
                        break

                if creates_triangle:
                    continue

    
                if size > max_size:
                    max_size = size
                    valid_sets = {frozenset(moves)}

                elif size == max_size:
                    valid_sets.add(frozenset(moves))

        return valid_sets
