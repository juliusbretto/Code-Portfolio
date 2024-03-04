package Chess;

import java.util.ArrayList;

import javax.swing.ImageIcon;

public class EmptyTile extends ChessPiece {

	public EmptyTile(ImageIcon icon, String color) {
		super(icon, color, "empty");
	}

	@Override
	public ArrayList<int[]> availableMoves(int i, int j, ChessPiece[][] board) {
		return null;
	}

}
