package Chess;

import java.util.ArrayList;

import javax.swing.ImageIcon;

public class Rook extends ChessPiece {

	public Rook(ImageIcon icon, String color) {
		super(icon, color, "Rook");
	}

	@Override
	public ArrayList<int[]> availableMoves(int r, int c, ChessPiece[][] board) {
		ChessPiece piece = board[r][c];
		ArrayList<int[]> straightMoves = new ArrayList<int[]>();
		
		//booleans som kontrollerar om fler steg framåt ska sökas
		boolean forward = true;
		boolean backward = true;
		boolean left = true;
		boolean right = true;
		
		for (int i = 1; i < ChessGame.BOARD_SIZE; i++) {  //börjar på 1, för 0:te steget är rutan vi står på
			int forwardStep = r + i;
			int backwardStep = r - i;
			int rightStep = c + i;
			int leftStep = c - i;
			
			//varje if-sats nedan kollar om det går att flytta pjäsen X antal steg i en riktning
			//booleansen ändras till false om man stöter på en pjäs av sin egna färg eller 
			//om steget är out of bounds, dvs ej mellan 8 och -1
			if (!(forwardStep < 8 && forwardStep > -1) || board[forwardStep][c].getColor().equals(piece.getColor())) {
				forward = false;
			}
			
			if (!(backwardStep < 8 && backwardStep > -1) || board[backwardStep][c].getColor().equals(piece.getColor())) {
				backward = false;
			}
			
			if (!(leftStep < 8 && leftStep > -1) || board[r][leftStep].getColor().equals(piece.getColor())) {
				left = false;
			}
			
			if (!(rightStep < 8 && rightStep > -1) || board[r][rightStep].getColor().equals(piece.getColor())) {
				right = false;
			}
			
			if (forward) {
				int[] temp = {forwardStep, c}; //lagrar koordinaten av den ruta som är möjlig
				straightMoves.add(temp);
				if (!(board[forwardStep][c].getColor().equals("empty"))) { //om rutan inte är tom dvs att den har en pjäs av motsatt färg
					forward = false; //så lagras ej några fler steg i den riktningen
				}
			}
			
			if (backward) {
				int[] temp = {backwardStep, c};
				straightMoves.add(temp);
				if (!(board[backwardStep][c].getColor().equals("empty"))) { 
					backward = false;
				}
			}
			
			if (left) {
				int[] temp = {r, leftStep};
				straightMoves.add(temp);
				if (!(board[r][leftStep].getColor().equals("empty"))) { 
					left = false;
				}
			}
			
			if (right) {
				int[] temp = {r, rightStep};
				straightMoves.add(temp);
				if (!(board[r][rightStep].getColor().equals("empty"))) { 
					right = false;
				}
			}
			
		}
		
		return straightMoves;
	}
	
}
