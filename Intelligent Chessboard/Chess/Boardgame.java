package Chess;

import java.util.ArrayList;

import javax.swing.ImageIcon;

public interface Boardgame {
	public boolean move(int x, int y); 		//Metoden move anropas och draget utförs, vid ett genomfört drag så returneras true och vid ett drag som inte går att genomföra returnerar metoden false. Spelets ställning uppdateras då inuti klassen och kan avläsas position för position genom metoden getStatus.  
	public ChessPiece getStatus(int x, int y); 	//Anrop av getMessage ger ett aktuellt meddelande som säger om draget gick bra eller ej. 
	public String getMessage(); 			//Vid felaktigt drag ska hjälpsam information ges.
	
    ArrayList<ChessPiece> getLostPiece(ChessPiece piece);	
    ArrayList<int[]> getAvailMoves(int r, int c);
	public ImageIcon getIcon(int row, int col); //returns the ImageIcon of the specified index
}
