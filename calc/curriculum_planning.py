#!/usr/bin/env python3
"""
Curriculum Planning Calendar
Print an ASCII calendar with time slots for Days 1-5
"""

from ssl import get_default_verify_paths


class Course:
    """
    Represents a course with its schedule information.
    
    Attributes:
        course_code (str): The course code (e.g., "MATH101")
        course_name (str): The course name (e.g., "Calculus I")
        lectures (list): List of tuples (day_index, slot_index) for lecture times
                        day_index: 0-4 represents DAY 1-5
                        slot_index: 0-6 represents time slots (0=Morning 1, 1=Morning 2, etc.)
        tutorials (list): List of tuples (day_index, slot_index) for tutorial times
    
    Example:
        course = Course(
            course_code="MATH101",
            course_name="Calculus I",
            lectures=[(0, 0), (2, 0)],  # DAY 1 Morning 1, DAY 3 Morning 1
            tutorials=[(1, 1)]           # DAY 2 Morning 2
        )
    """
    
    def __init__(self, course_code, course_name, lectures=None, tutorials=None):
        """
        Initialize a Course object.
        
        Args:
            course_code (str): The course code
            course_name (str): The course name
            lectures (list, optional): List of (day_index, slot_index) tuples for lectures
            tutorials (list, optional): List of (day_index, slot_index) tuples for tutorials
        """
        self.course_code = course_code
        self.course_name = course_name
        self.lectures = lectures if lectures is not None else []
        self.tutorials = tutorials if tutorials is not None else []
    
    def __repr__(self):
        return f"Course(code='{self.course_code}', name='{self.course_name}', lectures={self.lectures}, tutorials={self.tutorials})"
    
    def __str__(self):
        return f"{self.course_code}: {self.course_name}"
    
    def get_all_time_slots(self):
        """
        Get all time slots (both lectures and tutorials) for this course.
        
        Returns:
            list: List of tuples (day_index, slot_index, type) where type is 'Lecture' or 'Tutorial'
        """
        slots = []
        for day_idx, slot_idx in self.lectures:
            slots.append((day_idx, slot_idx, 'Lecture'))
        for day_idx, slot_idx in self.tutorials:
            slots.append((day_idx, slot_idx, 'Tutorial'))
        return slots


def print_calendar():
    """
    Print a weekly calendar with the following time slots:
    - Morning 1: 8:30-10:20
    - Morning 2: 10:30-11:50
    - Afternoon 1: 13:30-15:20
    - Afternoon 2: 15:30-16:50
    - Evening 1: 18:00-18:50
    - Evening 2: 19:00-19:50
    - Evening 3: 20:00-20:50
    """
    
    # Define time slots
    time_slots = [
        ("Morning 1", "8:30-10:20"),
        ("Morning 2", "10:30-11:50"),
        ("Afternoon 1", "13:30-15:20"),
        ("Afternoon 2", "15:30-16:50"),
        ("Evening 1", "18:00-18:50"),
        ("Evening 2", "19:00-19:50"),
        ("Evening 3", "20:00-20:50"),
    ]
    
    days = ["DAY 1", "DAY 2", "DAY 3", "DAY 4", "DAY 5"]
    
    # Print header separator
    print("=" * 100)
    
    # Print day headers
    header = "Time Slot\t\t"
    for day in days:
        header += f"{day}\t\t"
    print(header)
    
    print("=" * 100)
    
    # Print each time slot
    for slot_name, slot_time in time_slots:
        # Print slot name and time
        row = f"{slot_name} {slot_time}\t"
        
        # Print empty cells for each day
        for _ in days:
            row += "\t\t"
        
        print(row)
        print("-" * 100)
    
    print()


