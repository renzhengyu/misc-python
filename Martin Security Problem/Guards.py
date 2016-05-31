# About: Martin's facebook post on Jan 9, 2016. See EOF.

from copy import deepcopy
import sys

class Cell:
	def __init__(self, char):
		self.occupied = (char == "X")
		self.watched = False
		self.deployed = False	# = Occupied by a guard
		self.empty_neighbor_count = 0

	def empty(self):
		return not (self.occupied or self.watched or self.deployed)

class Facility:
	def __init__(self, column_count, c1, c2):
		self.column_count = column_count
		self.grid = list()
		r1 = list()
		r2 = list()
		for i in range(self.column_count):
			r1.append(Cell(c1[i]))
			r2.append(Cell(c2[i]))
		self.grid.append(r1)
		self.grid.append(r2)
		self.update_empty_neighbor_count()

	def update_empty_neighbor_count(self):
		for i in range(2):
			for j in range(self.column_count):
				counter = 0
				# check up or down neighbor
				t = 0 if i == 1 else 1
				if self.grid[t][j].empty(): counter = 1
				# check left neighbor
				t = j - 1
				if t>=0:
					if self.grid[i][t].empty(): counter += 1
				# check right neighbor
				t = j + 1
				if t < self.column_count:
					if self.grid[i][t].empty(): counter += 1
				self.grid[i][j].empty_neighbor_count = counter

	def unguarded_cell_count(self):
		result = 0
		for i in range(2):
			for j in range(self.column_count):
				if self.grid[i][j].empty():
					result += 1
		return result

	def fully_guarded(self):
		return (self.unguarded_cell_count() == 0)

	def display(self):
		for i in range(2):
			for j in range(self.column_count):
				c = self.grid[i][j]
				if c.occupied: print ("X", end="")
				if c.watched: print ("*", end="")
				if c.deployed: print ("G", end="")
				if c.empty(): print (".", end="")
			print ()
		print ("unguarded cell count: {0}.".format(self.unguarded_cell_count()))
		print ()

	def guard_power_array(self):
		r1 = list()
		r2 = list()
		for i in range(2):
			for j in range(self.column_count):
				p = 0
				d = 1 # How many directions this guard cover
				if self.grid[i][j].empty():
					p = 1
					t = 1 if i==0 else 0
					if self.grid[t][j].empty(): # The cell on the other row
						p += (4 - self.grid[t][j].empty_neighbor_count)
						d += 1
					l_counted = False # go through all the cells to the left
					t = j-1
					while (t >= 0):
						if not self.grid[i][t].empty(): break
						p += (4 - self.grid[i][t].empty_neighbor_count)
						t -= 1
						if not l_counted:
							d += 1
							l_counted = True
					r_counted = False # go through all the cells to the right
					t = j+1
					while (t < self.column_count):
						if not self.grid[i][t].empty(): break
						p += (4 - self.grid[i][t].empty_neighbor_count)
						t += 1
						if not r_counted:
							d += 1
							r_counted = True
				if i == 0: r1.append(p*d) 
				else: r2.append(p*d)
		result = list()
		result.append(r1)
		result.append(r2)
		return result

	def first_cell_to_guard(self):
		gpa = self.guard_power_array()
		max_val = gpa[0][0]
		max_row = 0
		max_col = 0
		for i in range(2):
			for j in range(self.column_count):
				if (gpa[i][j] > max_val):
					max_val = gpa[i][j]
					max_row = i
					max_col = j
		return (max_row, max_col)

	def guarded_facility(self, cell_to_guard):
		row, col = cell_to_guard
		result = deepcopy(self)
		result.grid[row][col].deployed = True
		t = 1 if row==0 else 0
		if result.grid[t][col].empty(): result.grid[t][col].watched = True
		t = col-1
		while (t>=0):
			if result.grid[row][t].occupied or result.grid[row][t].deployed: break
			result.grid[row][t].watched = True
			t -= 1
		t = col+1
		while (t<result.column_count):
			if result.grid[row][t].occupied or result.grid[row][t].deployed: break
			result.grid[row][t].watched = True
			t +=1
		result.update_empty_neighbor_count()
		return result

	def solve(self):
		guard_count = 0
		imagined_facility = deepcopy(self)
		imagined_facility.display()
		while not imagined_facility.fully_guarded():
			row, col = imagined_facility.first_cell_to_guard()
			guard_count += 1
			print ("Guarding cell ({0}, {1}), Guard Count: {2} ".format(row, col, guard_count))
			t = imagined_facility.guarded_facility((row, col))
			imagined_facility = deepcopy(t)
			imagined_facility.display()
		return guard_count

