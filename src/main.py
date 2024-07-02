import argparse
import pandas as pd
import matplotlib.pyplot as plt
import os, datetime


class FinanceApp:
    def __init__(self, csv_file="finance.csv"):
        self.csv_file = csv_file
        if os.path.exists(self.csv_file):
            self.df = pd.read_csv(self.csv_file)
        else:
            self.df = pd.DataFrame(columns=["date", "from", "amount", "type"])

    def add_income(self, amount, date=None, from_=None):
        if date is None:
            date = datetime.datetime.now().strftime("%d.%m.%y")
        if from_ is None:
            from_ = "Job"
        self.df = self.df._append(
            {"date": date, "from": from_, "amount": amount, "type": "income"},
            ignore_index=True,
        )
        self.df.to_csv(self.csv_file, index=False)

    def add_expense(self, amount, date=None, from_=None):
        if date is None:
            date = datetime.datetime.now().strftime("%d.%m.%y")
        if from_ is None:
            from_ = "Div"
        self.df = self.df._append(
            {"date": date, "from": from_, "amount": amount, "type": "expense"},
            ignore_index=True,
        )
        self.df.to_csv(self.csv_file, index=False)

    def show_expenses(self, month=None, year=None):
        if year:
            self.df = self.df[self.df["date"].dt.year == year]
        if month:
            self.df = self.df[self.df["date"].dt.month == month]

        income_df = self.df[self.df["type"] == "income"]
        expense_df = self.df[self.df["type"] == "expense"]

        total_income = income_df["amount"].sum()
        total_expense = expense_df["amount"].sum()

        remaining_balance = total_income - total_expense
        income_grouped = (
            income_df.groupby("from")["amount"].sum().sort_values(ascending=False)
        )
        expense_grouped = (
            expense_df.groupby("from")["amount"].sum().sort_values(ascending=False)
        )

        combined = pd.Series(income_grouped.sum(), index=["Total Income"])._append(
            expense_grouped
        )

        # Plotting the graph
        plt.figure(figsize=(10, 5))

        plt.subplot(121)  # subplot for pie chart
        plt.pie(
            combined,
            labels=combined.index,
            autopct="%1.1f%%",
        )
        plt.title("Income and Expenses for July")

        plt.subplot(122)  # subplot for table
        plt.axis("tight")
        plt.axis("off")
        plt.table(
            cellText=expense_df[["date", "from", "amount"]].values,
            colLabels=["date", "til", "amount"],
            cellLoc="center",
            loc="center",
        )

        summary_df = pd.DataFrame(
            {
                "Total Income": [total_income],
                "Total Expenses": [total_expense],
                "Remaining Balance": [remaining_balance],
            }
        )
        plt.table(
            cellText=summary_df.values,
            colLabels=summary_df.columns,
            cellLoc="center",
            loc="bottom",
        )

        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Finance tracking application.")
    parser.add_argument(
        "command", choices=["income", "expense", "show"], help="Command to execute."
    )
    parser.add_argument(
        "date", help="Date of the transaction (dd.mm.yy).", nargs="?", default=None
    )
    parser.add_argument(
        "from_", help="Source of the transaction.", nargs="?", default=None
    )
    parser.add_argument(
        "amount", type=float, help="Amount of the transaction.", nargs="?", default=None
    )
    parser.add_argument(
        "month", type=int, help="Month to show expenses.", nargs="?", default=None
    )
    parser.add_argument(
        "year", type=int, help="Year to show expenses.", nargs="?", default=None
    )
    args = parser.parse_args()

    app = FinanceApp()
    if args.command == "income":
        app.add_income(args.amount, args.date, args.from_)
    elif args.command == "expense":
        app.add_expense(args.amount, args.date, args.from_)
    elif args.command == "show":
        app.show_expenses(args.month, args.year)
