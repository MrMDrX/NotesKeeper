# Notes Keeper Application

This is a simple Notes Keeper application built with Python using the Tkinter and CustomTkinter library for the GUI, MongoDB as the database, and bcrypt for password hashing. The application allows users to register, log in, and manage their notes.

## Features

- **User Registration:** Users can create a new account by providing their full name, a unique username, and a secure password. Passwords are securely hashed using the bcrypt algorithm.

- **User Login:** Registered users can log in using their username and password. Passwords are securely checked against the stored hashed values in the database.

- **Note Management:** After logging in, users can add, edit, and delete their notes. Notes are stored in the MongoDB database, associated with the user who created them.

## Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/MrMDrX/NotesKeeper.git
   ```

2. **Navigate to the Project Directory:**

   ```bash
   cd NotesKeeper
   ```

3. **Create and Activate a Virtual Environment (Optional but recommended):**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use 'venv\Scripts\activate'
   ```

4. **Install Dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

5. **Run the Application:**
   ```bash
   python app.py
   ```

## Usage

1. **Registration:**

   - Open the application and click on the "Register" button.
   - Enter your full name, a unique username, and a password.
   - Click on the "Register" button.

2. **Login:**

   - After registration, you can log in by clicking on the "Login" button.
   - Enter your username and password.
   - Click on the "Login" button.

3. **Note Management:**
   - Once logged in, you can add a new note by providing a title and content.
   - Select a note from the list to edit or delete it.
   - Use the "Add," "Update," and "Delete" buttons for note management.
   - Click on the "Logout" button to log out.

## Screenshots

- Welcome UI
  ![Welcome UI](https://github.com/MrMDrX/NotesKeeper/blob/main/screenshots/welcome.png)
- Register UI
  ![Welcome UI](https://github.com/MrMDrX/NotesKeeper/blob/main/screenshots/signup.png)
- Login UI
  ![Welcome UI](https://github.com/MrMDrX/NotesKeeper/blob/main/screenshots/login.png)
- Main UI
  ![Welcome UI](https://github.com/MrMDrX/NotesKeeper/blob/main/screenshots/main.png)

## Contributing

If you'd like to contribute to this project, feel free to fork the repository and submit a pull request. You can also open issues for bug reports or feature requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
