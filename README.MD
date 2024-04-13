# Loan Tracker

Loan Tracker is a simple Python application that allows you to preview the repayment of multiple loans over time. It provides a graphical representation of the remaining balance for each loan, and calculates the time to repayment, total repayment, and total interest paid.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

You will need Python 3 and pip installed on your machine. You can download Python from the [official website](https://www.python.org/downloads/). Pip is included in Python 3.4 and later.

### Installation

1. Clone the repository:

```git clone https://github.com/KeanuWatts/loan-tracker.git```

2. Navigate to the project directory:

```cd loan-tracker```

3. Install the required dependencies:

```pip install -r requirements.txt```

## Usage

1. Run the application:

```python main.py```

2. The application will open a window with a tab for each loan. In each tab, enter the principal amount, annual interest rate, and monthly payment for the loan. You can also enter any additional deposits you plan to make.

3. The graph will update automatically whenever you change any of the input fields. The time to repayment, total repayment, and total interest paid are displayed below the input fields.

### Building the Application

You can build an executable version of the application using PyInstaller. Run the build script to do this:

```./build.sh```

This will create an executable named my_program.exe in the dist directory. You can distribute this executable to others, and they can run it on their own computers without needing to install Python or any of the application's dependencies.