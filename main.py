import tkinter as tk
from tkinter import messagebox, ttk
import csv
from datetime import datetime  
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
is_dashboard_created = False
def show_login_screen():
    """ Display the login screen. """
    login_window = tk.Toplevel()
    login_window.title("Login - FinTrack")
    login_window.geometry("500x400")
    login_window.config(bg="#A7C3FB")
    title_label = tk.Label(login_window, text="FinTrack", font=("Arial", 30, "bold"), fg="#003366", bg="#A7C3FB")
    title_label.pack(pady=20)
    subtitle_label = tk.Label(login_window, text="Your Personal Finance Tracker", font=("Arial", 14, "italic"), fg="#333333", bg="#A7C3FB")
    subtitle_label.pack(pady=5)
    username_label = tk.Label(login_window, text="Username:", font=("Arial", 14), bg="#A7C3FB")
    username_label.pack(pady=10)
    username_entry = tk.Entry(login_window, font=("Arial", 12), width=30)
    username_entry.pack(pady=5)
    password_label = tk.Label(login_window, text="Password:", font=("Arial", 14), bg="#A7C3FB")
    password_label.pack(pady=10)
    password_entry = tk.Entry(login_window, font=("Arial", 12), show="*", width=30)
    password_entry.pack(pady=5)
    def validate_login():
        username = username_entry.get()
        password = password_entry.get()

        if username == "aa" and password == "aa":
            login_window.destroy()
            home.deiconify()
            if not is_dashboard_created:
                show_dashboard()
        else:
            messagebox.showerror("Login Error", "Incorrect username or password")

    login_button = tk.Button(
        login_window, text="Login", font=("Arial", 16, "bold"),
        command=validate_login, width=20, height=2, bg="#005B96", fg="white"
    )
    login_button.pack(pady=25)

    home.withdraw()
def clear_main_frame():
    """ Clears the content of the main frame """
    for widget in main_frame.winfo_children():
        widget.destroy()
def get_current_month():
    """Return current month in YYYY-MM format."""
    return datetime.now().strftime("%Y-%m")
