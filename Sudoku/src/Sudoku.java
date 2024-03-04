package sudoku;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashSet;
import java.util.NoSuchElementException;
import java.util.Set;

import javax.swing.JTextField;

public class Sudoku implements SudokuSolver {
	private int[][] board;
	public static final int size = 9;
	
	
	public Sudoku() {
		board = new int[size][size];
		clear();
	}

	@Override
	public boolean solve() {
		if (!isValid()) {
			return false;
		}
		return solve(0,0);
	}
	
	/**
	 * Recursive helper algorithm for checking if sudoku is solvable.
	 * @param r, the row index to be tested
	 * @param c, the column index to be tested
	 * @return true if solvable, false if not
	 */
	private boolean solve(int r, int c) {
		if (r > 8) {
			return true;
		}
		
		if (c > 8) {
			return solve(r+1, 0);
		}
		
		else {
			if (board[r][c] == 0) {
				for (int i = 1; i < 10; i++) {
					add(r, c, i);
					if (isValid()) {
						boolean solvable = solve(r, c+1);
						if (solvable) {
							return true;
						}
					}
					remove(r, c);
				}
				return false;
			} else {
				return solve(r, c+1);
			}
		}
	}

	@Override
	public void add(int row, int col, int digit) {
		if (row < 0 || row > size-1 || col < 0 || col > size-1) {
			throw new NoSuchElementException("Den rutan finns inte på brädet.");
		} if (digit < 0 || digit > size) {
			throw new IllegalArgumentException("Siffran ska vara mellan 0-9.");
		}
		board[row][col] =  digit;
	}

	@Override
	public void remove(int row, int col) {
		if (row < 0 || row > size-1 || col < 0 || col > size-1) {
			throw new NoSuchElementException("Den rutan finns inte på brädet.");
		} 
		board[row][col] = 0;
	}

	@Override
	public int get(int row, int col) {
		if (row < 0 || row > size-1 || col < 0 || col > size-1) {
			throw new NoSuchElementException("Den rutan finns inte på brädet.");
		} 
		return board[row][col];
	}

	@Override
	public boolean isValid() {
		for (int r = 0; r < size; r++) { 
			if (!checkArray(board[r])) { //check rows
				return false;
			}
			
		for (int rr = 0; rr < size; rr++) { 
			int[] col = new int[size];
			for (int c = 0; c < size; c++) {
				col[c] = board[c][rr];
			}
			if (!checkArray(col)) { //check columns
				return false;
			}
		}
		
		for (int i = 0; i < size; i = i + 3) { 
			for (int k = 0; k < size; k = k + 3) {
				ArrayList<Integer> list = new ArrayList<Integer>();
				for (int a = i; a < i+3; a++) {
					for (int b = k; b < k+3; b++) {
						list.add(board[a][b]);
					}
				}
				int[] array = list.stream()
						.mapToInt(Integer::intValue)
						.toArray();
				if (!checkArray(array)) { //check 3x3-matrices
					return false;
				}
			}
		}
	}
	return true;
}
	/**
	 * Checks if an array of 9 numbers contain duplicates of numbers [1-9].
	 * @param array, an int[]-array of size 9
	 * @return true if no duplicates are found, false if they are
	 */
	private boolean checkArray(int[] array) {
		int[] freq = new int[size+1];
		for (int i = 0; i < size; i++) {
			freq[array[i]]++;
		}
		// check if any double
		for (int i = 1; i <= size; i++) {
			if (freq[i] > 1) return false;
		}
		return true;
		
	}
	

	@Override
	public void clear() {
		for (int r = 0; r < size; r++) {
			for (int c = 0; c < size; c++) {
				board[r][c] = 0;
			}
		}
		
	}

	@Override
	public void setMatrix(int[][] m) {
		if (m[0].length != size || m.length != size) {
			throw new IllegalArgumentException("Matrisen har fel dimensioner.");
		} for (int r = 0; r < size; r++) {
			for (int c = 0; c < size; c++) {
				if (m[r][c] < 0 || m[r][c] > size) {
					throw new IllegalArgumentException("Siffrorna i matrisen som sätts in uppfyller inte villkoret 0-9.");
				}
			}
		}	
		
	}

	@Override
	public int[][] getMatrix() {
		return board;
	}
}
