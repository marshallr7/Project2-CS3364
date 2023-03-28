import re


class Graph:
    def __init__(self, vertices):
        self.graph = {i: [] for i in range(vertices)}
        self.V = vertices

    def add_edge(self, u, v):
        self.graph[u].append(v)

    def topological_sort(self):
        visited = [False] * self.V
        stack = []
        for i in range(self.V):
            if not visited[i]:
                self.topological_sort_util(i, visited, stack)
        return stack[::-1]

    def topological_sort_util(self, v, visited, stack):
        visited[v] = True
        for i in self.graph[v]:
            if not visited[i]:
                self.topological_sort_util(i, visited, stack)
        stack.append(v)

    def get_semesters(self, courses, num_semesters, credits_per_semester):
        semester_map = {i: [] for i in range(1, num_semesters + 1)}
        taken_courses = set()

        def can_add_course(course, semester):
            if course in taken_courses:
                return False

            prereqs = [list(course_map.keys())[list(course_map.values()).index(i)] for i in
                       self.graph[course_map[course]] if
                       i in course_map.values()]

            for prereq in prereqs:
                if prereq not in taken_courses:
                    return False

            if sum([int(c[-1]) for c in semester_map[semester]]) + int(course[-1]) > credits_per_semester:
                return False

            return True

        for semester in range(1, num_semesters + 1):
            for course in courses:
                if can_add_course(course, semester):
                    semester_map[semester].append(course)
                    taken_courses.add(course)

        remaining_courses = set(courses) - taken_courses
        if remaining_courses:
            print(f"Couldn't fit {', '.join(remaining_courses)} into any semester")

        return semester_map


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
course_list = [list(course_map.keys())[list(course_map.values()).index(i)] for i in topo_order]

num_semesters = int(input("Enter the number of semesters you want to complete the degree in: "))
credits_per_semester = int(input("Enter the number of credits per semester you want to take: "))
semester_map = g.get_semesters(course_list, num_semesters, credits_per_semester)

for semester, courses in semester_map.items():
    print(f'Semester {semester}:')
    for course in courses:
        print(f'    {course}')

