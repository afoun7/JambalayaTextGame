# Avanti Prasanna and Amanda Foun
# CS111:Final Project - Jumbled Text Game
# December 9, 2014 

from Tkinter import * 
import random 

class Beginning(Tk):
    '''Displays opening window and gives user the option to begin a new game 
    or exit the program'''

    def __init__(self):
        '''Initializes all instance variables'''
        
        Tk.__init__(self)
        self.m_app = None
        self.title('Jambalya Text Startup Window') # sets Title name 
        self.grid()
        self.createWidgets() # makes the buttons and labels on the Beginning/Startup window.
    
    def createWidgets(self):
        '''Creates title, places image on the GUI and creates newGame and Quit Button'''
        
        titleLabel = Label(self,text='Welcome to Jambalaya Text',fg='orange',bg = 'black', font='Verdana 30 bold') # sets Title 
        titleLabel.grid(row=1,columnspan=3, sticky=N+E+W+S) # places Title on grid
        
        pic = PhotoImage(file='Alphabet_soup.gif') # calls photo from folder
        BimageLabel = Label(self, image=pic,borderwidth=0)
        BimageLabel.pic = pic
        BimageLabel.grid(row=2,column=0, sticky = W) # places on grid
        
        newGameButton = Button(self, fg='red', bg='yellow', text='Start New Game', command=self.onStartButtonClick) # creates Start New Game button 
        newGameButton.grid(row=3, sticky=N+E+W+S)
        
        QuitButton = Button(self, fg='brown', bg='green', text='Exit Game', command=self.onQuitButtonClick) # creates exit button
        QuitButton.grid(row=5, sticky=N+E+W+S)
    
        
    def onStartButtonClick(self):
        '''Starts the Jambalaya Text Game by making the new window'''
        
        if self.m_app!=None: self.m_app.destroy()  # Destroy existing window
        self.m_app = JambalayaTextGame(self) # self here refers to Beginning
        self.m_app.mainloop()

    def onQuitButtonClick(self):
        '''Exits game'''
        
        self.destroy()

class makeDictionary:
    ''' Takes a textfile and creates a dictionary of words with the key as the
    jumbled word and the value pair as all words that can be made from the
    jumbled word.'''
  
    def __init__(self, filename):
        '''initializes any instance variables'''
        self.filename = filename
        
    def makeUnjumbleKey(self, string):
        '''makes the unjumbled keys'''
        return "".join(sorted(string.lower())) 
    
    def getLinesFromFile(self):
        '''Returns a list of strings where each string is a line from the
        specified file. The trailing newline character is not included
        as part of a string in the list.'''
        lines = open(self.filename).readlines() # opens and reads in the file
        for i in range(0, len(lines)): # for each line in the file
            line = lines[i] # line is equal to each word in the file
            lines[i] = line[0:(len(line)-1)] # removes trailing newline character 
        return lines # returns a list of strings where each string is a line

    def jumbledDictionary(self):
        '''Returns a dictionary mapping the unjumble key of each word in the
       given wordlist file to the word.'''
        unjDict = {}
        words = self.getLinesFromFile() # invokes getLinesFromFile; returns a list
        for word in words: # for each word in the list 
            key = self.makeUnjumbleKey(word) # find canonical unjumble key for word
            if key not in unjDict:
                # if key not in dict, associate it with a new list with word
                unjDict[key] = [word]
            else: # otherwise, add word to existing list associated with dictionary
                unjDict[key].append(word)
        return unjDict # returns a dictionary of keys as the jumbled word and value-pairs as all possible words made from that jumbled key.

