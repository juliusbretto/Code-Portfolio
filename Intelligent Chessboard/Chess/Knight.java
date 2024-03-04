package Chess;

import java.util.ArrayList;

import javax.swing.ImageIcon;

public class Knight extends ChessPiece {
	private static int[][] legalMoves= {{-2, -1},
										{-2, 1},
										{-1, 2},
										{-1, -2},
										{1, 2}, 
										{1, -2}, 
										{2, -1}, 
										{2, 1}};

	public Knight(ImageIcon icon, String color) {
		super(icon, color, "Knight");

	}

	@Override
	public ArrayList<int[]> availableMoves(int r, int c, ChessPiece[][] board) {
		ChessPiece piece = board[r][c];
		ArrayList<int[]> moves = new ArrayList<int[]>();
		
		for (int i = 0; i < legalMoves.length; i++) {
			int row = r;
			int col = c;
			row = r+legalMoves[i][0];
			col = c+legalMoves[i][1];
			if ((row >= 0 && col >= 0) && (row <= 7 && col <= 7)) {
				if (!board[row][col].getColor().equals(piece.getColor())) { //om de inte har samma färg
					moves.add(new int[]{row, col});
				}
			}
		}
		return moves;
	}

}
