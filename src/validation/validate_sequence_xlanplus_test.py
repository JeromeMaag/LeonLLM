from src.validation.validate_sequence import evaluate_sequence


def test_evaluate_sequence():
    # List of test cases, each as a tuple (game_sequence, expected_error_type)
    test_cases = [
        ### INDICATOR ERROR ###
        (
            "Pd2d4- Pd7d5- Pc2c3- Pe7e5- Qd1a4+ Pc7c6- Pe2e3- Pe5d4x Pe3d4x Bc8d7- Bf1a6- Pb7a6x Qa4a6x Nb8a6x Ng1f3- Ng8f6- Ke1g1- Bd7g4- Nf3e5- Bg4f5- Rf1e1- Bf8d6- Ne5c6x",
            "indicator error",
        ),
        (
            "Pe2e4- Pe7e6- Pd2d3- Pd7d5- Bc1e3- Pd5d4- Be3d2- Pc7c5- Ng1f3- Nb8c6- Bf1e2- Bf8e7- Ph2h3- Pe6e5- Pc2c3- Ng8f6- Pc3d4x Pe5d4x Pa2a3- Ke8g8- Pe4e5- Nf6d5- Ph3h4- Nd5f4- Bd2f4x Pb7b6- Ph4h5- Bc8g4- Pe5e6- Pf7e6x Qd1c1- Bg4f3x Pg2f3x Nc6e5- Bf4e5x Be7h4- Rh1g1- Bh4g5- Be5g7x Rf8f7- Bg7f6+",
            "indicator error",
        ),
        (
            "Pd2d3- Pd7d6- Pe2e4- Pc7c5- Bf1e2- Nb8c6- Ng1f3- Pg7g6- Ke1g1- Bf8g7- Nb1c3- Ng8f6- Bc1e3- Ke8g8- Ph2h3- Pb7b6- Qd1d2- Bc8b7- Be3h6- Bg7h6x Qd2h6x Pe7e5- Nf3g5- Qd8e7- Qh6h4- Nc6d4- Ra1c1- Rf8e8- Qh4g3- Ra8c8- Pf2f4- Pe5f4x Rf1f4x Nd4e2$ Nc3e2x Pb6b5- Rc1f1- Pc5c4- Rf4f6x Qe7f6x Rf1f6x Pc4d3x Pc2d3x Rc8c2- Rf6f3- Rc2e2x Rf3f2- Re2e1+ Kg1h2- Kg8g7- Qg3f3- Re8e7- Qf3f6+ Kg7g8- Ng5f3- Re1c1- Rf2d2- Rc1c5- Qf6e7x Rc5h5+",
            "indicator error",
        ),
        (
            "Pd2d4- Pd7d6- Pd4d5- Pa7a6- Pc2c4- Pb7b5- Pc4b5x Pa6b5x Pe2e4- Bc8d7- Pa2a4- Pb5b4- Bf1b5- Bd7b5x Pa4b5x Ra8a1x Nb1d2- Ra1c1x Qd1c1x Pe7e5- Pd5c6-",
            "indicator error",
        ),
        (
            "Pe2e4- Pd7d5- Ng1f3- Pd5e4x Pd2d3- Pe4f3x Qd1f3x Ng8f6- Bf1e2- Pe7e5- Ke1g1- Bf8e7- Bc1g5- Ke8g8- Bg5f6x Be7f6x Nb1c3- Nb8c6- Be2d1- Bc8g4- Bd1e2- Bg4f3x Be2f3x Nc6d4- Nc3e4- Nd4f3$ Pg2f3x Qd8d4- Ne4f6$ Pg7f6x Kg1h1- Kg8h8- Rf1g1- Rf8g8- Rg1g8$ Ra8g8x Pc2c3- Qd4d3x Ra1e1- Qd3f3$",
            "indicator error",
        ),
        (
            "Pd2d4- Pd7d6- Qd1d3- Ke8d7- Pc2c4- Ng8f6- Ng1f3- Pe7e6- Pe2e4- Bf8e7- Pe4e5- Pd6e5x Pd4e5x",
            "indicator error",
        ),
        (
            "Pe2e3- Pe7e5- Qd1e2- Pd7d5- Qe2b5+ Bc8d7- Qb5b7x Nb8c6- Qb7b3- Ng8e7- Pd2d4- Pe5e4- Qb3b7- Pg7g6- Qb7b3- Bf8g7- Qb3c3- Ke8g8- Ng1e2- Ra8b8- Ne2f4- Pa7a5- Nf4e2- Bd7e6- Ne2f4- Be6f5- Nb1d2- Nc6b4- Qc3c5- Nb4c2$ Ke1e2- Nc2a1x Pg2g3- Bf5g4+ Pf2f3- Pe4f3$ Ke2f2- Na1c2- Ph2h3- Bg4f5- Pg3g4- Bf5e6- Nf4e6x Pf7e6$",
            "indicator error",
        ),
        (
            "Pd2d4- Pd7d6- Pg2g3- Nb8d7- Bf1h3- Pe7e6- Ng1f3- Ng8f6- Bc1g5- Bf8e7- Pc2c3- Ph7h6- Bg5f6x Be7f6x Ke1g1- Pd6d5- Nb1d2- Pe6e5- Pd4e5x Bf6e5x Nf3e5x Nd7e5x Nd2f3- Bc8h3x Nf3e5x Bh3f1x Kg1f1x Ke8g8- Qd1d5x Qd8d5x Ne5d3- Qd5d3x Pe2d3x Rf8e8- Ra1e1- Re8e1$ Kf1e1x Ra8e8+ Ke1d2- Kg8f8- Kd2c2- Pf7f6- Kc2b3- Kf8e7- Kb3b4- Ke7d6- Pa2a4- Pc7c6- Pb2b3- Re8e2- Ph2h4- Re2f2x Pa4a5- Rf2h2- Kb4a3- Rh2h3- Ka3b2- Rh3g3x Pb3b4- Rg3g2+ Kb2b3- Rg2a2- Pb4b5- Ra2a5x Pb5c6$",
            "indicator error",
        ),
        (
            "Pc2c4- Pe7e5- Qd1c2- Ng8f6- Nb1c3- Nb8c6- Pe2e3- Pd7d5- Pb2b3- Bc8g4- Bc1b2- Nc6b4- Qc2b1- Pe5e4- Ph2h3- Bg4h5- Pa2a3- Nb4d3+ Bf1d3x Pe4d3x Pg2g4- Bh5g6- Pf2f4- Qd8e7- Nc3d5x Nf6d5x Pc4d5x Ke8c8- Ng1f3- Bg6e4- Qb1c2- Ph7h5- Pg4g5+",
            "indicator error",
        ),
        (
            "Pg2g3- Pe7e6- Bf1g2- Pb7b6- Pc2c3- Pc7c6- Pa2a3- Bc8b7- Pb2b4- Qd8f6- Bc1b2- Nb8a6- Qd1b3- Ke8c8- Pc3c4- Qf6f5- Nb1c3- Na6c7- Ra1d1- Nc7e8- Pe2e3- Ne8d6- Nc3a4- Nd6c4x Qb3c4x Qf5c2- Qc4c2x Bf8e7- Bb2g7x Ng8f6- Bg7h8x Rd8h8x Na4b6$ Pa7b6x Qc2b2- Bb7a6- Ng1f3- Rh8g8- Nf3e5- Ba6b7- Ne5f7x Pc6c5- Nf7d6+ Be7d6x Qb2f6x Bd6e7- Qf6e7x Rg8d8- Qe7d6- Bb7g2x Ke1e2- Pc5b4x Pa3b4x Bg2f3+ Ke2e1- Bf3h1x Pd2d4- Bh1f3- Rd1d2- Kc8b7- Pe3e4- Ph7h5- Pe4e5- Rd8c8- Rd2c2- Rc8c2x Qd6d7$ Rc2c7- Qd7e6x Rc7c1+ Ke1d2- Rc1b1- Qe6d5+ Kb7b8- Qd5f3x Rb1b4x Qf3h5x Rb4d4$ Kd2e3- Rd4d5- Qh5h8+ Kb8c7- Qh8h7+ Kc7c6- Qh7g6+ Kc6c5- Pe5e6+",
            "indicator error",
        ),
        (
            "Ph2h3- Pe7e5- Pc2c3- Qd8h4- Pe2e3- Bf8c5- Pa2a3- Ng8e7- Pb2b4- Bc5b6- Pa3a4- Pc7c5- Pb4b5- Pa7a6- Pb5a6x Nb8a6x Pa4a5- Bb6c7- Ng1f3- Qh4f6- Qd1e2- Ke8g8- Pg2g4- Pe5e4- Nf3g1- Qf6g6- Ph3h4- Pf7f5- Pg4g5- Na6b8- Qe2c4+ Kg8h8- Ph4h5- Qg6g5x Rh1h2- Nb8c6- Ng1h3- Qg5g4- Nh3f4- Ne7d5- Nb1a3- Nd5f4x Pe3f4x Qg4f4x Pd2d3- Qf4h2x Na3b5- Bc7e5- Pa5a6- Pe4d3$",
            "indicator error",
        ),
        (
            "Pd2d4- Ng8f6- Pc2c3- Pg7g6- Pe2e4- Pd7d6- Pe4e5- Pd6e5x Pd4e5x Qd8d1$ Ke1d1x Nf6g4- Kd1e2- Nb8c6- Pf2f3- Ng4e5x Pf3f4- Ne5c4- Pb2b3- Nc4d6- Nb1d2- Pb7b6- Bc1b2- Bc8a6+ Ke2f3- Ba6b7- Bf1b5- Bf8g7- Bb5c6$ Bb7c6x",
            "indicator error",
        ),
        (
            "Pg2g3- Pe7e5- Pf2f4- Pe5e4- Pd2d3- Pe4d3x Qd1d3x Pd7d5- Nb1c3- Ng8f6- Bc1e3- Pc7c6- Pb2b4- Bf8b4x Be3d2- Pd5d4- Nc3e4- Nf6e4x Bd2b4x Ne4g3x Ra1d1- Ng3h1x Bf1g2- Nh1f2- Qd3d4x Qd8d4x Rd1d4x Nf2e4- Bg2e4x Pf7f5- Be4f5x Bc8f5x Rd4d6- Nb8d7- Ng1f3- Ke8c8- Rd6e6- Nd7b6- Re6e7- Nb6d5- Re7g7x Nd5b4x Rg7g5- Nb4c2x",
            "indicator error",
        ),
        (
            "Pe2e4- Ph7h5- Pg2g3- Pd7d5- Pe4e5- Bc8g4- Pf2f3- Bg4f5- Pd2d4- Pe7e6- Pc2c3- Nb8d7- Bf1d3- Bf5d3x Qd1d3x Pc7c5- Ng1e2- Pc5d4x Pc3d4x Bf8b4+ Bc1d2- Bb4d2$ Nb1d2x Ng8e7- Ke1g1- Ne7f5- Nd2b3- Pb7b6- Pg3g4- Ph5g4x Pf3g4x Nf5h6- Ph2h3- Qd8h4- Ne2g3- Qh4g3$ Qd3g3x Nh6f5- Qg3g2- Nf5d4x Ra1d1- Nd7c5- Rd1d4x Ke8c8- Nb3c5x Pb6c5x Rd4f4- Pa7a5- Pb2b3- Kc8c7- Pa2a4- Rd8b8- Rf1b1- Rb8b4- Rf4b4x Pc5b4x Qg2c2+ Kc7b6- Qc2f2+ Kb6a6- Qf2c5- Rh8b8- Rb1b2- Pg7g5- Rb2f2- Rb8h8- Rf2c2- Pf7f5- Pe5f6x Rh8f8- Pf6f7- Rf8f7x Qc5a5$ Ka6b7- Qa5b4x",
            "indicator error",
        ),
        (
            "Pd2d4- Pe7e6- Pe2e3- Pd7d5- Bc1d2- Pc7c5- Pc2c3- Nb8c6- Pd4c5x Bf8c5x Pb2b4- Bc5d6- Pb4b5- Nc6e5- Ng1f3- Ne5f3$ Qd1f3x Ng8f6- Bf1e2- Bc8d7- Ke1g1- Bd7b5x Be2b5$ Nf6d7- Bb5d7$ Qd8d7x Pa2a4- Ke8g8- Nb1a3- Pa7a6- Bd2c1- Qd7c7- Bc1d2- Ra8c8- Ra1c1- Qc7a5- Na3b5- Pa6b5x Pa4b5x Qa5b5x Ph2h4- Qb5b2- Pc3c4- Bd6e7- Bd2b4- Be7b4x Rc1b1- Qb2f6- Qf3f6x Pg7f6x Pc4d5x Pe6d5x Pg2g3- Rf8d8- Kg1g2- Pd5d4- Pe3d4x Rd8d4x Pf2f4- Rd4d2+ Kg2f3- Rc8c3+ Kf3g4- Rc3c8- Rf1d1- Rc8d8- Rd1d2x Rd8d2x Rb1b4x Pb7b6- Ph4h5- Kg8g7- Kg4f5- Rd2f2- Pg3g4- Rf2g2- Kf5e4- Rg2g4x Ke4f3- Rg4g3+ Kf3e4- Rg3h3- Rb4b3- Rh3h4- Rb3h3- Rh4h3x Ke4f5- Rh3h5$ Kf5g4- Rh5d5- Kg4f3- Pb6b5- Kf3e4- Pb5b4- Ke4e3- Pb4b3- Ke3f3- Pb3b2- Kf3e4- Qb2b1+ Ke4f3- Qb1b5- Kf3e4- Qb5c6+",
            "indicator error",
        ),
        ### MAX LENGTH ###
        (
            "Pc2c4- Pe7e5- Pd2d3- Ng8e7- Pg2g3- Ne7g6- Bf1g2- Pd7d6- Nb1c3- Bf8e7- Ng1f3- Ke8g8- Ke1g1- Ph7h6- Pb2b4- Be7f6- Pb4b5- Pb7b6- Pa2a4- Bc8b7- Bc1a3- Nb8d7- Nc3e4- Bb7e4x Pd3e4x Nd7c5- Nf3d2- Ra8b8- Nd2b3- Nc5e4x Bg2e4x Ng6e7- Be4c2- Pc7c6- Pb5c6x Ne7c6x Ra1b1- Nc6d4- Nb3d4x Pe5d4x Qd1d4x Bf6d4x Rb1d1- Bd4f6- Ba3c1- Qd8c7- Bc1f4- Qc7c5- Bf4d2- Rf8e8- Pa4a5- Pb6a5x Bd2a5x Rb8a8- Ba5d2- Ra8b8- Bd2c1- Rb8b4- Bc2d3- Qc5g5- Bd3e4- Re8e4x Pe2e3- Qg5g4- Rd1e1- Rb4b1- Re1d1- Rb1b2- Rd1e1- Bf6c3- Re1e2- Re4e3x Bc1e3x Rb2e2x Be3f4- Re2e4- Bf4d6x Re4e8- Bd6f4- Qg4h3-",
            "max length",
        ),
        (
            "Pd2d4- Pd7d5- Pg2g3- Pe7e6- Pf2f4- Pc7c5- Ng1f3- Nb8c6- Bf1g2- Ng8f6- Pc2c3- Bf8d6- Ke1g1- Bc8d7- Nf3e5- Qd8c7- Nb1d2- Ke8c8- Pb2b3- Ph7h6- Nd2f3- Nf6e4- Nf3d2- Ne4c3x Qd1c2- Nc3e4- Ne5c6x Bd7c6x Nd2e4x Pd5e4x Bg2e4x Bc6e4x Qc2e4x Pc5d4x Qe4d4x Bd6c5- Bc1b2- Bc5d4$ Bb2d4x Rd8d4x Pe2e3- Rd4d2- Rf1f2- Rd2f2x Kg1f2x Qc7c2+ Kf2f3- Qc2b2- Ra1g1- Qb2a2x Kf3e4- Rh8d8- Pf4f5- Qa2b3x Pg3g4- Qb3d5+ Ke4f4- Qd5d3- Ph2h4- Qd3e3$ Kf4e3x Rd8d5- Pf5e6x Pf7e6x Pg4g5- Ph6g5x Ph4g5x Rd5g5x Rg1g5x Pe6e5- Rg5e5x Pg7g6- Re5c5+ Kc8d7- Rc5d5+ Kd7c6- Rd5e5- Pa7a5- Re5e6+ Kc6b5- Re6g6x Pa5a4- Rg6g5+ Kb5b4- Ke3f4- Pa4a3- Rg5g3- Pa3a2- Rg3g1- Kb4b3- Rg1a1- Kb3b2- Ra1a2$ Kb2a2x Kf4e3- Ka2b3- Ke3d4- Kb3b4- Kd4e5- Kb4b3- Ke5f6- Kb3c2- Kf6f7- Kc2d1- Kf7f6- Kd1e1- Kf6e5- Ke1f1- Ke5d4- Kf1e1- Kd4e3- Ke1f1- Ke3f3- Kf1g1- Kf3g3- Kg1h1- Kg3h3- Pb7b5- Kh3g3- Pb5b4- Kg3h3- Pb4b3- Kh3g3- Pb3b2- Kg3h3-",
            "max length",
        ),
        (
            "Pe2e3- Pa7a6- Pg2g3- Pb7b6- Bf1g2- Nb8c6- Ng1e2- Ra8b8- Ke1g1- Bc8b7- Nb1c3- Pe7e5- Pd2d3- Bf8b4- Pe3e4- Bb4c3x Pb2c3x Ng8e7- Pd3d4- Pe5d4x Pc3d4x Ke8g8- Pc2c3- Pd7d5- Pe4e5- Ne7g6- Pf2f4- Ph7h6- Bc1a3- Rf8e8- Ba3d6- Nc6a5- Pf4f5- Ng6h8- Bd6c7x Qd8c7x Pf5f6- Nh8g6- Pe5e6- Pf7e6x Qd1d3- Na5c4- Qd3g6x Nc4e3- Qg6g7$ Qc7g7x Bf6g7x Kg8g7x Rf1f3- Ne3g2x Kg1g2x Bb7c8- Ne2f4- Re8e7- Ra1f1- Re7f7- Ph2h4- Rf7f4x Pg3f4x Kg7g6- Kg2g3- Pb6b5- Ph4h5+ Kg6h7- Rf3d3- Bc8b7- Kg3f3- Rb8g8- Kf3e3- Rg8g3+ Ke3d2- Rg3d3$ Kd2d3x Bb7c8- Kd3e3- Bc8d7- Ke3d3- Bd7e8- Kd3c2- Be8h5x Kc2b3- Bh5g6- Pa2a3- Bg6f7- Pa3a4- Bf7e8- Pa4a5- Be8d7- Pf4f5- Pe6f5x Pc3c4- Pb5c4$ Kb3c3- Ph6h5- Kc3d2- Ph5h4- Kd2e1- Ph4h3- Ke1f2- Ph3h2- Kf2g2- Bd7c8- Kg2h2x Bc8d7- Kh2g2- Bd7a4- Kg2f3- Ba4d1+ Kf3f4- Bd1h5- Kf4e5- Bh5e8- Ke5d6- Be8h5- Kd6c5- Bh5e8- Kc5b6- Be8h5- Kb6a6x Bh5e8- Ka6b7- Be8d7- Kb7a8- Kh7g6- Ka8b7-",
            "max length",
        ),
        (
            "Pb2b3- Pc7c6- Bc1b2- Pd7d5- Pe2e3- Pg7g6- Pg2g3- Bf8g7- Bf1g2- Ng8f6- Ng1e2- Ke8g8- Ke1g1- Pe7e5- Pd2d4- Pe5e4- Pc2c4- Bc8g4- Pc4d5x Bg4e2x Qd1e2x Pc6d5x Nb1d2- Pa7a6- Ra1c1- Nb8c6- Pa2a4- Pb7b5- Pa4b5x Pa6b5x Rc1a1- Ra8a1x Rf1a1x Qd8a8- Ra1a8x Rf8a8x Qe2b5x Nc6a7- Qb5b7- Ra8b8- Bb2a3- Rb8b7x Ba3d6- Rb7b3x Nd2b3x Na7b5- Bd6b4- Nb5c3- Pf2f3- Pe4f3x Bg2f3x Nf6e4- Bf3e4x Pd5e4x Nb3c5- Nc3d5- Bb4a5- Nd5e3x Nc5e4x Ne3f5- Ba5c7- Nf5e7- Bc7d6- Ne7d5- Bd6e5- Pf7f6- Be5f4- Nd5f4x Pg3f4x Kg8f7- Kg1f2- Kf7e6- Kf2f3- Ph7h6- Ph2h4- Pf6f5- Ne4c5+ Ke6d5- Nc5d7- Pg6g5-",
            "max length",
        ),
        (
            "Ng1f3- Pc7c5- Pg2g3- Nb8c6- Pc2c3- Pd7d5- Pd2d4- Pe7e5- Pd4c5x Bf8c5x Bf1g2- Ng8f6- Pb2b3- Ke8g8- Ke1g1- Pe5e4- Nf3d2- Qd8c7- Pc3c4- Bc8e6- Pc4d5x Nf6d5x Nb1c3- Ra8d8- Nd2e4x Nd5c3x Ne4c3x Rd8d1x Rf1d1x Rf8d8- Rd1d8$ Qc7d8x Bg2c6x Qd8d2- Bc6g2- Qd2c1$ Ra1c1x Bc5f2$ Kg1f2x Be6g4- Bg2f3- Bg4h3- Bf3b7x Bh3f5- Bb7f3- Pg7g6- Nc3d5- Kg8g7- Nd5f6- Bf5e6- Rc1c7- Pa7a5- Pa2a4- Be6b3x Bf3e4- Bb3e6- Rc7e7- Be6f5- Be4f5x Pg6f5x Re7a7- Ph7h6- Ra7a5x Kg7f6x Ra5f5$ Kf6e6- Rf5h5- Pf7f6- Rh5h6x Ke6e5- Rh6h5+ Ke5d4- Pa4a5- Kd4c3- Pa5a6- Kc3b2- Pa6a7- Kb2a3- Rh5h8- Ka3b3-",
            "max length",
        ),
        (
            "Pg2g3- Pe7e6- Bf1g2- Pg7g6- Pc2c4- Bf8g7- Nb1c3- Pb7b6- Pd2d4- Bc8b7- Ng1f3- Ng8f6- Qd1b3- Ke8g8- Bc1g5- Pa7a5- Ke1g1- Pa5a4- Qb3c2- Pb6b5- Pc4b5x Bb7f3x Bg2f3x Pc7c6- Pb5c6x Nb8c6x Bf3c6x Pd7c6x Bg5f6x Qd8f6x Pe2e4- Ra8b8- Pd4d5- Pc6d5x Pe4d5x Qf6f3- Qc2a4x Qf3d5x Ra1d1- Qd5a2x Qa4c6- Rb8d8- Rd1d8x Rf8d8x Qc6b7- Rd8f8- Nc3e4- Qa2d5- Qb7d5x Pe6d5x Ne4g5- Ph7h6- Ng5f3- Bg7f6- Nf3d2- Kg8g7- Nd2b3- Rf8d8- Nb3a5- Rd8a8- Na5b7- Ra8a3- Nb7d6- Ra3a2- Nd6e8+ Kg7f8- Ne8f6x Kf8e7- Nf6d5$ Ke7e6- Nd5c7+ Ke6e5- Nc7b5- Ra2b2x Kg1g2- Rb2b5x Pg3g4- Rb5b1- Ph2h4- Ke5d4-",
            "max length",
        ),
        (
            "Pg2g4- Pe7e5- Pg4g5- Qd8g5x Pd2d4- Qg5f6- Pd4e5x Qf6e5x Ng1f3- Qe5a5+ Qd1d2- Qa5d2$ Bc1d2x Pd7d6- Nb1c3- Pf7f6- Ke1c1- Bc8e6- Bf1h3- Nb8c6- Bh3e6x Nc6e5- Be6d5- Ke8c8- Bd5g8x Rh8g8x Nf3e5x Pd6e5x Pe2e4- Pg7g5- Pf2f3- Bf8h6- Nc3d5- Rd8d6- Bd2c3- Rd6b6- Pb2b4- Pc7c6- Nd5b6$ Pa7b6x Kc1b2- Rg8d8- Rd1d8$ Kc8d8x Rh1d1+ Kd8c7- Bc3e5$ Pf6e5x Rd1d2- Pb6b5- Pa2a4- Pb5a4x Pb4b5- Pc6b5x Rd2d5- Pb7b6- Rd5e5x Kc7c6- Re5f5- Pb5b4- Rf5f6+ Kc6c5- Rf6h6x Pb4b3- Pc2b3x Pa4b3x Kb2b3x Kc5b5- Rh6h7x Kb5c5- Pe4e5- Kc5d5- Rh7h6- Kd5e5x Rh6b6x Ke5f5- Rb6b8- Kf5e5- Rb8g8- Ke5f5-",
            "max length",
        ),
        (
            "Pc2c3- Pe7e6- Pe2e3- Pd7d5- Pd2d4- Pc7c5- Ng1f3- Nb8c6- Bf1b5- Bc8d7- Nf3e5- Qd8c7- Ne5d7x Qc7d7x Bb5c6x Pb7c6x Qd1a4- Bf8d6- Qa4c6x Qd7c6x Nb1d2- Ng8f6- Nd2f3- Nf6e4- Nf3e5- Bd6e5x Pd4e5x Qc6c7- Ke1g1- Ke8g8- Pf2f3- Ne4g5- Pf3f4- Ng5e4- Bc1d2- Pf7f5- Rf1f3- Ra8b8- Ra1b1- Rb8b7- Rb1d1- Pa7a5- Pa2a4- Rb7b6- Bd2e1- Pc5c4- Ph2h3- Ph7h6- Kg1h2- Pg7g5- Pg2g3- Pg5f4x Pe3f4x Qc7c5- Rf3e3- Qc5e7- Be1f2- Rb6b2x Rd1c1- Rb2f2$ Kh2g1- Rf2c2- Pg3g4- Pf5g4x Ph3g4x Rf8b8- Pf4f5- Rb8b3- Pf5f6- Qe7f7- Kg1f1- Ne4d2+ Kf1f2- Qf7g6- Kf2e1- Nd2f3+ Ke1d1- Nf3e5x Rc1c2x Qg6c2$",
            "max length",
        ),
        ### NO ERROR ###
        (
            "Pe2e4- Pa7a6- Ng1f3- Nb8c6- Bf1c4- Pe7e6- Nb1c3- Bf8c5- Pd2d3- Ng8f6- Pa2a3- Pd7d5- Bc4b3- Pd5e4x Nc3e4x Nf6e4x Pd3e4x Qd8d1$ Ke1d1x Ke8g8- Kd1e2- Pb7b5- Rh1d1- Bc8b7- Bc1e3- Bc5e7- Rd1d7- Rf8e8- Ra1d1- Ra8c8- Nf3d4- Nc6d4$ Be3d4x Bb7e4x Pf2f3- Be4c2x Rd7e7x Re8e7x Bd4g7x Bc2d1$ Ke2d1x Re7d7+ Kd1e2- Kg8g7x Pg2g4- Pc7c5- Pa3a4- Pb5a4x Bb3a4x Rd7b7- Pb2b3- Rb7b3x Ba4b3x Pc5c4- Bb3a2- Rc8b8- Ke2d2- Rb8b4- Kd2c3- Rb4b6- Ba2c4x Pa6a5- Kc3d3- Ph7h5- Pg4h5x Rb6c6- Bc4a6- Rc6a6x Kd3c4- Ra6c6+ Kc4b5- Rc6c3- Kb5a5x Rc3f3x Ph2h4- Rf3h3- Ph5h6+ Kg7h6x Ka5a6- Pf7f5- Ka6b5- Kh6h5- Kb5c5- Pf5f4- Kc5d4- Kh5h4x Kd4e4- Rh3g3- Ke4d4- Pf4f3- Kd4e5- Pf3f2- Ke5f6- Qf2f1+ Kf6e7- Rg3e3- Ke7d7- Qf1d1+ Kd7c7- Re3c3+ Kc7b6- Qd1b1+ Kb6a5- Rc3b3- Ka5a4- Rb3h3- Ka4a5- Qb1b3- Ka5a6- Qb3a4+ Ka6b7- Rh3b3+ Kb7c7- Qa4a6- Kc7d7- Rb3b7+ Kd7c8- Qa6a8# 0-1",
            "no error",
        ),
        (
            "Pe2e3- Pb7b5- Pc2c4- Pb5b4- Ng1f3- Pe7e6- Bf1e2- Ng8f6- Ke1g1- Bc8b7- Pd2d4- Pa7a5- Pa2a3- Pd7d5- Pa3b4x Pa5b4x Ra1a8x Bb7a8x Pc4d5x Ba8d5x Nb1d2- Nf6e4- Nd2e4x Bd5e4x Nf3e5- Qd8d5- Be2f3- Bf8d6- Bf3e4x Qd5e4x Ne5f7x Ke8f7x Qd1f3+ Qe4f3x Pg2f3x Nb8c6- Pe3e4- Nc6d4x Bc1e3- Nd4e2+ Kg1g2- Pc7c5- Rf1d1- Rh8d8- Rd1d5- Pe6d5x Pe4d5x Ne2f4+ Be3f4x Bd6f4x Kg2f1- Bf4h2x Kf1e2- Ph7h5- Ke2e3- Rd8d5x Ke3e4- Rd5d2- Pf3f4- Rd2b2x Ke4d5- Pb4b3- Kd5c5x Rb2f2x Kc5b5- Pb3b2- Kb5c4- Qb2b1- Kc4c5- Qb1c1+ Kc5d5- Rf2f4x Kd5d6- Qc1d1+ Kd6e5- Pg7g6- Ke5f4x",
            "no error",
        ),
        (
            "Pd2d4- Pg7g6- Pe2e4- Pd7d6- Nb1d2- Bf8g7- Ng1f3- Nb8c6- Bf1c4- Ng8f6- Ke1g1- Nf6e4x Nd2e4x Ke8g8- Pc2c3- Pe7e5- Pd4d5- Nc6e7- Bc1g5- Pc7c6- Pd5c6x Ne7c6x Qd1d5- Rf8e8- Rf1d1- Bc8e6- Qd5d6x Qd8d6x Rd1d6x Ra8d8- Ra1d1- Rd8d6x Rd1d6x Nc6e7- Bg5e7x Re8e7x Rd6d8+ Bg7f8- Nf3e5x Kg8g7- Pb2b3- Pa7a6- Ne5d7- Re7d7x Rd8f8x Kg7f8x Ph2h4- Pb7b5- Bc4e2- Rd7c7- Pa2a3- Pf7f5- Ne4g5- Be6b3x Pg2g4- Ph7h6- Ng5f3- Kf8g7- Pg4f5x Pg6f5x Nf3d4- Kg7f6- Nd4b3x Rc7c3x Nb3d2- Rc3a3x Nd2b1- Ra3a5- Be2b5x Ra5b5x Nb1a3- Rb5a5- Na3c4- Ra5c5- Nc4e3- Pa6a5- Ne3d5+ Kf6e5- Nd5e3- Rc5c3- Kg1g2- Pa5a4- Ne3c2- Pa4a3- Nc2a3x Rc3a3x Kg2f1- Pf5f4- Kf1e2- Ke5e4- Ke2d2- Ra3a2+ Kd2c1- Ke4d3- Pf2f3- Kd3e3- Kc1b1- Ra2f2- Ph4h5- Ke3f3x Kb1c1- Rf2h2- Kc1d1- Rh2h5x Kd1e1- Rh5h2- Ke1f1- Kf3g3- Kf1g1- Rh2b2- Kg1f1- Ph6h5- Kf1g1- Ph5h4- Kg1h1- Ph4h3- Kh1g1- Ph3h2+ Kg1f1- Rb2d2- Kf1e1- Rd2a2- Ke1f1- Qh2h1# 0-1",
            "no error",
        ),
        (
            "Pe2e4- Ph7h5- Pa2a4- Pd7d5- Pe4e5- Pf7f6- Pc2c3- Pg7g5- Pb2b4- Pa7a6- Nb1a3- Pb7b6- Pd2d4- Pc7c6- Pb4b5- Pc6b5x Pa4b5x Pa6a5- Pc3c4- Pd5c4x Na3c4x Pf6e5x Nc4e5x Nb8d7- Pd4d5- Bf8g7- Ne5c6- Qd8c7- Nc6a5x Nd7e5- Bc1g5x Bg7f8- Na5b3- Bc8d7- Pd5d6- Qc7c3+ Ke1e2- Qc3c4+ Qd1d3- Qc4b3x Qd3b3x Bd7e6- Qb3e6x Ne5g4- Pd6d7+ Ke8d8- Qe6b6$ Kd8d7x Qb6b7+ Kd7e6- Qb7a8x Ke6f7- Qa8d5+ Pe7e6- Qd5d7+ Kf7g6- Qd7e6$ Kg6g5x Qe6e5+ Kg5h6- Ra1a6+ Kh6h7- Qe5h5$ Ng8h6- Qh5g4x Nh6g4x Pf2f3- Ng4h2x Rh1h2$ Kh7g7- Ra6a7+ Kg7f6- Pb5b6- Bf8d6- Rh2h6+ Kf6e5- Pb6b7- Bd6b4- Ra7a8- Bb4c5- Rh6h5+ Ke5d6- Rb7b8- Rh8h5x Qb8d8+ Kd6c6- Ra8c8+ Kc6b6- Rc8c5x Kb6c5x Qd8c8+ Kc5b6- Pg2g4- Kb6a7- Pg4h5x Ka7b6- Ph5h6- Kb6a7- Ph6h7- Ka7b6- Qh7h8- Kb6a7- Qh8h7+ Ka7b6- Bf1h3- Kb6a5- Qc8b8- Ka5a4- Bh3d7+ Ka4a5- Bd7c8- Ka5a4- Qh7b7- Ka4a5- Pf3f4- Ka5a4- Pf4f5- Ka4a5- Pf5f6- Ka5a4- Pf6f7- Ka4a5- Qb8a8# 1-0",
            "no error",
        ),
        (
            "Pc2c3- Pe7e6- Pd2d3- Pf7f6- Pe2e4- Pd7d6- Pf2f3- Pb7b6- Pg2g4- Pc7c6- Ph2h4- Pa7a6- Ph4h5- Pa6a5- Pa2a4- Ra8a7- Rh1h2- Ra7e7- Rh2e2- Re7d7- Re2e3- Rd7f7- Re3e2- Rf7d7- Re2g2- Rd7e7- Rg2g3- Re7f7- Rg3g2- Rf7d7- Rg2e2- Rd7f7- Re2g2- Rf7d7- Rg2e2- Rd7f7- Re2f2- Rf7e7- Rf2e2- Re7d7- Re2e3- Rd7e7- Re3e2- Re7d7- Re2e3- Rd7e7- Re3e2- Re7d7- Re2e3-",
            "no error",
        ),
        (
            "Pe2e3- Pe7e6- Pf2f3- Pc7c5- Pc2c3- Pd7d5- Pd2d4- Bf8d6- Pd4c5x Bd6c5x Ng1e2- Ng8f6- Ne2f4- Qd8e7- Bf1b5+ Bc8d7- Bb5d7$ Nb8d7x Ke1g1- Ke8g8- Nb1d2- Pe6e5- Nf4d3- Bc5b6- Pb2b3- Ra8c8- Bc1b2- Pe5e4- Pf3e4x Pd5e4x Nd3f4- Nd7c5- Nd2c4- Nc5d3- Nc4b6x Nd3b2x Nb6c8x Rf8c8x Nf4d5- Nf6d5x Rf1f7x Nd5e3x Qd1d7- Qe7c5- Rf7g7$ Kg8f8- Rg7h7x Ne3g4+ Kg1h1- Ng4f2+ Kh1g1- Nf2h3+ Kg1h1- Nh3f2+ Kh1g1- Nf2h3+ Kg1h1- Nh3f2+ Kh1g1- Nf2g4+ Kg1h1- Ng4f2+ Kh1g1- Nf2h3+ Kg1h1- Nh3f2+ Kh1g1-",
            "no error",
        ),
        ### PATH OBSTRUCTION ###
        (
            "Pe2e4- Pg7g6- Pd2d4- Pc7c5- Pc2c3- Pc5d4x Pc3d4x Nb8c6- Ng1f3- Bf8g7- Nb1c3- Pd7d6- Bc1e3- Ng8f6- Bf1d3- Ke8g8- Ke1g1- Pe7e6- Ra1c1- Nf6g4- Ph2h3- Ng4e3x Pf2e3x Pd6d5- Pe4e5- Pf7f6- Bd3b1- Pf6f5- Qd1d2- Pa7a6- Pa2a3- Qd8e7- Nc3a4- Pb7b5- Na4c5- Bg7h6- Pg2g3- Bh6e3$ Qd2e3x Qe7c5x Qe3c5x Nc6d8- Qc5c8x Rf8c8x Rc1c8$ Kg8g7- Rc8a8x Ph7h5- Ra8a6x Pg6g5- Pg3g4- Kg7f7- Rf1c1- Ph5g4x Rc1c7+ Kf7g6- Rc7e7- Pg4f3x Re7e6$ Nd8e6x Ra6e6$ Kg6h5- Re6e8- Pf3f2+ Kg1f2x Pg5g4- Ph3g4$ Kh5g4x Re8h8- Pf5f4- Rh8g8+ Kg4f5- Bb1f5x Kf5e4- Rg8f8- Pf4f3- Pe5e6- Ke4f5x Pe6e7- Kf5e6- Be7e8- Ke6e7- Rf8f3x Ke7e8x Kf2e3- Ke8e7- Ke3f4- Ke7d8- Kf4e5- Kd8c8- Ke5d6- Kc8b8- Kd6c6- Kb8a8- Kc6b6- Ka8b8- Kb6a6- Kb8a8- Rf3f7- Ka8b8- Ka6b6- Kb8a8- Pa3a4- Ka8b8- Pa4b5x Kb8a8- Pb2b4- Ka8b8- Pd5d6- Kb8a8- Rf7c7- Ka8b8- Pd6d7- Kb8a8- Pd4d5- Ka8b8- Pd5d6- Kb8a8- Pd6d7- Ka8b8- Qd7d8# 1-0",
            "path obstruction",
        ),
        (
            "Pe2e3- Pd7d5- Pc2c4- Nb8c6- Qd1c2- Pd5d4- Pe3d4x Nc6d4x Qc2d1- Pe7e5- Nb1c3- Pc7c6- Pd2d3- Pf7f5- Bc1e3- Pe5e4- Pd3e4x Pf5e4x Be3d4x Bc8f5- Bd4e3- Ng8f6- Qd1d8$ Ra8d8x Pg2g3- Bf8b4- Pa2a3- Bb4c3$ Pb2c3x Bf5g4- Bf1g2- Ke8g8- Ke1f1- Ph7h6- Bg2e4x Nf6e4x Kf1g2- Ne4c3x Ra1c1- Nc3e4- Rc1a1- Pa7a6- Ph2h3- Bg4h5- Pg3g4- Bh5g6- Ra1d1- Rd8d1x Rh1d1x",
            "path obstruction",
        ),
        (
            "Pe2e4- Pa7a6- Nb1c3- Pb7b5- Bf1d3- Bc8b7- Nc3e2- Ng8f6- Ne2g3- Pe7e6- Pf2f3- Bf8e7- Ng1e2- Ke8g8- Ke1g1- Pc7c5- Pc2c3- Nb8c6- Bd3c2- Pd7d5- Pd2d4- Pc5d4x Pc3d4x Pd5e4x Pf3e4x Be7b4- Pd4d5- Pe6d5x Pe4d5x Nf6d5x Ne2c3- Nd5c3x Pb2c3x Bb4c3x Ra1b1- Nc6d4- Bc1e3- Bb7e4- Ng3e4x Nd4c2x Qd1c2x Bc3d4- Be3d4x Qd8d4$ Kg1h1- Rf8e8- Ne4g3- Qd4g4- Qc2e4- Qg4h5- Rf1e1- Re8e4x Re1e4x Ra8d8- Re4e1- Rd8d2- Ng3h5x Pg7g6- Nh5f6+ Kg8g7- Nf6g4- Ph7h5- Ng4e3- Pa6a5- Ph2h3- Pa5a4- Pa2a3- Pf7f5- Ne3d5- Pg6g5- Pg2g3- Pg5g4- Ph3g4x Pf5g4x Nd5f4- Kg7f6- Re1f1- Pg4g3x",
            "path obstruction",
        ),
        (
            "Pc2c4- Pe7e5- Pg2g3- Bf8c5- Nb1c3- Qd8f6- Pe2e3- Nb8c6- Pa2a3- Pa7a6- Pb2b4- Bc5a7- Bf1g2- Ng8e7- Bc1b2- Pd7d6- Nc3e4- Qf6g6- Ra1c1- Bc8f5- Pd2d3- Ke8c8- Ne4c3- Pd6d5- Pc4d5x Ne7d5x Bg2d5x Rd8d5x Nc3d5x Qg6d6- Nd5c3- Rh8d8- Ng1e2- Pg7g6- Ke1g1- Ph7h5- Qd1c2- Ph5h4- Nc3e4- Qd6e6- Rc1c6x",
            "path obstruction",
        ),
        (
            "Pd2d4- Pe7e5- Pd4d5- Pd7d6- Pf2f3- Pc7c6- Pe2e4- Pc6d5x Pe4d5x Bf8e7- Pc2c4- Ng8f6- Nb1c3- Ke8g8- Bf1d3- Pa7a6- Qd1e2- Pb7b5- Pb2b3- Pb5b4- Nc3e4- Nf6e4x Bd3e4x Pf7f5- Be4d3- Pe5e4- Pf3e4x Pf5e4x Bd3e4x Be7h4+ Ke1d2- Qd8g5+ Kd2c2- Bh4f6-",
            "path obstruction",
        ),
        (
            "Ng1h3- Pe7e5- Pe2e3- Pf7f6- Bf1c4- Pd7d5- Bc4d3- Pe5e4- Bd3b5+ Pc7c6- Bb5e2- Bc8h3x Pg2h3x Ng8h6- Qd1g1-",
            "path obstruction",
        ),
        (
            "Pd2d4- Pf7f6- Pc2c4- Pe7e6- Pd4d5- Pe6d5x Pc4d5x Pc7c6- Nb1c3- Pc6d5x Nc3d5x Nb8c6- Pe2e3- Ng8e7- Nd5e7x Bf8e7x Bf1b5- Nc6e5- Bb5d7$ Bc8d7x Pf2f4- Ne5c6- Ng1f3- Ke8g8- Ke1g1- Bd7g4- Qd1d8x Ra8d8x Ph2h3- Bg4h5- Pg2g4- Bh5f7- Kg1f2- Bf7d5- Pe3e4- Bd5e4x Rf1e1- Be4f3x Kf2f3x Nc6d4+ Kf3e4- Nd4c2- Re1d1- Nc2a1x Pg4g5- Pf6g5x Pf4g5x Rf8e8- Bc1f4- Na1c2- Rd1d8x Re8d8x Bf4c7- Rd8e8- Ke4d5- Re8d8+ Kd5c4- Be7g5x Ph3h4- Bg5h4x Kc4b5- Rd8d2- Pb2b4- Rd2a2x",
            "path obstruction",
        ),
        (
            "Pd2d4- Ph7h5- Pe2e3- Pg7g6- Ng1f3- Ng8f6- Pg2g3- Nf6e4- Bf1g2- Pd7d6- Ke1g1- Pc7c6- Nb1d2- Ne4f6- Nd2c4- Nf6h7- Pc2c3- Pf7f5- Nf3h4- Pe7e6- Nh4f3- Ph5h4- Nf3h4x Rh8h4x",
            "path obstruction",
        ),
        (
            "Pe2e4- Pc7c5- Pe4e5- Pd7d6- Pf2f3- Pd6e5x Pf3f4- Pe5f4x Pg2g3- Pf4g3x Ph2g3x Nb8c6- Pd2d3- Ng8f6- Pc2c3- Pe7e6- Pb2b3- Bf8e7- Pa2a3- Ke8g8- Ra1a2- Ph7h6- Ra2g2- Pe6e5- Rg2e2- Nf6h7- Re2g2- Pf7f5- Rg2d2- Pe5e4- Pd3e4x Pf5e4x Pg3g4- Bc8g4x Qd1g4x Qd8d2$ Nb1d2x Rf8f4- Qg4g2- Ra8f8- Bf1c4+ Kg8h8- Qg2g3- Rf4f6- Qg3g2- Be7d6- Nd2e4x Rf6f4- Bc1f4x Rf8f4x Ne4d6x Rf4c4x Pb3c4x Nc6d8- Nd6b7x Nd8b7x Rh1h3- Nb7a5- Rh3d3- Na5c4x Rd3d8+ Kh8h7-",
            "path obstruction",
        ),
        (
            "Pc2c3- Pd7d5- Pe2e4- Pd5d4- Qd1a4+ Bc8d7- Qa4d4x Ng8f6- Pe4e5- Nf6h5- Qd4h4- Nh5f6- Pe5f6x Pe7f6x Bf1c4- Bf8e7- Qh4h5- Pg7g6- Qh5f3- Nb8c6- Nb1a3- Nc6e5- Qf3f4- Ne5c4x Na3c4x Bd7e6- Nc4e3- Be6d7- Ne3d5- Bd7e6- Nd5e7x Qd8e7x Ke1g1-",
            "path obstruction",
        ),
        ### PIECE LOGIC ###
        (
            "Pe2e4- Pc7c5- Pb2b3- Nb8c6- Pd2d4- Pc5d4x Bc1b2- Pe7e5- Bf1c4- Pd7d6- Ng1f3- Bc8g4- Nb1d2- Pa7a6- Pa2a4- Pb7b5- Pa4b5x Pa6b5x Ra1a8x Qd8a8x Bc4b5x Qa8a5- Bb5c6$ Qa5c6x",
            "piece logic",
        ),
        (
            "Pe2e4- Nb8c6- Bf1c4- Nc6a5- Bc4f7$ Ke8f7x Qd1h5+ Pg7g6- Qh5a5x Pb7b6- Qa5d5+ Pe7e6- Qd5a8x Qd8g5- Ng1f3- Qg5g2x Rh1g1- Qg2f2$ Ke1d1- Qf2f3$ Kd1e1- Qf3e4$ Ke1d1- Ng8f6- Qa8c8x Qe4d5- Pc2c3- Qd5f3+ Kd1c2- Nf6e4- Qc8c7x Qf3f6- Qc7d7$ Ne4e7-",
            "piece logic",
        ),
        (
            "Nb1c3- Pe7e5- Pf2f4- Pe5e4- Pd2d3- Pe4e3- Bc1e3x Qd8e7- Qd1d2- Pd7d6- Ke1c1- Bc8e6- Ng1f3- Pc7c6- Pg2g3- Nb8d7- Bf1g2- Ph7h6- Rh1e1- Pg7g5- Kc1b1- Bf8g7- Pf4g5x Ph6g5x Be3g5x Pf7f6- Bg5f4- Ke8c8- Nf3d4- Nd7e5- Nd4e6x Qe7e6x Bf4e5x Qe6e5x Pd3d4- Qe5e7- Pd4d5- Pc6c5- Pe2e4- Ng8h6- Re1h1- Qe7e5- Rh1f1- Nh6g4- Rf1f5- Ng4h2x Rf5e5x Pf6e5x Nc3b5- Rd8d7- Qd2a5- Pa7a6- Qa5b6- Rh8d8- Qb6c7+ Kc8a8-",
            "piece logic",
        ),
        (
            "Pc2c3- Pb7b6- Pd2d4- Bc8b7- Pf2f3- Pg7g6- Pe2e4- Bf8g7- Bf1d3- Pd7d6- Ng1e2- Nb8d7- Ke1g1- Pe7e6- Bc1e3- Ng8e7- Qd1d2- Ph7h6- Be3h6x Bg7h6x Qd2h6x Rh8h6x Nb1d2- Pa7a6- Nd2c4- Pb6b5- Nc4e3- Pc7c5- Ne3g4- Rh6h8- Ng4h6- Pc5c4- Bd3c2- Ne7g8- Nh6g8x Rh8g8x Pe4e5- Pd6e5x Pd4e5x Qd8c7- Ra1d1- Nd7e5x Bc2e4- Bb7e4x Pf3e4x Qc7c5+ Kg1h1- Ne5g4- Rd1d2- Rg8h8- Ph2h3- Ng4e3- Rf1f3- Rh8h3$ Kh1g1- Rh3f3x Ne2d4- Rf3f1+ Kg1h2- Qc5e5+ Rd2f4-",
            "piece logic",
        ),
        (
            "Pc2c3- Pc7c5- Pd2d3- Pg7g6- Nb1d2- Bf8g7- Ph2h3- Ng8f6- Pg2g4- Ke8g8- Bf1g2- Pd7d5- Nd2f1- Pe7e5- Nf1g3- Nb8c6- Pg4g5- Nf6e8- Ph3h4- Ne8c7- Ph4h5- Pe5e4- Ph5g6x Pf7g6x Bg2h3- Pe4d3x Qd1d3x Bc8h3x Rh1h3x Pd5d4- Pc3c4- Qd8e8- Rh3h4- Nc7e6- Ng3e4- Nc6e5- Qd3h3- Pb7e4x",
            "piece logic",
        ),
        (
            "Pe2e4- Pe7e5- Ng1f3- Bf8c5- Pd2d3- Pd7d6- Nb1c3- Nb8c6- Pa2a3- Ng8f6- Pb2b4- Bc5b6- Ph2h3- Ke8g8- Nc3d5- Nf6d5x Pe4d5x Nc6d4- Nf3d4x Pe5d4x Bf1e2- Rf8e8- Qd1d2- Qd8f6- Ke1g1- Pc7c6- Pd5c6x Pb7c6x Be2f3- Pc6c5- Pc2c3- Bc8b7- Pc3d4x Bb7f3x Pg2f3x Qf6d4x Qd2c3- Qd4c3x Bc1b2- Qc3d3x Rf1d1- Qd3f3x Rd1d6x Bb6c7- Rd6d5- Qf3d5x Bb2g7x Qd5g5+ Kg1f1- Qg5g7x Ra1d1- Qg7c3- Rd1d5- Qc3a3x Rd5c5x Qa3b4x Rc5h5- Pf7f6- Kf1g2- Qb4g4+ Ph3g4x Bc7e5- Pf2f4- Be5f4x Rh5c5- Bf4e5- Rc5e3-",
            "piece logic",
        ),
        (
            "Pe2e4- Pf7f6- Pd2d4- Pd7d6- Pc2c4- Pe7e5- Pd4d5- Ng8e7- Pf2f4- Pb7b6- Pf4e5x Pd6e5x Ng1f3- Bc8b7- Bf1d3- Nb8d7- Nb1c3- Nd7c5- Bd3c2- Pg7g6- Pb2b4- Nc5d7- Pa2a3- Ph7h5- Ph2h4- Bf8g7- Bc1e3- Ke8g8- Qd1e2- Nd7b8- Ke1c1- Nb8a6- Pc4c5- Na6b8- Pc5c6- Bb7c8- Kc1b2- Bc8g4- Rd1d3- Pa7a5- Rh1d1- Pa5b4x Pa3b4x Nb8a6- Be3c5- Pb6c5x Pb4c5x Na6c5x Rd3d2- Ra8b8+ Kb2a2- Nc5a6- Rd1b1- Na6b4+ Ka2a3- Nb4c2$ Rd2c2x Rb8b1x Rc2b2- Rb1b2x Qe2b2x Qd8d6+ Pc6c5-",
            "piece logic",
        ),
        (
            "Pb2b4- Pe7e5- Nb1c3- Pd7d6- Ng1f3- Pf7f6- Pd2d4- Ng8e7- Pd4e5x Pf6e5x Pe2e4- Ne7g6- Pg2g3- Bf8e7- Bf1g2- Ke8g8- Ke1g1- Pc7c6- Pa2a4- Bc8e6- Ph2h3- Pd6d5- Pe4d5x Pc6d5x Nc3b5- Pa7a6- Nb5c3- Pe5e4- Nf3d4- Be7b4x Nc3a2- Qd8d7- Pc2c3- Bb4d6- Na2b4- Pa6a5- Nb4d5x Be6d5x Bg2e4x Bd5e4x Rf1e1- Be4d5- Bc1e3- Nb8c6- Nd4f5- Rf8f5x Be3c5- Bd6c5x Pc3c4- Bd5c4x Ra1c1- Bc5f2$ Kg1h1- Bc4d5+ Kh1h2- Bd5f7- Rc1c5- Rf5c5x Re1e2- Bf2g3$ Re2g3x",
            "piece logic",
        ),
        (
            "Pd2d3- Pd7d5- Pe2e4- Pb7b6- Ng1f3- Bc8b7- Nb1d2- Pd5e4x Pd3e4x Qd8d6- Pg2g3- Nb8c6- Bf1g2- Ke8c8- Ke1g1- Pe7e5- Pc2c3- Pf7f6- Qd1e2- Ng8e7- Pb2b4- Ph7h6- Pb4b5- Nc6a5- Bc1a3- Qd6d7- Ba3e7x Bf8e7x Ra1d1- Rh8f8- Nf3h4- Rd8e8- Bg2h3- Pf6f5- Pe4f5x Na5c4- Nd2c4x Bb7h1- Rd1d7x Kc8d7x Qe2d3+ Kd7c8- Qd3d7+ Kc8b7- Qd7c6+ Kb7b8- Qc6c7$ Kb8a8- Qc7c6+ Be7b7-",
            "piece logic",
        ),
        (
            "Pd2d4- Pe7e6- Pc2c3- Pg7g6- Pe2e4- Pd7d6- Bf1d3- Ng8e7- Ng1f3- Bf8g7- Ke1g1- Ke8g8- Pe4e5- Pd6e5x Pd4e5x Nb8c6- Rf1e1- Nc6e5x Nf3e5x Bg7e5x Bd3c2- Qd8d1x Re1d1x Bc8d7- Bc1h6- Rf8e8- Bc2e4- Be5g7- Bh6g7x Kg8g7x Be4b7x Ra8b8- Bb7a6- Rb8b2x Pa2a4- Rb2c2- Ba6b5- Rc2c3x Nb1c3x Re8a8- Ra1c1- Ra8b8- Bb5d7x Rb8b2- Rc1c2- Rb2c2x Rd1d2- Rc2c3x Rd2c3x",
            "piece logic",
        ),
        (
            "Pg2g3- Pf7f6- Bf1g2- Pf6f5- Pc2c3- Ng8f6- Qd1b3- Nb8c6- Ng1f3- Pe7e5- Pd2d3- Pe5e4- Pd3e4x Pf5e4x Nf3g1- Pd7d5- Pc3c4- Bc8e6- Pc4d5x Be6d5x Qb3b7x Bd5c4- Qb7c6$ Bc4d7-",
            "piece logic",
        ),
        ### PSEUDOLEGAL ###
        (
            "Pb2b3- Pe7e5- Bc1b2- Pe5e4- Ng1f3- Pe4f3x Pg2f3x Ng8f6- Pf3f4- Pd7d5- Pe2e3- Nb8c6- Bf1b5- Bf8c5- Bb5c6$ Pb7c6x Nb1c3- Bc8g4- Qd1c1- Bg4f3- Rh1g1- Ke8g8- Pd2d3- Rf8e8- Ke1d2- Pd5d4- Pe3d4x Bc5d4x Rg1g3- Bf3h5- Nc3e4- Nf6e4$ Pd3e4x Bd4b2$ Qc1b2x Qd8f6- Qb2f6x Pg7f6x Ra1e1- Ra8d8+ Kd2c1- Bh5g6- Pf4f5- Bg6h5- Rg3g1- Re8e7- Kc1b2- Re7d7- Pe4e5- Pf6e5x Re1e5x Rd7d2- Rg1g7+ Kg8g7x Re5e7+ Kg7f8- Re7c7x Rd8e8- Rc7c6x Re8e2- Rc6c8+ Kf8g7- Rc8c7- Re2f2x Rc7a7x Rf2h2x Ra7f7$ Kg7f7x Pa2a4- Ph7h6- Pa4a5- Rd2c2$ Kb2a3- Rc2a2+ Ka3b4- Ra2b2- Pa5a6- Rb2b3$ Kb4b3x Rh2h3+ Kb3b4- Bh5e2- Pa6a7- Be2b5- Kb4b5x Rh3a3- Kb5b6- Ra3a7x Kb6a7x Ph6h5- Ka7b6- Ph5h4- Kb6c5- Ph4h3- Kc5d4- Ph3h2- Kd4e3- Qh2h1- Ke3f4- Qh1h4+ Kf4e5- Kf7e7- Pf5f6+ Ke7f7- Ke5f5- Qh4f4+ Kf5f4x Kf7f6x Kf4g3- Kf6g5- Kg3h3- Kg5h4- Kh3h2- Kh4g4- Kh2h1- Kg4g3- Kh1g1- Pf6f5- Kg1h1- Pf5f4- Kh1g1- Pf4f3- Kg1h1- Pf3f2- Kh1h2-",
            "pseudolegal",
        ),
        (
            "Pe2e3- Pe7e5- Pf2f4- Pe5f4x Pb2b3- Pf4e3x Bc1b2- Pf7f6- Bf1d3- Bf8c5- Ng1f3- Pe3d2$ Nb1d2x Nb8c6- Ke1g1-",
            "pseudolegal",
        ),
        (
            "Pe2e4- Pe7e6- Qd1h5- Pg7g6- Qh5h3- Pd7d6- Ng1f3- Bf8g7- Bf1c4- Ng8f6- Pd2d3- Nb8c6- Nf3g5- Nc6e5- Bc4b3- Bc8d7- Bc1f4- Bd7c6- Ke1g1- Ph7h6- Ng5f3- Ne5f3$ Pg2f3x Nf6h5- Bf4e3- Bg7b2x Nb1d2- Bb2a1x Rf1a1x Nh5f4- Be3f4x Pe6e5- Bf4e3- Qd8d7- Nd2c4- Ke8c8- Nc4a5- Bc6b5- Bb3f7x Qd7f7x",
            "pseudolegal",
        ),
        (
            "Pe2e4- Pc7c6- Pg2g4- Pd7d5- Pe4e5- Bc8g4x Pf2f3- Bg4h5- Pd2d4- Pe7e6- Pc2c3- Bf8e7- Pf3f4- Ng8h6- Ph2h3- Nh6f5- Bf1d3- Nf5g3- Rh1h2- Ng3e4- Bc1e3- Be7h4+ Be3f2- Bh4f2$ Rh2f2x Pc6c5- Bd3e4x Pd5e4x Qd1g4- Qd8h4- Qg4h4x Nb8c6- Qh4h5x Pg7g6- Qh5e2- Pc5d4x Pc3d4x Nc6d4x Qe2e4x Nd4f5- Nb1c3- Ra8d8- Nc3b5- Ke8g8- Nb5c7- Rd8d7- Nc7e6x Pf7e6x Qe4c4- Rf8d8- Ra1d1- Nf5e3- Qc4e6$ Kg8g7- Rf2e2- Ne3d1x Ke1d1x",
            "pseudolegal",
        ),
        (
            "Pe2e4- Pc7c5- Pg2g3- Pb7b6- Bf1g2- Bc8b7- Ng1f3- Pe7e6- Pd2d3- Pd7d5- Pe4d5x Bb7d5x Ke1g1- Nb8d7- Nb1c3- Bd5f3x Bg2f3x Ng8f6- Bf3a8x Qd8a8x Nc3b5- Bf8e7- Bc1f4- Ke8g8- Nb5c7- Qa8c6- Nc7b5- Pe6e5- Bf4c1- Nf6d5- Rf1e1- Pf7f5- Pf2f4- Pe5e4- Pd3e4x Pf5e4x Qd1e2- Qc6b5x Qe2b5x Bd5c4-",
            "pseudolegal",
        ),
        (
            "Pc2c4- Pc7c5- Ng1f3- Pd7d6- Pg2g3- Ng8f6- Bf1g2- Nb8c6- Ke1g1- Pg7g6- Nb1c3- Bf8g7- Pa2a3- Ke8g8- Ra1b1- Pa7a6- Pb2b4- Pc5b4x Pa3b4x Pe7e5- Pb4b5- Pa6b5x Pc4b5x Nc6e7- Bc1b2- Bc8e6- Nf3g5- Be6c4- Bg2b7x Ra8b8- Bb7c6- Rb8b6- Bc6g2- Qd8c7- Pd2d3- Rb6b5x Nc3b5x Qc7b8- Nb5c3- Qb8b3- Qd1c2- Qb3c2x Rb1c1- Qc2b2x Nc3b5- Nf6e8- Nb5c7- Ne8c7x Rc1c4x Nc7e6- Rc4a4- Qb2b3- Ra4a7- Ne6g5x Ra7e7x Ng5e6- Re7e6x Pf7e6x Pe2e4- Ne6d4-",
            "pseudolegal",
        ),
        (
            "Pd2d4- Pd7d5- Pb2b3- Bc8f5- Ng1h3- Pe7e6- Pg2g3- Bf8b4+ Pc2c3- Bb4a5- Nh3f4- Pc7c6- Bf1g2- Ng8e7- Nb1a3- Pg7g5- Nf4h5- Ph7h6- Pb3b4- Ba5b6- Na3c2- Nb8d7- Nc2e3- Qd8c7- Ke1g1- Ke8c8- Pa2a4- Pa7a6- Pa4a5- Bb6a7- Bc1d2- Pe6e5- Pd4e5x Qc7e5x Ra1c1- Nd7f6- Ne3f5x Ne7f5x Pe2e4- Pd5e4x Qd1c2- Pg5g4- Qc2d1- Nf5e7- Bd2e3- Rd8d1x Rf1d1x Qe5h5x Rd1d2- Qh5h2$ Kg1f1- Qh2h1+ Bg2h1x Ph6h5- Rd2d4- Ne7d5- Be3g5- Nf6h7- Pf2f4- Nh7g5x Pf4g5x Ba7d4x Pc3d4x Rh8e8- Rc1d1- Nd5c3- Rd1c1- Nc3d5- Kf1g2- Pe4e3- Kg2f1- Nd5b4x Rc1b1- Nb4d3- Rb1b3- Re8e6- Rb3d3x Ne3d5-",
            "pseudolegal",
        ),
        (
            "Pe2e4- Pe7e5- Pb2b3- Nb8c6- Pc2c4- Ng8f6- Bc1b2- Bf8c5- Nb1c3- Pd7d6- Ng1f3- Bc8g4- Bf1e2- Ke8g8- Ke1g1- Bc5b4- Ph2h3- Bg4f3x Be2f3x Nc6d4- Bf3e2- Pc7c5- Pa2a3- Bb4a5- Pb3b4- Pc5b4x Pa3b4x Ba5b4x Nc3d5- Nf6d5x Pe4d5x Qd8g5- Be2g4- Ph7h5- Pf2f4- Pe5f4x Bb2d4x Ph5g4x Rf1f4x Pg4h3x Qd1f3- Ph3h2+ Kg1h1- Pf7f5- Rf4h4- Qg5g6- Qf3h3- Rf8f6- Ra1d1- Ra8f8- Rd1f1- Pf5f4- Bd4f6x Rf8f6x Rh4f4x Rf6f4x Qh3e6+ Qg6e6x Pd5e6x Rf4f1$ Kh1h2x Rf1f6- Pe6e7- Rf6e6- Pd2d4- Re6e7x Pd4d5- Re7e8- Kh2h3- Re8e5- Kh3g4- Kg8f7- Kg4f4- Kf7f6- Pg2g4- Re5e1- Pg4g5+ Kf6g6- Kf4g4- Re1g1+ Kg4h3- Pa7a5- Pc4c5- Pd6c5x Kh3h2- Rg1g5x Kh2h3- Pa5a4- Kh3h2- Pb4b3-",
            "pseudolegal",
        ),
        (
            "Pe2e4- Pc7c5- Bf1e2- Nb8c6- Nb1c3- Pe7e6- Ng1f3- Pa7a6- Ke1g1- Pb7b6- Pd2d4- Pc5d4x Nf3d4x Nc6d4x Qd1d4x Ng8f6- Rf1d1- Bf8c5- Qd4d3- Pb6b5- Bc1g5- Ke8g8- Pe4e5- Ph7h6- Bg5f6x Pg7f6x Qd3g3+ Kg8h7- Rd1d3- Pf6e5x Ra1d1- Qd8f6- Rd3f3- Qf6g6- Qg3e5x Ra8b8- Qe5c5x Bc8b7- Qc5d4- Bb7f3x Be2f3x Pd7d5- Pa2a3- Rf8d8- Qd4f6- Qg6f6x Rd1d4- Qf6g6- Rf3h3-",
            "pseudolegal",
        ),
        (
            "Pe2e4- Pc7c6- Pf2f4- Pd7d5- Qd1e2- Pd5e4x Qe2e4x Ng8f6- Qe4e2- Bc8g4- Ng1f3- Pe7e6- Ph2h3- Bg4f3x Qe2f3x Bf8e7- Pd2d3- Nb8d7- Nb1c3- Ke8g8- Bc1d2- Ph7h6- Ke1c1- Qd8a5- Kc1b1- Rf8d8- Qf3f2- Nd7c5- Bf1e2- Kg8h8- Pg2g4- Rd8d4- Pg4g5- Ph6g5x Pf4g5x Nf6d5- Nc3d5x Pc6d5x Ph3h4- Ra8c8- Ph4h5- Pc5c4-",
            "pseudolegal",
        ),
        (
            "Pc2c3- Pd7d5- Pd2d4- Ph7h6- Bc1e3- Pc7c5- Pg2g3- Bc8f5- Nb1a3- Pe7e6- Ng1f3- Nb8c6- Bf1g2- Ng8f6- Ke1g1- Nf6e4- Nf3d2- Ne4d2x Qd1d2x Bf5e4- Pf2f3- Be4g6- Pf3f4- Bf8e7- Bg2f3- Qd8c7- Pf4f5- Pe6f5x Be3f4- Qc7d7- Pe2e4- Pd5e4x Bf3e2- Be7f6- Pd4c5x Ke8c8- Qd2e3- Pg6g5-",
            "pseudolegal",
        ),
        ### SYNTAX ###
        (
            "Pd2d4- Ng8f6- Pe2e3- Pg7g6- Pg2g4- Bf8g7- Pg4g5- Nf6d5- Bf1c4- Nd5b6- Bc4b3- Pd7d5- Pa2a4- Pa7a5- Nb1c3- Ke8g8- Ph2h4- Bc8f5- Bb3a2- Bf5e4h1x",
            "syntax",
        ),
        (
            "Pb2b3- Pf7f6- Bc1b2- Pd7d6- Pf2f3- Nb8c6- Pe2e4- Pe7e5- Ng1e2- Pg7g5- Pc2c3- Ph7h5- Pd2d4- Bc8e6- Pd4d5- Be6d5x Pe4d5x Nc6e7- Pc3c4- Ne7f5- Qd1d2- Nf5e3- Qd2e3x Bf8h6- Qe3e4- Pg5g4- Qe4g6+ Ke8d7- Ne2g3- Pf6f5- Ng3f5x Qd8f6- Qg6f6x Ng8f6x Bb2c1- Pg4f3x Pg2f3x Nf6d5x Pc4d5x Rh8g8- Bf1h3- Rg8g7- Nf5h6$ Kd7e7- Nh6f5+ Ke7f6- Nf5g7x Kf6g7x K Ph5x Ra8h8- Kh6h8x Pc7c5- Pd5c6x Pb7c6x Pb3b4- Pd6d5- Pb4b5- Pc6b5x Bc1a3- Pa7a5- Nb1c3- Pb5b4- Ba3b4x Pa5b4x Nc3d5x Pb4b3- Pa2b3x Pe5e4- Pf3e4x Kg7g6- Rh1g1+ Kg6h5x Nd5f4+ Kh5h4- Nf4g2+ Kh4h3x Ra1a8- Kh3h2x Rg1g8- Kh2g2x Pe4e5- Kg2f3- Pe5e6- Kf3f4- Pe6e7- Kf4f5- Qe7e8- Kf5f6- Qe8f8+ Kf6e5- Ra8e8+ Ke5d4- Qf8f2+ Kd4c3- Qf2e3+ Kc3c2- Re8c8+ Kc2d1- Rc8c3- Kd1e1- Rg8e8- Ke1d1- Qe3e2+ Kd1c1- Re8e3- Kc1b1- Re3d3- Kb1a1- Qe2d1+ Ka1b2- Ng2e3- Kb2a3- Pb3b4- Ka3b4x Rd3d5- Kb4c4- Rd5a5- Kc4b4- Ra5c5- Kb4a4- Rc5c8- Ka4b4- Rc8b8+ Kb4c3x Rb8c8+",
            "syntax",
        ),
        (
            "Pe2e3- Pc7c5- Pb2b3- Pg7g6- Pf2f4- Bf8g7a1",
            "syntax",
        ),
        (
            "Pd2d4- Pd7d5- Pf2f3- Pg7g6- Ph2h4- Bf8g7- Pe2e3- Ng8f6- Pc2c3- Bc8f5- Pg2g4- Bf5d7- Ph4h5- Nf6h5x Pg4h5x Pg6h5x Rh1h5x Bd7e6 Ng1e2- Qd8c8- Pf3f4- Ph7h6- Ne2g3- Pc7c6- Qd1f3- Bd7g4- Qf3g4x Qc8g4x Bf1e2- Qg4g3$ Ke1d2- Qg3g1- Nb1a3- Qg1g2- Pb2b3- Nb8d7- Bc1b2- Nd7f6- Ra1h1- Nf6e4+ Kd2c1- Ne4g3- Rh1h4- Ng3e2$ Ng3e2x Qg2e2x Rh5e5- Qe2e3$ Kc1c2- Qe3f4x Rh4f4x Bg7e5x Pd4e5x Ke8c8- Bb2c1- Ph6h5- Bc1e3- Ph5h4- Rf4h4x Pf7f6- Rh4h8x Rd8h8x Pe5f6x Rh8h2+ Kc2d3- Rh2a2x Be3c5- Ra2a3x Pc3c4- Pd5c4$ Kd3c4x Ra3b3x Kc4b3x Kc8c7- Kb3c4- Kc7d7- Kc4d4- Kd7e6- Bc5a7x Ke6f6x Kd4e4- Pe7e5- Ke4f3- Kf6f5- Kf3f2- Kf5f4- Kf2e2- Pe5e4- Ke2f2- Pc6c5- Kf2e2- Pc5c4- Ke2d2- Kf4f3- Kd2c2- Kf3e3- Kc2b2- Ke3d4- Kb2a3- Kd4c3- Ka3a4- Pe4e3- Ka4a3- Pe3e2- Ka3a4- Pb7b6- Ka4a3- Qe2e1- Ka3a4- Pb6b5+ Ka4a3- Qe1a1+ Ka3b4- Pc4c3- Kb4b5x Pc3c2- Kb5b4- Qc2c1- Kb4b3- Qa1b2+ Kb3a4- Qc1a1# 0-1",
            "syntax",
        ),
    ]

    passes = 0
    fails = 0

    for i, (game_sequence, expected_error_type) in enumerate(test_cases):
        result = evaluate_sequence(
            game_sequences=[game_sequence],
            token_sequences=[game_sequence],
            notation="xLANplus",
            debug=False,
        )

        # Extract the actual error type from the result
        actual_error_type = result[0][2] if result else None

        # Check if the actual error type matches the expected error type
        if actual_error_type == expected_error_type:
            passes += 1
        else:
            print(
                f"Test case {i+1}: Expected: {expected_error_type}, Got: {actual_error_type}"
            )
            fails += 1

    print(
        f"Test Results: {passes} passed, {fails} failed => {passes/(passes+fails)*100:.2f}%"
    )


# Run the test function
test_evaluate_sequence()
