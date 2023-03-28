import re


class Graph:
    def __init__(self, vertices):
        self.graph = {i: [] for i in range(vertices)}
        self.V = vertices

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def topological_sort_util(self, v, visited, stack):
        visited[v] = True
        for i in self.graph[v]:
            if not visited[i]:
                self.topological_sort_util(i, visited, stack)
        stack.append(v)

    def topological_sort(self):
        visited = [False] * self.V
        stack = []
        for i in range(self.V):
            if not visited[i]:
                self.topological_sort_util(i, visited, stack)
        return stack[::-1]


class TextHandler:
    def __init__(self):
        pass

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


th = TextHandler()
# th.fix_file('courses.txt')
course_map, prerequisites = th.read_courses('courses.txt')
g = Graph(len(course_map))

for course, prereq in prerequisites:
    g.add_edge(course_map[prereq], course_map[course])

topo_order = g.topological_sort()
print("Topological Sort:")
for i in topo_order:
    print(list(course_map.keys())[list(course_map.values()).index(i)])
