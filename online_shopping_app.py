
#-----Statement of Authorship----------------------------------------#
#
#  This is an individual assessment item.  By submitting this
#  code I agree that it represents my own work.  I am aware of
#  the University rule that a student must not act in a manner
#  which constitutes academic dishonesty as stated and explained
#  in QUT's Manual of Policies and Procedures, Section C/5.3
#  "Academic Integrity" and Section E/2.1 "Student Code of Conduct".
#
#    Student no: 10269142
#    Student name: Anna Nguyen
#
#  NB: Files submitted without a completed copy of this statement
#  will not be marked.  Submitted files will be subjected to
#  software plagiarism analysis using the MoSS system
#  (http://theory.stanford.edu/~aiken/moss/).
#
#--------------------------------------------------------------------#



#-----Assignment Description-----------------------------------------#
#
#  Online Shopping Application
#
#  In this assignment you will combine your knowledge of HTMl/XML
#  mark-up languages with your skills in Python scripting, pattern
#  matching, and Graphical User Interface design to produce a useful
#  application for simulating an online shopping experience.  See
#  the instruction sheet accompanying this file for full details.
#
#--------------------------------------------------------------------#



#-----Imported Functions---------------------------------------------#
#
# Below are various import statements for helpful functions.  You
# should be able to complete this assignment using these
# functions only.  Note that not all of these functions are
# needed to successfully complete this assignment.
#

# The function for opening a web document given its URL.
# (You WILL need to use this function in your solution,
# either directly or via our "download" function.)
from urllib.request import urlopen

# Import the standard Tkinter functions. (You WILL need to use
# these functions in your solution.)
from tkinter import *

# Functions for finding all occurrences of a pattern
# defined via a regular expression, as well as
# the "multiline" and "dotall" flags.  (You do NOT need to
# use these functions in your solution, because the problem
# can be solved with the string "find" function, but it will
# be difficult to produce a concise and robust solution
# without using regular expressions.)
from re import findall, finditer, MULTILINE, DOTALL

# Import the standard SQLite functions (just in case they're
# needed).
from sqlite3 import *

#
#--------------------------------------------------------------------#



#-----Downloader Function--------------------------------------------#
#
# This is our function for downloading a web page's content and both
# saving it on a local file and returning its source code
# as a Unicode string. The function tries to produce
# a meaningful error message if the attempt fails.  WARNING: This
# function will silently overwrite the target file if it
# already exists!  NB: You should change the filename extension to
# "xhtml" when downloading an XML document.  (You do NOT need to use
# this function in your solution if you choose to call "urlopen"
# directly, but it is provided for your convenience.)
#
def download(url = 'http://www.wikipedia.org/',
             target_filename = 'download',
             filename_extension = 'html'):

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    # Open the web document for reading
    try:
        web_page = urlopen(url)
    except ValueError:
        raise Exception("Download error - Cannot find document at URL '" + url + "'")
    except HTTPError:
        raise Exception("Download error - Access denied to document at URL '" + url + "'")
    except:
        raise Exception("Download error - Something went wrong when trying to download " + \
                        "the document at URL '" + url + "'")

    # Read its contents as a Unicode string
    try:
        web_page_contents = web_page.read().decode('UTF-8')
    except UnicodeDecodeError:
        raise Exception("Download error - Unable to decode document at URL '" + \
                        url + "' as Unicode text")

    # Write the contents to a local text file as Unicode
    # characters (overwriting the file if it
    # already exists!)
    try:
        text_file = open(target_filename + '.' + filename_extension,
                         'w', encoding = 'UTF-8')
        text_file.write(web_page_contents)
        text_file.close()
    except:
        raise Exception("Download error - Unable to write to file '" + \
                        target_file + "'")

    # Return the downloaded document to the caller
    return web_page_contents

#-----Student's Solution---------------------------------------------#
##Global lists for developing products list and invoice list items
global PurchasedItemsList, Listing, TotalShopPrice
PurchasedItemsList = [] #List containing user purchases
Listing = []
TotalShopPrice = 0 #Used to calculate total price for invoice

