from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QPushButton, QMessageBox, QFileDialog, QVBoxLayout, QTableWidget, QTableWidgetItem, QInputDialog, QToolBar , QGridLayout ,QFormLayout, QDialog ,QComboBox, QMenu ,QHBoxLayout, QLabel, QLineEdit, QWidgetAction
from PyQt6.QtGui import QAction  ,QIcon
import sys
import os
import pandas as pd
from sqlalchemy import create_engine, text
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import mysql.connector
from dotenv import load_dotenv

load_dotenv()
userdb = os.getenv("UserDatabase")
db_info = os.getenv("Dbinfo")
userenv = os.getenv("user")
hostenv = os.getenv("host")
passenv = os.getenv("password")


class Window(QWidget):
    switch_window = pyqtSignal()

    def __init__(self):
        super().__init__()
        layout = QGridLayout()
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(10)
        self.setWindowTitle("LOGIN")
        self.resize(400, 250)
        self.move(540, 330)
        self.setLayout(layout)
        self.setWindowIcon(QIcon("login.png"))
        self.setWindowModality(Qt.WindowModality.ApplicationModal)        
        # Title Label
        title = QLabel("Login window")
        title.setProperty("class", "heading")
        layout.addWidget(title, 0, 3, 1, 1, Qt.AlignmentFlag.AlignCenter)

        # Username Label and Input
        user = QLabel("Username:")
        user.setProperty("class", "normal")
        layout.addWidget(user, 1, 0)
        self.input1 = QLineEdit()
        self.input1.returnPressed.connect(lambda: self.input2.setFocus())
        layout.addWidget(self.input1, 1, 1, 1, 8)

        # Password Label and Input
        pwd = QLabel("Password")
        pwd.setProperty("class", "normal")
        layout.addWidget(pwd, 2, 0)
        self.input2 = QLineEdit()
        self.input2.setEchoMode(QLineEdit.EchoMode.Password)
        self.input2.returnPressed.connect(self.login)
        layout.addWidget(self.input2, 2, 1, 1, 8)
        icon = QIcon("eye.png")
        self.pwd_action = self.input2.addAction(icon, QLineEdit.ActionPosition.TrailingPosition)
        try:
            self.pwd_action.triggered.connect(self.toggle_password_visibility)
        except Exception:
            pass

        self.apply_custom_styles()
        # Register and Login Buttons
        button1 = QPushButton("Register")
        button1.clicked.connect(self.Register)
        button1.setFixedSize(200, 30)

        button2 = QPushButton("Login")
        button2.clicked.connect(self.login)
        button2.setFixedSize(430, 34)

        button3 = QPushButton("Guest")
        button3.clicked.connect(self.Guest)
        button3.setFixedSize(200, 30)

        layout.addWidget(button2, 4, 0, 1, 9, Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(button1, 5, 0, 1, 4, Qt.AlignmentFlag.AlignLeft)

        layout.addWidget(button3, 5, 3, 1, 6, Qt.AlignmentFlag.AlignRight)
    def login(self):
        
        engine = create_engine(userdb)
        name1 = self.input1.text()
        pass1 = self.input2.text()
        Dbname = name1
        rows = []
        rowp = []
        names = []
        UserData = "Select * from userpass"
        ds = pd.read_sql_query(UserData, engine)
        for row in ds.itertuples(index=False):
            usern = row[0]
            passn = row[1]
            name = row[2]
            rowp.append(passn)
            rows.append(usern)
            names.append(name)

        if name1 in rows:
            idx = rows.index(name1)
            if pass1 == rowp[idx]:
                QMessageBox.about(self, "Success", f"Successfully Login \n Welcome {names[idx]}")
                global g_Dbname , g_name ,ab
                g_Dbname = Dbname
                g_name = names[idx]
                ab = ab + 1
                try:
                    self.switch_window.emit()
                except Exception:
                    pass
                self.close()
                
            else:
                QMessageBox.warning(self, "Invalid password", "Wrong password!!! Try Again")
        else:
            QMessageBox.warning(self, "Username not found", "Username Not Found !! Register or retry")


    def Register(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("REGISTER")
        dialog.setWindowIcon(QIcon("login.png"))
        dialog.resize(400, 300)

        layout = QGridLayout(dialog)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(10)

        title = QLabel("Register new user")
        title.setProperty("class", "heading")
        layout.addWidget(title, 0, 3, 1, 1, Qt.AlignmentFlag.AlignCenter)

        name = QLabel("Name:")
        name.setProperty("class", "normal")
        layout.addWidget(name, 1, 0)
        self.reg_input3 = QLineEdit()
        layout.addWidget(self.reg_input3, 1, 1, 1, 8)
        self.reg_input3.returnPressed.connect(lambda: self.reg_input1.setFocus())

        user = QLabel("Username:")
        user.setProperty("class", "normal")
        layout.addWidget(user, 2, 0)
        self.reg_input1 = QLineEdit()
        layout.addWidget(self.reg_input1, 2, 1, 1, 8)
        self.reg_input1.returnPressed.connect(lambda: self.reg_input2.setFocus())


        pwd = QLabel("Password:")
        pwd.setProperty("class", "normal")
        layout.addWidget(pwd, 3, 0)
        self.reg_input2 = QLineEdit()
        self.reg_input2.setEchoMode(QLineEdit.EchoMode.Password)
        layout.addWidget(self.reg_input2, 3, 1, 1, 8)
        self.reg_input2.returnPressed.connect(lambda: self.perform_registration(dialog))
        

        register_button = QPushButton("Register")
        register_button.clicked.connect(lambda: self.perform_registration(dialog))
        register_button.setFixedSize(150, 30)
        register_button.setAutoDefault(False)
        register_button.setDefault(False)
        cancel_button = QPushButton("Cancel")
        cancel_button.clicked.connect(dialog.close)
        cancel_button.setFixedSize(150, 30)
        cancel_button.setAutoDefault(False)
        cancel_button.setDefault(False)

        layout.addWidget(register_button, 5, 0, 1, 0, Qt.AlignmentFlag.AlignLeft)
        layout.addWidget(cancel_button, 5, 3, 1, 6, Qt.AlignmentFlag.AlignRight)

        dialog.setStyleSheet(self.styleSheet())
        dialog.exec()


    def perform_registration(self, dialog):
        username1 = self.reg_input1.text().strip()
        username = username1.lower()
        password = self.reg_input2.text()
        name = self.reg_input3.text().strip()

        if not username or not password or not name:
            QMessageBox.warning(self, "Warn", "Please enter username, password and name")
            return

        engine = create_engine(userdb)
        UserData = "Select * from userpass"
        try:
            ds = pd.read_sql_query(UserData, engine)
            rows = [row[0] for row in ds.itertuples(index=False)]
        except Exception:
            rows = []

        if username in rows:
            QMessageBox.warning(self, "Warn", "Username already Exist!! Try another or login")
            return

        with engine.begin() as conn:
            conn.execute(
                text("INSERT INTO userpass (Username, Password, Name) VALUES (:u, :p, :n)"),
                {"u": username, "p": password, "n": name}
            )

        QMessageBox.information(self, "Registered", "Registered Successfully")
        dialog.close()

        connection = mysql.connector.connect(host= hostenv , user= userenv, password= passenv)
        if connection.is_connected():
            cursor = connection.cursor()
            db_name = username
            cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`")
            connection.close()

    def Guest(self):
        Dbname = "ExcelData"
        global g_Dbname , g_name ,ab
        g_name = "GUEST"
        g_Dbname = Dbname
        ab = ab + 1
        try:
            self.switch_window.emit()
        except Exception:
            pass
        self.close()
        QMessageBox.about(self,"Login as Guest", "WELCOME, Guest \n Everyone can excess your file")

    def toggle_password_visibility(self):
        if self.input2.echoMode() == QLineEdit.EchoMode.Password:
            self.input2.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.input2.setEchoMode(QLineEdit.EchoMode.Password)

    def apply_custom_styles(self):
        self.setStyleSheet('''
QWidget {
    background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:1, stop:0 #2b2b2b, stop:1 #141414);
    color: #e8e8e8;
    font-family: "Segoe UI", Arial, sans-serif;
}

QLabel[class="heading"] {
    font-size: 24px;
    font-weight: 700;
    color: #ffffff;
    padding-bottom: 12px;
}

QLabel[class="normal"] {
    font-size: 13px;
    margin-bottom: 6px;
}

QPushButton {
    background-color: #4b76ff;
    border: none;
    border-radius: 12px;
    color: #ffffff;
    padding: 10px 14px;
    min-height: 38px;
    font-weight: 600;
}

QPushButton:hover {
    background-color: #5e8dff;
}

QPushButton:pressed {
    background-color: #3f5bf2;
}

QLineEdit {
    background-color: #242424;
    border: 1px solid #4f5a7d;
    border-radius: 8px;
    color: #ffffff;
    padding: 10px;
}

QLineEdit:focus {
    border: 1px solid #758cff;
    background-color: #2d2d2d;
}

QMessageBox {
    background-color: #2b2b2b;
}

QMessageBox QLabel {
    color: #e8e8e8;
}

QMessageBox QPushButton {
    background-color: #4b76ff;
    border: none;
    border-radius: 6px;
    color: #ffffff;
    padding: 6px 12px;
    min-height: 40px;
    min-width: 80px;
    font-weight: 600;
}

QMessageBox QPushButton:hover {
    background-color: #5e8dff;
}

QMessageBox QPushButton:pressed {
    background-color: #3f5bf2;
}
''')


class Canvas(FigureCanvas):
    def __init__(self):
        fig = Figure(figsize=(5, 4), facecolor="#121212")
        self.ax = fig.add_subplot(111)
        self._set_dark_theme(self.ax)
        super().__init__(fig)

    def _set_dark_theme(self, ax):
        ax.set_facecolor("#121212")
        ax.figure.patch.set_facecolor("#121212")
        ax.tick_params(colors="#e0e0e0", labelcolor="#e0e0e0")
        for spine in ax.spines.values():
            spine.set_color("#4f5a7d")
        ax.title.set_color("#ffffff")
        ax.xaxis.label.set_color("#e0e0e0")
        ax.yaxis.label.set_color("#e0e0e0")

class AnotherWindow(QWidget):
    def __init__(self, table_name):
        try:
            super().__init__()
            self.setWindowTitle("More Graphical Analysis")
            self.setGeometry(600, 100, 1100, 950)
            toolbar = QToolBar("ANALYSIS TOOLBAR")
            toolbar.setMovable(False)
            layout = QVBoxLayout(self)
            layout.setContentsMargins(12, 12, 12, 12)
            layout.setSpacing(12)
            layout.addWidget(toolbar)
            Table_name = table_name.upper()
            header_label = QLabel(f"Graphical Analysis for: {Table_name}")
            header_label.setStyleSheet("font-size: 16px; font-weight: bold;")
            layout.addWidget(header_label)
            self.setWindowIcon(QIcon("icon.jpg"))
            
            
            engine = create_engine(f'{db_info}{g_Dbname}')  
            tableData = f"SELECT * FROM `{table_name}` ORDER BY `Date` "
            ds = pd.read_sql_query(tableData, engine)
            headerlable = ds.columns.tolist()
        
    
    ##
            items = headerlable
            # Dilog for selecting columns
            dialog = QDialog()
            dialog.setWindowTitle("Select Columns")
            dialog.setStyleSheet(
                "QDialog { background: #1e1e1e; border: 1px solid #3d3d3d; border-radius: 12px; }"
                "QLabel { font-size: 13px; color: #e0e0e0; }"
                "QComboBox { min-width: 280px; padding: 8px 10px; font-size: 13px; color: #e0e0e0; border: 1px solid #3d3d3d; border-radius: 8px; background: #2d2d2d; }"
                "QComboBox::drop-down { subcontrol-origin: padding; subcontrol-position: top right; width: 24px; border-left: 1px solid #3d3d3d; background: #2d2d2d; }"
                "QComboBox::down-arrow { image: url(warrow.png); width: 12px; height: 12px; }"
                "QComboBox QAbstractItemView { border: 1px solid #3d3d3d; selection-background-color: #0d47a1; background: #2d2d2d; color: #e0e0e0; }"
                "QPushButton { background: #0d47a1; color: #ffffff; padding: 8px 16px; border-radius: 8px; font-weight: 600; }"
                "QPushButton:hover { background: #1565c0; }"
                "QPushButton#cancel { background: #424242; }"
                "QPushButton#cancel:hover { background: #616161; }"
            )
            form = QFormLayout()
            form.setSpacing(12)
            
            product_combo = QComboBox()
            product_combo.setObjectName("product_combo")
            product_combo.addItems(items)
            if "Product" in items:
                product_combo.setCurrentText("Product")
            form.addRow("Select Product Column:", product_combo)
            
            quantity_combo = QComboBox()
            quantity_combo.setObjectName("quantity_combo")
            quantity_combo.addItems(items)
            if "Quantity" in items:
                quantity_combo.setCurrentText("Quantity")
            form.addRow("Select Quantity Column:", quantity_combo)
            
            source_combo = QComboBox()
            source_combo.setObjectName("source_combo")
            source_combo.addItems(items)
            if "ReferralSource" in items:
                source_combo.setCurrentText("ReferralSource")
            form.addRow("Select Referral Source Column:", source_combo)
            
            status_combo = QComboBox()
            status_combo.setObjectName("status_combo")
            status_combo.addItems(items)
            if "OrderStatus" in items:
                status_combo.setCurrentText("OrderStatus")
            form.addRow("Select Order Status Column:", status_combo)
            
            pay_combo = QComboBox()
            pay_combo.setObjectName("pay_combo")
            pay_combo.addItems(items)
            if "PaymentMethod" in items:
                pay_combo.setCurrentText("PaymentMethod")
            form.addRow("Select Payment Method Column:", pay_combo)
            
            button_layout = QHBoxLayout()
            button_layout.addStretch()
            ok_button = QPushButton("OK")
            cancel_button = QPushButton("Cancel")
            cancel_button.setObjectName("cancel")
            # Improve button sizes
            ok_button.setFixedHeight(30)
            cancel_button.setFixedHeight(30)
            ok_button.setFixedWidth(90)
            cancel_button.setFixedWidth(90)
            button_layout.addWidget(ok_button)
            button_layout.addWidget(cancel_button)
            
            main_layout = QVBoxLayout(dialog)
            main_layout.setContentsMargins(12, 12, 12, 12)
            main_layout.setSpacing(10)
            main_layout.addLayout(form)
            main_layout.addLayout(button_layout)
            
            okPressed = False
            def on_ok():
                nonlocal okPressed
                okPressed = True
                dialog.close()
            
            ok_button.clicked.connect(on_ok)
            cancel_button.clicked.connect(dialog.close)

        
            dialog.exec()
            if not okPressed:
                return

            Product = headerlable.index(product_combo.currentText())
            Quantity = headerlable.index(quantity_combo.currentText())
            Source1 = headerlable.index(source_combo.currentText())
            Status1 = headerlable.index(status_combo.currentText())
            Pay1 = headerlable.index(pay_combo.currentText())

            # Keys for the selected columns use in Functions
            self.Product = Product
            self.Quantity = Quantity
            self.Source1 = Source1
            self.Status1 = Status1
            self.Pay1 = Pay1

        #Data Processing for Graphs and Charts
            #Data for Product and Quantity
            rows = []
            for row in ds.itertuples(index=False):
                prod = row[self.Product]
                quan = row[self.Quantity]
                if pd.notna(prod) and pd.notna(quan):
                    try:
                        rows.append((prod, pd.to_numeric(quan, errors='coerce')))
                    except:
                        pass

            df_cols = pd.DataFrame(rows, columns=["Product", "Quantity"]) if rows else pd.DataFrame(columns=["Product", "Quantity"])
            df_cols = df_cols.dropna()
            grouped_df = df_cols.groupby("Product")["Quantity"].sum().reset_index()

            #  Bar Chart 1  OF Product and Quantity
            bar1 = Canvas()
            ax = bar1.figure.add_subplot(111)
            bar1._set_dark_theme(ax)
            ax.bar(grouped_df["Product"], grouped_df["Quantity"], color="#56ccf2", edgecolor="#ffffff")
            ax.set_title("Total Quantity of Product", color="#ffffff")

            #Data for Refral Source and Quantity
            rows= []
            for row in ds.itertuples(index=False):
                Pay2 = row[Source1]
                quan = row[Quantity]
                if pd.notna(Pay2) and pd.notna(quan):
                    try:
                        rows.append((Pay2, pd.to_numeric(quan, errors='coerce')))
                    except:
                        pass
            
            df_cols = pd.DataFrame(rows, columns=["Refral Source", "Quantity"]) if rows else pd.DataFrame(columns=["Refral Source", "Quantity"])
            df_cols = df_cols.dropna()
            grouped_df = df_cols.groupby("Refral Source")["Quantity"].sum().reset_index()
            
            Source = grouped_df["Refral Source"]
            quantity = grouped_df["Quantity"]

            #Pie Chart 1 for Refral Source and Quantity
            pie1 = Canvas()
            ax = pie1.figure.add_subplot(111)
            pie1._set_dark_theme(ax)
            if len(quantity) > 0 and quantity.sum() > 0:
                ax.pie(quantity, labels=Source, autopct="%1.1f%%", startangle=90, textprops={"color":"#e0e0e0"})
            ax.set_title("Refral Source Distribution", color="#ffffff")

            #Data for Order Status and Quantity
            rows = []
            for row in ds.itertuples(index=False):
                status2 = row[Status1]
                quan = row[Quantity]
                if pd.notna(status2) and pd.notna(quan):
                    try:
                        rows.append((status2, pd.to_numeric(quan, errors='coerce')))
                    except:
                        pass
            df_cols = pd.DataFrame(rows, columns=["Order Status", "Quantity"]) if rows else pd.DataFrame(columns=["Order Status", "Quantity"])
            df_cols = df_cols.dropna()
            grouped_df = df_cols.groupby("Order Status")["Quantity"].sum().reset_index() 
            
            #Bar Chart 2 for Order Status and Quantity
            bar2 = Canvas()
            ax = bar2.figure.add_subplot(111)
            bar2._set_dark_theme(ax)
            ax.bar(grouped_df["Order Status"], grouped_df["Quantity"], color="#ff8c69", edgecolor="#ffffff")
            ax.set_title("Total Product Status", color="#ffffff")

            #Data for Payment Method and Quantity

            rows= []
            for row in ds.itertuples(index=False):
                Pay2 = row[Pay1]
                quan = row[Quantity]
                if pd.notna(Pay2) and pd.notna(quan):
                    try:
                        rows.append((Pay2, pd.to_numeric(quan, errors='coerce')))
                    except:
                        pass
            df_cols = pd.DataFrame(rows, columns=["Payment Method", "Quantity"]) if rows else pd.DataFrame(columns=["Payment Method", "Quantity"])
            df_cols = df_cols.dropna()
            grouped_df = df_cols.groupby("Payment Method")["Quantity"].sum().reset_index()
            Pay = grouped_df["Payment Method"]
            quantity = grouped_df["Quantity"]

            # Pie Chart 2 for Payment Method and Quantity 
            pie2 = Canvas()
            ax = pie2.figure.add_subplot(111)
            pie2._set_dark_theme(ax)
            if len(quantity) > 0 and quantity.sum() > 0:
                ax.pie(quantity, labels=Pay, autopct="%1.1f%%", startangle=90, textprops={"color":"#e0e0e0"})
            ax.set_title("Payment Method Distribution", color = "#ffffff")
            chart_layout = QGridLayout()
            chart_layout.addWidget(bar1, 0, 0)
            chart_layout.addWidget(pie1, 0, 1)
            chart_layout.addWidget(bar2, 1, 1)
            chart_layout.addWidget(pie2, 1, 0)
            layout.addLayout(chart_layout)
            
            
            self.checkactions = []
           


        except Exception :
            QMessageBox.warning(self, "Error", "unable to open Graph Window")
            return
    

##############################################################################################################################################      
########################################################### MAIN WINDOW  #####################################################################
class analysis(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("Excel Analysis")
        self.setGeometry(100,100,1300,900)
        self.setWindowIcon(QIcon("icon.jpg"))
        layout = QVBoxLayout()
        self.apply_custom_styles()
        self._checkable_actions = []
        self.current_table = 'data'
        #cbtn = Show Data
        #sbtn = Last Revenue
        #stbtn = Last Stats
        #gbtn = Revenue Time Graph Representation
        
        button = QAction("Load Data to database", self)
        button.setStatusTip("Load Excel Data into Database")
        button.triggered.connect(self.loadData)
        #button.setCheckable(True)
        #self._checkable_actions.append(button)
        #button.toggled.connect(lambda checked, a=button: self._exclusive_check(a, checked))
#
        Selectbtn = QAction("Select Table", self)
        Selectbtn.setStatusTip("Select Which Excel file you want to Analyse")
        Selectbtn.triggered.connect(self.selectdata)
        Selectbtn.setCheckable(True)
        self._checkable_actions.append(Selectbtn)
        Selectbtn.toggled.connect(lambda checked, a= Selectbtn : self._exclusive_check(a, checked) )

        Delbtn = QAction("Delete Saved Data ")
        Delbtn.setStatusTip("Delete Data From Database")
        Delbtn.triggered.connect(self.deletedata)
        #Delbtn.setCheckable(True)
        self._checkable_actions.append(Delbtn)
        Delbtn.toggled.connect(lambda checked, a= Delbtn : self._exclusive_check(a, checked) )

        cbtn = QAction("Show Selected Data ", self)
        cbtn.setStatusTip("Show Data from Database")
        cbtn.triggered.connect(self.CData)        

        cbtn.setCheckable(True)
        self._checkable_actions.append(cbtn)
        cbtn.toggled.connect(lambda checked, a=cbtn: self._exclusive_check(a, checked))

        sbtn = QAction("Show Daily Revenue", self)
        sbtn.setStatusTip("Show Revenue Data")
        sbtn.triggered.connect(self.rev)
        sbtn.setCheckable(True)
        self._checkable_actions.append(sbtn)
        sbtn.toggled.connect(lambda checked, a=sbtn: self._exclusive_check(a, checked))


        stbtn = QAction("Show Last Few Data of the Table", self)
        stbtn.setStatusTip("Show Last Stats Data")
        stbtn.triggered.connect(self.lstasts)  
        stbtn.setCheckable(True)
        self._checkable_actions.append(stbtn)
        stbtn.toggled.connect(lambda checked, a=stbtn: self._exclusive_check(a, checked))
        
        mbtn = QAction("Graphical Analysis of Selected Data", self)
        mbtn.setStatusTip("Show Graphical Analysis")
        mbtn.triggered.connect(self.more_window)
        mbtn.setCheckable(True)
        self._checkable_actions.append(mbtn)
        mbtn.toggled.connect(lambda checked, a=mbtn: self._exclusive_check(a, checked))

        '''loginbtn = QAction("Log Out", self)
        loginbtn.setStatusTip("LogOut")
        loginbtn.triggered.connect(self.Login_pg)
        loginbtn.setCheckable(True)
        self._checkable_actions.append(loginbtn)
        loginbtn.toggled.connect(lambda checked, a=loginbtn: self._exclusive_check(a, checked))
        loginbtn = QPushButton("Logout")
        loginbtn.setStyleSheet("QPushButton { background-color: Red; color: white; } QPushButton:hover { background-color: darkred; }")
        loginbtn.clicked.connect(self.Login_pg)'''
#############################################################
        if ab == 0:
            try:
                self.close()
            except Exception:
                pass
            self.loginWindow = Window()
            self.loginWindow.show()
            return



        exportbtn = QAction("Export Data Into Excel formate", self)
        exportbtn.setStatusTip("Export Data to Excel")
        exportbtn.triggered.connect(self.export_data)
    
        #exportbtn.setCheckable(True)
        self._checkable_actions.append(exportbtn)
        exportbtn.toggled.connect(lambda checked, a=exportbtn: self._exclusive_check(a, checked))

        saveasbtn = QAction("Save as", self)
        saveasbtn.setStatusTip("Save as")
        saveasbtn.triggered.connect(self.saveas_data)
    
       # saveasbtn.setCheckable(True)
        self._checkable_actions.append(saveasbtn)
        saveasbtn.toggled.connect(lambda checked, a=saveasbtn: self._exclusive_check(a, checked))

        
        savebtn = QAction("Save", self)
        savebtn.setStatusTip("Save Edited Table Data to Database")
        savebtn.triggered.connect(self.saveEditedData)
        savebtn.setCheckable(True)
        self._checkable_actions.append(savebtn)
        savebtn.toggled.connect(lambda checked, a=savebtn: self._exclusive_check(a, checked))

        save_button = QPushButton("Save")
        save_button.setStyleSheet("QPushButton { background-color: Blue; color: white; } QPushButton:hover { background-color: darkblue; }")
        save_button.clicked.connect(self.saveEditedData)

        find_button = QPushButton("Find")
        find_button.setStyleSheet("QPushButton { background-color: #0066cc; color: white; } QPushButton:hover { background-color: #004c99; }")
        find_button.clicked.connect(self.find_in_table)

        menu = self.menuBar()
        self.userMenu = menu.addMenu(QIcon("avt.png"), f"&Hi,{g_name}")
        self.userMenu.setStyleSheet("""
            QMenu {
                background-color: Gray;
                width: 520px;
                height: 400px;
                padding: 10px;
            }
            QMenu::item:selected {
                background-color: #d4a574;
            }
        """)
        
        userMenuWidget = QWidget()
        userMenuWidget.setFixedWidth(500)
        userMenuLayout = QVBoxLayout()
        userMenuLayout.setContentsMargins(10, 10, 10, 10)
        userMenuLayout.setSpacing(10)
        
        avatarLabel = QLabel()
        avatarLabel.setPixmap(QIcon("avt.png").pixmap(80, 80))
        avatarLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        userMenuLayout.addWidget(avatarLabel)
        
        self.nameLabel = QLabel(f"Hi,{g_name}")
        self.nameLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.nameLabel.setStyleSheet("font-weight: bold; font-size: 12px;")
        userMenuLayout.addWidget(self.nameLabel)

        buttonLayout2 = QVBoxLayout()
        buttonLayout2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        userMenuLayout.addLayout(buttonLayout2)
        userMenuLayout.addSpacing(5)
        userMenuLayout.addStretch()
        buttonLayout = QHBoxLayout()
        buttonLayout.setSpacing(5)
    ##
        engine = create_engine(f'{db_info}{g_Dbname}')
        try:
            tables_df = pd.read_sql_query("SHOW TABLES", engine)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to retrieve tables:\n{str(e)}")
            tables_df = pd.DataFrame()

        table_names = tables_df.iloc[:, 0].astype(str).tolist() if not tables_df.empty else []

        tablesLabel = QLabel("My Data")
        tablesLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        tablesLabel.setStyleSheet("font-weight: bold; color: white;")
        userMenuLayout.addWidget(tablesLabel)

        self.tableButtonsLayout = QVBoxLayout()
        self.tableButtonsLayout.setSpacing(5)
        self.tableButtonsLayout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        for table_name in table_names:
            table_name1 = table_name.upper()
            tableBtn = QPushButton(table_name1)
            tableBtn.setStyleSheet("QPushButton { background-color: Transparent ; color: white; border-radius: 3px; padding: 5px; } QPushButton:hover { background-color: #0098ff; }")
            tableBtn.setFixedSize(180, 30)
            tableBtn.clicked.connect(lambda _, tn=table_name: self.load_table_by_name(tn))
            self.tableButtonsLayout.addWidget(tableBtn)
        userMenuLayout.addLayout(self.tableButtonsLayout)



        userMenuLayout.addSpacing(35)

        
        logoutBtn = QPushButton("Logout")
        logoutBtn.setStyleSheet("QPushButton { background-color: #AD1313; color: white; border-radius: 3px; padding: 5px; } QPushButton:hover { background-color: #FE0101; }")
        logoutBtn.setFixedSize(180, 30)
        buttonLayout.addWidget(logoutBtn)
        logoutBtn.clicked.connect(self.Login_pg)
        
        

        Delacbtn = QPushButton("Delete Account")
        Delacbtn.setStyleSheet("QPushButton { background-color: #AD1313; color: white; border-radius: 3px; padding: 5px; } QPushButton:hover { background-color: #FE0101; }")
        Delacbtn.setFixedSize(180, 30)
        buttonLayout.addWidget(Delacbtn)
        Delacbtn.clicked.connect(self.delac)
        
       
        
        userMenuLayout.addLayout(buttonLayout)
        userMenuWidget.setLayout(userMenuLayout)
        
        userMenuAction = QWidgetAction(self)
        userMenuAction.setDefaultWidget(userMenuWidget)
        self.userMenu.addAction(userMenuAction)
       

        FileMenu = menu.addMenu("File")
        FileMenu.addAction(button)
        FileMenu.addSeparator()
        FileMenu.addAction(Delbtn)
        FileMenu.addSeparator()
        FileMenu.addAction(exportbtn)
        FileMenu.addSeparator()
        FileMenu.addAction(saveasbtn)
        FileMenu.addSeparator()
        menu.addAction(Selectbtn)
        menu.addSeparator()
       
        AnalysisMenu = menu.addMenu("Analysis")
        #AnalysisMenu.addAction(cbtn)
        AnalysisMenu.addSeparator()
        AnalysisMenu.addAction(sbtn)
        AnalysisMenu.addSeparator()
        AnalysisMenu.addAction(stbtn)
        AnalysisMenu.addSeparator()
        AnalysisMenu.addAction(mbtn)
        AnalysisMenu.addSeparator()

        
        rcorner_widget = QWidget()
        rcorner_layout = QHBoxLayout()
        rcorner_layout.setContentsMargins(0, 0, 0, 0)
        rcorner_layout.addWidget(save_button)
        rcorner_layout.addSpacing(10)
        rcorner_layout.addWidget(find_button)
        rcorner_layout.addSpacing(10)
        '''rcorner_layout.addWidget(loginbtn)
        rcorner_layout.addSpacing(10)'''
        rcorner_widget.setLayout(rcorner_layout)
        menu.setCornerWidget(rcorner_widget, Qt.Corner.TopRightCorner)
        menu.addSeparator()

        def on_menu_triggered(action):
            if action in self._checkable_actions:
                if not action.isChecked():
                    action.setChecked(True)
                self._exclusive_check(action, True)

        menu.triggered.connect(on_menu_triggered)

        self.table = QTableWidget()
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.showTableContextMenu)
        layout.addWidget(self.table)

        central_widget = QWidget(self)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.table.horizontalHeader().sectionClicked.connect(self.onHeaderClicked)
        
        self.show()

        ####

    def load_table_by_name(self, table_name):
        engine = create_engine(f'{db_info}{g_Dbname}')

        try:
            ds = pd.read_sql_query(f"SELECT * FROM `{table_name}`", engine)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load table data:\n{str(e)}")
            return

        self.table.setRowCount(ds.shape[0])
        self.table.setColumnCount(ds.shape[1])
        self.table.setHorizontalHeaderLabels(ds.columns)
        for i in range(ds.shape[0]):
            for j in range(ds.shape[1]):
                self.table.setItem(i, j, QTableWidgetItem(str(ds.iat[i, j])))
        self.current_table = table_name

    def refresh_table_buttons(self):
        engine = create_engine(f'{db_info}{g_Dbname}')
        try:
            tables_df = pd.read_sql_query("SHOW TABLES", engine)
            table_names = tables_df.iloc[:, 0].astype(str).tolist() if not tables_df.empty else []
        except Exception:
            table_names = []

        while self.tableButtonsLayout.count():
            item = self.tableButtonsLayout.takeAt(0)
            if item is None:
                continue
            widget = item.widget()
            if widget:
                widget.setParent(None)

        for table_name in table_names:
            table_name1 = table_name.upper()
            tableBtn = QPushButton(table_name1)
            tableBtn.setStyleSheet("QPushButton { background-color: Transparent ; color: white; border-radius: 3px; padding: 5px; } QPushButton:hover { background-color: #0098ff; }")
            tableBtn.setFixedSize(180, 30)
            tableBtn.clicked.connect(lambda checked, tn=table_name: self.load_table_by_name(tn))
            self.tableButtonsLayout.addWidget(tableBtn)

    def Login_pg(self):
        dlg = QMessageBox(self)
        dlg.setWindowTitle("Confirm LogOut!")
        dlg.setText("You want to Logout?")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dlg.setIcon(QMessageBox.Icon.Question)
        button = dlg.exec()
        y = 0
        if button == QMessageBox.StandardButton.Yes:
            y = 1
        else:
            y = 0
        if y==1:    
            self.table.setColumnCount(0)
            self.table.setRowCount(0)
            self.close()
            global g_name
            g_name = ""
            self.loginWindow = Window()
            self.loginWindow.switch_window.connect(self.update_user_name_and_show)
            self.loginWindow.show()
            try:
                self.loginWindow.raise_()
                self.loginWindow.activateWindow()
            except Exception:
                pass

        else:
            return       

    def delac(self):
        global g_Dbname
        if g_Dbname == "ExcelData":
            QMessageBox.warning(self,"Guest Can't be Delete","You Can not Delete Guest Account. \n You can Delete Your Data!")
        else:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Confirm Delete Account!")
            dlg.setText("You want to Delete your account? \n It losses all your data ")
            dlg.setStandardButtons(QMessageBox.StandardButton.No | QMessageBox.StandardButton.Yes)
            dlg.setIcon(QMessageBox.Icon.Question)
            button = dlg.exec()
            y = 0
            if button == QMessageBox.StandardButton.Yes:
                y = 1
            else:
                y = 0
            if y == 1 :
                connection = mysql.connector.connect(host= hostenv, user= userenv , password= passenv )
                if connection.is_connected():
                    cursor = connection.cursor()
                    cursor.execute(f"DROP DATABASE IF EXISTS `{g_Dbname}`")
                    connection.close()
                delete_conn = mysql.connector.connect(host= hostenv, user= userenv, password= passenv , database="UserData")
                if delete_conn.is_connected():
                    delete_cursor = delete_conn.cursor()
                    delete_cursor.execute("DELETE FROM userpass WHERE Username = %s", (g_Dbname,))
                    delete_conn.commit()
                    delete_cursor.close()
                    delete_conn.close()
                self.Login_pg()
            else:
                return



    def update_user_name_and_show(self):
        try:
            self.userMenu.setTitle(f"&Hi,{g_name}")
            self.nameLabel.setText(f"Hi,{g_name}")
        except Exception:
            pass
        self.show()

    def showTableContextMenu(self, pos):
        index = self.table.indexAt(pos)
        if not index.isValid():
            return

        menu = QMenu(self)
        copy_cell = QAction("Copy Cell", self)
        copy_cell.triggered.connect(self.copyCellValue)
        copy_row = QAction("Copy Row", self)
        copy_row.triggered.connect(self.copyRowValues)
        copy_selected = QAction("Copy Selected Text", self)
        copy_selected.triggered.connect(self.copySelectedText)
        delete_row = QAction("Delete Row", self)
        delete_row.triggered.connect(self.deleteSelectedRow)
        export_sel = QAction("Export Selected Data", self)
        export_sel.triggered.connect(self.exportSelectedData)
        summary = QAction("Selection Summary", self)
        summary.triggered.connect(self.selectionSummary)

        menu.addAction(copy_cell)
        menu.addAction(copy_row)
        menu.addAction(copy_selected)
        menu.addAction(delete_row)
        menu.addSeparator()
        menu.addAction(export_sel)
        menu.addAction(summary)
        menu.exec(self.table.viewport().mapToGlobal(pos))

    def copyCellValue(self):
        item = self.table.currentItem()
        if item is None:
            selected = self.table.selectedItems()
            item = selected[0] if selected else None
        if item is None:
            QMessageBox.information(self, "Copy Cell", "No cell selected.")
            return
        QApplication.clipboard().setText(item.text())
        QMessageBox.information(self, "Copied", "Cell value copied to clipboard.")

    def copyRowValues(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Copy Row", "No row selected.")
            return
        values = []
        for column in range(self.table.columnCount()):
            item = self.table.item(row, column)
            values.append(item.text() if item else "")
        QApplication.clipboard().setText("\t".join(values))
        QMessageBox.information(self, "Copied", "Row copied to clipboard.")

    def copySelectedText(self):
        items = self.table.selectedItems()
        if not items:
            QMessageBox.information(self, "Copy Selected Text", "No text selected.")
            return
        # Preserve selection order by row then column
        items.sort(key=lambda it: (it.row(), it.column()))
        rows = {}
        for it in items:
            rows.setdefault(it.row(), []).append(it.text())
        lines = ["\t".join(rows[r]) for r in sorted(rows.keys())]
        QApplication.clipboard().setText("\n".join(lines))
        QMessageBox.information(self, "Copied", "Selected text copied to clipboard.")

    def deleteSelectedRow(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.information(self, "Delete Row", "No row selected.")
            return
        result = QMessageBox.question(
            self,
            "Delete Row",
            "Do you want to delete the selected row?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
        )
        if result == QMessageBox.StandardButton.Yes:
            self.table.removeRow(row)

    def exportSelectedData(self):
        selected_ranges = self.table.selectedRanges()
        if not selected_ranges:
            QMessageBox.information(self, "Export Selected Rows", "No selection found.")
            return
        rows = set()
        columns = set()
        for selection in selected_ranges:
            rows.update(range(selection.topRow(), selection.bottomRow() + 1))
            columns.update(range(selection.leftColumn(), selection.rightColumn() + 1))
        rows = sorted(rows)
        columns = sorted(columns)
        if not rows or not columns:
            QMessageBox.information(self, "Export Selected Rows", "No selection found.")
            return

        headers = [
            self.table.horizontalHeaderItem(column).text()
            if self.table.horizontalHeaderItem(column)
            else ""
            for column in columns
        ]
        data = []
        for row in rows:
            row_values = []
            for column in columns:
                item = self.table.item(row, column)
                row_values.append(item.text() if item else "")
            data.append(row_values)

        df = pd.DataFrame(data, columns=headers)
        path, _ = QFileDialog.getSaveFileName(
            self,
            "Export Selected Rows",
            "",
            "Excel Files (*.xlsx);;CSV Files (*.csv)",
        )
        if not path:
            return
        try:
            if path.lower().endswith(".csv"):
                df.to_csv(path, index=False)
            else:
                if not path.lower().endswith(".xlsx"):
                    path += ".xlsx"
                df.to_excel(path, index=False)
            QMessageBox.information(self, "Exported", "Selected data exported successfully.")
        except Exception:
            QMessageBox.warning(self, "Export Failed", "Failed to export selected data.")

    def selectionSummary(self):
        selected_items = self.table.selectedItems()
        if not selected_items:
            QMessageBox.information(self, "Selection Summary", "No cells selected.")
            return
        rows = sorted({item.row() for item in selected_items})
        cells = len(selected_items)
        QMessageBox.information(
            self,
            "Selection Summary",
            f"Selected rows: {len(rows)}\nSelected cells: {cells}",
        )

    def apply_custom_styles(self):
        self.setStyleSheet('''
            QMainWindow {
                background-color: #1f2430;
            }
            QLabel {
                color: #f0f4ff;
                font-size: 16px;
                font-family: 'Segoe UI', Arial;
            }
            QComboBox{ background-color: #2a3044;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;}
            QPushButton {
                background-color: #3a4161;
                color: white;
                border-radius: 5px;
                padding: 8px;
                font-weight: bold;
            }
            
            QHeaderView::section {
            background-color: #434852;
            color: white;padding-left: 4px; border: 1px solid #6c6c6c;}
            QHeaderView::section:checked
            { background-color: black;}
        
            QMenu {
                background-color: #161C3C;
                border: 1px solid rgba(0,0,0,0.6);
                border-radius: 8px;
                padding: 6px;
                /* subtle shadow-like effect via semi-transparent border and spacing */
            }
            QMenu::item {
                background-color: transparent;
                padding: 6px 18px;
                border-radius: 6px;
            }
            QMenu::item:selected {
                background-color: qlineargradient(x1:0, y1:0, x2:1, y2:0, stop:0 #1E90FF, stop:1 #1976D2);
                color: white;
            }
            QMenu::item:checked {
                background-color: #5E45E8;
                color: white;
            }
            QMenu::separator {
                height: 2px;
                background: rgba(255,255,255,0.06);
                margin-left: 8px;
                margin-right: 8px;
                border-radius: 1px;
            }
            QMenuBar {
                background-color: #1a1f26;
                spacing: 10px;
                border-bottom: 2px solid #0E69B5;
            }
            QMenuBar::item {
                color: #e8eef8;
                padding: 8px 14px;
                border-radius: 5px;
                margin: 3px 2px;
                font-weight: 600;
            }
            QMenuBar::item:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #1E4D7B, stop:1 #0E69B5);
                color: #ffffff;
                border: 1px solid #0E69B5;
            }
            QMenuBar::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #0E69B5, stop:1 #0B4F8A);
                color: white;
                border: 1px solid #0E69B5;
            }
            QMenuBar::item:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #539FDF, stop:1 #2B7FD1);
                color: white;
                border: 1px solid #539FDF;
            }
            QMenuBar::item:open {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1, stop:0 #539FDF, stop:1 #2B7FD1);
                color: white;
                border: 1px solid #539FDF;
            }

            QPushButton:hover {
                background-color: #0098ff;
            }''')

    def onHeaderClicked(self, logicalIndex):
        engine = create_engine(f'{db_info}{g_Dbname}')
        table_name = getattr(self, 'current_table', 'data') or 'data'
        tableData = f"SELECT * FROM `{table_name}`"
        ds = pd.read_sql_query(tableData, engine)
        a = logicalIndex
        sort_col = ds.columns[a]
        ds = ds.sort_values(by=sort_col)
        self.table.setRowCount(ds.shape[0])
        self.table.setColumnCount(ds.shape[1])
        self.table.setHorizontalHeaderLabels(ds.columns)
        for i in range(ds.shape[0]):
            for j in range(ds.shape[1]):
                self.table.setItem(i, j,QTableWidgetItem(str(ds.iat[i, j])))
        try:
            self.table.horizontalHeader().sectionClicked.disconnect(self.onHeaderClicked)
        except Exception:
            pass
        self.table.horizontalHeader().sectionClicked.connect(self.onHeader2ndClicked)

    def onHeader2ndClicked(self, logicalIndex):    
        a = logicalIndex
        engine = create_engine(f'{db_info}{g_Dbname}')
        table_name = getattr(self, 'current_table', 'data') or 'data'
        tableData = f"SELECT * FROM `{table_name}`"
        ds = pd.read_sql_query(tableData, engine)
        sort_col = ds.columns[a]
        ds = ds.sort_values(by=sort_col, ascending=False)
        self.table.setRowCount(ds.shape[0])
        self.table.setColumnCount(ds.shape[1])
        self.table.setHorizontalHeaderLabels(ds.columns)
        for i in range(ds.shape[0]):
            for j in range(ds.shape[1]):
                self.table.setItem(i, j,QTableWidgetItem(str(ds.iat[i, j])))
        try:
            self.table.horizontalHeader().sectionClicked.disconnect(self.onHeader2ndClicked)
        except Exception:
            pass
        self.table.horizontalHeader().sectionClicked.connect(self.onHeaderClicked)

    def _exclusive_check(self, action, checked):
        if not checked:
            return
        for act in self._checkable_actions:
            if act is not action:
                act.setChecked(False)

    def loadData(self):

        file_name = QFileDialog.getOpenFileName(self,"Select Excel File","","Excel Files (*.xlsx *.xls)")
        if not file_name[0]:
            return

        try:
            df = pd.read_excel(file_name[0])
            self.table.setRowCount(df.shape[0])
            self.table.setColumnCount(df.shape[1])
            self.table.setHorizontalHeaderLabels(df.columns)
            for i in range(df.shape[0]):
                for j in range(df.shape[1]):
                    self.table.setItem(i, j,QTableWidgetItem(str(df.iat[i, j])))
        except Exception:
            QMessageBox.warning(self,"Error","Failed to Load Excel File")
            return

        dlg = QMessageBox(self)
        dlg.setWindowTitle("Confirm File!")
        dlg.setText("You want to upload this file in sql")
        dlg.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        dlg.setIcon(QMessageBox.Icon.Question)
        button = dlg.exec()
        y = 0
        if button == QMessageBox.StandardButton.Yes:
            y = 1
        else:
            QMessageBox.warning(self,"Error","File Upload failed in Database")

        if y == 1:

            try:
                df = pd.read_excel(file_name[0])
                base = os.path.basename(file_name[0])
                base_name = base.lower()
                table_name = os.path.splitext(base_name)[0]
                engine = create_engine(f'{db_info}{g_Dbname}')
                df.columns = df.columns.astype(str)
                columns = []
                seen = {}
                for col in df.columns:
                    if col in seen:
                        seen[col] += 1
                        columns.append(f"{col}_{seen[col]}")
                    else:
                        seen[col] = 0
                        columns.append(col)
                df.columns = columns
                df.to_sql(table_name, con= engine, if_exists="replace",  index=False)
                self.current_table = table_name
                self.refresh_table_buttons()
                QMessageBox.about(self, "Success", f"Data inserted into database table '{table_name}' successfully")
            except Exception as e:
                QMessageBox.warning(self, "Error", "Failed to Insert Data into Database")
                return

    def selectdata(self):
        engine = create_engine(f'{db_info}{g_Dbname}')
        try:
            tables_df = pd.read_sql_query("SHOW TABLES", engine)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to retrieve tables:\n{str(e)}")
            return

        if tables_df.empty:
            QMessageBox.information(self, "No Tables", "No tables found in database.")
            return

        table_names = tables_df.iloc[:, 0].astype(str).tolist()

        dialog = QDialog(self)
        dialog.setWindowTitle("Select Table to Load")
        dialog.setModal(True)
        dialog.resize(420, 170)

        info_label = QLabel("Choose a table from the database to display.")
        info_label.setWordWrap(True)

        form = QFormLayout()
        button_layout = QHBoxLayout()
        ok_button = QPushButton("Load")
        cancel_button = QPushButton("Cancel")
        ok_button.setDefault(True)
        cancel_button.setAutoDefault(False)
        button_layout.addStretch(1)
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        main_layout = QVBoxLayout(dialog)
        main_layout.addWidget(info_label)
        main_layout.addLayout(form)
        main_layout.addLayout(button_layout)

        table_combo = QComboBox()
        table_combo.addItems(table_names)
        table_combo.setCurrentIndex(0)
        form.addRow("Table:", table_combo)
        okPressed = False

        def on_ok():
            nonlocal okPressed
            okPressed = True
            dialog.accept()

        ok_button.clicked.connect(on_ok)
        cancel_button.clicked.connect(dialog.reject)

        if dialog.exec() != QDialog.DialogCode.Accepted or not okPressed:
            return

        table_name = table_combo.currentText()
        try:
            ds = pd.read_sql_query(f"SELECT * FROM `{table_name}`", engine)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load table data:\n{str(e)}")
            return

        self.table.setRowCount(ds.shape[0])
        self.table.setColumnCount(ds.shape[1])
        self.table.setHorizontalHeaderLabels(ds.columns)
        for i in range(ds.shape[0]):
            for j in range(ds.shape[1]):
                self.table.setItem(i, j, QTableWidgetItem(str(ds.iat[i, j])))
        self.current_table = table_name

    def deletedata(self):
        engine = create_engine(f'{db_info}{g_Dbname}')
        try:
            tables_df = pd.read_sql_query("SHOW TABLES", engine)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to retrieve tables")
            return

        if tables_df.empty:
            QMessageBox.information(self, "No Tables", "No tables found in database.")
            return

        table_names = tables_df.iloc[:, 0].astype(str).tolist()

        dialog = QDialog(self)
        dialog.setWindowTitle("Select Table")
        form = QFormLayout()
        button_layout = QVBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        main_layout = QVBoxLayout(dialog)
        main_layout.addLayout(form)
        main_layout.addLayout(button_layout)

        table_combo = QComboBox()
        table_combo.addItems(table_names)
        form.addRow("Select Table:", table_combo)
        okPressed = False

        def on_ok():
            nonlocal okPressed
            okPressed = True
            dialog.accept()

        ok_button.clicked.connect(on_ok)
        cancel_button.clicked.connect(dialog.reject)

        if dialog.exec() != QDialog.DialogCode.Accepted or not okPressed:
            return

        Dtable_name = table_combo.currentText()
        try:
            self.table.setColumnCount(0)
            self.table.setRowCount(0)
            with engine.begin() as conn:
                conn.execute(text(f"DROP TABLE `{Dtable_name}`"))
            self.current_table = None
            self.refresh_table_buttons()
            QMessageBox.about(self, "Success", f"Successfully Deleted Table: {Dtable_name}")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to delete table {Dtable_name}:\n{str(e)}")
            return


    
    def CData(self):
        engine = create_engine(f'{db_info}{g_Dbname}')
        table_name = getattr(self, 'current_table', None)
        if not table_name:
            QMessageBox.warning(self, "Error", "No table is selected for display")
            return
        tableData = f"SELECT * FROM `{table_name}`"
        try:
            ds = pd.read_sql_query(tableData, engine)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load table data:First Select Table Data")
            return
        self.current_table = table_name
        self.table.setRowCount(ds.shape[0])
        self.table.setColumnCount(ds.shape[1])
        self.table.setHorizontalHeaderLabels(ds.columns)
        for i in range(ds.shape[0]):
            for j in range(ds.shape[1]):
                self.table.setItem(i, j,QTableWidgetItem(str(ds.iat[i, j])))

    def rev(self):
        engine = create_engine(f'{db_info}{g_Dbname}')
        table_name = getattr(self, 'current_table', None)
        if not table_name:
            QMessageBox.warning(self, "Error", "No table is selected for display")
            return
        tableData = f"SELECT * FROM `{table_name}`"
        try:
            ds = pd.read_sql_query(tableData, engine)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load table data:Make Sure to Select Table")
            return
        headerlable = ds.columns.tolist()
        rows = []
        items = headerlable
        dialog = QDialog(self)
        dialog.setWindowTitle("Select Date and Revenue Columns")
        dialog.setWindowModality(Qt.WindowModality.ApplicationModal)
        dialog.resize(460, 230)
        dialog.setStyleSheet('''
            QDialog { background-color: #232733; }
            QLabel { color: #f0f4ff; font-size: 14px; }
            QComboBox {
                background-color: #2c3346;
                color: #ffffff;
                border: 1px solid #546d99;
                border-radius: 6px;
                padding: 6px 8px;
                min-width: 280px;
            }
            QPushButton {
                background-color: #0E69B5;
                color: #ffffff;
                border-radius: 6px;
                padding: 8px 14px;
                min-width: 90px;
            }
            QPushButton:hover { background-color: #1e83d0; }
        ''')

        form = QFormLayout()
        form.setLabelAlignment(Qt.AlignmentFlag.AlignLeft)
        form.setHorizontalSpacing(16)
        button_layout = QHBoxLayout()
        ok_button = QPushButton("OK")
        cancel_button = QPushButton("Cancel")
        button_layout.addStretch()
        button_layout.addWidget(ok_button)
        button_layout.addWidget(cancel_button)

        main_layout = QVBoxLayout(dialog)
        main_layout.addLayout(form)
        main_layout.addLayout(button_layout)

        Date_combo = QComboBox()
        Date_combo.addItems(items)
        Date_combo.setToolTip("Choose the date column for revenue aggregation")
        if "Date" in items:
            Date_combo.setCurrentText("Date")
        form.addRow("Date Column:", Date_combo)

        rev_combo = QComboBox()
        rev_combo.addItems(items)
        rev_combo.setToolTip("Choose the revenue column to summarize")
        if "TotalPrice" in items:
            rev_combo.setCurrentText("TotalPrice")
        form.addRow("Revenue Column:", rev_combo)

        okPressed = False

        def on_ok():
            nonlocal okPressed
            okPressed = True
            dialog.accept()

        ok_button.clicked.connect(on_ok)
        cancel_button.clicked.connect(dialog.reject)

        if dialog.exec() != QDialog.DialogCode.Accepted or not okPressed:
            return

        date = headerlable.index(Date_combo.currentText())
        rev = headerlable.index(rev_combo.currentText())

        for row in ds.itertuples(index=False):
            date1 = row[date]
            rev1 = row[rev]
            rows.append((date1, rev1))

        revun = pd.DataFrame(rows, columns=["Date", "Revenue"]) if rows else pd.DataFrame(columns=["Date","Revenue"])
        revd = revun.groupby("Date")["Revenue"].sum().reset_index()

        self.table.setRowCount(revd.shape[0])
        self.table.setColumnCount(revd.shape[1])
        self.table.setHorizontalHeaderLabels(revd.columns)

        for i in range(revd.shape[0]):
            for j in range(revd.shape[1]):
                self.table.setItem(i, j,QTableWidgetItem(str(revd.iat[i, j])))

    def lstasts(self):
        engine = create_engine(f'{db_info}{g_Dbname}')
        table_name = getattr(self, 'current_table', None)
        if not table_name:
            QMessageBox.warning(self, "Error", "No table is selected for display")
            return
        tableData = f"SELECT * FROM `{table_name}` Order by `Date`"
        try:
            ds = pd.read_sql_query(tableData, engine)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to load table data:Make Sure to Select Table")
            return
        
        # Create dialog with predefined options
        dialog = QDialog(self)
        dialog.setWindowTitle("Preview Rows")
        layout = QVBoxLayout()
        
        label = QLabel("Select number of rows to preview or enter manually:")
        layout.addWidget(label)
        
        combo = QComboBox()
        predefined_values = ["10", "20", "50", "100"]
        combo.addItems(predefined_values)
        combo.setEditable(True)
        combo.setEditText("10")
        layout.addWidget(combo)
        
        button_layout = QHBoxLayout()
        ok_btn = QPushButton("OK")
        cancel_btn = QPushButton("Cancel")
        button_layout.addWidget(ok_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
        dialog.setLayout(layout)
        
        ok_clicked = False
        def on_ok():
            nonlocal ok_clicked
            ok_clicked = True
            dialog.accept()
        
        ok_btn.clicked.connect(on_ok)
        cancel_btn.clicked.connect(dialog.reject)
        
        if dialog.exec() != QDialog.DialogCode.Accepted or not ok_clicked:
            return
        
        try:
            lastdt = int(combo.currentText().strip())
            if lastdt <= 0:
                raise ValueError
        except ValueError:
            QMessageBox.warning(self, "Invalid input", "Please enter a valid positive number of rows.")
            return
        
        stats = ds.tail(lastdt)
        self.table.setRowCount(stats.shape[0])
        self.table.setColumnCount(stats.shape[1])
        self.table.setHorizontalHeaderLabels([str(col) for col in stats.columns])
        for i in range(stats.shape[0]):
            for j in range(stats.shape[1]):
                value = stats.iloc[i, j]
                self.table.setItem(i, j, QTableWidgetItem(str(value)))

        

    def _save_dataframe_to_file(self, ds, file_name, selected_filter):
        if not file_name:
            return False

        name, ext = os.path.splitext(file_name)
        ext = ext.lower()
        if not ext:
            if selected_filter and "CSV" in selected_filter:
                ext = ".csv"
            elif selected_filter and "PDF" in selected_filter:
                ext = ".pdf"
            elif selected_filter and "HTML" in selected_filter:
                ext = ".html"
            else:
                ext = ".xlsx"
            file_name = name + ext

        try:
            if ext in ['.xlsx', '.xls']:
                ds.to_excel(file_name, index=False)
            elif ext == '.csv':
                ds.to_csv(file_name, index=False)
            elif ext in ['.html', '.htm']:
                ds.to_html(file_name, index=False)
            elif ext == '.pdf':
                fig, ax = plt.subplots(figsize=(11.69, 8.27))
                ax.axis('tight')
                ax.axis('off')
                table = ax.table(cellText=ds.values.tolist(), colLabels=ds.columns.tolist(), loc='center')
                table.auto_set_font_size(False)
                table.set_fontsize(8)
                table.scale(1, 1.5)
                fig.subplots_adjust(left=0.05, right=0.95, top=0.95, bottom=0.05)
                fig.savefig(file_name, format='pdf', bbox_inches='tight')
                plt.close(fig)
            else:
                ds.to_excel(file_name, index=False)
            return True
        except Exception:
            return False

    def export_data(self):
        table_name = getattr(self, 'current_table')
        try:
            tableData = f"SELECT * FROM `{table_name}`"
            engine = create_engine(f'{db_info}{g_Dbname}')
            ds = pd.read_sql_query(tableData, engine)

            try:
                file_name, selected_filter = QFileDialog.getSaveFileName(self,"Save File","","Excel Files (*.xlsx)")
                if file_name:
                    if self._save_dataframe_to_file(ds, file_name, selected_filter):
                        QMessageBox.about(self, "Success", "Data exported successfully.")
                    else:
                        QMessageBox.warning(self, "Error", "Failed to export data.")
                    return
            except Exception:
                QMessageBox.warning(self, "Error", "Failed to export data.")
                return
        except:
           QMessageBox.warning(self, "Error", "First select a table.")


    def saveas_data(self):
        table_name = getattr(self, 'current_table')
        try:
            tableData = f"SELECT * FROM `{table_name}`"
            engine = create_engine(f'{db_info}/{g_Dbname}')
            ds = pd.read_sql_query(tableData, engine)

            try:
                file_name, selected_filter = QFileDialog.getSaveFileName(self,"Save File","","Excel Files (*.xlsx);;CSV Files (*.csv);;PDF Files (*..pdf);;HTML Files (*.html *.htm)")
                if file_name:
                    if self._save_dataframe_to_file(ds, file_name, selected_filter):
                        QMessageBox.about(self, "Success", "Data exported successfully.")
                    else:
                        QMessageBox.warning(self, "Error", "Failed to export data.")
                    return
            except Exception:
                QMessageBox.warning(self, "Error", "Failed to export data.")
                return
        except:
           QMessageBox.warning(self, "Error", "First select a table.")

    def saveEditedData(self):
        table_name = getattr(self, 'current_table', None)
        if not table_name:
            QMessageBox.warning(self, "Error", "No table is selected to save.")
            return
        row_count = self.table.rowCount()
        col_count = self.table.columnCount()
        if row_count == 0 or col_count == 0:
            QMessageBox.warning(self, "Error", "No data available in the table to save.")
            return
        headers = []
        for col in range(col_count):
            item = self.table.horizontalHeaderItem(col)
            if item is None or not item.text():
                QMessageBox.warning(self, "Error", "Missing table headers. Cannot save data.")
                return
            headers.append(item.text())
        data = []
        for i in range(row_count):
            row_values = []
            for j in range(col_count):
                item = self.table.item(i, j)
                row_values.append(item.text() if item else "")
            data.append(row_values)
        try:
            df = pd.DataFrame(data, columns=headers)
            engine = create_engine(f'{db_info}{g_Dbname}')
            df.to_sql(table_name, con=engine, if_exists='replace', index=False)
            QMessageBox.about(self, "Success", f"Edited data saved to database table '{table_name}'.")
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Failed to save edited data:\n{str(e)}")

    def find_in_table(self):
        if self.table.rowCount() == 0 or self.table.columnCount() == 0:
            QMessageBox.warning(self, "Find", "No table data available to search.")
            return
        text, ok = QInputDialog.getText(self, "Find in Table", "Enter text to find:")
        if not ok:
            return
        search_text = text.strip()
        if not search_text:
            QMessageBox.warning(self, "Find", "Please enter text to search for.")
            return

        found_items = []
        for row in range(self.table.rowCount()):
            for col in range(self.table.columnCount()):
                item = self.table.item(row, col)
                if item and search_text.lower() in item.text().lower():
                    found_items.append(item)

        self.table.clearSelection()
        if not found_items:
            QMessageBox.information(self, "Find", f"No matches found for '{search_text}'.")
            return

        for item in found_items:
            item.setSelected(True)
        first_item = found_items[0]
        self.table.setCurrentItem(first_item)
        self.table.scrollToItem(first_item)
        QMessageBox.information(self, "Find", f"Found {len(found_items)} matching cell(s).")

    def more_window(self):
        try:
            tableData = f"SELECT * FROM `{self.current_table}`"
            engine = create_engine(f'{db_info}{g_Dbname}')
            ds = pd.read_sql_query(tableData, engine)
            self.another_window = AnotherWindow(getattr(self, 'current_table'))
            self.another_window.show()
        except:
           QMessageBox.warning(self,"Error","First Select file for Anlaysis From Select tab")

class Controller:
    def __init__(self):
        self.initial = Window()
        self.main = None
        self.initial.switch_window.connect(self.show_main) # Connect signal
        self.initial.show()

    def show_main(self):
        self.main = analysis() # Keep reference
        self.main.show()
        self.initial.close() # Close previous


g_Dbname =""
g_name = ""
ab = 0

app = QApplication(sys.argv)
controller = Controller()
sys.exit(app.exec())
        
        
