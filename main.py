# main.py - The View Layer
from app.schedule import ScheduleManager

def front_desk_daily_roster(manager, day):
    """Displays a pretty table of all lessons on a given day."""
    print(f"\n--- Daily Roster for {day} ---")
    lessons = manager.get_lessons_for_day(day)
    if not lessons:
        print(f"No lessons found for {day}")
        return
    for item in lessons:
        c = item["course"]
        l = item["lesson"]
        print(f"Lesson ID:{l['lesson_id']} | Course:{c.name} | Time:{l['start_time']} | Room:{l['room']}")


def switch_course(manager, student_id, from_course_id, to_course_id):
    pass


def main():
    """Main function to run the MSMS application."""
    manager = ScheduleManager() # Create ONE instance of the application brain.

    while True:
        print("\n===== MSMS v3 (Object‑Oriented) =====")
        print("1. Student Check‑in")
        print("2. Show daily lesson roster")
        print("q. Quit")
        choice = input("Enter choice: ")

        if choice == '1':
            try:
                sid = int(input("Enter student id: "))
                cid = int(input("Enter course id: "))
                manager.check_in(sid, cid)
            except ValueError:
                print("Error: ID must be number.")
        elif choice == '2':
            day = input("Enter day (e.g., Monday): ")
            front_desk_daily_roster(manager, day)
        elif choice.lower() == 'q':
            print("Exiting program.")
            break
        else:
            print("Invalid option, try again.")


if __name__ == "__main__":
    main()
