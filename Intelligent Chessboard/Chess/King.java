package Chess;

import java.util.ArrayList;

import javax.swing.ImageIcon;

public class King extends ChessPiece {
	private int[][] legalMoves = {{1, 0}, {-1, 0}, {0, 1}, {0, -1},
								{1, 1}, {-1, 1}, {1, -1}, {-1, -1}};
	//private boolean checked = false;

	public King(ImageIcon icon, String color) {
		super(icon, color, "King");
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
				if (!board[row][col].getColor().equals(piece.getColor())) {
					moves.add(new int[]{row, col});
				}
			}
		}
		return moves;
	}

}
