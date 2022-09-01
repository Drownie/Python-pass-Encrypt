import math
from tkinter import StringVar, Toplevel, ttk, Tk, END, messagebox
from functions import Functions

class authentication(Tk):
    def __init__(self):
        super().__init__()

        # Initiate functions
        self.functions = Functions()

        # Window setting
        self.title("Authentication phase")
        self.geometry("350x100")
        self.resizable(False, False)

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
        self.pwdEntry = ttk.Entry(self, textvariable=self.pwdVal, show="*")
        self.pwdEntry.grid(row=1, column=1)

        # Login button
        self.submit = ttk.Button(self, text="Login")
        self.submit.grid(row=2, column=1, ipadx=30, sticky="EW")
        self.submit['command'] = self.onLogin

        # Register button
        self.register = ttk.Button(self, text="Register")
        self.register.grid(row=2, column=0, ipadx=20, sticky="EW")
        self.register['command'] = self.onRegister

    def checkEmpty(self, entries):
        if entries.get():
            return entries.get()
        else:
            return 

    def onRegister(self):
        if self.checkEmpty(self.userEntry) and self.checkEmpty(self.pwdEntry):
            inp = [self.userEntry.get(), self.pwdEntry.get()]
            res = self.functions.register(inp)
            if res['success']:
                messagebox.showinfo("Registration result", res['result'])
            else:
                messagebox.showerror("Registration result", res['result'])
            self.userVal.set("")
            self.pwdVal.set("")
        else:
            messagebox.showwarning("Warning", "Please fill the box username and password")

    def onLogin(self):
        if self.checkEmpty(self.userEntry) and self.checkEmpty(self.pwdEntry):
            inp = [self.userEntry.get(), self.pwdEntry.get()]
            res = self.functions.authenticate(inp)
            if res['success']:
                apk = app(self, res, lambda: self.onLogout(apk))
                apk.protocol("WM_DELETE_WINDOW", lambda: self.onClosed(apk))
                self.withdraw()
            else:
                messagebox.showerror("Login result", res['result'])
        else:
            messagebox.showwarning("Warning", "Please fill the box username and password")

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
    def __init__(self, root, userData, logout):
        super().__init__(root)

        # Initiate functions
        self.functions = Functions()

        # Register variable
        self.user = userData["user"]
        self.privateKey = userData["result"]

        # Window setting
        self.title("Password Encrypter")
        self.geometry("350x150")
        self.resizable(False, False)

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
        self.siteValue = StringVar()
        self.siteEntry = ttk.Entry(self, textvariable=self.siteValue)
        self.siteEntry.grid(row=0, column=1, columnspan=2, ipadx=20, ipady=1)

        # Row 1
        ttk.Label(self, text="Username:").grid(row=1, column=0)
        self.userValue = StringVar()
        self.userEntry = ttk.Entry(self, textvariable=self.userValue)
        self.userEntry.grid(row=1, column=1, columnspan=2, ipadx=20, ipady=1)

        # Row 2
        ttk.Label(self, text="Password:").grid(row=2, column=0)
        self.pwdValue = StringVar()
        self.pwdEntry = ttk.Entry(self, textvariable=self.pwdValue, show="*")
        self.pwdEntry.grid(row=2, column=1, columnspan=2, ipadx=20, ipady=1)

        # Row 3
        self.listButton = ttk.Button(self, text="List...")
        self.listButton.grid(row=3, column=0, ipadx=10)
        self.listButton['command'] = self.onOpenList
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
            res = self.functions.addNewData(self.user, self.privateKey, newData)
            self.siteValue.set("")
            self.pwdValue.set("")
            self.userValue.set("")
            messagebox.showinfo("Encryption Result", res['result'])
        else:
            messagebox.showwarning("Warning", "Please fill all the data required")

    def onOpenList(self):
        dataApk = dataApp(self, {"user": self.user, "result": self.privateKey}, 10)
        dataApk.protocol("WM_DELETE_WINDOW", lambda: self.onDataAppClosed(dataApk))
        self.withdraw()

    def onDataAppClosed(self, apk):
        apk.destroy()
        self.deiconify()

    def update(self):
        self.update_idletasks()

class dataApp(Toplevel):
    def __init__(self, root, userData, mpp=10):
        super().__init__(root)

        # App setting
        self.page = 1
        self.n = 0
        self.maks_per_page = mpp
        self.functions = Functions()
        self.user = userData["user"]
        self.privateKey = userData["result"]

        # Window setting
        self.title("Data App")
        self.geometry("500x260")
        self.resizable(False, False)

        # Configure grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)
        self.rowconfigure(2, weight=1)

        # Define columns
        col = ('no', 'site', 'username', 'pwd')

        # Row 1
        self.tree = ttk.Treeview(self, columns=col, show='headings')
        self.tree.grid(row=0, column=0, columnspan=3)

        self.tree.column('no', width=40, anchor='c')
        self.tree.column('site', width=180, anchor='c')
        self.tree.column('username', width=180, anchor='c')
        self.tree.column('pwd', width=100, anchor='c')

        # Define headings
        self.tree.heading('no', text="No")
        self.tree.heading('site', text="Site")
        self.tree.heading('username', text="Username")
        self.tree.heading('pwd', text="Password")

        # fill the tree
        self.onFetch()

        # Row 2
        self.prevButton = ttk.Button(self, text="Prev")
        self.prevButton.grid(row=1, column=0)
        self.prevButton['command'] = self.onPrev

        self.pageVal = StringVar()
        self.pageLabel = ttk.Label(self, textvariable=self.pageVal)
        self.pageLabel.grid(row=1, column=1)

        self.nextButton = ttk.Button(self, text="Next")
        self.nextButton.grid(row=1, column=2, padx=60)
        self.nextButton['command'] = self.onNext
        self.update()
    
    def onNext(self):
        if self.n > self.page * self.maks_per_page:
            self.page += 1
            self.pageVal.set(f"{self.page} / {int(self.n / self.maks_per_page) + 1}")
            self.onFetch()
        self.update()

    def onFetch(self):
        for i in self.tree.get_children():
            self.tree.delete(i)
        tmpData, self.n = self.functions.decodeData(self.user, self.privateKey, self.page, self.maks_per_page)

        for id, data in enumerate(tmpData):
            self.tree.insert('', END, values=(id+1, data['site'], data['username'], data['password']))

    def onPrev(self):
        if self.page > 1:
            self.page -= 1
            self.onFetch()
        self.update()
    
    def update(self):
        # page label
        self.pageVal.set(f"{self.page} / {math.ceil(self.n / self.maks_per_page)}")

        # prev button
        if self.page > 1:
            self.prevButton['state'] = 'active'
        else:
            self.prevButton['state'] = 'disabled'
        
        # next button
        if self.n > self.page * self.maks_per_page:
            self.nextButton['state'] = 'active'
        else:
            self.nextButton['state'] = 'disabled'
        self.update_idletasks()

if __name__ == "__main__":
    test = authentication() #"Drownie12", "test"
    test.mainloop()