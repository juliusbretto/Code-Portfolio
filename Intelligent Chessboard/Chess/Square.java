package Chess;

import java.awt.BorderLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.Icon;
import javax.swing.ImageIcon;
import javax.swing.JButton;

public class Square extends JButton {
	private int row;
    private int column;
    private boolean hasPiece;
    public String desc;

    //Konstruktor med Icon
    public Square(int row, int column, ImageIcon icon) {
        this.row = row;
        this.column = column;
        hasPiece = true;
        
        this.setIcon(icon);
	}
    
    //Konstruktor utan Icon, för "Blank pieces"
   /** public Square(int row, int column) {
    		this.row = row;
            this.column = column;
            hasPiece = false;
    }**/

    public int getRow() {
    	return row;
    }
    
    public int getColumn() {
    	return column;
    }

	public String getColor() {
		if (desc.equals("white")) {
			return "white";
		}
		return "black";
	}
	
    public boolean hasPiece() {
        return hasPiece;
    }

    public void setPiece(boolean hasPiece) {
        this.hasPiece = hasPiece;
    }
}
