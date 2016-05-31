import copy
from datetime import datetime

class Cell:
    valid_value_range = range(1,10)             # 1~9
    def __init__(self, v):
        self.possible_values = Cell.valid_value_range
        self.value = 0
        if v in Cell.valid_value_range:
            self.value = v
        else:
            self.value = 0
    def possible_values_count(self):
        return len(self.possible_values)

class Sudoku:
    dimension = range (0,9)
    blocks_r = 3
    blocks_c = 3
    
    def __init__(self, source):
        self.cell = [[],[],[],[],[],[],[],[],[]]
        self.easy = True
        for r in Sudoku.dimension:
            for c in Sudoku.dimension:
                self.cell[r].append(Cell(source[r][c]))
        self.refresh
    
    def cues_count(self):
        counter = 0
        for r in Sudoku.dimension:
            for c in Sudoku.dimension:
                if self.cell[r][c].value != 0:
                    counter += 1
        return counter       
    
    def show(self):
        hr = "+---------+---------+---------+"
        print()
        print(hr)
        for r in Sudoku.dimension:
            print("|", end="")
            for c in Sudoku.dimension:
                t = self.cell[r][c].value
                if t == 0:
                    t = "."
                print(" {0} ".format(t), end="")
                if c == 2 or c == 5:
                    print("|", end="")
            print("|")
            if r == 2 or r == 5:
                print(hr)
        print(hr)
        print("{0} cues. {1} blanks.".format(self.cues_count(), len(Sudoku.dimension)**2-self.cues_count()))
        if self.legit():
            print("Sudoku is legit.")
        else:
            print("Sudoku is NOT legit.")
    
    def row(self, r):
        t = []
        for c in Sudoku.dimension:
            if self.cell[r][c].value != 0:
                t.append(self.cell[r][c].value)
        return t
    
    def column(self, c):
        t = []
        for r in Sudoku.dimension:
            if self.cell[r][c].value != 0:
                t.append(self.cell[r][c].value)
        return t
    
    def block(self, r, c):
        t = []
        for i in range(int(r/Sudoku.blocks_r)*Sudoku.blocks_r, int(r/Sudoku.blocks_r)*Sudoku.blocks_r+Sudoku.blocks_r):
            for j in range(int(c/Sudoku.blocks_c)*Sudoku.blocks_c, int(c/Sudoku.blocks_c)*Sudoku.blocks_c+Sudoku.blocks_c):
                if self.cell[i][j].value != 0:
                    t.append(self.cell[i][j].value)
        return t
    
    def rcb(self, r, c):
        t = []
        t.extend(self.row(r))
        t.extend(self.column(c))
        t.extend(self.block(r, c))
        return t
    
    def legit(self):
        self.refresh()
        t = True
        for r in Sudoku.dimension:
            for c in Sudoku.dimension:
                if self.cell[r][c].value != 0:
                    if self.rcb(r,c).count(self.cell[r][c].value) > Sudoku.blocks_r:
                        #print("Cell ({0}, {1}) is invalid.".format(r, c))
                        t = False
                else:
                    if len(self.cell[r][c].possible_values) < 1:
                        #print("Cell ({0}, {1}) is blank but has no possible values.".format(r, c))
                        t = False
        return t
    
    def refresh(self):
        for r in Sudoku.dimension:
            for c in Sudoku.dimension:
                if self.cell[r][c].value != 0:
                    self.cell[r][c].possible_values = []
                else:
                    self.cell[r][c].possible_values = list(set(self.cell[r][c].possible_values) - set(self.rcb(r, c)))
    
    def show_hint(self):
        hr = "         +---------+---------+---------+"
        print()
        print("         HINTS - possible values count")
        print(hr)
        for r in Sudoku.dimension:
            print("         |", end="")
            for c in Sudoku.dimension:
                t = self.cell[r][c].possible_values_count()
                if t == 0:
                    t = "-"
                print(" {0} ".format(t), end="")
                if c == 2 or c == 5:
                    print("|", end="")
            print("|")
            if r == 2 or r == 5:
                print(hr)
        print(hr)
    
    def fill_one(self):
        self.refresh()
        for r in Sudoku.dimension:
            for c in Sudoku.dimension:
                if self.cell[r][c].possible_values_count() == 1:
                    self.cell[r][c].value = self.cell[r][c].possible_values[0]
        self.refresh()
    
    def solve_one(self):
        s = []
        while True:
            t = self.cues_count()
            self.fill_one()
            s.append(self.cues_count()-t)
            if t == self.cues_count():
                self.easy = False
                break
        #print()
        #print("Solve_one tried fill_one {0} times. Each time filled {1} cells.".format(len(s), s))
        return self.cues_count() == len(Sudoku.dimension) ** 2
    
    def hypo(self, r, c, v):
        ts = list()
        for i in Sudoku.dimension:
            tr = list()
            for j in Sudoku.dimension:
                tr.append(self.cell[i][j].value)
            ts.append(tr)
        ts[r][c] = v
        return ts
    
    def solve_two(self):
        counter = 0
        for r in Sudoku.dimension:
            for c in Sudoku.dimension:
                if len(self.cell[r][c].possible_values) > 1:
                    for v in self.cell[r][c].possible_values:
                        t = copy.deepcopy(self)
                        t.cell[r][c].value = v
                        #t.show()
                        #input("Hit Enter...")
                        t.fill_one()
                        t.solve_one()
                        if not t.legit():
                            counter += 1
                            self.cell[r][c].possible_values.remove(v)
    
    def solve(self):
        timer1 = datetime.now()
        t = self.cues_count()
        self.solve_one()
        while True:
            self.solve_two()
            self.solve_one()
            if self.cues_count() == len(Cell.valid_value_range)**2 or t == self.cues_count():
                break
        timer2 = datetime.now()
        
        print()
        if self.cues_count() == len(Cell.valid_value_range)**2:
            print("Solution found in {0} seconds.".format(timer2-timer1))
        else:
            print("Solution not found in {0} seconds".format(timer2-timer1))


