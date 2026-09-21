# 📊 Excel Data Analyzer

A desktop-based **Excel Data Analysis and Management application** built with **Python and PyQt6**. The application allows users to import Excel files, store data in MySQL, edit and analyze datasets, visualize data using charts, and export results in multiple formats.

## 🚀 Features

* 🔐 User Login & Registration
* 👤 Guest Mode
* 🗄️ MySQL Database Storage
* 📥 Import Excel (`.xlsx`, `.xls`)
* 📋 View and edit tabular data
* 🔎 Search data within tables
* ↕️ Sort data by columns
* 🗑️ Delete rows and database tables
* 💾 Save edited data to MySQL
* 📈 Daily Revenue Analysis
* 📊 Graphical Analysis using Bar & Pie Charts
* 📤 Export data to:

  * Excel
  * CSV
  * PDF
  * HTML
* 📋 Copy cells, rows, or selected data
* 📊 Selection summary
* 🗂️ Multiple tables/files for each user
* 🎨 Dark-themed PyQt6 interface

## 🛠️ Technologies Used

* **Python**
* **PyQt6** – Desktop GUI
* **Pandas** – Data processing
* **MySQL** – Database
* **SQLAlchemy** – Database connectivity
* **Matplotlib** – Data visualization
* **python-dotenv** – Environment variable management

## 📂 Project Workflow

```text
Excel File
    ↓
Pandas
    ↓
PyQt6 Interface
    ↓
MySQL Database
    ↓
Data Processing & Analysis
    ↓
Charts / Reports / Export
```

## 📊 Analysis Features

The application can generate graphical analysis based on the selected dataset, including:

* Product vs Quantity
* Referral Source Distribution
* Order Status vs Quantity
* Payment Method Distribution

It also provides daily revenue aggregation and allows users to preview the latest rows of a dataset.

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/sajankr26/Data-Analysis.git
cd Data-Analysis
```

Install the required packages:

```bash
pip install PyQt6 pandas sqlalchemy matplotlib mysql-connector-python python-dotenv openpyxl
```

## 🔐 Environment Variables

Create a `.env` file in the project directory and configure your database credentials.

Example:

```env
UserDatabase=your_user_database_connection
Dbinfo=your_database_connection_prefix
user=your_mysql_username
host=your_mysql_host
password=your_mysql_password
```

> ⚠️ Never upload your `.env` file or database credentials to GitHub.

## ▶️ Run the Application

```bash
python main.py
```

The application will open with the login/registration interface.

## 🗄️ Database

The application uses **MySQL** for storing:

* User credentials
* User information
* Uploaded Excel datasets
* Edited table data

Each registered user can have their own database for storing uploaded datasets.

## 📸 Application

The application provides a dark-themed desktop interface for managing, analyzing, and exporting Excel data.

## 🎯 Purpose

The project was developed to practice and demonstrate practical skills in:

* Python GUI development
* Database management
* Data analysis
* Data visualization
* Excel automation
* CRUD operations
* Desktop application development

## 👨‍💻 Developer

**Sajan Kumar**

B.Tech – Artificial Intelligence & Data Science

Skills demonstrated in this project:

`Python` • `PyQt6` • `Pandas` • `SQL` • `MySQL` • `SQLAlchemy` • `Matplotlib`

---