class InputDataError (Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)
		pass

class Dataset:
	def __init__(self, filename):
		self.facility_count = 0
		self.facilities = list()
		try:
			f = open (filename)
			first_line_of_file = f.readline()
			self.facility_count = int(first_line_of_file.strip())
			for i in range(self.facility_count):
				first_line_of_facility = f.readline()
				column_count = int(first_line_of_facility.strip())
				r1 = f.readline().strip().upper()
				r2 = f.readline().strip().upper()
				#print (column_count, r1, r2, len(r1), len(r2))
				if r1 == "" or r2 == "": raise InputDataError("Input file too short.")
				if column_count != len(r1) or column_count != len(r2): 
					raise InputDataError("Column count inconsistent in facility No. {0}".format(i+1))
				self.facilities.append((column_count, r1, r2))
			if self.facility_count != len(self.facilities):
				raise InputDataError("Facility count inconsistent. Check input file.")
		except InputDataError as e: print ("Input data error: {0}".format(e.value))
		except IOError as e: print ("I/O error({0}): {1}".format(e.errno, e.strerror))
		except ValueError: print ("Could not convert data to an integer.")
		except: print ("Unexpected error:", sys.exc_info()[0])

inputdata = Dataset("input.txt")
print ("Total facilities: {0}".format(inputdata.facility_count))
print (inputdata.facilities)

output_file = open("output.txt", 'w')
i = 0
for f in inputdata.facilities:
	i += 1
	facility = Facility(*f)
	guard_count = facility.solve()
	output_file.write("Case #{0}: {1}\n".format(i, guard_count))
output_file.close()


# f1 = Facility(16, "X...XXX.XXXXXX.X", "................")
# f1.solve()

# I'm interested if I know anyone clever enough to answer the following question by 
# writing a short computer program to solve it. See below and respond if you think 
# you'd be able to do it. My best hope is in Nathan Poulton.

# A top-secret algorithmic research facility has decided to up its security by 
# hiring guards to keep watch over the premises. After all, they don't want anyone
# sneaking in and learning the answers to questions such as "does P = NP?".

# When viewed from above, the facility can be modeled as a grid G with 2 rows and
# N columns. The jth cell in the ith row is either empty (represented by Gi,j = ".")
# or occupied by a building (Gi,j = "X"), and the grid includes at least one empty cell.

# Guards may be potentially stationed in any of the empty cells. A guard can see not
# only their own cell, but also all contiguous empty cells in each of the 4 compass
# directions (up, down, left, and right) until the edge of the grid or a building.
# For example, in the grid below, the guard ("G") can see every cell marked with 
# an asterisk ("*"):
# .*.X.X..
# *G*****X
# What is the minimum number of guards required such that every empty cell in
# the grid can be seen by at least one of them?
# Input
# Input begins with an integer T, the number of facilities that need guarding.
# For each facility, there is first a line containing the integer N. The next
# line contains the grid cells G1,1 to G1,N in order. The third line contains
# the grid cells G2,1 to G2,N in order.
# Output
# For the ith facility, print a line containing "Case ‪#‎i‬: " followed by the
# number of guards required to guard the facility.
# Constraints
# 1 ≤ T ≤ 200 
# 1 ≤ N ≤ 1,000
# Explanation of Sample
# In the first case, one solution is to place three guards as follows:
# .G.X.XG.
# ....G..X

###############
##  RESULTS  ##
###############

# Python 3.5.1 (v3.5.1:37a07cee5969, Dec 6 2015, 01:38:48) [MSC v.1900 32 bit (Intel)] on win32

# C:\Users\renzh\Documents\Coding\Python\Martin Security Problem>py Guards.py
# X...XXX.XXXXXX.X
# ................
# unguarded cell count: 21.

# Guarding cell (1, 7), Guard Count: 1
# X...XXX*XXXXXX.X
# *******G********
# unguarded cell count: 4.

# Guarding cell (0, 2), Guard Count: 2
# X*G*XXX*XXXXXX.X
# *******G********
# unguarded cell count: 1.

# Guarding cell (0, 14), Guard Count: 3
# X*G*XXX*XXXXXXGX
# *******G********
# unguarded cell count: 0.