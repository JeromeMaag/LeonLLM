import unittest
import chess.pgn
from pgn_to_xlan import pgn_to_xlan
from io import StringIO


class pgn_to_xlan_test(unittest.TestCase):
    def setUp(self):
        self.converter = pgn_to_xlan(
            "dummy_input_path",
            "dummy_output_path",
            min_number_of_moves_per_game=5,
        )

    def test_pawn_move_to_lan(self):
        self.assertEqual(self.converter.move_lan_to_xlan("e2-e4", True), "Pe2-e4")

    def test_king_move_to_lan(self):
        self.assertEqual(self.converter.move_lan_to_xlan("Ng1-f3", True), "Ng1-f3")

    def test_convert_castling_for_white_and_black(self):
        self.assertEqual(self.converter.convert_castling("O-O", True), "Ke1g1")
        self.assertEqual(self.converter.convert_castling("O-O-O", True), "Ke1c1")

    def test_convert_castling_for_black(self):
        self.assertEqual(self.converter.convert_castling("O-O", False), "Ke8g8")
        self.assertEqual(self.converter.convert_castling("O-O-O", False), "Ke8c8")

    def test_convert_promotion(self):
        self.assertEqual(self.converter.convert_promotion("d7-d8=Q"), "Qd7-d8")
        self.assertEqual(self.converter.convert_promotion("Pd7-d8=Q"), "Qd7-d8")

    def test_game_to_lan_1(self):
        pgn_str = "1. g3 e6 2. Bg2 Qf6 3. f4 Bc5 4. e4 Qd4 5. e5 Qf2# 0-1"
        game = chess.pgn.read_game(self._pgn_io(pgn_str))
        lan_str = next(self.converter.game_to_xlan(game))

        self.assertEqual(
            lan_str,
            "1. Pg2-g3 Pe7-e6 2. Bf1-g2 Qd8-f6 3. Pf2-f4 Bf8-c5 4. Pe2-e4 Qf6-d4 5. Pe4-e5 Qd4-f2# 0-1",
        )

    def test_game_to_lan_2(self):
        pgn_str = "1. e4 Nc6 2. Nf3 e5 3. Bb5 a6 4. Bc4 Nd4 5. Nxe5 Qg5 6. Nxf7 Qxg2 7. Rf1 Qxe4+ 8. Be2 Nf3# 0-1"
        game = chess.pgn.read_game(self._pgn_io(pgn_str))
        lan_str = next(self.converter.game_to_xlan(game))
        self.assertEqual(
            lan_str,
            "1. Pe2-e4 Nb8-c6 2. Ng1-f3 Pe7-e5 3. Bf1-b5 Pa7-a6 4. Bb5-c4 Nc6-d4 5. Nf3xe5 Qd8-g5 6. Ne5xf7 Qg5xg2 7. Rh1-f1 Qg2xe4+ 8. Bc4-e2 Nd4-f3# 0-1",
        )

    def _pgn_io(self, pgn_str):
        # Utility method to convert a string to StringIO for reading PGN
        return StringIO(pgn_str)


if __name__ == "__main__":
    unittest.main()
