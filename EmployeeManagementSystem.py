import tkinter as tk
from tkinter import messagebox
import mysql.connector
from PIL import Image, ImageTk

# Connect to MySQL database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="vaibhav@2004",
    database="employee_management"
)
cursor = conn.cursor()

class EmployeeManagementSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Employee Management System")

        # Create background image
        self.bg_image = Image.open("Data-mgmt-1024x444.jpg")
        new_width = self.bg_image.width * 2  # Double the width
        new_height = self.bg_image.height * 2  # Double the height
        resized_bg_image = self.bg_image.resize((new_width, new_height))
        self.bg_photo = ImageTk.PhotoImage(resized_bg_image)
        self.bg_label = tk.Label(root, image=self.bg_photo)
        self.bg_label.pack(fill="both", expand=True)
        self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        self.create_widgets()

    def create_widgets(self):
        # Calculate the center coordinates of the screen
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        center_x = screen_width // 2
        center_y = screen_height // 2

        # Calculate the width and height of each widget
        widget_width = 100
        widget_height = 30

        # Place each widget at the calculated center coordinates
        self.label_employee_id = tk.Label(self.root, text="Employee ID:", bg="white")
        self.label_employee_id.place(x=center_x - widget_width, y=center_y - 3 * widget_height)
        self.entry_employee_id = tk.Entry(self.root, bg="lightgreen")
        self.entry_employee_id.place(x=center_x, y=center_y - 3 * widget_height)

        self.label_name = tk.Label(self.root, text="Name:", bg="white")
        self.label_name.place(x=center_x - widget_width, y=center_y - 2 * widget_height)
        self.entry_name = tk.Entry(self.root, bg="lightgreen")
        self.entry_name.place(x=center_x, y=center_y - 2 * widget_height)

        self.label_department = tk.Label(self.root, text="Department:", bg="white")
        self.label_department.place(x=center_x - widget_width, y=center_y - widget_height)
        self.entry_department = tk.Entry(self.root, bg="lightgreen")
        self.entry_department.place(x=center_x, y=center_y - widget_height)

        self.label_position = tk.Label(self.root, text="Position:", bg="white")
        self.label_position.place(x=center_x - widget_width, y=center_y)
        self.entry_position = tk.Entry(self.root, bg="lightgreen")
        self.entry_position.place(x=center_x, y=center_y)

        self.button_add = tk.Button(self.root, text="Display Employees", command=self.display_employees, bg="green", fg="white")
        self.button_add.place(x=center_x - 1, y=center_y + 115)
        
        self.button_display = tk.Button(self.root, text="Add Employee", command=self.add_employee, bg="blue", fg="white")
        self.button_display.place(x=center_x, y=center_y + 50)

        self.button_delete = tk.Button(self.root, text="Delete Employee", command=self.delete_employee, bg="red", fg="white")
        self.button_delete.place(x=center_x - 2, y=center_y + 180)


    def add_employee(self):
        employee_id = self.entry_employee_id.get()
        name = self.entry_name.get()
        department = self.entry_department.get()
        position = self.entry_position.get()

        if employee_id and name and department and position:
            try:
                query = "INSERT INTO employees (employee_id, name, department, position) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (employee_id, name, department, position))
                conn.commit()
                messagebox.showinfo("Success", "Employee added successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error occurred: {err}")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def display_employees(self):
        try:
            query = "SELECT * FROM employees"
            cursor.execute(query)
            employees = cursor.fetchall()
            if employees:
                display_text = ""
                for emp in employees:
                    display_text += f"Employee ID: {emp[0]}\n"
                    display_text += f"Name: {emp[1]}\n"
                    display_text += f"Department: {emp[2]}\n"
                    display_text += f"Position: {emp[3]}\n\n"
                messagebox.showinfo("Employees", display_text)
            else:
                messagebox.showinfo("Employees", "No employees found.")
        except mysql.connector.Error as err:
            messagebox.showerror("Error", f"Error occurred: {err}")

    def delete_employee(self):
        employee_id = self.entry_employee_id.get()
        if employee_id:
            try:
                query = "DELETE FROM employees WHERE employee_id = %s"
                cursor.execute(query, (employee_id,))
                conn.commit()
                messagebox.showinfo("Success", "Employee deleted successfully!")
            except mysql.connector.Error as err:
                messagebox.showerror("Error", f"Error occurred: {err}")
        else:
            messagebox.showerror("Error", "Please enter the Employee ID.")

if __name__ == "__main__":
    root = tk.Tk()
    app = EmployeeManagementSystem(root)
    root.mainloop()
