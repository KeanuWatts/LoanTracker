import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# Create the main window
window = tk.Tk()

# Create a Notebook
notebook = ttk.Notebook(window)
notebook.pack()

# Create a dictionary to store the input fields for each tab
tabs = {}

def update_data():
    # Clear the previous graph
    figure.clear()

    # Create a new subplot
    ax = figure.add_subplot(111)

    # Set the y-axis formatter to display large numbers in full
    ax.get_yaxis().set_major_formatter(ticker.FuncFormatter(lambda x, p: format(int(x), ',')))
    # Plot a new line for each tab
    for i, (tab, fields) in enumerate(tabs.items(), start=0):
        # Get the input values
        principal_str = fields[0].get()
        annual_interest_str = fields[1].get()
        monthly_payment_str = fields[2].get()
        deposits = fields[3] if fields[3] is not None else {}

        # Skip this tab if any input value is missing
        if not principal_str or not annual_interest_str or not monthly_payment_str:
            continue

        # Convert the input values to float
        principal = float(principal_str)
        annual_interest = float(annual_interest_str) / 100 / 12  # Convert annual rate to monthly and to a proportion
        monthly_payment = float(monthly_payment_str)

        # Calculate the remaining balance for each month
        balance = principal
        balances = []
        total_repayment_value = 0
        total_interest_value = 0

        balances.append(balance)
        for j in range(1000):  # Assume a maximum of 1000 months for simplicity
            interest = balance * annual_interest
            adjustment = monthly_payment - interest
            balance -= adjustment
            total_repayment_value += monthly_payment
            total_interest_value += interest

            # Check if there is a deposit for the current month
            if j+1 in deposits:
                balance -= deposits[j+1]
                total_repayment_value += deposits[j+1]

            balances.append(balance)

            if balance <= 0:
                break

        # Plot the line for this tab
        ax.plot(balances, label=f"Tab {i}")
        
        # Calculate the new values
        time_to_repayment_value = len(balances)-1

        # Update the output fields
        fields[4].config(text=str(round(time_to_repayment_value, 2)))
        fields[5].config(text=str(round(total_repayment_value, 2)))
        fields[6].config(text=str(round(total_interest_value, 2)))


    # Add labels and legend to the graph
    ax.set_xlabel('Month')
    ax.set_ylabel('Remaining Balance')
    ax.set_title('Loan Repayment Over Time')
    ax.legend()

    # Adjust the layout to make sure that the labels fit within the figure area
    figure.tight_layout()
    # Redraw the canvas
    canvas.draw()

# Create a function to add a tab
def add_tab():
    # Create a new tab
    tab = ttk.Frame(notebook)
    notebook.add(tab, text=f"Tab {len(tabs) + 1}")

 
    # Create a StringVar for each input field
    principal_amount_var = tk.StringVar()
    interest_rate_var = tk.StringVar()
    monthly_payment_var = tk.StringVar()

    # Create labels and input fields for the new tab
    principal_amount_label = tk.Label(tab, text="Principal Amount")
    principal_amount_label.grid(row=0, column=0)
    principal_amount = tk.Entry(tab, textvariable=principal_amount_var)
    principal_amount.grid(row=0, column=1)

    interest_rate_label = tk.Label(tab, text="Interest Rate")
    interest_rate_label.grid(row=1, column=0)
    interest_rate = tk.Entry(tab, textvariable=interest_rate_var)
    interest_rate.grid(row=1, column=1)

    monthly_payment_label = tk.Label(tab, text="Monthly Payment")
    monthly_payment_label.grid(row=2, column=0)
    monthly_payment = tk.Entry(tab, textvariable=monthly_payment_var)
    monthly_payment.grid(row=2, column=1)

    # Create labels and output fields for the new values
    time_to_repayment_label = tk.Label(tab, text="Time to Repayment")
    time_to_repayment_label.grid(row=3, column=0)
    time_to_repayment = tk.Label(tab)
    time_to_repayment.grid(row=3, column=1)

    total_repayment_label = tk.Label(tab, text="Total Repayment")
    total_repayment_label.grid(row=4, column=0)
    total_repayment = tk.Label(tab)
    total_repayment.grid(row=4, column=1)

    total_interest_label = tk.Label(tab, text="Total Paid to Interest")
    total_interest_label.grid(row=5, column=0)
    total_interest = tk.Label(tab)
    total_interest.grid(row=5, column=1)

   
    # Add a gap between the columns
    gap = tk.Label(tab, width=10)
    gap.grid(row=0, column=2)

    # Create labels and input fields for deposits
    deposit_month_label = tk.Label(tab, text="Deposit Month")
    deposit_month_label.grid(row=0, column=3)
    deposit_month = tk.Entry(tab)
    deposit_month.grid(row=0, column=4)

    deposit_amount_label = tk.Label(tab, text="Deposit Amount")
    deposit_amount_label.grid(row=1, column=3)
    deposit_amount = tk.Entry(tab)
    deposit_amount.grid(row=1, column=4)

    # Create a listbox to display the deposits
    deposits_listbox = tk.Listbox(tab)
    deposits_listbox.grid(row=2, column=3, columnspan=2)

    # Create a dictionary to store the deposits
    deposits = {}

    # Create a function to add a deposit
    def add_deposit():
        month = int(deposit_month.get())
        amount = float(deposit_amount.get())
        deposits[month] = amount
        deposits_listbox.insert(tk.END, f"Month {month}: {amount}")

    # Create a function to remove a deposit
    def remove_deposit():
        # Get the selected deposit
        selection = deposits_listbox.curselection()
        if selection:
            # Get the deposit details
            deposit = deposits_listbox.get(selection[0])
            month = int(deposit.split(":")[0].split(" ")[1])

            # Remove the deposit from the dictionary and the listbox
            del deposits[month]
            deposits_listbox.delete(selection[0])

    # Create buttons to add and remove a deposit
    add_deposit_button = tk.Button(tab, text="Add Deposit", command=add_deposit)
    add_deposit_button.grid(row=3, column=3)

    remove_deposit_button = tk.Button(tab, text="Remove Deposit", command=remove_deposit)
    remove_deposit_button.grid(row=3, column=4)

    # Call update_graph whenever an input field is changed
    principal_amount_var.trace("w", lambda name, index, mode: update_data())
    interest_rate_var.trace("w", lambda name, index, mode: update_data())
    monthly_payment_var.trace("w", lambda name, index, mode: update_data())

    # Store the input fields, deposits, and output fields in the tabs dictionary
    tabs[tab] = [principal_amount_var, interest_rate_var, monthly_payment_var, deposits, time_to_repayment, total_repayment, total_interest]

# Create a button to add a tab
add_tab_button = tk.Button(window, text="Add Tab", command=add_tab)
add_tab_button.pack()

# Create a figure for the graph
figure = Figure(figsize=(5, 4), dpi=100)
canvas = FigureCanvasTkAgg(figure, master=window)
canvas.get_tk_widget().pack()

# Start the main loop
window.mainloop()