def add_transaction(category_entry, amount_entry, transaction_type_var, category_label, category_input, transaction_tree):
    """ Add new transaction based on user input and save to respective file """
    category = category_entry.get()
    amount = amount_entry.get()
    transaction_type = transaction_type_var.get()
    if not category or not amount:
        messagebox.showwarning("Input Error", "Please fill all fields")
        return

    try:
        amount = float(amount)
    except ValueError:
        messagebox.showwarning("Input Error", "Please enter a valid number for amount")
        return
    current_date = datetime.now().strftime("%Y-%m-%d") 
    if transaction_type == "Expense":
        with open('expenses.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([category, amount, current_date])
    else:
        with open('income.csv', mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([category, amount, current_date])

    messagebox.showinfo("Success", f"{transaction_type} added successfully")
    category_entry.delete(0, tk.END)
    amount_entry.delete(0, tk.END)
    update_transaction_history(transaction_tree)

    if transaction_type == "Expense":
        current_month = get_current_month() 
        spent = 0.0
        try:
            with open('expenses.csv', mode='r') as f:
                reader = csv.reader(f)
                for row in reader:
                    try:
                        row_cat = row[0]
                        row_amt = float(row[1])
                        row_date = row[2]  # YYYY-MM-DD
                        if row_cat == category and row_date.startswith(current_month):
                            spent += row_amt
                    except Exception:
                        continue
        except FileNotFoundError:
            spent = amount  
        budget_amt = None
        try:
            with open('budget.csv', mode='r') as f:
                reader = csv.reader(f)
                for row in reader:
                    if len(row) >= 3 and row[0] == category and row[2] == current_month:
                        try:
                            budget_amt = float(row[1])
                        except:
                            budget_amt = None
                        break
        except FileNotFoundError:
            budget_amt = None

        if budget_amt is not None and spent > budget_amt:
            messagebox.showwarning("Budget Exceeded", f"You have exceeded the budget for '{category}' this month.\nBudget: ₹{budget_amt:.2f}\nSpent: ₹{spent:.2f}")

def show_add_transaction_screen():
    clear_main_frame()

   
    input_frame = tk.Frame(main_frame, bg="#A7C3FB")
    input_frame.pack(pady=40)

    transaction_type_var = tk.StringVar(value="Expense")  

    
    def update_category_state():
        if transaction_type_var.get() == "Income":
            category_combobox.set("Income")
            category_combobox.config(state="disabled")  
        else:
            category_combobox.config(state="readonly")  
            category_combobox.set("Select Category")

    
    expense_radio = tk.Radiobutton(
        input_frame, text="Expense", variable=transaction_type_var, value="Expense",
        font=("Arial", 12), bg="#A7C3FB", command=update_category_state
    )
    expense_radio.grid(row=0, column=0, padx=10, pady=10)

    income_radio = tk.Radiobutton(
        input_frame, text="Income", variable=transaction_type_var, value="Income",
        font=("Arial", 12), bg="#A7C3FB", command=update_category_state
    )
    income_radio.grid(row=0, column=1, padx=10, pady=10)

 
    category_label = tk.Label(input_frame, text="Category:", font=("Arial", 12), bg="#A7C3FB")
    category_label.grid(row=1, column=0, padx=10, pady=10)

    categories = ["Rent", "Utilities", "Home Essentials", "Food", "Travel", "Medical"]
    category_combobox = ttk.Combobox(input_frame, values=categories, font=("Arial", 12), state="readonly")
    category_combobox.grid(row=1, column=1, padx=10, pady=10)
    category_combobox.set("Select Category")

    amount_label = tk.Label(input_frame, text="Amount:", font=("Arial", 12), bg="#A7C3FB")
    amount_label.grid(row=2, column=0, padx=10, pady=10)

    amount_entry = tk.Entry(input_frame, font=("Arial", 12))
    amount_entry.grid(row=2, column=1, padx=10, pady=10)
 
    add_button = tk.Button(
        input_frame, text="Add Transaction", font=("Arial", 12),
        command=lambda: add_transaction(
            category_combobox, amount_entry, transaction_type_var,
            category_label, category_combobox, transaction_tree
        ),
        width=20, height=2, bg="#005B96", fg="white"
    )
    add_button.grid(row=3, columnspan=2, pady=20)
    transaction_tree = ttk.Treeview(
        input_frame, columns=("Category", "Amount", "Type", "Date"),
        show="headings", height=20
    )
    transaction_tree.heading("Category", text="Category")
    transaction_tree.heading("Amount", text="Amount")
    transaction_tree.heading("Type", text="Type")
    transaction_tree.heading("Date", text="Date")
    transaction_tree.grid(row=4, columnspan=4, pady=40)

    update_transaction_history(transaction_tree)

def show_dashboard():
    global is_dashboard_created

    if not is_dashboard_created:
        dash.place(x=0, y=0)

        title_label = tk.Label(dash, text="FinTrack", font=("Arial", 24, "bold"), bg="#2F739D", fg="white")
        title_label.pack(pady=20)

        add_expense_income_button = tk.Button(dash, text="Add Expense / Income", font=("Arial", 16), command=show_add_transaction_screen, width=20, height=2, bg="#005B96", fg="white")
        add_expense_income_button.pack(pady=10)

        budget_management_button = tk.Button(dash, text="Budget Management", font=("Arial", 16), command=show_budget_management_screen, width=20, height=2, bg="#005B96", fg="white")
        budget_management_button.pack(pady=10)

        reports_charts_button = tk.Button(dash, text="Reports and Charts", font=("Arial", 16), command=show_reports_screen, width=20, height=2, bg="#005B96", fg="white")
        reports_charts_button.pack(pady=10)

        logout_button = tk.Button(dash, text="Logout", font=("Arial", 16), command=logout, width=20, height=2, bg="#D32F2F", fg="white")
        logout_button.pack(pady=20)

        is_dashboard_created = True

    clear_main_frame()
    show_add_transaction_screen()

def logout():
    home.withdraw()
    show_login_screen()  

def show_budget_management_screen():
    clear_main_frame()

    budget_label = tk.Label(main_frame, text="Budget Management", font=("Arial", 24, "bold"), bg="#A7C3FB")
    budget_label.pack(pady=20)

    budget_info_label = tk.Label(main_frame, text="Here you can manage your budget.", font=("Arial", 16), bg="#A7C3FB")
    budget_info_label.pack(pady=10)
def set_budget(category, amount_str, budget_tree=None):
    """Set or update the budget for the current month for a category."""
    if not category or category == "Select Category":
        messagebox.showwarning("Input Error", "Please select a category")
        return
    try:
        amount = float(amount_str)
    except ValueError:
        messagebox.showwarning("Input Error", "Enter a valid number for budget amount")
        return

    month = get_current_month()
    rows = []
    found = False
    # Read existing budgets
    try:
        with open('budget.csv', mode='r', newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3 and row[0] == category and row[2] == month:
                    rows.append([category, f"{amount:.2f}", month])
                    found = True
                else:
                    rows.append(row)
    except FileNotFoundError:
        rows = []

    if not found:
        rows.append([category, f"{amount:.2f}", month])

    with open('budget.csv', mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(rows)

    messagebox.showinfo("Budget Saved", f"Budget for '{category}' set to ₹{amount:.2f} for {month}")
    if budget_tree:
        update_budget_table(budget_tree)

def update_budget_table(budget_tree):
    """Populate the budget_tree with Category | Budget | Spent | Remaining | Status for current month."""
    for r in budget_tree.get_children():
        budget_tree.delete(r)

    month = get_current_month()


    budgets = {}
    try:
        with open('budget.csv', mode='r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3 and row[2] == month:
                    try:
                        budgets[row[0]] = float(row[1])
                    except:
                        budgets[row[0]] = 0.0
    except FileNotFoundError:
        budgets = {}

    spent = {}  
    try:
        with open('expenses.csv', mode='r') as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    cat = row[0]
                    amt = float(row[1])
                    date = row[2]
                except Exception:
                    continue
                if date.startswith(month):
                    spent[cat] = spent.get(cat, 0.0) + amt
    except FileNotFoundError:
        spent = {}
    all_categories = set(list(budgets.keys()) + list(spent.keys()))
    for cat in sorted(all_categories):
        b_amt = budgets.get(cat, 0.0)
        s_amt = spent.get(cat, 0.0)
        remaining = b_amt - s_amt
        if b_amt == 0:
            status = "No Budget Set"
        else:
            pct = (s_amt / b_amt) * 100
            if pct < 75:
                status = "Within Limit"
            elif pct < 100:
                status = "Near Limit"
            else:
                status = "Exceeded"

        budget_tree.insert("", "end", values=(cat, f"₹{b_amt:.2f}", f"₹{s_amt:.2f}", f"₹{remaining:.2f}", status))
def create_budget_bar_chart(parent_frame):
    """Create a Budget vs Spent bar chart for current month and embed into the given parent_frame."""
    month = get_current_month()
    budgets = {}
    try:
        with open('budget.csv', mode='r') as f:
            reader = csv.reader(f)
            for row in reader:
                if len(row) >= 3 and row[2] == month:
                    try:
                        budgets[row[0]] = float(row[1])
                    except:
                        budgets[row[0]] = 0.0
    except FileNotFoundError:
        messagebox.showinfo("No Data", "No budgets set yet for the current month.")
        return

    spent = {}
    try:
        with open('expenses.csv', mode='r') as f:
            reader = csv.reader(f)
            for row in reader:
                try:
                    cat = row[0]; amt = float(row[1]); date = row[2]
                except:
                    continue
                if date.startswith(month):
                    spent[cat] = spent.get(cat, 0.0) + amt
    except FileNotFoundError:
        spent = {}

    categories = sorted(list(set(list(budgets.keys()) + list(spent.keys()))))
    if not categories:
        messagebox.showinfo("No Data", "No budgets or expenses data to show for chart.")
        return

    budget_values = [budgets.get(c, 0.0) for c in categories]
    spent_values = [spent.get(c, 0.0) for c in categories]

    fig, ax = plt.subplots(figsize=(6, 4))
    x = range(len(categories))
    ax.bar([i - 0.15 for i in x], budget_values, width=0.3, label='Budget')
    ax.bar([i + 0.15 for i in x], spent_values, width=0.3, label='Spent')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right')
    ax.set_ylabel('Amount (₹)')
    ax.set_title(f'Budget vs Spent ({month})')
    ax.legend()
    fig.tight_layout()

    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    widget = canvas.get_tk_widget()
    widget.pack(pady=10)
def show_budget_management_screen():
    clear_main_frame()

    tk.Label(main_frame, text="Budget Management", font=("Arial", 24, "bold"), bg="#A7C3FB").pack(pady=10)

    # Input frame
    input_frame = tk.Frame(main_frame, bg="#A7C3FB")
    input_frame.pack(pady=10, fill="x")

    tk.Label(input_frame, text="Category:", font=("Arial", 12), bg="#A7C3FB").grid(row=0, column=0, padx=10, pady=8, sticky="w")
    categories = ["Rent", "Utilities", "Home Essentials", "Food", "Travel", "Medical"]
    category_box = ttk.Combobox(input_frame, values=categories, state="readonly", font=("Arial", 12), width=20)
    category_box.grid(row=0, column=1, padx=10, pady=8)
    category_box.set("Select Category")

    tk.Label(input_frame, text="Budget Amount (₹):", font=("Arial", 12), bg="#A7C3FB").grid(row=0, column=2, padx=10, pady=8, sticky="w")
    budget_entry = tk.Entry(input_frame, font=("Arial", 12), width=15)
    budget_entry.grid(row=0, column=3, padx=10, pady=8)

    budget_tree_holder = tk.Frame(main_frame, bg="#A7C3FB")
    budget_tree_holder.pack(pady=10, fill="both", expand=False)

    tk.Button(input_frame, text="Set Budget", font=("Arial", 12), bg="#005B96", fg="white",
              command=lambda: set_budget(category_box.get(), budget_entry.get(), budget_tree)).grid(row=0, column=4, padx=10)
    cols = ("Category", "Budget", "Spent", "Remaining", "Status")
    budget_tree = ttk.Treeview(budget_tree_holder, columns=cols, show="headings", height=8)
    for c in cols:
        budget_tree.heading(c, text=c)
        budget_tree.column(c, width=120, anchor="center")
    budget_tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)


    sb = ttk.Scrollbar(budget_tree_holder, orient="vertical", command=budget_tree.yview)
    budget_tree.configure(yscroll=sb.set)
    sb.pack(side="right", fill="y")

    update_budget_table(budget_tree)

    chart_frame = tk.Frame(main_frame, bg="#A7C3FB")
    chart_frame.pack(pady=5, fill="both", expand=False)

   
    tk.Button(chart_frame, text="Show Budget vs Spent Chart", font=("Arial", 12), bg="#005B96", fg="white",
              command=lambda: [  # clear previous chart widgets
                  [w.destroy() for w in chart_frame.winfo_children()],
                  create_budget_bar_chart(chart_frame)
              ]).pack(pady=10)


def show_reports_screen():
    clear_main_frame()

    reports_label = tk.Label(main_frame, text="Reports and Charts", font=("Arial", 24, "bold"), bg="#A7C3FB")
    reports_label.pack(pady=20)

    reports_info_label = tk.Label(main_frame, text="Here you can view your financial reports.", font=("Arial", 16), bg="#A7C3FB")
    reports_info_label.pack(pady=10)

def update_transaction_history(transaction_tree):
    for row in transaction_tree.get_children():
        transaction_tree.delete(row)

    try:
        with open('expenses.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                transaction_tree.insert("", "end", values=(row[0], row[1], "Expense", row[2]))
    except FileNotFoundError:
        pass

    try:
        with open('income.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                transaction_tree.insert("", "end", values=(row[0], row[1], "Income", row[2]))
    except FileNotFoundError:
        pass

home = tk.Tk()
home.title("Fintrack")
width = home.winfo_screenwidth()
height = home.winfo_screenheight()
home.geometry(f"{width}x{height}+0+0")
home.config(bg="#A7C3FB")
dash = tk.Frame(home, width=350, height=800, background="#2F739D")
dash.place(x=0, y=0)
dash.pack_propagate(False)
main_frame = tk.Frame(home, bg="#A7C3FB", height=800, width=1150)
main_frame.place(x=350, y=0)
main_frame.pack_propagate(False)


show_login_screen()
def show_reports_screen():
    clear_main_frame()

    reports_label = tk.Label(main_frame, text="Reports and Charts", font=("Arial", 24, "bold"), bg="#A7C3FB")
    reports_label.pack(pady=20)

    reports_info_label = tk.Label(main_frame, text="Your financial summary and analysis", font=("Arial", 16), bg="#A7C3FB")
    reports_info_label.pack(pady=10)
    total_income = 0
    total_expense = 0

    try:
        with open('income.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                total_income += float(row[1])
    except FileNotFoundError:
        pass

    try:
        with open('expenses.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                total_expense += float(row[1])
    except FileNotFoundError:
        pass
    summary_frame = tk.Frame(main_frame, bg="#A7C3FB")
    summary_frame.pack(pady=20)

    income_label = tk.Label(summary_frame, text=f"Total Income: ₹{total_income:.2f}", font=("Arial", 16, "bold"), fg="green", bg="#A7C3FB")
    income_label.grid(row=0, column=0, padx=40, pady=10)

    expense_label = tk.Label(summary_frame, text=f"Total Expense: ₹{total_expense:.2f}", font=("Arial", 16, "bold"), fg="red", bg="#A7C3FB")
    expense_label.grid(row=0, column=1, padx=40, pady=10)
    balance = total_income - total_expense
    balance_color = "green" if balance >= 0 else "red"
    balance_label = tk.Label(summary_frame, text=f"Net Balance: ₹{balance:.2f}", font=("Arial", 16, "bold"), fg=balance_color, bg="#A7C3FB")
    balance_label.grid(row=1, column=0, columnspan=2, pady=10) 
    create_expense_pie_chart()

def create_expense_pie_chart():
    categories = {}
    
    try:
        with open('expenses.csv', mode='r') as file:
            reader = csv.reader(file)
            for row in reader:
                category = row[0]
                amount = float(row[1])
                categories[category] = categories.get(category, 0) + amount
    except FileNotFoundError:
        messagebox.showerror("File Error", "Expenses CSV file not found.")
        return
    if not categories:
        messagebox.showinfo("No Data", "No expenses data available to show.")
        return
    labels = list(categories.keys())
    sizes = list(categories.values())
    fig, ax = plt.subplots(figsize=(10, 5))  
    wedges, texts, autotexts = ax.pie(
        sizes, labels=labels, autopct='%1.1f%%', startangle=90, 
        colors=plt.cm.Paired.colors, textprops={'fontsize': 10}
    )
    ax.axis('equal')
    canvas = FigureCanvasTkAgg(fig, master=main_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(pady=30)

    pie_chart_description = tk.Label(main_frame, text="Expense Breakdown by Category", font=("Arial", 16), bg="#A7C3FB")
    pie_chart_description.pack(pady=10)
home.mainloop()
