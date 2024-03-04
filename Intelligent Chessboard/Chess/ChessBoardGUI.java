package Chess;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.FlowLayout;
import java.awt.Font;
import java.awt.GridLayout;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

import javax.swing.JFrame;
import javax.swing.JLabel;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTextField;

public class ChessBoardGUI extends JFrame implements ActionListener {
	private Boardgame game;
    private final int BOARD_SIZE = 8;
    private final int frameSize = 700;
    private Square[][] board;        // Square är subklass till JButton
    private JTextField message = new JTextField("White, you start!");  // JLabel/JTextField
    public static JFrame frame;
    private JPanel panel;
    private String title;

    public ChessBoardGUI (Boardgame gm) {  // OK med fler parametrar om ni vill
         this.game = gm;
         
         frame();
         grid();
         message();
         frame.setVisible(true);
    }
    
    private void frame() {
    	frame = new JFrame("CHESS");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(frameSize, frameSize);
        frame.setLocationRelativeTo(null);
        
        panel = new JPanel(new GridLayout(BOARD_SIZE, BOARD_SIZE));
        panel.setSize(frameSize, frameSize);
        frame.add(panel);
        frame.setResizable(false);
    }
    
	private void grid() {
    	board = new Square[BOARD_SIZE][BOARD_SIZE];
    	for (int row = 0; row < BOARD_SIZE; row++) {
    		for (int col = 0; col < BOARD_SIZE; col++) {
    			ChessPiece piece = game.getStatus(row, col);
        		Square sq = new Square(row, col, piece.getIcon()); 
        		
        		if ((row + col) % 2 == 0) {
        			sq.setBackground(new Color(153, 189, 165));
                } else {
                	sq.setBackground(new Color(90, 125, 102));
                }
        		
                sq.setOpaque(true);
                sq.setBorderPainted(false);
        		sq.addActionListener(this);

        		//Lägger till squaren på panel, den synliggörs
        		panel.add(sq);
        		
        		//Lägger till squaren i board-matrisen
        		board[row][col] = sq;
        	}
    	}
    }
	
    private void message() {
    	JPanel messagePanel = new JPanel();
    	messagePanel.add(message);
    	frame.add(messagePanel, BorderLayout.SOUTH);
    	message.setPreferredSize(new Dimension(500, 25));
        message.setEditable(false);
        message.setFont(new Font("Sans Serif", Font.BOLD, 14));
        message.setHorizontalAlignment(JTextField.CENTER); //texten i mitten av TextFieldet (rutan)**/
    }
    
	@Override
	public void actionPerformed(ActionEvent e) {
		Square sq = (Square) e.getSource();
		boolean validMove = game.move(sq.getRow(), sq.getColumn());
		
		if (validMove) {
			updateBoard();
			message.setText(game.getMessage());
		} else {
			message.setText(game.getMessage());
		}
	}
	
	public void updateBoard() {
		for (int r = 0; r < BOARD_SIZE; r++) {
			for (int c = 0; c < BOARD_SIZE; c++) {
				ChessPiece piece = game.getStatus(r, c); //for every square on the board
				Square sq = board[r][c]; //we retrieve the current piece and Square (GUI-component)
				sq.setIcon(piece.getIcon()); //sets the icon of the Square to the piece's icon
				
				if (piece.isHighlighted()) { //om pjäsen har highlighted-attributet = true
					sq.setBackground(Color.orange);
					sq.setVisible(true);
				}

				//om pjäsen har highlighted-attributet = false men bakgrunden fortfarande är highlighted
				if (!piece.isHighlighted() && board[r][c].getBackground().equals(Color.orange)) {
					if ((r + c) % 2 == 0) {
						sq.setBackground(new Color(153, 189, 165));
	                } else {
	                	sq.setBackground(new Color(90, 125, 102));
	                }
				}
			}
		}
	}
	
	public static void main(String[] args) {
		ChessBoardGUI cbg = new ChessBoardGUI(new ChessGame());
	}
	
}