def print_calendar_with_courses(schedule=None):
    """
    Print a weekly calendar with courses filled in.
    
    Args:
        schedule: Dictionary with structure:
                  {(day_index, slot_index): "Course Name"}
                  day_index: 0-4 (DAY 1-5)
                  slot_index: 0-6 (Morning 1 to Evening 3)
    
    Example:
        schedule = {
            (0, 0): "Math",      # DAY 1, Morning 1
            (0, 1): "Physics",   # DAY 1, Morning 2
            (1, 2): "Chemistry", # DAY 2, Afternoon 1
        }
    """
    
    if schedule is None:
        schedule = {}
    
    # Define time slots
    time_slots = [
        ("Morning 1", "8:30-10:20"),
        ("Morning 2", "10:30-11:50"),
        ("Afternoon 1", "13:30-15:20"),
        ("Afternoon 2", "15:30-16:50"),
        ("Evening 1", "18:00-18:50"),
        ("Evening 2", "19:00-19:50"),
        ("Evening 3", "20:00-20:50"),
    ]
    
    days = ["DAY 1", "DAY 2", "DAY 3", "DAY 4", "DAY 5"]
    
    # Print header separator
    print("=" * 100)
    
    # Print day headers
    header = "Time Slot\t\t"
    for day in days:
        header += f"{day}\t\t"
    print(header)
    
    print("=" * 100)
    
    # Print each time slot
    for slot_idx, (slot_name, slot_time) in enumerate(time_slots):
        # Print slot name and time
        row = f"{slot_name} {slot_time}\t"
        
        # Print cells for each day
        for day_idx in range(len(days)):
            course = schedule.get((day_idx, slot_idx), "")
            row += f"{course}\t\t"
        
        print(row)
        print("-" * 100)
    
    print()


def print_calendar_with_course_list(courses):
    """
    Print a weekly calendar with courses from a list of Course objects.
    Uses course codes to fill in the calendar slots.
    
    Args:
        courses (list): List of Course objects
    
    Example:
        course1 = Course("MAT1001", "Calculus", lectures=[(0, 0), (2, 0)], tutorials=[(1, 1)])
        course2 = Course("PHY1001", "Physics", lectures=[(0, 2), (3, 2)])
        print_calendar_with_course_list([course1, course2])
    """
    
    # Define time slots
    time_slots = [
        ("Morning 1", "8:30-10:20"),
        ("Morning 2", "10:30-11:50"),
        ("Afternoon 1", "13:30-15:20"),
        ("Afternoon 2", "15:30-16:50"),
        ("Evening 1", "18:00-18:50"),
        ("Evening 2", "19:00-19:50"),
        ("Evening 3", "20:00-20:50"),
    ]
    
    days = ["DAY 1", "DAY 2", "DAY 3", "DAY 4", "DAY 5"]
    
    # Build schedule dictionary from course list
    schedule = {}
    for course in courses:
        # Add lectures
        for day_idx, slot_idx in course.lectures:
            key = (day_idx, slot_idx)
            if key in schedule:
                # If slot is already occupied, append to it
                schedule[key] += f" / {course.course_code}"
            else:
                schedule[key] = f"{course.course_code}"
        
        # Add tutorials
        for day_idx, slot_idx in course.tutorials:
            key = (day_idx, slot_idx)
            if key in schedule:
                # If slot is already occupied, append to it
                schedule[key] += f" / {course.course_code}"
            else:
                schedule[key] = f"{course.course_code}"
    
    # Print header separator
    print("=" * 100)
    
    # Print day headers
    header = "Time Slot\t\t"
    for day in days:
        header += f"{day}\t\t"
    print(header)
    
    print("=" * 100)
    
    # Print each time slot
    for slot_idx, (slot_name, slot_time) in enumerate(time_slots):
        # Print slot name and time
        row = f"{slot_name} {slot_time}\t"
        
        # Print cells for each day
        for day_idx in range(len(days)):
            course_info = schedule.get((day_idx, slot_idx), "")
            row += f"{course_info}\t\t"
        
        print(row)
        print("-" * 100)
    
    print()


