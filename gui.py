from tkinter import StringVar, Toplevel, ttk, Tk
from functions import Functions

class authentication(Tk):
    def __init__(self):
        super().__init__()

        # Initiate functions
        self.functions = Functions()

        # Window setting
        self.title("Authentication phase")
        self.geometry("350x100")

        # Configure grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=2)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        # Row 0
        ttk.Label(self, text="User:").grid(row=0, column=0, padx=10)
        self.userVal = StringVar()
        self.userEntry = ttk.Entry(self, textvariable=self.userVal)
        self.userEntry.grid(row=0, column=1)

        # Row 1
        ttk.Label(self, text="Password:").grid(row=1, column=0, padx=10)
        self.pwdVal = StringVar()
        self.pwdEntry = ttk.Entry(self, textvariable=self.pwdVal)
        self.pwdEntry.grid(row=1, column=1)

        # Login button
        self.submit = ttk.Button(self, text="Login")
        self.submit.grid(row=2, column=1, ipadx=30, sticky="EW")
        self.submit['command'] = self.onLogin

        # Register button
        self.register = ttk.Button(self, text="Register")
        self.register.grid(row=2, column=0, ipadx=20, sticky="EW")
        self.register['command'] = self.onRegister

        # Test only
        self.userVal.set("Drownie")
        self.pwdVal.set("12345")

    def checkEmpty(self, entries):
        if entries.get():
            return entries.get()
        else:
            return 

    def onRegister(self):
        if self.checkEmpty(self.userEntry) and self.checkEmpty(self.pwdEntry):
            inp = [self.userEntry.get(), self.pwdEntry.get()]
            res = self.functions.register(inp)
            print(res)
        else:
            print("Please fill the box username and password")

    def onLogin(self):
        if self.checkEmpty(self.userEntry) and self.checkEmpty(self.pwdEntry):
            inp = [self.userEntry.get(), self.pwdEntry.get()]
            res = self.functions.authenticate(inp)
            if res['success']:
                apk = app(self, res['result'], lambda: self.onLogout(apk))
                apk.protocol("WM_DELETE_WINDOW", lambda: self.onClosed(apk))
                self.withdraw()
            else:
                print(f"Gagal - {res['result']}")
        else:
            print("Please fill the box username and password")

    def onLogout(self, apk):
        self.userVal.set("")
        self.pwdVal.set("")
        self.deiconify()
        apk.destroy()

    def onClosed(self, apk):
        apk.destroy()
        self.destroy()

    def update(self):
        self.update_idletasks()

class app(Toplevel):
    def __init__(self, root, private_key, logout):
        super().__init__(root)

        # Initiate functions
        self.functions = Functions()

        # Register private key
        self.privateKey = private_key

        # Window setting
        self.title("Password Encrypter")
        self.geometry("350x150")

        # configure grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.columnconfigure(2, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)
        self.rowconfigure(3, weight=1)

        # Row 0
        ttk.Label(self, text="Site: ").grid(row=0, column=0)
        siteValue = StringVar()
        self.siteEntry = ttk.Entry(self, textvariable=siteValue)
        self.siteEntry.grid(row=0, column=1, columnspan=2, ipadx=20, ipady=1)

        # Row 1
        ttk.Label(self, text="Username:").grid(row=1, column=0)
        userValue = StringVar()
        self.userEntry = ttk.Entry(self, textvariable=userValue)
        self.userEntry.grid(row=1, column=1, columnspan=2, ipadx=20, ipady=1)

        # Row 2
        ttk.Label(self, text="Password:").grid(row=2, column=0)
        pwdValue = StringVar()
        self.pwdEntry = ttk.Entry(self, textvariable=pwdValue)
        self.pwdEntry.grid(row=2, column=1, columnspan=2, ipadx=20, ipady=1)

        # Row 3
        self.listButton = ttk.Button(self, text="List...")
        self.listButton.grid(row=3, column=0, ipadx=10)
        self.encryptButton = ttk.Button(self, text="Encrypt")
        self.encryptButton.grid(row=3, column=1, ipadx=10)
        self.encryptButton['command'] = self.onEncrypt
        self.logoutButton = ttk.Button(self, text="Logout")
        self.logoutButton.grid(row=3, column=2, ipadx=10)
        self.logoutButton['command'] = logout
    
    def checkEmpty(self, entries):
        if entries.get():
            return entries.get()
        else:
            return 

    def onEncrypt(self):
        if (self.checkEmpty(self.siteEntry) and self.checkEmpty(self.userEntry) and self.checkEmpty(self.pwdEntry)):
            newData = {"site": self.siteEntry.get(), "username": self.userEntry.get(), "password": self.pwdEntry.get()}
            # print(newData, self.privateKey)
            res = self.functions.addNewData(self.privateKey, newData)
            print(res['result'])
        else:
            print("Please fill the box username and password")

    def update(self):
        self.update_idletasks()

if __name__ == "__main__":
    test = authentication()
    test.mainloop()