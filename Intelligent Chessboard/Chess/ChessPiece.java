package Chess;

import java.util.ArrayList;

import javax.swing.ImageIcon;

public abstract class ChessPiece {
	private ImageIcon icon;
    private String color;
    private boolean highlighted = false;
    private String name = "piece";

    public ChessPiece(ImageIcon icon, String color, String name){
        this.icon = icon;
        this.color = color;
        this.name = name;
    }
    
    public abstract ArrayList<int[]> availableMoves(int i, int j, ChessPiece[][] board); //returnerar alla "möjliga" drag för en pjäs unika position
    
    
    public void changeHighlightStatus(){
        if (highlighted){
            highlighted = false;
        } else {
            highlighted = true;
        }
    }

    public boolean isHighlighted(){
        return highlighted;
    }
    
    public String getColor() {
    	return color;
    }
    
    public ImageIcon getIcon(){
        return icon;
    }
    
    public String getName() {
    	return name;
    }
    
	
}
