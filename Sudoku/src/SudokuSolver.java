package sudoku;

import javax.swing.JTextField;

public interface SudokuSolver {
	/**
	 * Solves the board
	 * @return boolean true if solveable, false if not
	 */
	boolean solve();

	/**
	 * Puts digit in the box row, col.
	 * 
	 * @param row   The row
	 * @param col   The column
	 * @param digit The digit to insert in box row, col
	 * @throws IllegalArgumentException if row, col or digit is outside the range
	 *                                  [0..9]
	 */
	void add(int row, int col, int digit);

	/**
	 * Removes (by setting digit to 0) a specified box on the board.
	 * 
	 * @param row, the specified row index to remove
	 * @param col, the specified column index to remove
	 * @throws IllegalArgumentException if row or col is outside [0-8]
	 * 
	 */
	void remove(int row, int col);

	/**
	 * Retrieves the digit at the specified row and column.
	 * 
	 * @param row, the specified row index to retrieve
	 * @param col, the specified column index to reteieve
	 * @return the int at specified row and col
	 * @throws IllegalArgumentException if row and col is outside [0-8]
	 * 
	 */
	int get(int row, int col);

	/**
	 * Checks that all filled in digits follow the the sudoku rules.
	 * @return boolean true if valid, false if invalid
	 */
	boolean isValid();

	
	/**
	 * Fills the grid's all boxes with the digit 0, clearing it.
	 */
	void clear();

	/**
	 * Fills the grid with the digits in m. The digit 0 represents an empty box.
	 * 
	 * @param m the matrix with the digits to insert
	 * @throws IllegalArgumentException if m has the wrong dimension or contains
	 *                                  values outside the range [0..9]
	 */
	void setMatrix(int[][] m);

	/**
	 * Returns the board as a matrix filled with ints [0-9] where 0 indiciates empty.
	 * @return an int[][] representation of the sudoku board.
	 */
	int[][] getMatrix();

}