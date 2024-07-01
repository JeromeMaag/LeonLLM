import chess
import streamlit as st
import chess.engine


class MyChess:
    def __init__(self, width, fen, player_side="white"):
        self.width = width
        self.fen = fen
        self.player_side = player_side

    def __header__(self):
        return """
        <link rel="stylesheet"
            href="https://unpkg.com/@chrisoakman/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.css"
            integrity="sha384-q94+BZtLrkL1/ohfjR8c6L+A6qzNH9R2hBLwyoAfu3i/WCvQjzL2RQJ3uNHDISdU"
            crossorigin="anonymous">
        <script src="https://code.jquery.com/jquery-1.12.4.min.js"></script>
        <script src="https://unpkg.com/@chrisoakman/chessboardjs@1.0.0/dist/chessboard-1.0.0.min.js"
            integrity="sha384-8Vi8VHwn3vjQ9eUHUxex3JSN/NFqUg3QbPyX8kWyb93+8AC/pPWTzj+nHtbC5bxD"
            crossorigin="anonymous"></script>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/chess.js/0.10.2/chess.js"
            integrity="sha384-s3XgLpvmHyscVpijnseAmye819Ee3yaGa8NxstkJVyA6nuDFjt59u1QvuEl/mecz"
            crossorigin="anonymous"></script>
        """

    def __sidetomove__(self):
        return "white" if chess.Board(self.fen).turn else "black"

    def __board_placeholder__(self):
        return f"""
        <div id="myBoard" style="width: {self.width}px"></div><br>
        <label><strong>Status:</strong></label>
        <div id="status"></div>
        """

    def game_board(self):
        sidetomove = self.__sidetomove__()

        engine_move = f"""
      function makeComputerMoveFromAPI(retryWithStockfish = false) {{
          var currentFen = game.fen();
          var history = game.pgn();
          var playerModel = retryWithStockfish ? 'stockfish' : '{st.session_state.selected_model}';
          
          fetch('http://localhost:8000/get_move', {{
              method: 'POST',
              headers: {{
                  'Content-Type': 'application/json'
              }},
              body: JSON.stringify({{fen: currentFen, history: history, model: playerModel}})
          }})
          .then(response => response.json())
          .then(data => {{
              var move = game.move(data.move, {{sloppy: true}});
              if (move === null) {{
                  if (!retryWithStockfish) {{
                      console.log('Invalid move received, trying Stockfish...');
                      makeComputerMoveFromAPI(true);
                  }} else {{
                      alert('Invalid move received from Stockfish.');
                  }}
                  return;
              }}
              board.position(game.fen());  // Update the board position
              updateStatus();  // Update status after the engine move
          }})
          .catch(error => console.error('Error fetching move from API:', error));
      }}
      """

        script1 = f"""
      // NOTE: this example uses the chess.js library:
      // https://github.com/jhlywa/chess.js

      var board = null
      var game = new Chess('{self.fen}')
      var $status = $('#status')
      var $fen = $('#fen')
      var $pgn = $('#pgn')
      """

        game_over_ = """
      // do not pick up pieces if the game is over
      if (game.game_over()) return false
      if ((game.turn() === 'w' && piece.search(/^b/) !== -1) ||
          (game.turn() === 'b' && piece.search(/^w/) !== -1)) return false
      """

        script2 = f"""
      function onDragStart (source, piece, position, orientation) {{{game_over_}}}
      """

        script3 = """
      function onDrop(source, target) {
        // See if the move is legal
        var move = game.move({
          from: source,
          to: target,
          promotion: 'q' // NOTE: always promote to a queen for example simplicity
        })

        // illegal move
        if (move === null) return 'snapback'

        updateStatus()  // Update game status immediately after the move

        // Check if the game is over after the move
        if (game.game_over()) {
          // Optionally send game status to Streamlit
          if (window.parent) {
            window.parent.stBridges.send("my-bridge", {'move': move, 'fen': game.fen(), 'pgn': game.pgn(), 'status': 'Game Over'});
          }
          else {
            window.stBridges.send("my-bridge", {'move': move, 'fen': game.fen(), 'pgn': game.pgn(), 'status': 'Game Over'});
          }
          return;  // Exit the function if the game is over
        }

        // Make computer move if the game is still ongoing
        makeComputerMoveFromAPI()
      }
      """

        script4 = """
      // update the board position after the piece snap
      // for castling, en passant, pawn promotion
      function onSnapEnd () {
        board.position(game.fen())
      }

      function updateStatus () {
        var status = ''

        var moveColor = 'White'
        if (game.turn() === 'b') {
          moveColor = 'Black'
        }

        if (game.in_checkmate()) {
          status = 'Game over, ' + moveColor + ' is in checkmate.'
        }

        // draw?
        else if (game.in_draw()) {
          status = 'Game over, drawn position'
        }

        // game still on
        else {
          status = moveColor + ' to move'

          // check?
          if (game.in_check()) {
            status += ', ' + moveColor + ' is in check'
          }
        }
        $status.html(status)
      }
      """

        config_ = f"""
      pieceTheme: 'https://chessboardjs.com/img/chesspieces/wikipedia/{{piece}}.png',
      position: '{self.fen}',
      orientation: '{st.session_state.side_choice}',
      draggable: true,
      onDragStart: onDragStart,
      onDrop: onDrop,
      onSnapEnd: onSnapEnd
      """

        script5 = f"""
      var config = {{{config_}}}
      board = Chessboard('myBoard', config)

      updateStatus()

      if ('{self.player_side}' === 'black') {{
          makeComputerMoveFromAPI();
      }}
      """

        ret = []

        ret.append(self.__header__())
        ret.append(self.__board_placeholder__())
        ret.append("<script>")
        ret.append(engine_move)

        ret.append(script1)
        ret.append(script2)
        ret.append(script3)
        ret.append(script4)
        ret.append(script5)
        ret.append("</script>")

        return "\n".join(ret)
