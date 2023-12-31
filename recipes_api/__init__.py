import sqlite3
import pandas as pd

class CurrentWindow:
    def _init_(self):
      self.name = 'MainWindow'
    def recipes_callback(self):
       self.name = 'RecipesWindow'


def ErrorMessage(valor):
   if valor:
      print("Try it later. Recipes are not avaliable now")
      
    
class RecipesAPI:        
   def _init_(self):
     self.APIAvailable = True
     self.message = False
   def error(self):
     self.APIAvailable=False
     if not self.APIAvailable:
        self.message = True
        ErrorMessage(self.message)

def getrecipe():
   #From the phone, the user writes something
   string = "pizza"
   return string
        

class SearchBar:
   def _init_(self):
      self.visibilitykeyboard=False
   def searchbar_callback(self):
      self.visibilitykeyboard=True
   def recipesearch(self):
      #verify there is something written
      recipename = getrecipe()
      self.recipe=True 
      self.recipefound= False
      if not recipename: #check the is not empty
         self.recipe= False
      else: 
        # Load database of recipts
       database = pd.read_csv('db/recetario.csv', header=None, encoding='unicode_escape', sep='\t')                       
            
       # search for word "pizza"
       recetas_word = database[database.apply(lambda row: recipename in row.values, axis=1)]
        # Show the recipe which contains this word"
      # print("Recipes found wth the words:")
      # print(recetas_word)
      self.recipefound= True
       #There is no recipe with this word
      if recetas_word.empty:
      #  print("There is NO result")
       self.recipefound= False
      return self.recipefound