def find_all_valid_schedules(courses):
    """
    Find all valid course schedules where no time slots conflict.
    
    For each course:
    - ALL lecture time slots must be included (mandatory)
    - Only ONE tutorial time slot needs to be selected from available options
    
    Args:
        courses (list): List of Course objects
    
    Returns:
        list: List of tuples (course_selection, tutorial_selection) where:
              - course_selection: list of Course objects that can be taken together
              - tutorial_selection: dict mapping course to selected tutorial slot (day_idx, slot_idx)
    
    Example:
        course1 = Course("MAT1001", "Calculus", lectures=[(0, 0)], tutorials=[(1, 1), (2, 1)])
        course2 = Course("PHY1001", "Physics", lectures=[(0, 2)], tutorials=[(1, 1), (3, 2)])
        # Math and Physics lectures don't conflict
        # But both have tutorial option at (1, 1), so we need to pick different tutorial times
        
        valid_schedules = find_all_valid_schedules([course1, course2])
        # Returns combinations where tutorial times don't conflict
    """
    from itertools import combinations, product
    
    def lectures_conflict(course_list):
        """Check if lectures of courses conflict."""
        occupied_slots = set()
        for course in course_list:
            for day_idx, slot_idx in course.lectures:
                slot = (day_idx, slot_idx)
                if slot in occupied_slots:
                    return True
                occupied_slots.add(slot)
        return False
    
    def find_valid_tutorial_combinations(course_list):
        """
        Find all valid tutorial selections for a list of courses.
        Returns list of dicts mapping course to selected tutorial slot.
        """
        # Get all lecture slots that are occupied
        occupied_by_lectures = set()
        for course in course_list:
            for day_idx, slot_idx in course.lectures:
                occupied_by_lectures.add((day_idx, slot_idx))
        
        # For each course, get available tutorial options (that don't conflict with lectures)
        tutorial_options = []
        courses_with_tutorials = []
        
        for course in course_list:
            if course.tutorials:
                # Filter out tutorials that conflict with lectures
                available = [t for t in course.tutorials if t not in occupied_by_lectures]
                if not available:
                    # No valid tutorial time available for this course
                    return []
                tutorial_options.append(available)
                courses_with_tutorials.append(course)
            # If course has no tutorials, skip it
        
        if not courses_with_tutorials:
            # No courses have tutorials
            return [{}]
        
        # Generate all combinations of tutorial selections
        valid_combinations = []
        for tutorial_combo in product(*tutorial_options):
            # Check if this combination has conflicts
            tutorial_slots = set()
            has_conflict = False
            
            for slot in tutorial_combo:
                if slot in tutorial_slots or slot in occupied_by_lectures:
                    has_conflict = True
                    break
                tutorial_slots.add(slot)
            
            if not has_conflict:
                # Create mapping of course to selected tutorial
                tutorial_selection = {}
                for course, tutorial_slot in zip(courses_with_tutorials, tutorial_combo):
                    tutorial_selection[course] = tutorial_slot
                valid_combinations.append(tutorial_selection)
        
        return valid_combinations
    
    # Find all valid combinations
    valid_schedules = []
    
    # Try all possible combinations of courses (from 1 course to all courses)
    for r in range(1, len(courses) + 1):
        for combination in combinations(courses, r):
            course_list = list(combination)
            
            # First check if lectures conflict
            if lectures_conflict(course_list):
                continue
            
            # Then find all valid tutorial combinations
            tutorial_combos = find_valid_tutorial_combinations(course_list)
            
            for tutorial_selection in tutorial_combos:
                valid_schedules.append((course_list, tutorial_selection))
    
    # Filter out schedules that are subsets of other schedules
    # We only want maximal schedules (schedules that can't add more courses)
    maximal_schedules = []
    for schedule in valid_schedules:
        course_list, _ = schedule
        is_maximal = True
        
        for other_schedule in valid_schedules:
            other_course_list, _ = other_schedule
            if len(other_course_list) > len(course_list):
                # Check if course_list is a subset of other_course_list
                if all(course in other_course_list for course in course_list):
                    is_maximal = False
                    break
        
        if is_maximal:
            maximal_schedules.append(schedule)
    
    return maximal_schedules


