
package Chess;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.GridLayout;
import java.util.ArrayList;

import javax.swing.Icon;
import javax.swing.ImageIcon;
import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;

public class ChessGame implements Boardgame {
	public final static int BOARD_SIZE = 8;
	public static boolean turn = true; //true betyder vit, false betyder svart
	private boolean pickedUp = false;
	private String message = "No message yet.";
	private ChessPiece[][] board = new ChessPiece[BOARD_SIZE][BOARD_SIZE];
	private int[] pickedUpCoord = new int[2];
	
	private ImageIcon[] icons = {new ImageIcon("BlackRook.png"),
								new ImageIcon("BlackKnight.png"), 
								new ImageIcon("BlackBishop.png"),
								new ImageIcon("BlackQueen.png"),
								new ImageIcon("BlackKing.png"),
								new ImageIcon("BlackBishop.png"),
								new ImageIcon("BlackKnight.png"),
								new ImageIcon("BlackRook.png"),
								new ImageIcon("BlackPawn.png"),
								new ImageIcon("WhiteRook.png"),
								new ImageIcon("WhiteKnight.png"), 
								new ImageIcon("WhiteBishop.png"),
								new ImageIcon("WhiteQueen.png"),
								new ImageIcon("WhiteKing.png"),
								new ImageIcon("WhiteBishop.png"),
								new ImageIcon("WhiteKnight.png"),
								new ImageIcon("WhiteRook.png"),
								new ImageIcon("WhitePawn.png"),
								};
	
	public ChessGame() {
		initializeBoard();
	}
	
	public void initializeBoard() {
		for (int r = 0; r < BOARD_SIZE; r++) {
			
			if (r == 0) { //Första raden, svarta innersta raden
				for (int c = 0; c < BOARD_SIZE; c++) {
					if (c == 0 || c == 7) {
						board[r][c] = new Rook(icons[c], "black"); //ROOK
					} else if (c == 2 || c == 5) {
						board[r][c] = new Bishop(icons[c], "black"); //BISHOP
					} else if (c == 1 || c == 6) {
						board[r][c] = new Knight(icons[c], "black"); //KNIGHT
					} else if (c == 3) {
						board[r][c] = new Queen(icons[c], "black"); //QUEEN
					} else if (c == 4) {
						board[r][c] = new King(icons[c], "black"); //KING
					}
					
				}
			} else if (r==1) { //Andra raden, svarta bönder
				for (int c = 0; c < BOARD_SIZE; c++) {
					board[r][c] = new Pawn(icons[8], "black");
				}
				
			} else if (r==6) { //Sjätte raden, vita bönder
				for (int c = 0; c < BOARD_SIZE; c++) {
					board[r][c] = new Pawn(icons[17], "white");
				}
				
			} else if (r==7) { //Sista raden, vita innersta raden
				for (int c = 0; c < BOARD_SIZE; c++) {
					if (c == 0 || c == 7) {
						board[r][c] = new Rook(icons[c+9], "white"); //ROOK
					} else if (c == 2 || c == 5) {
						board[r][c] = new Bishop(icons[c+9], "white"); //BISHOP
					} else if (c == 1 || c == 6) {
						board[r][c] = new Knight(icons[c+9], "white"); //KNIGHT
					} else if (c == 3) {
						board[r][c] = new Queen(icons[c+9], "white"); //QUEEN
					} else if (c == 4) {
						board[r][c] = new King(icons[c+9], "white"); //KING
					}
				}
				
			} else { //Om r är >1 och <7 ska det vara "tomma rutor"
				for (int c = 0; c < BOARD_SIZE; c++) {
					board[r][c] = new EmptyTile(null, "empty");
				}
			}
		}
	}
	
	@Override
	public ImageIcon getIcon(int row, int col) {
		return null;
	}

