package Chess;

import java.util.ArrayList;

import javax.swing.ImageIcon;

public class Bishop extends ChessPiece {

	public Bishop(ImageIcon icon, String color) {
		super(icon, color, "Bishop");
		// TODO Auto-generated constructor stub
	}

	@Override
	public ArrayList<int[]> availableMoves(int r, int c, ChessPiece[][] board) {
		ChessPiece piece = board[r][c];
		ArrayList<int[]> diagonalMoves = new ArrayList<int[]>();
		
		//booleans som kontrollerar om fler steg framåt ska sökas
		boolean northWest = true;
		boolean southWest = true;
		boolean northEast = true;
		boolean southEast = true;
		
		for (int i = 1; i < ChessGame.BOARD_SIZE; i++) {  //börjar på 1, för 0:te steget är rutan vi står på
			int forwardStep = r + i;
			int backwardStep = r - i;
			int rightStep = c + i;
			int leftStep = c - i;
			
			//varje if-sats nedan kollar om det går att flytta pjäsen X antal steg i en riktning
			//booleansen ändras till false om man stöter på en pjäs av sin egna färg  
			//ELLER om steget är out of bounds, dvs ej mellan 8 och -1
			if (!isWithinBoard(backwardStep, leftStep) || board[backwardStep][leftStep].getColor().equals(piece.getColor())) {
				northWest = false;
			}
			
			if (!isWithinBoard(forwardStep, leftStep) || board[forwardStep][leftStep].getColor().equals(piece.getColor())) {
				southWest = false;
			}
			
			if (!isWithinBoard(backwardStep, rightStep) || board[backwardStep][rightStep].getColor().equals(piece.getColor())) {
				northEast = false;
			}
			
			if (!isWithinBoard(forwardStep, rightStep) || board[forwardStep][rightStep].getColor().equals(piece.getColor())) {
				southEast = false;
			}
			
			if (northWest) {
				int[] temp = {backwardStep, leftStep}; //lagrar koordinaten av den ruta som är möjlig
				diagonalMoves.add(temp);
				if (!(board[backwardStep][leftStep].getColor().equals("empty"))) { //om rutan inte är tom dvs att den har en pjäs av motsatt färg
					northWest = false; //så lagras ej några fler steg i den riktningen
				}
			}
			
			if (southWest) {
				int[] temp = {forwardStep, leftStep};
				diagonalMoves.add(temp);
				if (!(board[forwardStep][leftStep].getColor().equals("empty"))) { 
					southWest = false;
				}
			}
			
			if (northEast) {
				int[] temp = {backwardStep, rightStep};
				diagonalMoves.add(temp);
				if (!(board[backwardStep][rightStep].getColor().equals("empty"))) { 
					northEast = false;
				}
			}
			
			if (southEast) {
				int[] temp = {forwardStep, rightStep};
				diagonalMoves.add(temp);
				if (!(board[forwardStep][rightStep].getColor().equals("empty"))) { 
					southEast = false;
				}
			}
		}
		
		return diagonalMoves;
	}
	
	private boolean isWithinBoard(int row, int col) {
		return row < ChessGame.BOARD_SIZE && row >= 0 && col < ChessGame.BOARD_SIZE && col >= 0;
	}

}
