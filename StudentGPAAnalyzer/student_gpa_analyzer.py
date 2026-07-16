import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd


class GPAApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student GPA and Ranking")
        self.data = None

        tk.Label(root, text="Open file:").grid(row=0, column=0, padx=10, pady=5)
        tk.Button(root, text="Browse", command=self.load_file).grid(
            row=0, column=1, padx=10, pady=5
        )

        tk.Label(root, text="ID:").grid(row=1, column=0, padx=10, pady=5)
        self.id_entry = tk.Entry(root)
        self.id_entry.grid(row=1, column=1, padx=10, pady=5)

        self.name_label = tk.Label(root, text="Name Surname:")
        self.name_label.grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        self.gpa_label = tk.Label(root, text="GPA:")
        self.gpa_label.grid(row=3, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        self.rank_label = tk.Label(root, text="Rank:")
        self.rank_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=10, pady=5)

        tk.Label(root, text="Select file type:").grid(
            row=5, column=0, padx=10, pady=5
        )
        self.file_type_var = tk.StringVar(value=".txt")
        tk.OptionMenu(root, self.file_type_var, ".txt", ".xlsx").grid(
            row=5, column=1, padx=10, pady=5
        )

        tk.Button(root, text="Display", command=self.display_student).grid(
            row=6, column=0, padx=10, pady=5
        )
        tk.Button(root, text="Export", command=self.export_file).grid(
            row=6, column=1, padx=10, pady=5
        )
        tk.Button(root, text="Clear", command=self.clear_labels).grid(
            row=7, column=0, columnspan=2, pady=5
        )

    def load_file(self):
        file_path = filedialog.askopenfilename(
            filetypes=[("Excel Files", "*.xlsx")]
        )
        if not file_path:
            return

        try:
            self.data = pd.read_excel(file_path)

            required_columns = {
                "ID",
                "Name",
                "Physics",
                "Calculus",
                "Advanced Programming",
                "Chemistry",
            }
            missing_columns = required_columns.difference(self.data.columns)
            if missing_columns:
                raise ValueError(
                    "Missing columns: " + ", ".join(sorted(missing_columns))
                )

            self.data["GPA"] = (
                self.data["Physics"] * 0.25
                + self.data["Calculus"] * 0.25
                + self.data["Advanced Programming"] * 0.30
                + self.data["Chemistry"] * 0.20
            )
            self.data["Rank"] = (
                self.data["GPA"].rank(method="min", ascending=False).astype(int)
            )

            messagebox.showinfo("Success", "File loaded successfully!")
        except Exception as error:
            self.data = None
            messagebox.showerror("Error", f"Could not load file: {error}")

    def display_student(self):
        if self.data is None:
            messagebox.showwarning("Warning", "Please load a file first!")
            return

        student_id = self.id_entry.get().strip()
        if not student_id.isdigit():
            messagebox.showwarning("Warning", "Invalid ID format!")
            return

        student = self.data[self.data["ID"] == int(student_id)]
        if student.empty:
            messagebox.showwarning("Warning", "Student not found!")
            return

        row = student.iloc[0]
        self.name_label.config(text=f"Name Surname: {row['Name']}")
        self.gpa_label.config(text=f"GPA: {row['GPA']:.2f}")
        self.rank_label.config(text=f"Rank: {row['Rank']}")

    def export_file(self):
        if not self.name_label.cget("text").startswith("Name Surname:"):
            messagebox.showwarning("Warning", "No data to export!")
            return

        student_id = self.id_entry.get().strip()
        student = self.data[self.data["ID"] == int(student_id)].iloc[0]
        student_name = str(student["Name"]).replace(" ", "_")
        file_type = self.file_type_var.get()
        file_name = f"{student_id}_{student_name}{file_type}"

        try:
            if file_type == ".txt":
                with open(file_name, "w", encoding="utf-8") as file:
                    file.write(f"{self.name_label.cget('text')}\n")
                    file.write(f"{self.gpa_label.cget('text')}\n")
                    file.write(f"{self.rank_label.cget('text')}\n")
            else:
                pd.DataFrame(
                    [
                        {
                            "ID": int(student_id),
                            "Name Surname": student["Name"],
                            "GPA": round(float(student["GPA"]), 2),
                            "Rank": int(student["Rank"]),
                        }
                    ]
                ).to_excel(file_name, index=False)

            messagebox.showinfo("Success", f"File exported as {file_name}")
        except Exception as error:
            messagebox.showerror("Error", f"Could not export file: {error}")

    def clear_labels(self):
        self.id_entry.delete(0, tk.END)
        self.name_label.config(text="Name Surname:")
        self.gpa_label.config(text="GPA:")
        self.rank_label.config(text="Rank:")


if __name__ == "__main__":
    root = tk.Tk()
    GPAApp(root)
    root.mainloop()
