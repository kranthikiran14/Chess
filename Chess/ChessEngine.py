class GameState:

    def __init__(self):
        self.board = [['bR', 'bN', 'bB', 'bQ', 'bK', 'bB', 'bN', 'bR'],
                      ['bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp', 'bp'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['--', '--', '--', '--', '--', '--', '--', '--'],
                      ['wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp', 'wp'],
                      ['wR', 'wN', 'wB', 'wQ', 'wK', 'wB', 'wN', 'wR']]

        self.moveFunctions = {'p': self.getPawnMoves, 'R': self.getRookMoves, 'K': self.getKingMoves,
                              'Q': self.getQueenMoves, 'N': self.getKnightMoves, 'B': self.getBishopMoves}
        self.whiteToMove = True
        self.moveLog = []

    def makeMove(self, move):
        """
        Takes a move as a parameter and executes it (this will not work for castling, pawn promotion, and en-passant)
        :param move:
        :return:
        """
        self.board[move.startRow][move.startCol] = "--"
        self.board[move.endRow][move.endCol] = move.pieceMoved
        self.moveLog.append(move)  # log the move so we can undo it later
        self.whiteToMove = not self.whiteToMove  # swap players

    def undoMove(self):
        if len(self.moveLog) != 0:
            move = self.moveLog.pop()
            self.board[move.startRow][move.startCol] = move.pieceMoved
            self.board[move.endRow][move.endCol] = move.pieceCaptured
            self.whiteToMove = not self.whiteToMove

    def getValidMoves(self):
        """
        All moves considering checks
        :return:
        """
        return self.getAllPossibleMoves()

    def getAllPossibleMoves(self):
        """
        All moves without considering checks
        :return:
        """
        moves = []
        for r in range(len(self.board)):
            for c in range(len(self.board[r])):
                turn = self.board[r][c][0]
                if (turn == 'w' and self.whiteToMove) or (turn == 'b' and not self.whiteToMove):
                    piece = self.board[r][c][1]
                    self.moveFunctions[piece](r, c, moves)
        return moves

    def getPawnMoves(self, r, c, moves):
        """
        Get all the pawn moves for the pawn located at row, col and add these moves to the list
        :param r:
        :param c:
        :param moves:
        :return:
        """
        if self.whiteToMove:  # white pawn moves
            if self.board[r - 1][c] == '--':  # 1 square pawn advance
                moves.append(Move((r, c), (r - 1, c), self.board))
                if r == 6 and self.board[r - 2][c] == "--":  # 2 square pawn advance
                    moves.append(Move((r, c), (r - 2, c), self.board))
            if c - 1 >= 0:  # captures to the left
                if self.board[r - 1][c - 1][0] == 'b':  # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c - 1), self.board))
            if c + 1 < 7:  # captures to the right
                if self.board[r - 1][c + 1][0] == 'b':  # enemy piece to capture
                    moves.append(Move((r, c), (r - 1, c + 1), self.board))

        else:  # black pawn moves
            if self.board[r + 1][c] == '--':  # 1 square pawn advance
                moves.append(Move((r, c), (r + 1, c), self.board))
                if r == 1 and self.board[r + 2][c] == "--":  # 2 square pawn advance
                    moves.append(Move((r, c), (r + 2, c), self.board))
            if c - 1 >= 0:  # captures to the left
                if self.board[r + 1][c - 1][0] == 'w':  # enemy piece to capture
                    moves.append(Move((r, c), (r + 1, c - 1), self.board))
            if c + 1 < 7:  # captures to the right
                if self.board[r + 1][c + 1][0] == 'w':  # enemy piece to capture
                    moves.append(Move((r, c), (r + 1, c + 1), self.board))

    def getRookMoves(self, r, c, moves):
        """
        Get all the Rook moves for the pawn located at row, col and add these moves to the list
        :param r:
        :param c:
        :param moves:
        :return:
        """
        directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        enemy = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                row = r + d[0] * i
                col = c + d[1] * i
                if 0 <= row < 8 and 0 <= col < 8:
                    if self.board[row][col] == "--":
                        moves.append(Move((r, c), (row, col), self.board))
                    elif self.board[row][col][0] == enemy:
                        moves.append(Move((r, c), (row, col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKnightMoves(self, r, c, moves):
        """
                Get all the Knight moves for the pawn located at row, col and add these moves to the list
                :param r:
                :param c:
                :param moves:
                :return:
        """
        directions = [(-2, -1), (-2, 1), (2, -1), (2, 1), (1, -2), (1, 2), (-1, -2), (-1, 2)]
        notEnemy = "w" if self.whiteToMove else "b"
        for d in directions:
            row = r + d[0]
            col = c + d[1]
            if 0 <= row < 8 and 0 <= col < 8:
                if self.board[row][col] != notEnemy:
                    moves.append(Move((r, c), (row, col), self.board))

    def getBishopMoves(self, r, c, moves):
        """
                Get all the Bishop moves for the pawn located at row, col and add these moves to the list
                :param r:
                :param c:
                :param moves:
                :return:
        """
        directions = [(1, 1), (-1, 1), (1, -1), (-1, -1)]
        enemy = "b" if self.whiteToMove else "w"
        for d in directions:
            for i in range(1, 8):
                row = r + d[0] * i
                col = c + d[1] * i
                if 0 <= row < 8 and 0 <= col < 8:
                    if self.board[row][col] == "--":
                        moves.append(Move((r, c), (row, col), self.board))
                    elif self.board[row][col][0] == enemy:
                        moves.append(Move((r, c), (row, col), self.board))
                        break
                    else:
                        break
                else:
                    break

    def getKingMoves(self, r, c, moves):
        """
                Get all the King moves for the pawn located at row, col and add these moves to the list
                :param r:
                :param c:
                :param moves:
                :return:
        """
        directions = [(-1, -1), (-1, 0), (-1, 1), (0, 1), (1, 1), (1, 0), (1, -1), (0, -1)]
        notEnemy = "w" if self.whiteToMove else "b"
        for d in directions:
            row = r + d[0]
            col = c + d[1]
            if 0 <= row < 8 and 0 <= col < 8:
                if self.board[row][col] != notEnemy:
                    moves.append(Move((r, c), (row, col), self.board))

    def getQueenMoves(self, r, c, moves):
        """
                Get all the Queen moves for the pawn located at row, col and add these moves to the list
                :param r:
                :param c:
                :param moves:
                :return:
        """
        self.getBishopMoves(r, c, moves)
        self.getRookMoves(r, c, moves)


class Move:
    # maps keys to values
    # key : value
    ranksToRows = {"1": 7, "2": 6, "3": 5, "4": 4,
                   "5": 3, "6": 2, "7": 1, "8": 0}
    rowsToRanks = {v: k for k, v in ranksToRows.items()}
    filesToCols = {"a": 0, "b": 1, "c": 2, "d": 3,
                   "e": 4, "f": 5, "g": 6, "h": 7}
    colsToFiles = {v: k for k, v in filesToCols.items()}

    def __init__(self, startSq, endSq, board):
        self.startRow = startSq[0]
        self.startCol = startSq[1]
        self.endRow = endSq[0]
        self.endCol = endSq[1]
        self.pieceMoved = board[self.startRow][self.startCol]
        self.pieceCaptured = board[self.endRow][self.endCol]
        self.moveID = self.startRow * 1000 + self.startCol * 100 + self.endRow * 10 + self.endCol

    def __eq__(self, other):
        """
        Overriding the equals method
        :param other:
        :return:
        """
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        return self.getRankFile(self.startRow, self.startCol) + self.getRankFile(self.endRow, self.endCol)

    def getRankFile(self, r, c):
        return self.colsToFiles[c] + self.rowsToRanks[r]