#Original URL links to products
AccessoryURL = "https://otakuarmyshop.com/caps-jewelry-accessories/?orderby=newest"
ShirtsURL = "https://otakuarmyshop.com/special-creation-t-shirts/"
PosterURL = "http://otakushop.us/?orderby=date&product_cat=poster"
BagURL = "http://otakushop.us/?orderby=date&product_cat=backpack"

 ##Subroutine to extract elements from RegEx and adding to lists
def Stock(ProductName, ProductPrice, ProductImageSource, ListboxProducts,
          StoreProductInfo, ItemName, ItemPrice, ItemImage):
    ##Function to extract first 10 instances from RegEx results into lists
    def extract(StockInfo, RegEx):
        for items in range(10):
            StockInfo.append(RegEx[items])
   ##Function to combine extracted lists together
    def products(ListboxProducts, StoreProductInfo, ProductName,
                 ProductPrice, ProductImageSource):
        for items in range(10):
            #Write out product names and prices into list for listbox
            ListboxProducts.append(ProductName[items] + ' ($' + ProductPrice[items] + ')')
            #Combine elements together into list containing all product information 
            StoreProductInfo.append("['" + ProductName[items] + " $" + ProductPrice[items] +
                                  ', ' + ProductImageSource[items] + "]")
    extract(ProductName, ItemName)
    extract(ProductPrice, ItemPrice)
    extract(ProductImageSource, ItemImage)
    products(ListboxProducts, StoreProductInfo, ProductName,
            ProductPrice, ProductImageSource)
   
def ShopItems(ShopCategory):
    def AddItemsToCart():
        if ProductsList.curselection() !=():
             #Change state of textbox for writing to insert purchased item into textbox
             ShoppingCart["state"] = NORMAL
             ShoppingCart.insert(END, ProductsList.get(ProductsList.curselection()) + '\n')
             ShoppingCart["state"] = DISABLED #User proofing the textbox
             #Return the position of the currently selected item in listbox
             position = ProductsList.index(ProductsList.curselection())
             #Write customer purchases into PurchasedItemsList for invoice development
             PurchasedItemsList.append(StoreProductInfo[position])
             #enable 'Print Invoice' button; originally user proofed to prevent producing an empty invoice
             PrintInvoice["state"] = NORMAL
    #Create a new window containing list of items
    LocalShop = Toplevel(Main_App)
    LocalShop.geometry("585x255")
    LocalShop.configure(background = "SteelBlue")
    #Create local lists to store elements from file
    ProductName = []
    ProductPrice = []
    ProductImageSource = []
    ListboxProducts = []
    StoreProductInfo = []
    ##Determine file opening method, RegEx and additional information
        #to use depending on given ShopCategory
    if ShopCategory == "Accessories" or ShopCategory == "Shirts":
        if ShopCategory == "Accessories":
            FileDirectory = "Local files/Otaku Army Shop Accessories.html"
            URL = AccessoryURL
            Heading = "Otaku Army Shop's Accessories! (USD)"
        else: 
            FileDirectory = "Local files/Otaku Army Shop T-shirts.html"
            URL = ShirtsURL
            Heading = "Otaku Army Shop's T-shirts! (USD)"
        Shop = open(FileDirectory).read()
        #Since local files from same site, extract elements using the same RegEx 
        ItemName = findall('"title">([A-Za-z- ]+)</', Shop)
        ItemPrice = findall('data-saleprice="([0-9\.]+)">', Shop)
        ItemImage = findall('img src="(https://[/.A-Za-z0-9-/]+.[0-9a-x]+[\.jpgen]+)', Shop)
    else:
        if ShopCategory == "Posters":
            Heading = "Otaku Shop's Poster Sets! (USD)"
            URL = PosterURL
        else:
            Heading = "Otaku Shop's Backpacks! (USD)"
            URL = BagURL
        #Open webpage for reading
        Shop = urlopen(URL).read().decode("UTF-8")
        #Since live webpages from same site, extract elements using the same RegEx
        ItemName = findall("[】>]([A-Za-z0-9-!\(\) ]+)</h3>", Shop)
        ItemPrice = findall("&#36;([0-9\.]+)</span></ins>", Shop)
        ItemImage =  findall('src="(http://[\./0-9A-Za-z-]+\.jpg)" class="', Shop)
    #Execute subroutine to extract stock from RegEx and store into product lists
    Stock(ProductName, ProductPrice, ProductImageSource, ListboxProducts,
          StoreProductInfo, ItemName, ItemPrice, ItemImage)
    #Create widgets for store window
    Label(LocalShop, text = Heading, font = ("Verdana", 16), background = "SteelBlue",
         fg = "white").grid(row = 0, column = 5, padx = 5)
    ProductsList = Listbox(LocalShop, width = 70, height = 10, font = ("Verdana", 10))
    ProductsList.grid(row = 3, column = 5, padx = 10)
   #Populate listbox with products 
    for items in ListboxProducts:
      ProductsList.insert(END, items)
    Add_Items = Button(LocalShop, text = "Add to cart",
                      command = AddItemsToCart)
    Add_Items.grid(row = 4, column = 5)
    Label(LocalShop, text = URL, font = ("Verdana", 10), background = "SteelBlue",
                                            fg = "white").grid(row = 5, column = 5, padx = 5)

