#------------------------------------------#
# Title: CDInventory.py
# Desc: Version of CD Inventory program
# designed around classes and functions.
# Change Log: (Who, When, What)
# Alex Angelico, 20200817, Created File
# Alex Angelico, 20200818, Completed functions
# for adding new CDs and deleting current CDs.
#------------------------------------------#

# -- DATA -- #
menuChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.txt'  # data storage file
objFile = None  # file object


# -- PROCESSING -- #
class DataProcessor:
    
    @staticmethod
    def add_cd(ID, title, artist, table):
        """Collects new CD data from user and converts into dict for appending to current inventory table
        
        Args:
            ID (string): numerical identification for the new CD
            title (string): album title of the new CD
            artist (string): artist name of the new CD
            table (list of dicts): 2D data structure (list of dicts) that holds the data during runtime
        
        Returns:
            None.
        """
        dicRow = {'ID': ID, 'Title': title, 'Artist': artist}
        table.append(dicRow)
        print()
        
    @staticmethod
    def delete_cd(delID, table):
        """Deletes dicts by ID key from 2D data structure
        
        Args:
            delID (list of strings): holds one or more ID values designated for deleiton
            table (list of dicts): 2D data structure (list of dicts) that holds the data during runtime
            
        Returns:
            None.
        """
        for row in delID: delID = row.strip().split(',')
        delIDln = int(len(delID))
        cdcount = int()
        while cdcount < delIDln: # this loop causes an interminable error if delID item is not in table
            for item in delID:
                rowcount = int()
                while rowcount < len(table):
                    for row in table:
                        if row['ID'] == item:
                            rowcount += 1
                            cdcount += 1
                            table.remove(row)
                            delID.remove(item)
                            break
                        else:
                            rowcount += 1
                            continue
                        
        if len(delID) == 0: print('IDs deleted.')
        elif cdcount == 0: print('IDs not found.')
        elif cdcount != len(delID) and len(delID) > 0: print('One or more IDs was not found:',delID[:])

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name, table):
        """Function to manage data ingestion from file to a list of dictionaries

        Reads the data from file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        table.clear()  # this clears existing data and allows to load data from file
        objFile = open(file_name, 'r')
        for line in objFile:
            data = line.strip().split(',')
            dicRow = {'ID': data[0], 'Title': data[1], 'Artist': data[2]}
            table.append(dicRow)
        objFile.close()

    @staticmethod
    def write_file(file_name, table):
        """Function to manage transcription of data from list of dictionaries in
        current inventory to file
        
        Args:
            file_name (string): name of file used to wrtie the data to
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
            
        Returns:
            None.
        """
        objFile = open(file_name, 'w')
        for row in table:
            lstValues = list(row.values())
            lstValues[0] = str(lstValues[0])
            objFile.write(','.join(lstValues) + '\n')
        objFile.close()

# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')
        
    @staticmethod
    def add_cd_input(table, IDchecklist):
        """Gets user input for new CD information
        
        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.
            IDchecklist (list): persistent list of new IDs being added to current inventory to prevent accidental duplicate input by user
        
        Returns:
            IDchecklist (list): persistent list of new IDs being added to current inventory to prevent accidental duplicate input by user
            ID (string): numerical identification for the new CD
            title (string): album title of the new CD
            artist (string): artist name of the new CD
        """
        ID = ' '
        rowcount = int()
        while rowcount < len(table):
            ID = input('Enter numerical ID: ').strip()
            if ID.isnumeric() is True:
                for row in table:
                    if row['ID'] == ID:
                        print('That ID already exists. Please enter a new ID.')
                        rowcount = 0
                    else:
                        rowcount += 1
                IDchecklistitemcount = int()
                while IDchecklistitemcount < len(IDchecklist):
                    for item in IDchecklist:
                        if item == int(ID): # I do not know why this instance of the ID variable has to be converted to int(), but an interminable error results if it is not
                            print('That ID already exists. Please enter a new ID.')
                            IDchecklistitemcount = 0
                        else:
                            IDchecklistitemcount += 1
            else:
                continue
        IDchecklist.append(ID)
        title = input('What is the CD\'s title? ').strip()
        artist = input('What is the Artist\'s name? ').strip()
        return IDchecklist, ID, title, artist

# 1. When program starts, read in the currently saved Inventory
FileProcessor.read_file(strFileName, lstTbl)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    menuChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if menuChoice == 'x':
        break
    # 3.2 process load inventory
    if menuChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        overwrite_verification = input('Type \'yes\' to continue and reload from file. Otherwise reload will be canceled.\n')
        if overwrite_verification.lower() == 'yes':
            print('reloading...')
            FileProcessor.read_file(strFileName, lstTbl)
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif menuChoice == 'a':
        print("Please provide new CD info.")
        cdIDlist = []
        add_verification = 'y'
        while add_verification == 'y':
            # 3.3.1 Ask user for new ID, CD Title and Artist
            cdIDlist,cdID,cdTitle,cdArtist = IO.add_cd_input(lstTbl, cdIDlist) # cdIDlist is both extracted from the add_cd_input function and applied to it as an argument because it contains a persistent list of new CD IDs being added to the current inventory to prevent duplicate use across multiple CD entries
            # 3.3.2 Add item to the table and ask user if they want to add another CD
            DataProcessor.add_cd(cdID, cdTitle, cdArtist, lstTbl)
            add_verification = input('Would you like to add another CD? [y/n] ').lower()
            if add_verification == 'n': break
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif menuChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif menuChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        cdIDdel = [input('Enter one or more IDs to delete, separated by commas (example: "1,2,3"): ').strip()]
        # 3.5.2 search through table and delete CD
        DataProcessor.delete_cd(cdIDdel, lstTbl)
        # 3.5.3 display altered Inventory to user
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif menuChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        save_verification = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if save_verification == 'y':
            # 3.6.2.1 save data
            FileProcessor.write_file(strFileName, lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be safe:
    else:
        print('General Error')




