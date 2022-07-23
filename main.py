import os, sys
import tkinter as tk
from resources.web import createUser

FILE_PATH = os.path.dirname(os.path.abspath(__file__))

class loginWindow: 
    def __init__(self): 
        # Setup Paths 
        self.ICON = os.path.join(FILE_PATH, "assets", "icon.png")

        # Window Sizing 
        self.HEIGHT, self.WIDTH = 553, 253
        self.MIN_HEIGHT, self.MIN_WIDTH = 372, 256
        
        # Setup Window
        self.root = tk.Tk()
        self.root.title("System Login")
        self.root.resizable(False, False)

        # Buttons 
        self.userName, self.userEntry, self.passWord, self.passEntry = None, None, None, None
        self.statusMSG, self.showPassActive = None, False 
        self.userValue, self.passValue = None, None
        
        # Check Platform Since icons Config are Different
        self.__platformCheck()
     
            
    def __platformCheck(self):  
        if sys.platform.lower() == 'darwin':
            self.ICONIMG = tk.Image('photo', file=self.ICON)
            self.root.tk.call('wm', 'iconphoto', self.root._w, self.ICONIMG)
        elif sys.platform.lower() == 'win32':
            self.root.iconbitmap(self.ICON.replace('.png', '.ico'))
            self.HEIGHT, self.WIDTH = 626, 299
            self.MIN_HEIGHT, self.MIN_WIDTH = 626, 299
        else:
            pass 
            #self.root.iconbitmap(self.ICON.replace('.png', '.xbm'))
        
        self.root.resizable(False,False)
    
    
    def checkSize(self, event=None): 
        print(self.root.winfo_width(), self.root.winfo_height())
    

    def showPass(self): 
        if(not self.showPassActive):
            self.passEntry.config(show='')
            self.showPassActive = True
        else: 
            self.passEntry.config(show='*')
            self.showPassActive = False 
           
    
    def createWindow(self): 
        # Create Window
        self.root.geometry(f'{self.HEIGHT}x{self.WIDTH}')
        self.root.resizable(self.MIN_WIDTH, self.MIN_HEIGHT )

        self.statusMSG= tk.Label(self.root, text="Please Login Below", anchor='center', font=('American Typewriter', 18))
        self.statusMSG.grid(row=1, column=2, columnspan=2, sticky=tk.N)
       
       
        self.userName = tk.Label(self.root, text="Username:", pady=20, padx=20, anchor='center', font=('American Typewriter', 18))
        self.userEntry = tk.Entry(self.root, bd=2, width=30, font=('American Typewriter', 18))
        
        self.userName.grid(row=2, column=1, columnspan=2, sticky=tk.W)
        self.userEntry.grid(row=2, column=2, sticky=tk.W)
        
        
        self.passWord = tk.Label( self.root, text="Password:", pady=20, padx=20, anchor='center', font=('American Typewriter', 18))
        self.passEntry = tk.Entry(self.root, bd=2, width=30, font=('American Typewriter', 18), show='*')
        
        self.passWord.grid(row=3, column=1, sticky=tk.W)
        self.passEntry.grid(row=3, column=2, sticky=tk.W)
        tk.Checkbutton(self.root, text="Show Password", font=('American Typewriter', 18),  command=self.showPass).grid(row=4, column=2, sticky=tk.W)
       
        
        tk.Button(self.root, text="Login", pady=20, padx=20, height=1, width=8, command=self.attemptLogin, anchor='center').grid(row=5, column=2, columnspan=2)
  
    
        
    def attemptLogin(self):
       self.userValue = self.userEntry.get()
       self.passValue = self.passEntry.get()
   
       if (self.userValue and self.passValue):   
        self.userEntry.delete(0, tk.END)
        self.passEntry.delete(0, tk.END)
        res, text = createUser(self.userValue, self.passValue)
        if(res): 
            # For Now We Are Connecting the Login Screen to the Signup Endpoint, 
            # until i modify the server to allow for login from this companion app
            print("User Created")
        else: 
            print(f"Error: {text}")
            self.statusMSG.config(text=f"Error: {text}", bg='red', fg='white', font=('American Typewriter', 18, 'bold'))
       else: 
           self.statusMSG.config(text="Do not leave blank fields", bg='red', fg='white', font=('American Typewriter', 18, 'bold')) 
       
           
    def run(self): 
         self.createWindow()
         self.root.mainloop()
   
   
         
if __name__=='__main__':
    app = loginWindow() 
    app.run()