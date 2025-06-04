
import tkinter as tk
from tkinter import messagebox, filedialog, simpledialog
import mysql.connector
import os

class DigiLockerApp:
    def _init_(self, root):
        self.root = root
        self.root.title("DigiLocker System")
        self.root.geometry("800x600")

        # MySQL Database connection
        self.db = mysql.connector.connect(
            host="localhost",  # Your MySQL host (usually localhost)
            user="root",       # Your MySQL username
            password="Pavi@0412",  # Your MySQL password
            database="digilocker"  # The name of your database
        )
        self.cursor = self.db.cursor()
        self.current_user_id = None
        self.show_login()

    def clear(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def show_login(self):
        self.clear()
        frame = tk.Frame(self.root)
        frame.pack(pady=100)

        tk.Label(frame, text="Login", font=("Arial", 16)).pack()
        tk.Label(frame, text="Username").pack()
        self.username_entry = tk.Entry(frame)
        self.username_entry.pack()
        tk.Label(frame, text="Password").pack()
        self.password_entry = tk.Entry(frame, show="*")
        self.password_entry.pack()

        tk.Button(frame, text="Login", command=self.login).pack(pady=5)
        tk.Button(frame, text="Register", command=self.show_register).pack()

    def show_register(self):
        self.clear()
        frame = tk.Frame(self.root)
        frame.pack(pady=100)

        tk.Label(frame, text="Register", font=("Arial", 16)).pack()
        tk.Label(frame, text="Username").pack()
        self.reg_username = tk.Entry(frame)
        self.reg_username.pack()
        tk.Label(frame, text="Password").pack()
        self.reg_password = tk.Entry(frame, show="*")
        self.reg_password.pack()
        tk.Label(frame, text="Email").pack()
        self.reg_email = tk.Entry(frame)
        self.reg_email.pack()

        tk.Button(frame, text="Register", command=self.register).pack(pady=5)
        tk.Button(frame, text="Back", command=self.show_login).pack()

    def register(self):
        u, p, e = self.reg_username.get(), self.reg_password.get(), self.reg_email.get()
        if not u or not p or not e:
            messagebox.showerror("Error", "All fields required.")
            return
        self.cursor.execute("SELECT * FROM users WHERE username=%s OR email=%s", (u, e))
        if self.cursor.fetchone():
            messagebox.showerror("Error", "Username or Email exists.")
            return
        self.cursor.execute("INSERT INTO users (username, password, email) VALUES (%s, %s, %s)", (u, p, e))
        self.db.commit()
        messagebox.showinfo("Success", "Registered successfully.")
        self.show_login()

    def login(self):
        u, p = self.username_entry.get(), self.password_entry.get()
        self.cursor.execute("SELECT id FROM users WHERE username=%s AND password=%s", (u, p))
        user = self.cursor.fetchone()
        if user:
            self.current_user_id = user[0]
            messagebox.showinfo("Welcome", f"Welcome {u}!")
            self.show_dashboard()
        else:
            messagebox.showerror("Failed", "Invalid credentials.")

    def show_dashboard(self):
        self.clear()
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="Dashboard", font=("Arial", 16)).pack(pady=10)

        tk.Button(frame, text="Upload Document", command=self.upload_document).pack(pady=5)
        tk.Button(frame, text="My Documents", command=self.view_documents).pack(pady=5)
        tk.Button(frame, text="Recently Viewed", command=self.view_recently_viewed).pack(pady=5)
        tk.Button(frame, text="Logout", command=self.show_login).pack(pady=10)

    def upload_document(self):
        file = filedialog.askopenfilename()
        if file:
            with open(file, "rb") as f:
                size = len(f.read())
            name = os.path.basename(file)
            self.cursor.execute(
                "INSERT INTO documents (user_id, document_name, file_path, file_size) VALUES (%s, %s, %s, %s)",
                (self.current_user_id, name, file, size)
            )
            self.db.commit()
            messagebox.showinfo("Success", "Document uploaded.")

    def view_documents(self):
        self.clear()
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        tk.Label(frame, text="My Documents", font=("Arial", 16)).pack()

        self.cursor.execute("SELECT id, document_name FROM documents WHERE user_id=%s", (self.current_user_id,))
        docs = self.cursor.fetchall()

        for doc_id, name in docs:
            row = tk.Frame(frame)
            row.pack(pady=2)
            tk.Label(row, text=name).pack(side=tk.LEFT)
            tk.Button(row, text="View", command=lambda d=doc_id: self.view_document_detail(d)).pack(side=tk.LEFT)
            tk.Button(row, text="Update", command=lambda d=doc_id: self.update_document(d)).pack(side=tk.LEFT)
            tk.Button(row, text="Share", command=lambda d=doc_id: self.share_document(d)).pack(side=tk.LEFT)
            tk.Button(row, text="Delete", command=lambda d=doc_id: self.delete_document(d)).pack(side=tk.LEFT)

        tk.Button(frame, text="Back", command=self.show_dashboard).pack(pady=10)

    def view_document_detail(self, doc_id):
        self.clear()
        frame = tk.Frame(self.root)
        frame.pack(pady=20)

        self.cursor.execute("SELECT document_name, file_path, file_size FROM documents WHERE id=%s", (doc_id,))
        doc = self.cursor.fetchone()

        if not doc:
            messagebox.showerror("Error", "Document not found.")
            self.view_documents()
            return

        name, path, size = doc

        # Insert record into recently_viewed
        self.cursor.execute("INSERT INTO recently_viewed (user_id, document_id) VALUES (%s, %s)", (self.current_user_id, doc_id))
        self.db.commit()

        tk.Label(frame, text="Document Details", font=("Arial", 16)).pack(pady=10)
        tk.Label(frame, text=f"Document Name: {name}", font=("Arial", 12)).pack(pady=5)
        tk.Label(frame, text=f"File Path: {path}", font=("Arial", 12)).pack(pady=5)
        tk.Label(frame, text=f"File Size: {size} bytes", font=("Arial", 12)).pack(pady=5)
        tk.Button(frame, text="Back", command=self.view_documents).pack(pady=20)

    def update_document(self, doc_id):
        file = filedialog.askopenfilename()
        if file:
            with open(file, "rb") as f:
                size = len(f.read())
            name = os.path.basename(file)
            self.cursor.execute(
                "UPDATE documents SET document_name=%s, file_path=%s, file_size=%s WHERE id=%s",
                (name, file, size, doc_id)
            )
            self.db.commit()
            messagebox.showinfo("Updated", "Document updated.")
            self.view_documents()

    def share_document(self, doc_id):
        email = simpledialog.askstring("Share", "Enter email to share with:")
        if email:
            self.cursor.execute(
                "INSERT INTO shared_documents (document_id, shared_with_email) VALUES (%s, %s)",
                (doc_id, email)
            )
            self.db.commit()
            messagebox.showinfo("Shared", f"Shared with {email}.")

    def delete_document(self, doc_id):
        self.cursor.execute("DELETE FROM documents WHERE id=%s", (doc_id,))
        self.db.commit()
        messagebox.showinfo("Deleted", "Document deleted.")
        self.view_documents()

    def view_recently_viewed(self):
        self.clear()
        frame = tk.Frame(self.root)
        frame.pack(pady=20)
        tk.Label(frame, text="Recently Viewed", font=("Arial", 16)).pack()

        self.cursor.execute("""
            SELECT d.id, d.document_name, r.viewed_at
            FROM recently_viewed r
            JOIN documents d ON r.document_id = d.id
            WHERE r.user_id = %s
            ORDER BY r.viewed_at DESC
            LIMIT 10
        """, (self.current_user_id,))
        rows = self.cursor.fetchall()

        if not rows:
            tk.Label(frame, text="No recently viewed documents.").pack()

        for doc_id, name, viewed in rows:
            row = tk.Frame(frame)
            row.pack(pady=5)
            tk.Label(row, text=f"{name} (Viewed at: {viewed})").pack(side=tk.LEFT)
            tk.Button(row, text="Open", command=lambda d=doc_id: self.view_document_detail(d)).pack(side=tk.LEFT, padx=5)

        tk.Button(frame, text="Back", command=self.show_dashboard).pack(pady=10)

    def _del_(self):
        if self.db.is_connected():
            self.cursor.close()
            self.db.close()

if _name_ == "_main_":
    root = tk.Tk()
    app = DigiLockerApp(root)
    root.mainloop()
