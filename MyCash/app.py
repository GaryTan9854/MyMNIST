from flask import Flask, render_template, request, redirect, url_for
import json
from datetime import datetime

app = Flask(__name__)

# --- Load and Save Expenses Functions ---
def load_expenses(filename="expenses.json"):
    """Loads expenses from a JSON file. Creates an empty file if it doesn't exist."""
    try:
        with open(filename, "r") as f:
            try:  # Nested try to catch JSON-specific errors
                return json.load(f)
            except json.JSONDecodeError:
                print(f"Warning: File '{filename}' contained invalid JSON. Returning empty list.")
                return []  # Return empty list
    except FileNotFoundError:
        print(f"Info: File '{filename}' not found. Creating an empty file.")
        with open(filename, "w") as f: # Create the file if it doesn't exist
            json.dump([], f) # Initialize with an empty JSON list
        return []  # Return empty list

def save_expenses(expenses, filename="expenses.json"):
    """Saves expenses to a JSON file."""
    with open(filename, "w") as f:
        json.dump(expenses, f, indent=4)  # Use indent for pretty formatting


def add_expense(expenses, category, subcategory, date_str, amount, description=""):
    """Adds a new expense."""
    try:
        date = datetime.strptime(date_str, "%Y-%m-%d").date()  # Parse date
    except ValueError:
        print("Invalid date format. Use YYYY-MM-DD.")
        return

    new_expense = {
        "category": category,
        "subcategory": subcategory,
        "date": date.strftime("%Y-%m-%d"),  # Store date as string
        "amount": float(amount),  # Convert amount to float
        "description": description,
    }
    expenses.append(new_expense)
    print("Expense added successfully!")


# --- Categories and Subcategories ---
CATEGORIES = {
    "Eat and Drink": ["Breakfast", "Lunch", "Dinner/Supper", "Big Meal", "Routine meal + milk + fruits", "Hair Cut", "Misc", "Groceries"],
    "Buy/Spending items": ["Small Items / Clothes", "Big Items", "Medical (vitamin 保健品 etc)", "傢俱修繕"],
    "House hold": ["Rental", "Internet+ Water", "House Mgt Fee+Car Park", "Cleaning", "Electric", "Water", "Gas", "Wash car", "Television + Internet", "Services (KKBox, NetFilx,tidal)"],
    "家庭成員": ["Yiming", "Jiayu", "Zaotian", "Anna", "Jupiter", "Mer"],
    "Insurance": ["Insurance-健保、年金", "Insurance-Life", "Insurance-Car/Motor/House", "Car-Fine, service etc", "Tax"],
    "RedPacket": ["RedPacket-PT", "RedPacket-Home (Hong, mer, noelle)", "RedPackel-others"],
    "Gary": ["Mobile Xox", "Allowance", "Leisure/Sports", "Learning", "Travel&BzTraval", "Gifts & others", "應酬"]
}

@app.route("/input", methods=["GET", "POST"])
def input():
    expenses = load_expenses()
    default_date = datetime.now().strftime("%Y-%m-%d")

    if request.method == "POST":
        category = request.form.get("category")
        subcategory = request.form.get("subcategory")
        date = request.form.get("date")
        amount = request.form.get("amount")
        description = request.form.get("description")

        add_expense(expenses, category, subcategory, date, amount, description)
        save_expenses(expenses)  # Save expenses
        return redirect(url_for('input'))

    return render_template("input.html", expenses=expenses, categories=CATEGORIES, default_date=default_date)


@app.route("/summary")
def summary():
    expenses = load_expenses()

    # 處理日期格式
    for expense in expenses:
        date_obj = datetime.strptime(expense['date'], '%Y-%m-%d')
        expense['month'] = date_obj.strftime('%Y-%m')

    # 建立 Excel 表格資料結構
    excel_data = {}
    for expense in expenses:
        month = expense['month']
        item = expense['subcategory']
        amount = expense['amount']

        if month not in excel_data:
            excel_data[month] = {}

        if item not in excel_data[month]:
            excel_data[month][item] = 0

        excel_data[month][item] += amount

    # 將資料轉換為 Excel 表格格式
    table_data = []
    header = ['項目'] + list(excel_data.keys())
    table_data.append(header)

    items = set()
    for month_data in excel_data.values():
        items.update(month_data.keys())

    for item in items:
        row = [item]
        for month in excel_data.keys():
            row.append(excel_data[month].get(item, 0))
        table_data.append(row)

    return render_template("summary.html", table_data=table_data)


# --- Flask Routes ---
@app.route("/", methods=["GET", "POST"])
def index():
    return redirect(url_for('input')) # 預設進入輸入畫面


if __name__ == "__main__":
    app.run(debug=True)