def print_all_valid_schedules(courses):
    """
    Find and print all valid course schedules where no time slots conflict.
    For each valid schedule, prints the course list and a calendar visualization.
    
    Args:
        courses (list): List of Course objects
    
    Example:
        course1 = Course("MAT1001", "Calculus", lectures=[(0, 0)], tutorials=[(1, 1), (2, 1)])
        course2 = Course("PHY1001", "Physics", lectures=[(0, 2)], tutorials=[(1, 1), (3, 2)])
        
        print_all_valid_schedules([course1, course2])
    """
    valid_schedules = find_all_valid_schedules(courses)
    
    if not valid_schedules:
        print("No valid schedules found! All courses have conflicts.")
        return
    
    print(f"Found {len(valid_schedules)} valid schedule(s):\n")
    
    for idx, (course_list, tutorial_selection) in enumerate(valid_schedules, 1):
        print("=" * 100)
        # Create a summary line with all course codes
        course_codes = ", ".join([course.course_code for course in course_list])
        print(f"SCHEDULE #{idx} - {len(course_list)} course(s): [{course_codes}]")
        print("=" * 100)
        
        # Print course details
        print("\nCourses in this schedule:")
        for course in course_list:
            print(f"  • {course.course_code}: {course.course_name}")
            # if course.lectures:
                # print(f"    Lectures: {len(course.lectures)} session(s) - ALL required")
            # if course.tutorials:
            #     selected_tutorial = tutorial_selection.get(course)
            #     if selected_tutorial:
            #         day_idx, slot_idx = selected_tutorial
            #         time_slots = [
            #             "Morning 1 (8:30-10:20)",
            #             "Morning 2 (10:30-11:50)",
            #             "Afternoon 1 (13:30-15:20)",
            #             "Afternoon 2 (15:30-16:50)",
            #             "Evening 1 (18:00-18:50)",
            #             "Evening 2 (19:00-19:50)",
            #             "Evening 3 (20:00-20:50)",
            #         ]
            #         days = ["DAY 1", "DAY 2", "DAY 3", "DAY 4", "DAY 5"]
            #         print(f"    Tutorial: Selected {days[day_idx]} {time_slots[slot_idx]} (from {len(course.tutorials)} option(s))")
        
        print("\nCalendar View:")
        # Create modified course objects with only selected tutorials
        modified_courses = []
        for course in course_list:
            selected_tutorial = tutorial_selection.get(course)
            if selected_tutorial:
                # Create a new course with only the selected tutorial
                modified_course = Course(
                    course.course_code,
                    course.course_name,
                    lectures=course.lectures,
                    tutorials=[selected_tutorial]
                )
            else:
                # No tutorial for this course
                modified_course = Course(
                    course.course_code,
                    course.course_name,
                    lectures=course.lectures,
                    tutorials=[]
                )
            modified_courses.append(modified_course)
        
        print_calendar_with_course_list(modified_courses)
        
        if idx < len(valid_schedules):
            print("\n")


def print_time_slots_reference():
    """Print a reference table for time slots."""
    time_slots = [
        ("Morning 1", "8:30-10:20"),
        ("Morning 2", "10:30-11:50"),
        ("Afternoon 1", "13:30-15:20"),
        ("Afternoon 2", "15:30-16:50"),
        ("Evening 1", "18:00-18:50"),
        ("Evening 2", "19:00-19:50"),
        ("Evening 3", "20:00-20:50"),
    ]
    
    days = ["DAY 1", "DAY 2", "DAY 3", "DAY 4", "DAY 5"]
    
    print("\nTime Slot Reference:")
    print("-" * 60)
    print("Day numbers: 1-5 (DAY 1 = Monday, DAY 5 = Friday)")
    print("\nTime slot numbers:")
    for idx, (name, time) in enumerate(time_slots):
        print(f"  {idx}: {name} ({time})")
    print("-" * 60)
    print()