	@Override
	public boolean move(int r, int c) {
		if (!pickedUp) { //om en pjäs inte är upplockad
			if (turn && board[r][c].getColor().equals("black")) { //turn=true är vit, turn=false är black
				message = "Not your turn, black. White, pick a white piece to move!";
				return false;
			} else if (!turn && board[r][c].getColor().equals("white")) {
				message = "Not your turn, white. Black, pick a black piece to move!";
				return false;
			}

			ArrayList<int[]> moves = getAvailMoves(r, c);
			boolean pickUpValid = highlight(moves);
			
			if (moves.size() == 1) {
				pickedUp = false;
				turn = !turn;
				return autoMove(r, c);
				
			} else if (!pickUpValid) {
				message = "That piece has no available moves. Pick another one!";
				return false;
				
			} else {
				pickedUp = true;
				message = "No message yet.";
				return true;
			}

		} else { //om en pjäs är upplockad och ska placeras
			boolean putDownMove = makeMove(r, c);
			if (!putDownMove) { //om man väljer en ruta som ej är highlighted
				message = "That move is not available. Pick one of the highlighted squares!";
				
			} else { //lyckas sätta ner pjäsen
				pickedUp = false;
				turn = !turn;
				message = "No message yet.";
				
				//Om det är bondens första drag
				if (board[r][c].getName().equals("Pawn")) {
					Pawn pawn = (Pawn) board[r][c];
					if (pawn.isPawnsFirstMove()) {
						pawn.firstMoveDone();
					}
					
					//Promovering av bonde --> drottning
					if (pawn.getColor().equals("white") && r == 0) {
						board[r][c] = new Queen(icons[12], "white");
					} else if (pawn.getColor().equals("black") && r == 7) {
						board[r][c] = new Queen(icons[3], "black");
					}
				}
				
				//tar bort alla highlightade rutor efter nedsatt pjäs
				for (int row = 0; row < BOARD_SIZE; row++) {
					for (int col = 0; col < BOARD_SIZE; col++) {
						if (board[row][col].isHighlighted()) {
							board[row][col].changeHighlightStatus();
						}
					}
				}
			}
			isChecked();
			return true;
		}
	}

	@Override
	public ChessPiece getStatus(int x, int y) { //returnerar the current status of en ruta, ex Queen eller empty
		return board[x][y];
	}

	@Override
	public String getMessage() {
		return message;
	}

	//sparar alla utslagna pjäser
	@Override
	public ArrayList<ChessPiece> getLostPiece(ChessPiece piece) {
		ArrayList<ChessPiece> lostPieces = new ArrayList<ChessPiece>();
		if (piece.getColor().equals("empty")) {
			return lostPieces;
		}

		lostPieces.add(piece);
		return lostPieces;
	}
	
	@Override
	public ArrayList<int[]> getAvailMoves(int r, int c) { 
		ChessPiece picked = this.getStatus(r, c);
		pickedUpCoord[0] = r; //den upplockade pjäsens koordinaten lagras
		pickedUpCoord[1] = c;
		ArrayList<int[]> movesPickedUp = picked.availableMoves(r, c, board); //och sen körs den pjästypens availableMoves-metod
		
		return movesPickedUp; //returnerar de möjliga (valid) dragen för upplockad pjäs
	}
	
	private boolean highlight(ArrayList<int[]> moves) {
		if (moves == null || moves.size() == 0) {
			return false;
		} else {
			for (int[] move : moves) { 
				board[move[0]][move[1]].changeHighlightStatus();
			}
			return true;
		}
	}
	
	//Automatisk move när en pjäs endast har 1 möjligt drag
	private boolean autoMove(int r, int c) {
		ChessPiece clickedPiece = board[r][c];
		ArrayList<int[]> onlyMove = getAvailMoves(r, c);
		if (onlyMove.size() == 1) {
			int[] coordinates = onlyMove.get(0);
			if (board[coordinates[0]][coordinates[1]].isHighlighted()) {
				int newRow = coordinates[0];
				int newCol = coordinates[1];
				board[r][c] = new EmptyTile(null, "empty");
				getLostPiece(board[newRow][newCol]);
				board[newRow][newCol] = clickedPiece;
				JOptionPane.showMessageDialog(ChessBoardGUI.frame, "Only one move available, click OK to confirm.");
				return true;
			}
		}
		return false;
	}
	
	private boolean makeMove(int r, int c) { //om rutan som klickas är highlighted så returneras true
		ChessPiece squareToMoveTo = board[r][c];
		if (squareToMoveTo.isHighlighted()) {  //om rutan är highlighted
			int row = pickedUpCoord[0];
			int col = pickedUpCoord[1];
			
			ChessPiece piece = board[row][col]; //lagrar pjäsen som plockats upp
			board[row][col] = new EmptyTile(null, "empty"); //ändrar dess originalplats till empty
			getLostPiece(board[r][c]); //innan uppdatering av ny ruta, lagras fd pjäs (om den ej är empty)
			board[r][c] = piece; //uppdaterar den nya platsen med en ny pjäs, så om det står en pjäs där blir den överskriven och är ute ur spelet
			return true;
		}
		return false;
	}

	//Kolla om en av kungarna är checked
	private void isChecked() {
		for (int r = 0; r < BOARD_SIZE; r++) {
			for (int c = 0; c < BOARD_SIZE; c++) {
				ChessPiece piece = board[r][c];
				
				if (!piece.getName().equals("empty")) {
						ArrayList<int[]> searchKing = piece.availableMoves(r, c, board);
					for (int[] coord : searchKing) {
						int row = coord[0];
						int col = coord[1];
						if (board[row][col] != null && board[row][col].getName().equals("King") && !piece.getColor().equals(board[row][col].getColor())) {
							message = "Your king is checked, " + board[row][col].getColor() + "!";
						}
					}
				}
				
			}
		}
	}

	
	
}