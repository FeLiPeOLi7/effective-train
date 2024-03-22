import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        _, _, w, h = draw.textbbox((0, 0), letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)

        Node consistency: When all the values in a variable's domain satisfy the variable's unary constraint
        """
        for v in self.domains:#Pass through all variables
            l = v.length#Get the lenght of the variable
            words = self.domains[v].copy()#Make a copy so it doesn't change in the iteration
            for x in words:#Pass through all values in the domain of that variable
                if len(x) !=l:#Check if x is or is not equal the lenght of v
                    self.domains[v].remove(x)#If it is not the same lenght remove the value from the domain.

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Detects if the values overlap
        def no_conflict(x, value_x, y, value_y, overlap):
            i, j = overlap
            return value_x[i] == value_y[j]

        revised = False  # Initial state of revised
        domain_x = self.domains[x].copy()  # Make possible that domains don't change while iterating
        for value_x in domain_x:  # For each x in domain(x)
            if (x,y) in self.crossword.overlaps:
                overlap = self.crossword.overlaps[x, y]  # Retrieves the overlap point between positions x and y
            else:
                overlap = None
            if overlap is not None:  # If there is an overlap at x and y
                # Checks for each possible value_y in the domain of y if there is no conflict with value_x at the overlap point
                if not any(no_conflict(x, value_x, y, value_y, overlap) for value_y in self.domains[y]):
                    self.domains[x].remove(value_x) # If the condition is true remove v_x from x
                    revised = True  # Domains of x has been revised

        return revised


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        if not arcs:#When arcs is none
            arcs = [(x, y) for x in self.domains for y in self.domains if x != y]#Arcs will be a list of all pairs of values
        while arcs:#When arcs is not none (if arcs is an empty list the value of the while will be false and break the loop)
            x, y = arcs.pop(0)#Pop up the first(the 0th item) pair of (x, y)
            if self.revise(x, y):#Uses the revise function
                if not self.domains[x]:#If self.domais[x] is now empty return false ("not()" checks if it is None(true) or non_None(false))
                    return False
                #Maintaning X consistent with neighbors different of Y
                for z in self.crossword.neighbors(x):#Each Z represents a neighbor of X that is not Y
                    if not(z == y):#Z is not equal Y
                        arcs.append((z, x))#Add Z to the arcs list
        return True#Arc consistency is enforced and no domains are empty


    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        for variable in self.domains:#Pass in each variable
            if variable not in assignment:#Checks if the variable is None in the assignment
                return False#If true return false

        return True#Else return true

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        for v in assignment:#Pass trough all variables
            l = v.length#Gets length
            words = self.domains[v].copy()#Make a copy of the variable to not change in the iteration
            #Every value is the correct length
            for x in words:#Pass trough all the values in the variable
                if x in assignment and len(assignment[x]) != l:#If x != than lenght return assignment = false
                    return False

            #All values must be distinct
            if (len(set(words)) != len(words)):#The set() removes any duplicate value (this gives me the len of unique words in my list and the total len of my list, including the duplicate values)
                return False

            #No conflicts
            for y in self.crossword.neighbors(v):#Iterating over all the neighbors of the variable v
                if y in assignment:#Checks if y is already assigned a word in the assignment list
                    var = self.crossword.overlaps[v, y]#Gets the overlapping position between the variable v and its neighbor y
                    if not(assignment[v][var[0]] == assignment[y][var[1]]):#Checks if the letter overlapping position of v’s assigned word == the letter overlapping position of y’s assigned word.
                        return False

        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        domain_values = []#Empty list

        for value_var in self.domains[var]:#Pass trought the domain of var
            ruled_var = 0#Initalize ruled_var
            for y in self.crossword.neighbors(var):#y is the neighbor of var
                if y not in assignment:#checks if y is unassigned
                    for value_y in self.domains[y]:#pass trough the values of the neighbor
                        if not self.consistent(assignment):#Indirectly overlaps, checks for consistency
                            ruled_var += 1#Add the ruled out values of var each time it loop

            domain_values.append((value_var, ruled_var))#Make a tuple

        domain_values.sort(key=lambda x: x[1])#Pops just the value of the tuple
        var = [value for value, _ in domain_values]#iterates over domain_values and for each tuple, takes the first element (value) and ignore the second(_)

        return var#Return the var list

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        u = []#Empty list
        variable = set(self.domains)
        for unassigned in variable.difference(set(assignment)):#Difference between assigned variable and unassigned variables
            u.append((unassigned, len(self.domains[unassigned])))#Appending these variable in my u.list()

        s = sorted(u, key=lambda x: x[1])#Ascending order of domain size
        value = []#List of smallest domain size

        for i in range(len(s)):#Iterates over each element in the list s
            if s[i][1] == s[0][1]:#If a random variable have a domain size equals the domain size of the smallest variable append it to the list
                value.append(s[i][0])#Append the i variable
            else:#If not, just break
                break

        u = list()#Create a tuple of the variable in value and number of neighbors
        for y in value:#Iterates over all variables in value
            u.append((y, len(self.crossword.neighbors(y))))#Apends the degree of the variable

        return sorted(u, key=lambda x: x[1], reverse=True)[0][0]#Return the variable with highest degree and smallest domain size.


    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        if self.assignment_complete(assignment):
            return assignment
        var = self.select_unassigned_variable(assignment)
        value = self.order_domain_values(var, assignment)
        for v in value:
            assignment[var] = v
            if self.consistent(assignment):
                result=self.backtrack(assignment)
                if not(result==None):
                    return result
            assignment.pop(var)
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
