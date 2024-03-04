package sudoku;

import java.awt.BorderLayout;
import java.awt.Color;
import java.awt.Container;
import java.awt.Dimension;
import java.awt.Font;
import java.awt.GridLayout;

import javax.swing.JButton;
import javax.swing.JFrame;
import javax.swing.JOptionPane;
import javax.swing.JPanel;
import javax.swing.JTextField;
import javax.swing.border.EmptyBorder;

public class SudokuView {
	SudokuSolver s;
	JFrame frame;
	Container pane;
	JTextField[][] textField;
	private static final Color color = new Color(0, 111, 122);
	
	public SudokuView() {
		s = new Sudoku();
		frame = new JFrame("Sudoku Solver");
		pane = frame.getContentPane();
		textField = new JTextField[Sudoku.size][Sudoku.size];
		GUI();
	}
	
	private void GUI() {
		frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
		addButtons();
		addBoard();
		frame.pack();
		frame.setResizable(false);
		frame.setVisible(true);
		
	}

	private void addBoard() {
		JPanel panel1 = new JPanel();
		panel1.setPreferredSize(new Dimension(600, 600));
		panel1.setLayout(new GridLayout(Sudoku.size, Sudoku.size));
		
		for (int i = 0; i < Sudoku.size; i++) {
			for (int k = 0; k < Sudoku.size; k++) {
				textField[i][k] = new JTextField();
				textField[i][k].setColumns(2);
				if (i < 3 && k < 3) {textField[i][k].setBackground(color);}
				if (i > 5 && k < 3) {textField[i][k].setBackground(color);}
				if (i < 3 && k > 5) {textField[i][k].setBackground(color);}
				if ((i > 2 && i < 6) && (k > 2 && k < 6)) {textField[i][k].setBackground(color);}
				if (i > 5 && k > 5) {textField[i][k].setBackground(color);}
				panel1.add(textField[i][k], BorderLayout.CENTER);
			}
		}
		panel1.setBorder(new EmptyBorder(35,35,35,35));
		pane.add(panel1, BorderLayout.PAGE_START);
		
	}
	
	/**
	 * Adds the numbers in textfield to the sudokuboard-matrix.
	 * @param tf the textfield matrix where user input is taken.
	 * @throws IllegalArgumentException if values in textfields are not 0-9 and if dimension of tf is wrong
	 */
	public void addUserInput(JTextField[][] tf) throws IllegalArgumentException {
		if (tf.length != Sudoku.size || tf[0].length != Sudoku.size) throw new IllegalArgumentException("Fel dimensioner på input textField!");
		for (int i = 0; i < Sudoku.size; i++) {
			for (int j = 0; j < Sudoku.size; j++) {
				if (tf[i][j].getText().equals("")) {
					s.add(i,j,0);
				} else {
					int z;
					try {
						z = Integer.parseInt(tf[i][j].getText());
					} catch (Exception e) {
						throw new IllegalArgumentException("Brädet innehåller en icke-siffra!");
					}
					if (z < 1 || z > Sudoku.size) throw new IllegalArgumentException("Endast siffror mellan 1-9 är tillåtna.");
					s.add(i,j,z);
				}				
			}
		}
	}
	
	private void addButtons() {
		JPanel panel = new JPanel();
		JButton clear = new JButton("Clear");
		JButton solve = new JButton("Solve");
		panel.add(clear);
		panel.add(solve);
		pane.add(panel, BorderLayout.PAGE_END);
		
		clear.addActionListener(e -> {
			s.clear();
			for (int i = 0; i < Sudoku.size; i++) {
				for (int k = 0; k < Sudoku.size; k++) {
					textField[i][k].setText("");
				}	
			}});
		
		solve.addActionListener(e -> {
			try {
				addUserInput(textField);
				boolean solveable = s.solve();
				if (!solveable) JOptionPane.showMessageDialog(null,"Sudoku gick ej att lösa.");  
				for (int i = 0; i < Sudoku.size; i++) {
					for (int k = 0; k < Sudoku.size; k++) {
						if (s.get(i,k) == 0) return;
						textField[i][k].setText(String.valueOf(s.get(i,k)));
					}
				}
			} catch (Exception ex) {
				JOptionPane.showMessageDialog(null, ex.getMessage());
			}
		});
	}
	
	
}