easy = [    [0,8,0,0,0,5,0,0,3],
            [5,0,0,0,8,6,0,7,2],
            [7,2,3,0,0,9,0,0,0],
            [0,0,2,7,0,0,0,5,4],
            [0,0,0,6,2,4,0,0,0],
            [6,4,0,0,0,3,9,0,0],
            [0,0,0,9,0,0,5,3,8],
            [9,7,0,1,3,0,0,0,6],
            [3,0,0,5,0,0,0,1,0]]

medium = [  [0,0,4,0,0,9,0,0,0],
            [0,0,0,0,0,0,0,1,6],
            [2,3,7,0,0,5,0,9,0],
            [0,4,0,5,8,7,0,0,9],
            [0,5,0,2,0,1,0,4,0],
            [7,0,0,9,6,4,0,5,0],
            [0,6,0,7,0,0,4,3,2],
            [4,2,0,0,0,0,0,0,0],
            [0,0,0,3,0,0,5,0,0]]

hard = [    [0,4,0,0,5,1,0,0,0],
            [5,2,0,0,0,0,4,0,9],
            [0,9,0,2,0,0,0,0,6],
            [9,0,0,0,0,0,0,2,0],
            [0,0,2,5,0,7,1,0,0],
            [0,3,0,0,0,0,0,0,7],
            [8,0,0,0,0,5,0,9,0],
            [7,0,4,0,0,0,0,8,1],
            [0,0,0,6,8,0,0,7,0]]

evil = [    [7,0,0,0,0,3,0,9,0],
            [0,0,0,0,0,7,0,6,0],
            [1,8,0,9,0,0,0,4,0],
            [0,0,0,0,0,0,4,0,0],
            [0,0,5,2,4,1,8,0,0],
            [0,0,6,0,0,0,0,0,0],
            [0,5,0,0,0,4,0,8,7],
            [0,2,0,3,0,0,0,0,0],
            [0,4,0,6,0,0,0,0,5]]

a = Sudoku(evil)
a.show()
if a.legit():
    a.solve()
    a.show()
