import json
from datetime import datetime

# ------------------ FILE HANDLING ------------------

def load_queue():
    try:
        with open("queue.json", "r") as f:
            return json.load(f)
    except:
        return []

def save_queue(queue):
    with open("queue.json", "w") as f:
        json.dump(queue, f, indent=4)

# ------------------ CORE FUNCTIONS ------------------

def take_ticket(queue, ticket_number):
    name = input("Enter your name: ").strip()

    while True:
        priority = input("Priority (normal/vip): ").lower()
        if priority in ["normal", "vip"]:
            break
        print("Invalid priority. Try again.")

    person = {
        "name": name,
        "ticket": ticket_number,
        "priority": priority,
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

    queue.append(person)

    print(f"\n✅ Ticket #{ticket_number} assigned to {name}")
    return ticket_number + 1


def call_next(queue, served_count):
    if not queue:
        print("\n⚠️ Queue is empty")
        return served_count

    # Check VIP first
    for i, person in enumerate(queue):
        if person["priority"] == "vip":
            next_person = queue.pop(i)
            print(f"\n🔔 Calling VIP {next_person['name']} (Ticket #{next_person['ticket']})")
            return served_count + 1

    # Otherwise normal
    next_person = queue.pop(0)
    print(f"\n🔔 Calling {next_person['name']} (Ticket #{next_person['ticket']})")
    return served_count + 1


def view_queue(queue):
    if not queue:
        print("\n📭 Queue is empty")
        return

    print("\n📋 Current Queue:")
    for person in queue:
        print(f"#{person['ticket']} | {person['name']} | {person['priority']} | {person['time']}")


def show_statistics(served_count, queue):
    print("\n📊 Statistics:")
    print(f"People served: {served_count}")
    print(f"People waiting: {len(queue)}")

# ------------------ MAIN PROGRAM ------------------

def main():
    queue = load_queue()
    ticket_number = len(queue) + 1
    served_count = 0

    ADMIN_PASSWORD = "1234"

    while True:
        print("\n====== SMART QUEUE SYSTEM ======")
        print("1. Take Ticket")
        print("2. Call Next (Admin)")
        print("3. View Queue")
        print("4. Show Statistics")
        print("5. Exit")

        try:
            choice = int(input("Choose an option: "))
        except:
            print("❌ Invalid input. Enter a number.")
            continue

        if choice == 1:
            ticket_number = take_ticket(queue, ticket_number)

        elif choice == 2:
            password = input("Enter admin password: ")
            if password == ADMIN_PASSWORD:
                served_count = call_next(queue, served_count)
            else:
                print("❌ Wrong password")

        elif choice == 3:
            view_queue(queue)

        elif choice == 4:
            show_statistics(served_count, queue)

        elif choice == 5:
            save_queue(queue)
            print("\n💾 Queue saved. Goodbye!")
            break

        else:
            print("❌ Invalid choice")

# ------------------ RUN ------------------

if __name__ == "__main__":
    main()


