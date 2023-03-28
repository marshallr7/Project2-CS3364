import re


# Define the Graph class to represent a directed graph
class Graph:
    # Initialize the Graph object with the number of vertices
    def __init__(self, vertices):
        self.graph = {i: [] for i in range(vertices)}
        self.V = vertices

    # Add an edge from vertex u to vertex v
    def add_edge(self, u, v):
        self.graph[u].append(v)

    # Helper function for the topological sort to perform a depth-first search
    def topological_sort_util(self, v, visited, stack):
        visited[v] = True
        for i in self.graph[v]:
            if not visited[i]:
                self.topological_sort_util(i, visited, stack)
        stack.append(v)

    # Perform a topological sort on the graph and return the result
    def topological_sort(self):
        visited = [False] * self.V
        stack = []
        for i in range(self.V):
            if not visited[i]:
                self.topological_sort_util(i, visited, stack)
        return stack[::-1]


# Define the TextHandler class to handle reading and processing text files
class TextHandler:
    def __init__(self):
        pass

    # Fix the formatting of the input file by adding spaces after 'CS'
    @staticmethod
    def fix_file(file):
        with open(file, 'r+') as f:
            text = f.read()
            f.seek(0)
            i = 0
            while i < len(text):
                if text[i:i + 2] == 'CS' and (i + 2 >= len(text) or text[i + 2] != ' '):
                    f.write('CS ')
                    i += 2
                else:
                    f.write(text[i])
                    i += 1
            f.truncate()

    # Read the courses and their prerequisites from the input file
    @staticmethod
    def read_courses(file_name):
        courses = {}
        prerequisites = []

        with open(file_name, 'r') as file:
            lines = file.readlines()
            for line in lines:
                parts = line.strip().split(' - ')
                course = parts[0]
                prereq_str = parts[-1].split('(')[-1].strip(')')  # extract prerequisite string from the line
                # Define regular expression pattern to match course codes of the form 'ABCD 1234' or 'ABCD1234'
                pattern = r'\b[A-Z]{2,4}\s?\d{4}\b'
                # Use the findall() method to extract all matches of the pattern from the prerequisite string
                prereqs = re.findall(pattern, prereq_str) if prereq_str != 'N/A' else []
                # Add each prerequisite to the list of prerequisites for the current course
                for prereq in prereqs:
                    if prereq != 'N/A':
                        prerequisites.append((course, prereq))
                # Add the current course to the course map if it is not already present
                if course not in courses:
                    courses[course] = len(courses)

        return courses, prerequisites


# Create a TextHandler object
th = TextHandler()
# Uncomment the following line to fix the input file formatting if necessary
th.fix_file('courses.txt')
# Read the course data from the input file
course_map, prerequisites = th.read_courses('courses.txt')
# Create a Graph object with the number of courses as vertices
g = Graph(len(course_map))

# Add the edges representing prerequisites to the graph
for course, prereq in prerequisites:
    g.add_edge(course_map[prereq], course_map[course])

    # Perform a topological sort on the graph to find a valid course order
topo_order = g.topological_sort()
# Print the result of the topological sort
print("Topological Sort:")
for i in topo_order:
    print(list(course_map.keys())[list(course_map.values()).index(i)])