def print_invoice(invoice_file = 'invoice.html'):
    #Open invoice file for writing 
    customer_invoice_file = open(invoice_file, 'w', encoding = 'UTF-8')
    #Initialising variable to calculate Total price
    ShopPrices = 0
    ##Manipulating contents of PurchasedItemsList
    for products in PurchasedItemsList:
        #General RegEx to extract items from PurchasedItemsList
        RetrievedProducts = findall("'([A-Za-z-!\(\) ]+)", products)
        RetrievedPrices = findall('\$([0-9\.]+)', products) 
        RetrievedImage = findall("(https?://[\./0-9A-Za-z-_]+[\.jpgen])", products)
        #Rewrite contents into Listing
        Listing.append(RetrievedProducts + RetrievedPrices + RetrievedImage)
    ##Calculating Total Price
    for prices in PurchasedItemsList:
        OrderPrices = float(findall('\$([0-9\.]+)', prices)[0]) #prices expressed as a string
        ShopPrices = ShopPrices + OrderPrices
    #Converting prices in USD -> AUD
    TotalShopPrice = '$' + str(round((ShopPrices * 1.33), 2))
    
    #Write standard HTML headers into invoice file
    customer_invoice_file.write('''<!DOCTYPE html>
    <html>
        <head>
            <title>Your Purchases with AniMerch!</title>
        </head>
        <style>
            h1, h2, h3 {text-align: center; font-family: Verdana, Sans-serif;}
            p {font-family: Verdana, Sans-serif;}
            tr:nth-child(even) {background-color: #5c91bc;}
            tr:nth-child(odd) {background-color: #ffa64d; color: white;}
            body {background-color: #33658a;}
            td {border: 2px solid black; font-family: Verdana, Sans-serif;}
            ul {margin-left: 425px;}
            li a {color: white; font-family: Verdana, Sans-serif; font-size: 15px;}
        </style>                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                   
        <body>
            <h1>Thank you for shopping with </h1>
            <!-- Image source of logo and website used to create logo -->
            <p align='center'>'''
                '<a target="_top" href="https://www.flamingtext.com/" ><img src="https://blog.flamingtext.com/blog/2018/05/26/' + \
                        'flamingtext_com_1527333525_203077455.png" border="0" alt="Logo Design by FlamingText.com" ' + \
                        'title="Logo Design by FlamingText.com"></a><br/>Logo Design by ' + \
                        '<a href="https://www.flamingtext.com/" >FlamingText.com</a>'
            '''<!--Total Price in AUD -->
            <h2>Total price: <b>''' + TotalShopPrice + '''(AUD)</b></h2>
            <h3>You purchased the following items: </h3>
            
            <!-- Table of items bough by user -->
            <table align='center'>''')
    #Write contents in Listing into html table
    for contents in Listing:
        customer_invoice_file.write('''
    <tr>
        <!-- Image source of product -->
        <td><img src="''' + contents[2] + '''" width = 240 border="3"></td>
        <!-- Product name and price in USD -->
        <td>''' + contents[0] + '($''' + contents[1] + ''' USD)</td>
    </tr>
    ''')
    #Closing tags to complete html document with links to original sources
    customer_invoice_file.write('''</table>
    <p align='center'><b>Our products were retrieved from the following sources:</b></p>
    <ul>
        <li><a href="''' + AccessoryURL + '''"/>Otaku Army Shop - Caps, Jewlery and Accessories</a></li>
        <li><a href="''' + ShirtsURL + '''"/>Otaku Army Shop - Special Creation T-shirts</a></li>
        <li><a href="''' + PosterURL + '''"/>Otaku Shop - Posters</a></li>
        <li><a href="''' + BagURL + '''"/>Otaku Shop - Backpacks</a></li>
    </ul>
    </body>
    </html>''')
    #Close HTML file which can be viewed in browser
    customer_invoice_file.close()

    ##Part B - Saving recently purchased items into database
    #Connect to ShoppingCart database
    Connection = connect('shopping_cart.db')
    #Retrieve view of database's contents
    RecentPurchases = Connection.cursor()
    #Clear contents already in database
    RecentPurchases.execute("""DELETE FROM ShoppingCart""")
    #Insert product name and prices into database
    for items in Listing:
        RecentPurchases.execute("""INSERT INTO ShoppingCart
            VALUES ('""" + items[0] + "', '" + items[1] +"')")
    #Commit changes
    Connection.commit()
    #Release the connection
    RecentPurchases.close()
    Connection.close()
    #Clear contents in Listing for when 'Print Invoice' button is
    #pressed again in the same session
    Listing.clear()
    
