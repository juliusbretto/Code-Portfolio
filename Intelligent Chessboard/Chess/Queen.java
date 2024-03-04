package Chess;

import java.util.ArrayList;

import javax.swing.ImageIcon;

public class Queen extends ChessPiece {

	public Queen(ImageIcon icon, String color) {
		super(icon, color, "Queen");
	}

	@Override
	public ArrayList<int[]> availableMoves(int r, int c, ChessPiece[][] board) {
		ChessPiece piece = board[r][c]; //hämtar pjäs-objektet (icon, color, name) från board
		ArrayList<int[]> qMoves = new ArrayList<int[]>();
		
		Bishop bi = new Bishop(null, piece.getColor());
		Rook ro = new Rook(null, piece.getColor());
		
		for (int[] validMove : bi.availableMoves(r, c, board)) {
			qMoves.add(validMove);
		}
		
		for (int[] validMove : ro.availableMoves(r, c, board)) {
			qMoves.add(validMove);
		}
		
		return qMoves;
	}

}