class JambalayaTextGame(Toplevel):
    ''' Creates the gameboard and displays a random chosen word from Dictionary 
    Class. User can input their guess in the textbox. Program checks if the word 
    is a valid entry and if not, returns invalid. If it is a valid word, the 
    word is added to a list of correct words. If all words are guessed, the game 
    is over and the user has the option to play again or exit the program. '''
    
    def __init__(self, beginningObject):
        '''Initializes any instance variables'''
        
        Toplevel.__init__(self)
        self.beginningObject = beginningObject # instance variable
        self.title('Jambalya Text') # sets Title for window
        self.grid()
        self.oldText = '' # will append to empty string when showing correctly guessed words
        self.Dictionary = makeDictionary('tinyWordList.txt').jumbledDictionary()  # makes Dictionary of jumbled words and answers
        self.createWidgets() # creates buttons and lables for the game window 
        self.updateTimer() # starts timer

    def createWidgets(self):
        '''Makes the general gameboard:Creates the titles and labels for the 
        program; Creates Exit, Play Again, Guess buttons; Creates the textbox'''
        
        # Title and Image
        titleLabel = Label(self,text='Jambalaya Text',fg='midnight blue',font='Verdana 30 bold')
        titleLabel.grid(row=1,columnspan=3, sticky=N+E+W+S)
        
        pic = PhotoImage(file='JumbledWords.gif') # calls the file from the folder
        imageLabel = Label(self, image=pic,borderwidth=0)
        imageLabel.pic = pic
        imageLabel.grid(row=3,column=1, sticky = W) # places image on the grid
    
        # Directions 
        directionsLabel = Label(self, text = 'Directions: Guess all possible words\nusing all the provided letters \nin 60 seconds.Good luck!', font = 'Verdana 14')
        directionsLabel.grid(row = 3, column = 2, sticky = E)
        
        # The jumbled word
        textLabel3 = Label(self, text='Jumbled Word:')
        textLabel3.grid(row= 4,column=1,sticky=N+E+W+S)
        self.string = StringVar()
        stringLabel = Label(self, fg='blue', font='Verdana 20', textvariable = self.string) # self.string is set in randomWord()
        stringLabel.grid(row=4,column=2,sticky=N+E+W+S)
        self.randomWord() # calls for the randomly selected jumbled word from the jumbled Dictionary
                
        # Displaying Remaining words for the user to guess 
        self.string2 = StringVar()
        self.textLabel2 = Label(self, textvariable= self.string2) # self.string2 is set in compare()
        self.string2.set(str(self.lengthOfValues) +' words remaining')
        self.textLabel2.grid(row=5,column = 1, sticky=N+E+W+S)

        # Input guess       
        textLabel = Label(self, text='Word guess:')
        textLabel.grid(row= 6,column=1,sticky=N+E+W+S)
        self.textEntry = Entry(self) # creates the entry field the user will type into
        self.textEntry.grid(row=6,column=2,sticky=N+E+W+S)
        
        # Timer
        
        self.timer = 60  # 60 seconds to start with
        self.timerLabel = Label(self,text= str(self.timer), fg = 'dark violet', font='Verdana 14 bold') # creates Timer
        self.timerLabel.grid(row = 8, column = 1, sticky = N+E+W+S)
        
        textLabelTimer = Label(self, text='Seconds Left: ', fg = 'dark violet', font='Verdana 14 bold')
        textLabelTimer.grid(row= 7,column=1,sticky=N+E+W+S)
        
        # Guess Button
        self.SubmitButton = Button(self, fg='red', bg='yellow', text='Guess', command=self.Compare)
        self.SubmitButton.grid(row=7, column = 2, sticky=N+E+W+S)
            
        # Displays Correctly Users' guessed words 
        textLabel2 = Label(self, text='Past words that you have correctly guessed:')
        textLabel2.grid(row=11,column=1, sticky=N+E+W+S)

        self.AddingText = StringVar()
        guessWords = Label(self, textvariable = self.AddingText) # adds to the string of correctly guessed words
        guessWords.grid(row=11,column=2)
        
        # Exits the user from the game
        QuitButton2 = Button(self, fg='brown', bg='green', text='Exit Game', command=self.onQuitButtonClick2)
        QuitButton2.grid(row=14, column = 2, sticky=E) 
    
        # Message/Label displayed when the user guesses an Invalid Word
        self.wrongLabel = Label(self,text='', fg = 'red',font='Verdana 20 bold' ) # text = '' so that we can set it to Invalid Guess when the player is wrong or Congratulations when the user has won
        self.wrongLabel.grid(row=13,column=1)
        
    def randomWord(self):
        '''Chooses a randomly jumbled word from the jumbled dictionary'''
        self.listOfKeys = self.Dictionary.keys() # list of Keys
        num = random.randint(0, len( self.listOfKeys)-1) # select a random key
        self.key =  self.listOfKeys[num] # randomly selected key
        self.listOfValues = self.Dictionary[self.key] # list of values; the answers/words associated to the randomly selected jumbled word
        self.lengthOfValues = len(self.listOfValues) # used to display total words user must guess; later will be decreased as user correctly guesses words
        self.string.set(self.key) # sets the random word
    
    def updateTimer(self):
        if self.timer>0:  # Stop when timer reaches 0
            self.timer -= 1  # Decrement timer by 1 second
            self.timerLabel.configure(text=str(self.timer))
            self.after(1000, self.updateTimer)  # 1000 milliseconds is 1 sec. 
        else:
            self.wrongLabel.config(text = 'You have run out of time!')
            self.SubmitButton.config(state = 'disabled')
            YesButton = Button(self, fg='brown', bg='green', text='Play Again!', command=self.onYesButtonClick) # PROBLEM: Does not show newly generated word or guesses remaining
            YesButton.grid(row=14, column = 1, sticky=E) # row entry will need to be a variable to reflect the expanding textbook
          
            
    def Compare(self):
        '''Compares what the user inputs to the jumbledDictionary created. If 
        the word is a value for the key in the dictionary, the word is added to
        the list of correctly guessed words and the guessed word is popped out 
        of the dictionary. Otherwise, the program returns "Invalid Word"'''
        
        self.wrongLabel.config(text='') # sets text to an empty string; will be filled later depending on user's actions
        self.guessEntry = self.textEntry.get()
        self.guessEntry = self.guessEntry.rstrip().lstrip() # strips leading and ending white space 
        if self.guessEntry in self.listOfValues: # if guess is in list of answers 
            self.oldText = self.oldText + self.guessEntry + ' ' # concatenates correctly guessed words to previously guessed words; starts with empty cause nothing has been guessed
            self.AddingText.set(self.oldText)  # sets correctly guessed words
            self.listOfValues.remove(self.guessEntry) # removes guessed word from possible answers
            
            self.lengthOfValues = self.lengthOfValues - 1 # reduces the number of words the user has to guess
            self.numberText = str(self.lengthOfValues)  +' words remaining' # makes "the updated number of words remaining"-string
            self.string2.set(self.numberText) # isplays the updated number of words remaining 
           
           #Checks to see if the user has won the game
            if self.lengthOfValues == 0: # if there are no words to guess
                self.wrongLabel.config(text = 'Congratulations! You won!') # changes the message
                self.SubmitButton.config(state = 'disabled')   
                self.updateTimer = False # disables the timer
                YesButton = Button(self, fg='brown', bg='green', text='Play Again!', command=self.onYesButtonClick) # displays "Play Again!"- button
                YesButton.grid(row=14, column = 1, sticky=E) 
        else:
            self.wrongLabel.config(text = 'invalid word') # display invalid word for wrongly guessed word
            
    def onYesButtonClick(self):
        '''Destroys current window and starts newGame'''

        self.beginningObject.m_app = JambalayaTextGame(self.beginningObject) # creates new gameboard
        self.destroy() # destroys old game window
        self.beginningObject.m_app.mainloop() # starts the newly created gameboard
    
    def onQuitButtonClick2(self):
        '''Exits program'''
        
        self.destroy()

### Test Invocation
app = Beginning()
app.mainloop()