##Main Window
Main_App = Tk()
Main_App.geometry("445x440")
Main_App.title('AniMerch - Online Shopping App for Anime merchandise')
Main_App.configure(background = "SteelBlue")
##Create widgets for main window
#Shop Logo
Shop_Logo_Image = PhotoImage(file = 'AniMerch Shop Logo.gif')
ShopLogo = Label(Main_App, image = Shop_Logo_Image,
                 background = "SteelBlue")
ShopLogo.place(x = 40,  y = 0)
##Widgets for local files - Otaku Army Shop's Accessories and T-Shirts
Label(Main_App, text = "Current Stock: ", font = ("Verdana", 12),
      background = "SteelBlue", fg = "white").place(x = 40, y = 110)
Accessories = Button(Main_App, text = "Clothing Accessories", font = ("Verdana", 10),
                     command = lambda: ShopItems("Accessories"))
Accessories.place(x = 30, y = 140)
Shirts = Button(Main_App, text = "T-shirts", font = ("Verdana", 10),
                command = lambda: ShopItems("Shirts"), width = 8)
Shirts.place(x = 70, y = 175)
#Widgets for live source - Anime NPC's Nendoroid and machine toy
Label(Main_App, text = "New Stock!", font = ("Verdana", 12),
      background = "SteelBlue", fg = "white").place(x = 260, y = 110)
Posters = Button(Main_App, text = "Poster Sets", font = ("Verdana", 10),
                   command = lambda: ShopItems("Posters"), width = 12)
Posters.place(x = 260, y = 140)
Backpacks = Button(Main_App, text = "Backpacks", font = ("Verdana", 10),
                   command = lambda: ShopItems("Backpack"), width = 10)
Backpacks.place(x = 268, y = 175)
#Textbox to display items purchased by user 
Label(Main_App, text = "You have purchased: ", font = ("Verdana", 10),
      background = "SteelBlue", fg = "white").place(x = 150, y = 225)
ShoppingCart = Text(Main_App, width = 60, height = 10,
                    borderwidth = 2, relief = "groove", font = ("Verdana", 8))
ShoppingCart.place(x = 10, y = 250)
#Button to print invoice - disabled until an item is added to the cart
PrintInvoice = Button(Main_App, text = "Print Invoice",
                      font = ("Verdana", 10), state = DISABLED, command = print_invoice)
PrintInvoice.place(x = 175, y = 395)
#Start event loop to react to user inputs
Main_App.mainloop()



        

                        
                  
    