def input_time_slots(slot_type="lecture"):
    """
    Interactively input time slots for lectures or tutorials.
    
    Args:
        slot_type (str): "lecture" or "tutorial"
    
    Returns:
        list: List of tuples (day_index, slot_index)
    """
    time_slots_list = []
    
    print(f"\nPlease input {slot_type} time slots.")
    print_time_slots_reference()
    
    while True:
        try:
            day_input = input(f"Enter day number (1-5) for this {slot_type}, or 'e' to finish: \n> ").strip().lower()
            
            if day_input.strip().lower() == 'e':
                break
            
            day_num = int(day_input)
            if day_num < 1 or day_num > 5:
                print("[ERROR] Day number must be between 1 and 5.")
                continue
            
            slot_input = input(f"Enter time slot number (0-6) for this {slot_type}: \n> ").strip()
            slot_num = int(slot_input)
            if slot_num < 0 or slot_num > 6:
                print("[ERROR] Time slot number must be between 0 and 6.")
                continue
            
            # Convert to 0-based indexing
            day_index = day_num - 1
            slot_index = slot_num
            
            time_slot = (day_index, slot_index)
            if time_slot in time_slots_list:
                print(f"[WARNING] This time slot is already added. Skipping duplicate.")
            else:
                time_slots_list.append(time_slot)
                time_slots = [
                    ("Morning 1", "8:30-10:20"),
                    ("Morning 2", "10:30-11:50"),
                    ("Afternoon 1", "13:30-15:20"),
                    ("Afternoon 2", "15:30-16:50"),
                    ("Evening 1", "18:00-18:50"),
                    ("Evening 2", "19:00-19:50"),
                    ("Evening 3", "20:00-20:50"),
                ]
                days = ["DAY 1", "DAY 2", "DAY 3", "DAY 4", "DAY 5"]
                print(f"  Added: {days[day_index]} {time_slots[slot_index][0]} ({time_slots[slot_index][1]})")
                
        except ValueError:
            print("[ERROR] Please enter a valid number.")
            continue
    
    return time_slots_list


if __name__ == "__main__":

    print("=== Curriculum Planner ===")
    print("==== Author: Yimeng (Rosalind) ====")
    print("==== Github Profile: https://github.com/TeenSpirit1107 ====")
    print("==== Email: yimengteng@link.cuhk.edu.cn ====")
    # Create courses with multiple tutorial options
    # Note: ALL lectures must be attended, but only ONE tutorial time needs to be selected
    
    # e.g.
    
    # # major
    
    # swEng = Course("CSC4001", "Software Engineering",
    #                lectures=[(0, 0), (2, 0)],
    #                tutorials=[])

    # # GE

    # gedGen = Course("GED2003", "Gender Matters",
    #                 lectures = [(0,1)],
    #                 tutorials = [(2,1)]
    #                 )

    course_ls = []
    course_code_ls = []
    while True:
        print(f"\n{'='*60}")
        print(f"Please add your {len(course_code_ls)+1}th course.")
        print('='*60)
        
        while True:
            course_code = input("Please input the course code: \n> ").strip()
            if course_code == "":
                print("[ERROR] Course code cannot be empty.")
                continue
            if course_code in course_code_ls:
                print("[ERROR] Duplicated course code. Please enter a different code.")
                continue
            break

        course_name = input("Please input the course name (DEFAULT_NAME by default): \n> ").strip()
        if course_name == "":
            course_name = "DEFAULT_NAME"

        # Input lectures
        lectures = input_time_slots("lecture")
        
        # Input tutorials
        tutorials = input_time_slots("tutorial")
        
        # Create Course object
        new_course = Course(course_code, course_name, lectures=lectures, tutorials=tutorials)
        course_ls.append(new_course)
        course_code_ls.append(course_code)
        
        cont = input("\nPress ENTER to add another course; press 'e' to finish: \n> ")
        if cont.strip().lower() == "e":
            break
    
    print(f"\n{'='*60}")
    print(f"Total courses added: {len(course_ls)}")
    print('='*60)
    
    if course_ls:
        print_all_valid_schedules(course_ls)
    else:
        print("No courses added. Exiting.")    
    