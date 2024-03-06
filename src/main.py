import json
import datetime
import re

DATABASE_FILE = 'database.json'

def load_data():
    try:
        with open(DATABASE_FILE, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {'users': [], 'projects': []}

def save_data(data):
    with open(DATABASE_FILE, 'w') as file:
        json.dump(data, file, indent=4)

def validate_email(email):
    email_regex = r'^[\w-]+(\.[\w-]+)*@([\w-]+\.)+[a-zA-Z]{2,7}$'
    return re.match(email_regex, email)

def validate_phone(phone):
    phone_regex = r'^01[0-2]{1}[0-9]{8}$'
    return re.match(phone_regex, phone)

def register():
    data = load_data()
    first_name = input("enter your first name ")
    last_name = input("enter your last name ")
    email = input("enter your email ")
    while not validate_email(email):
        print("invalid email format... Please enter a valid email!!")
        email = input("enter your email ")
    password = input("enter your password")
    confirm_password = input("confirm your password pleaseee")
    while password != confirm_password:
        print("passwords dont matches please write it agaaain !!")
        password = input("enter your password: ")
        confirm_password = input("confirm your password ")
    phone = input("enter your phone number ")
    while not validate_phone(phone):
        print("invalid egyptian phone number!!!")
        phone = input("enter your mobile phone number agaiiin ")
    user = {
        'first_name': first_name,
        'last_name': last_name,
        'email': email,
        'password': password,
        'phone': phone
    }
    data['users'].append(user)
    save_data(data)
    print("registration successfulyyy :)")

def login():
    data = load_data()
    email = input("enter your email ")
    password = input("enter your password ")
    for user in data['users']:
        if user['email'] == email and user['password'] == password:
            print("login successfulyyy :)")
            return user
    print("invalid email or password.")
    return None

def create_project(user):
    data = load_data()
    title = input("enter project title ")
    details = input("enter project details ")
    target = float(input("enter total target amount "))
    start_date = input("enter start date (YYYY-MM-DD) ")
    end_date = input("enter end date (YYYY-MM-DD) ")
    while True:
        try:
            start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
            end_date = datetime.datetime.strptime(end_date, '%Y-%m-%d')
            break
        except ValueError:
            print("invalid date format. please enter the date in YYYY-MM-DD format")
            start_date = input("enter start date (YYYY-MM-DD) ")
            end_date = input("enter end date (YYYY-MM-DD) ")
    project = {
        'title': title,
        'details': details,
        'target': target,
        'start_date': start_date.strftime('%Y-%m-%d'),
        'end_date': end_date.strftime('%Y-%m-%d'),
        'user_email': user['email']
    }
    data['projects'].append(project)
    save_data(data)
    print("project created successfullyyyy.")
    
def view_projects():
    data = load_data()
    if not data['projects']:
        print("No projects exist yet")
    else:
        for project in data['projects']:
            print(f"Title: {project['title']}")
            print(f"Details: {project['details']}")
            print(f"Target: {project['target']} EGP")
            print(f"Start Date: {project['start_date']}")
            print(f"End Date: {project['end_date']}")
            print("---------------------------------------")

def edit_project(user):
    data = load_data()
    view_projects()
    project_title = input("enter the title of the project you want to edit ")
    for project in data['projects']:
        if project['user_email'] == user['email'] and project['title'] == project_title:
            new_title = input("enter new title")
            if new_title.strip():
                project['title'] = new_title
            new_details = input("enter new details")
            if new_details.strip():
                project['details'] = new_details
            new_target = input("enter new target amount")
            if new_target.strip():
                project['target'] = float(new_target)
            new_start_date = input("enter new start date (YYYY-MM-DD)")
            if new_start_date.strip():
                project['start_date'] = new_start_date
            new_end_date = input("enter new end date (YYYY-MM-DD)")
            if new_end_date.strip():
                project['end_date'] = new_end_date
            save_data(data)
            print("project edited successfullyyy :)")
            return
    print(" project does not exist!!!")

def delete_project(user):
    data = load_data()
    view_projects()
    project_title = input("enter the title of the project you want to delete pleaseee ")
    for project in data['projects']:
        if project['user_email'] == user['email'] and project['title'] == project_title:
            data['projects'].remove(project)
            save_data(data)
            print("project deleted successfullyyyy")
            return
    print(" project does not exist!!!")


def main():
    while True:
        print("\nWelcome to Crowdfunding Console App")
        print("1. Register")
        print("2. Login")
        print("3. Create Project")
        print("4. View Projects")
        print("5. Edit Project")
        print("6. Delete Project")
        print("7. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            register()
        elif choice == '2':
            user = login()
            if user:
                while True:
                    print("\n1. Create Project")
                    print("2. View Projects")
                    print("3. Edit Project")
                    print("4. Delete Project")
                    print("5. Logout")
                    choice = input("Enter your Choice: ")
                    if choice == '1':
                        create_project(user)
                    elif choice == '2':
                        view_projects()
                    elif choice == '3':
                        edit_project(user)
                    elif choice == '4':
                        delete_project(user)
                    elif choice == '5':
                        break
                    else:
                        print("Invalid choice. Please try again...")
        elif choice == '3':
            print("please login first to create a project.")
        elif choice == '4':
            view_projects()
        elif choice == '5':
            print("please login first to edit a project.")
        elif choice == '6':
            print("please login first to delete a project.")
        elif choice == '7':
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
