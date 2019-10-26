from typing import Tuple

import numpy as np
import tensorflow as tf

from battleship.board import Board, BOARD_NUM_ROWS, BOARD_NUM_COLS
from battleship.player import CPUPlayer, Player

BOARD_SIZE = BOARD_NUM_ROWS * BOARD_NUM_COLS
_DEFAULT_NUM_TRAINING_GAMES = 100


class CPUPlayerReinforcment(CPUPlayer):
    """A CPU that learns via reinforcement learning"""
    def __init__(self, board: Board, name: str = None):
        super().__init__(board, name=name)

        self.moves_played = []

        hidden_units = BOARD_SIZE
        output_units = BOARD_SIZE

        self.input_positions = tf.placeholder(
            tf.float32, shape=(1, BOARD_SIZE))
        self.labels = tf.placeholder(tf.int64)
        self.learning_rate = tf.placeholder(tf.float32, shape=[])
        # Generate hidden layer
        W1 = tf.Variable(tf.truncated_normal([BOARD_SIZE, hidden_units],
                         stddev=0.1 / np.sqrt(float(BOARD_SIZE))))
        b1 = tf.Variable(tf.zeros([1, hidden_units]))
        h1 = tf.tanh(tf.matmul(self.input_positions, W1) + b1)
        # Second layer -- linear classifier for action logits
        W2 = tf.Variable(tf.truncated_normal([hidden_units, output_units],
                         stddev=0.1 / np.sqrt(float(hidden_units))))
        b2 = tf.Variable(tf.zeros([1, output_units]))
        logits = tf.matmul(h1, W2) + b2
        self.probabilities = tf.nn.softmax(logits)

        init = tf.initialize_all_variables()
        cross_entropy = tf.nn.sparse_softmax_cross_entropy_with_logits(
                logits=logits, labels=self.labels, name='xentropy')
        self.train_step = tf.train.GradientDescentOptimizer(
            learning_rate=self.learning_rate).minimize(cross_entropy)
        # Start TF session
        self.sess = tf.Session()
        self.sess.run(init)

    def train(self):
        game_lengths = []
        alpha = 0.06
        print(f"{self} is training itself how to play battleship..")

        for game in range(_DEFAULT_NUM_TRAINING_GAMES):
            board_position_log, action_log, hit_log, hit_log_sizes = \
                self.play_game()

            game_lengths.append(len(action_log))
            rewards_log = self.rewards_calculator(hit_log, hit_log_sizes)
            for reward, current_board, action in zip(rewards_log,
                                                     board_position_log,
                                                     action_log):
                # Take step along gradient
                self.sess.run(
                    [self.train_step],
                    feed_dict={
                        self.input_positions: current_board,
                        self.labels: [action],
                        self.learning_rate: alpha * reward
                    }
                )
        print(f"{self} has learned how to play battleship. Watch out!")

    def play_game(self):
        """ Play game of battleship using network."""
        # create opponent board to play against with random ship placements
        opponent_board = Board()
        opponent_player = Player(opponent_board)
        # Initialize logs for game
        board_position_log = []
        action_log = []
        hit_log = []
        hit_log_sizes = []
        # Play through game
        current_board = [opponent_board.serialize()]
        while True:
            board_position_log.append([[i for i in current_board[0]]])
            probs = self.sess.run(
                [self.probabilities],
                feed_dict={self.input_positions: current_board})[0][0]
            probs = [p * (index not in action_log)
                     for index, p in enumerate(probs)]
            probs = [p / sum(probs) for p in probs]
            serialized_index = np.random.choice(BOARD_SIZE, p=probs)
            # bomb_index = np.argmax(probs)
            # update board, logs
            is_hit, is_ship_down = opponent_board.fire(serialized_index)
            is_hit = 1 if is_hit else 0
            ship_at = opponent_board.ship_at(serialized_index)
            size = ship_at.size if ship_at else 0
            hit_log.append(is_hit)
            hit_log_sizes.append(size)
            action_log.append(serialized_index)
            if opponent_player.all_ships_down():
                break
        return board_position_log, action_log, hit_log, hit_log_sizes

    def rewards_calculator(self, hit_log, hit_log_sizes, gamma=0.5):
        """Discounted sum of future hits over trajectory"""
        hit_log_weighted = [
            (item - float(hit_log_sizes[index] -
             sum(hit_log[:index])) / float(
                    BOARD_SIZE - index)) * (gamma ** index)
            for index, item in enumerate(hit_log)
        ]
        return [((gamma) ** (-i)) * sum(hit_log_weighted[i:])
                for i in range(len(hit_log))]

    def pick_move(self, board: Board) -> Tuple[int, int]:
        """CPU logic to pick a move"""
        current_board = board.serialize()
        probs = self.sess.run(
                [self.probabilities],
                feed_dict={self.input_positions: [current_board]})[0][0]
        probs = [p * (index not in self.moves_played)
                 for index, p in enumerate(probs)]
        probs = [p / sum(probs) for p in probs]
        serialized_index = np.argmax(probs)
        self.moves_played.append(serialized_index)
        return board.position_for_serialized_index(serialized_index)
