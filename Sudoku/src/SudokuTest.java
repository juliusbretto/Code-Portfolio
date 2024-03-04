package sudoku;

import static org.junit.jupiter.api.Assertions.*;

import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import sudoku.Sudoku;
import sudoku.SudokuSolver;

class SudokuTest {
private static SudokuSolver s;
private static SudokuSolver empty;
	@BeforeEach
	void setUp() throws Exception {
		s = new Sudoku();
		int[][] sud = {{ 0,0,8,0,0,9,0,6,2},
							{0,0,0,0,0,0,0,0,5},
							{1,0,2,5,0,0,0,0,0},
							{0,0,0,2,1,0,0,9,0},
							{0,5,0,0,0,0,6,0,0},
							{6,0,0,0,0,0,0,2,8},
							{4,1,0,6,0,8,0,0,0},
							{8,6,0,0,3,0,1,0,0},
							{0,0,0,0,0,0,4,0,0}};
		s.setMatrix(sud);
		empty = new Sudoku();
	}

	@AfterEach
	void tearDown() throws Exception {
		s = null;
	}

	
	
	@Test
	void dubblett() {
		s.add(0, 0, 8);
		s.add(0, 1, 8);
		assertFalse(s.isValid(), "dubblet går ej");
	}
	
	@Test 
	void remove() {
		s.add(2, 4, 1);
		s.remove(2, 4);
		assertEquals(s.get(2, 4), 0, "bortagning funkar inte");
	}
	
	@Test
	void getAndAdd() {
		s.add(1, 1, 2);		
		assertEquals(s.get(1, 1), 2, "fel vid get eller add matris");
		
	}
	
	@Test
	void isSValid() {		
		assertTrue(s.isValid());
		}
	
	@Test
	void test1() {
		assertTrue(empty.solve());	
	}
	
	
	@Test
	void solveS() {
		assertTrue(s.solve(), "fel i solve");
		
	}
	
	
	
	}


