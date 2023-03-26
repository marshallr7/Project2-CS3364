def read_courses(file_name):
    courses = {}
    prerequisites = []

    with open(file_name, 'r') as file:
        lines = file.readlines()
        for line in lines:
            course, prereq = line.strip().split(' - ')
            if prereq != 'N/A':
                prerequisites.append((course, prereq))
            if course not in courses:
                courses[course] = len(courses)

    return courses, prerequisites


if __name__ == '__main__':
    print(read_courses("courses.txt"))

