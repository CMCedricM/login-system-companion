import os, sys
import tkinter as tk
from resources.web import createUser, loginUser, logoutUser

FILE_PATH = os.path.dirname(os.path.abspath(__file__))
WAIT_TIME = 5 * 1000 # Check Every 5 Seconds
TIMEOUT = 30*1000 # Wait 30 seconds

         

# This will be the main window, aka login window
class mainWindow(tk.Tk): 
    def __init__(self): 
        
        # Setup Paths 
        self.ICON = os.path.join(FILE_PATH, "assets", "icon.png")
        super().__init__()
        # Window Sizing 
        self.HEIGHT, self.WIDTH = 553, 253
        self.MIN_HEIGHT, self.MIN_WIDTH = 372, 256
        
        # Setup Window
        self.title("System Login")
        self.resizable(False, False)

        # Buttons 
        self.userName, self.userEntry, self.passWord, self.passEntry = None, None, None, None
        self.statusMSG, self.showPassActive = None, False 
        self.userValue, self.passValue = None, None
        self.bgColor = None 
        
        
        # External Windows
        self.toDoWindow = None 
        # Check Platform Since icons Config are Different
        self.__platformCheck()
     
            
    def __platformCheck(self):  
        if sys.platform.lower() == 'darwin':
            self.ICONIMG = tk.Image('photo', file=self.ICON)
            self.tk.call('wm', 'iconphoto', self._w, self.ICONIMG)
        elif sys.platform.lower() == 'win32':
            self.iconbitmap(self.ICON.replace('.png', '.ico'))
            self.HEIGHT, self.WIDTH = 626, 299
            self.MIN_HEIGHT, self.MIN_WIDTH = 626, 299
        else:
            pass 
            #self.root.iconbitmap(self.ICON.replace('.png', '.xbm'))
        
        self.resizable(False,False)
    
    
    def checkSize(self, event=None): 
        print(self.winfo_width(), self.winfo_height())
    

    def showPass(self): 
        if(not self.showPassActive):
            self.passEntry.config(show='')
            self.showPassActive = True
        else: 
            self.passEntry.config(show='*')
            self.showPassActive = False 
           
    
    def createWindow(self): 
        # Create Window
        self.geometry(f'{self.HEIGHT}x{self.WIDTH}')
        self.resizable(self.MIN_WIDTH, self.MIN_HEIGHT )

        self.statusMSG= tk.Label(self, text="Please Login Below", anchor='center', font=('American Typewriter', 18))
        self.bgColor = self.statusMSG.cget("background") # Need to do this so i can reset the prompt later
        self.statusMSG.grid(row=1, column=2, columnspan=2, sticky=tk.N)
       
       
        self.userName = tk.Label(self, text="Username:", pady=20, padx=20, anchor='center', font=('American Typewriter', 18))
        self.userEntry = tk.Entry(self, bd=2, width=30, font=('American Typewriter', 18))
        
        self.userName.grid(row=2, column=1, columnspan=2, sticky=tk.W)
        self.userEntry.grid(row=2, column=2, sticky=tk.W)
    
        
        self.passWord = tk.Label( self, text="Password:", pady=20, padx=20, anchor='center', font=('American Typewriter', 18))
        self.passEntry = tk.Entry(self, bd=2, width=30, font=('American Typewriter', 18), show='*')
        
        self.passWord.grid(row=3, column=1, sticky=tk.W)
        self.passEntry.grid(row=3, column=2, sticky=tk.W)
        tk.Checkbutton(self, text="Show Password", font=('American Typewriter', 18),  command=self.showPass).grid(row=4, column=2, sticky=tk.W)
        
        # Attempt Login on "Enter" Keypress
        self.passEntry.bind("<Return>", self.attemptLogin)
        
        tk.Button(self, text="Login", pady=20, padx=20, height=1, width=8, command=self.attemptLogin, anchor='center').grid(row=5, column=2, columnspan=2)
    
        # Set a timer to check if the user has input any data
        self.checkForInputTimer()
        
    # The trick is we want to wait for input before we create the timeout to clear the data
    def checkForInputTimer(self): 
       # If there is data input then give the user an additonal TIMEOUT seconds to finish input
        if(self.userEntry.get() != '' or self.passEntry.get() != ''): 
            self.passEntry.after(TIMEOUT, self.clearInput)
        else:  # If there is no data, continue checking every WAIT_TIME secs for input
            self.passEntry.after(WAIT_TIME, self.checkForInputTimer)
        
    def clearInput(self): 
        # If there is data, then clear input
        self.userEntry.delete(0, tk.END)
        self.passEntry.delete(0, tk.END)
        # Keep Checking For Input
        self.checkForInputTimer() 
        
        
    def attemptLogin(self, e=None):
       self.userValue = self.userEntry.get()
       self.passValue = self.passEntry.get()
   
       if (self.userValue and self.passValue): 
           
            res, text = loginUser(self.userValue, self.passValue)
            if(res): 
                self.statusMSG.config(text="Please Login Below",bg=self.bgColor, fg='white', font=('American Typewriter', 18))
                self.userEntry.delete(0, tk.END)
                self.passEntry.delete(0, tk.END)
                # Since We Have Been Verified, Show the To Do Window
                self.showToDoWindow()
            else: 
                self.statusMSG.config(text=f"Error: {text}", bg='red', fg='white', font=('American Typewriter', 18, 'bold'))
                # Set a timeout to clear the input 
                self.checkForInputTimer()
           
       else: 
           self.statusMSG.config(text="Do not leave blank fields", bg='red', fg='white', font=('American Typewriter', 18, 'bold')) 
           self.checkForInputTimer()
       
    def showToDoWindow(self): 
        self.withdraw()
        self.toDoWindow = toDoWindow(self) 
        self.toDoWindow.grab_set()
           
    def run(self): 
         self.createWindow()
         self.mainloop()
 
 
# Just Testing Creating a New Basic Window  
class toDoWindow(tk.Toplevel): 
    def __init__(self, parent):
        super().__init__(parent)
        self.parentWindow = parent
        self.HEIGHT, self.WIDTH = 553, 253
        
        self.closeButton = None
        self.setupWindow()
    
    def setupWindow(self): 
        self.geometry(f'{self.WIDTH}x{self.HEIGHT}')
        self.title("To Do List")
        self.bind("<Destroy>", self.closeWindow)
        self.closeButton = tk.Button(self, text="Close", command=self.destroy, anchor='center')
        self.closeButton.pack(expand=True)
 
 
    def closeWindow(self, e): 
        if(not logoutUser()): 
            print("There was an error!")
        self.parentWindow.deiconify()
       
    
    
   
        
        
        
        
        
    
         
if __name__=='__main__':
    app = mainWindow() 
    app.run()