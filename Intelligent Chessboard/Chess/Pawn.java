package Chess;

import java.util.ArrayList;

import javax.swing.ImageIcon;

public class Pawn extends ChessPiece {
	private ImageIcon icon;
	private boolean firstMove;
	private ArrayList<int[]> validMoves;
	private int[][] legalMoves = new int[4][2]; //bönder kan endast röra sig i 4 olika koordinat-kombinationer
	private String color;
	
	public Pawn(ImageIcon icon, String color) {
		super(icon, color, "Pawn");
		this.firstMove = true;
		this.color = color;
		
		if (color.equals("white")) { //VITA PJÄSER
			legalMoves[0] = new int[]{-2,0}; //two squares forward, row decreased by two
			legalMoves[1] = new int[]{-1,0}; //one square forward, row decreased by one
			legalMoves[2] = new int[]{-1,-1}; //diagonally left, both row and column is decreased by one
			legalMoves[3] = new int[]{-1,1}; //diagonally right, row is decreased by one and column is added by one
		} else { //SVARTA PJÄSER
			legalMoves[0] = new int[]{2,0}; //two squares forward, row increased by two
			legalMoves[1] = new int[]{1,0}; //one square forward, row increased by one
			legalMoves[2] = new int[]{1,1}; //diagonally right, both row and column is increased by one
			legalMoves[3] = new int[]{1,-1};  //diagonally left, row increased and column decreased
		}
		
	}

	public void firstMoveDone() {
		firstMove = false;
	}
	
	public boolean isPawnsFirstMove() {
		return firstMove;
	}
	
	@Override
	public ArrayList<int[]> availableMoves(int r, int c, ChessPiece[][] board) {
		validMoves = new ArrayList<int[]>();
		int[][] moves = allMoves(r, c);
		
		if (firstMove) {
			int row2step = moves[0][0]; //första (0:te) raden i moves är 2-stegs draget
			int col2step = moves[0][1];
			int row1step = moves[1][0];
			int col1step = moves[1][1];
			
			if ((row1step >= 0 && col1step >= 0) && (row1step <= 7 && col1step <= 7)) { //om 1 steg fram är inom brädet
				if (board[row1step][col1step].getColor().equals("empty")) { //om första steget fram är en tom ruta
					validMoves.add(new int[]{row1step, col1step}); //lägg till som validMove
				
					//if-sats för row2step?
					if (board[row2step][col2step].getColor().equals("empty")) { //OBS båda rutor måste vara empty för att 2 step ska vara valid, bönder kan ej hoppa
						validMoves.add(new int[]{row2step, col2step});
					}
				}
			}
			
		checkDiagonal(moves, board); //de diagonala läggs till om valid
		
		} else { //om inte first move
			int row1step = moves[0][0];
			int col1step = moves[0][1];
			if ((row1step >= 0 && col1step >= 0) && (row1step <= 7 && col1step <= 7)) {
				if (board[row1step][col1step].getColor().contentEquals("empty")) {
					validMoves.add(new int[] {row1step, col1step});
			}
		}
		
		checkDiagonal(moves, board);
		}
		return validMoves;
	}
	
	public int[][] allMoves(int r, int c) {
		int[][] moves;
		if (firstMove) {
			moves = new int[4][2]; //4x2 matris, håller 4 koordinatpar
			for(int i = 0; i < 4; i++) { //för alla possible moves för en bonde
				int row = r + legalMoves[i][0];  //raden bonden står på just nu + i:te legalMoves-radens row-element
				int col = c + legalMoves[i][1]; 
				moves[i] = new int[]{row, col}; //lägger till möjliga "nya positioner" i moves
			}
		} else {
			moves = new int[3][2]; //två-stegs öppningen ej möjlig
			for (int i = 1; i < 4; i++) {
				int row = r + legalMoves[i][0];  
				int col = c + legalMoves[i][1]; 
				moves[i-1] = new int[]{row, col};
			}
		}
		return moves;
	}
	
	//Unik för Pawn-klassen
	private void checkDiagonal(int[][] moves, ChessPiece[][] board) {
		String opponentColor;
		if (color.equals("white")) {
			opponentColor = "black";
		} else {
			opponentColor = "white";
		}
		
		int counter = 1;
		if (firstMove) { //om det är första draget har moves längd 4, annars 3
			counter = 2; //så därför skippar vi de två första
		}				//annars skippar vi bara första (one straight forward)
		
		for (int i = counter; i < moves.length; i++) {
			int row = moves[i][0]; //kollar the moves row-koordinat ligger inom brädet
			int col = moves[i][1]; //samma för col
			if ((row >= 0 && col >= 0) && (row <= 7 && col <= 7)) { 
				if (board[row][col].getColor().equals(opponentColor)) { //om pjäsen på den potentiella positionen är av den andra färgen
					validMoves.add(new int[]{row, col}); //lägger vi till draget som "valid"
				}
			}
		}
	}
	
}
