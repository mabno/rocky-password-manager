import os
import shutil
import time
from termcolor import cprint, colored

class UI:
	row_size = 25
	clear = lambda _: os.system('clear')
	def view(self, title):
		self.clear()
		header_string = "Rocky Password Manager 1.0.0"
		cprint(' '*shutil.get_terminal_size().columns, 'white', 'on_blue')
		cprint(header_string.center(shutil.get_terminal_size().columns), 'white', 'on_blue')
		cprint(' '*shutil.get_terminal_size().columns, 'white', 'on_blue')
		title_string = colored(title, 'cyan', attrs=['dark', 'underline'])
		print(f'\n   {title_string}\n')

	def printOptions(self, options):
		for key in options:
			print("{} {}".format(colored('['+key+']', 'cyan'), options[key]))

	def messageAndSleep(self, message, color):
		cprint(message, color)
		time.sleep(1)

	def printTable(self, rows):
		def prettyRow(row, size):
			return row + ' '*(size-len(row))
		for row in rows:
			id = prettyRow(str(row[0]), 3)
			name = prettyRow(str(row[1]), self.row_size)
			password = prettyRow(str(row[2]), self.row_size)
			print('{} {} {}'.format(id, colored(name, 'yellow'), password))

	def detailsTable(self, values):
		print('{}: {}'.format(colored('ID', 'yellow'), values[0]))
		print('{}: {}'.format(colored('Name', 'yellow'), values[1]))
		print('{}: {}'.format(colored('Password', 'yellow'), values[2]))
		print('{}: {}'.format(colored('Username', 'yellow'), values[3]))
		print('{}: {}'.format(colored('Last update', 'yellow'), values[4]))
		print('{}: {}'.format(colored('Created at', 'yellow'), values[5]))

	def banner(self):
		self.clear()
		print("""                                  
                                  
                                  
            ██      ██            
          ██████  ██████          
          ██████  ██████          
          ██████  ██████          
      ██    ██      ██    ██      {}
    ██████              ██████    Developed by Mabno
    ██████    ██████    ██████    mariano1baldovino@gmail.com
    ████    ██████████    ████    
          ██████████████          {}
        ██████████████████        
      ██████████████████████      
      ██████████████████████      
        ██████████████████        
          ██████  ██████          
                                  
                                  """.format(colored('Rocky Password Manager 1.0.0', 'cyan'), colored('Press enter to continue', attrs=['blink'])))
		
