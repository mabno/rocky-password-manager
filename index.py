from database import Database
from ui import UI, cprint, colored
from utils import readFile, writeFile
from cryptography.fernet import Fernet

class App:
	def __init__(self):
		self.ui = UI()

		with open('.user', 'r') as reader:
			self.user_info = reader.read()

		key = self.readOrCreateKey()
		self.fernet = Fernet(key)
		self.db = Database('database.db', key)
		self.init()
		self.login()

	def readOrCreateKey(self):
		key_path = readFile('.keypath')
		if key_path == '':
			cprint('Give a path to key!', 'red')
		else:
			try:
				key = readFile(key_path, True)
				return key
			except:
				key = Fernet.generate_key()
				writeFile(key_path, key, True)
				return key

	def init(self):
		self.ui.banner()
		input()

	def register(self):
		self.ui.view('REGISTER')
		print("Create a password for protect your passwords(don't forget it)")
		print('Input a password:')
		password = input()
		password_encrypted = self.fernet.encrypt(password.encode())
		writeFile('.user', password_encrypted.decode())
		self.ui.messageAndSleep('Password created', 'green')
		self.mainMenu()

	def login(self, attempts=0):
		if self.user_info == '':
			self.register()
			return
		self.ui.view('LOGIN')
		print('Input your password:')
		password = input()
		decrypted_password = self.fernet.decrypt(self.user_info.encode())
		if password == decrypted_password.decode():
			self.ui.messageAndSleep('You are authenticated', 'green')
			self.mainMenu()
		else:
			if attempts < 2 :
				self.ui.messageAndSleep('Incorrect password, retry again', 'red')
				self.login(attempts+1)
			else:
				cprint('3 incorrect attempts, bye', 'red')

	def viewDetailsChoise(self, back):
		print('Input {} for view details or press enter to back'.format(colored('<id>', 'yellow')))
		user_input = input()
		if user_input == '':
			self.mainMenu()
			return

		if not user_input.isnumeric():
			self.ui.messageAndSleep('Set a numeric ID', 'red')
			back()
			return

		result = self.db.readone(user_input)

		if result == None:
			self.ui.messageAndSleep('Set a valid ID', 'red')
			back()
			return

		if isinstance(result, Exception):
			cprint('Database error: '+str(result), 'red')
			return

		self.details(result, back)

	def details(self, values, back):
		self.ui.view('{}({}) DETAILS'.format(values[1], values[0]))
		self.ui.detailsTable(values)
		print('\nPress enter to back')
		input()
		back()

	def getPasswords(self):
		result = self.db.read()

		if isinstance(result, Exception):
			cprint('Database error: '+str(result), 'red')
			return

		if len(result) > 0:
			self.ui.printTable(result)
			cprint('{} passwords registered'.format(len(result)), 'green')
		else:
			cprint('Database empty', 'red')



	def getList(self):
		self.ui.view('LIST')
		self.getPasswords()
		self.viewDetailsChoise(self.getList)
		

	def search(self):
		self.ui.view('SEARCH')
		print('Input {} to search in the records (by name field) or press enter to back'.format(colored('<text>', 'yellow')))
		to_search = input()

		if to_search == '':
			self.mainMenu()
			return

		result = self.db.search(to_search)

		if isinstance(result, Exception):
			cprint('Database error: '+str(result), 'red')
			return

		self.ui.printTable(result)
		cprint('{} matches'.format(len(result)), 'green')
		self.viewDetailsChoise(self.search)




	def create(self):
		self.ui.view('CREATE')
		print('Input {} or press enter to back'.format(colored('<name> <password> <username>', 'yellow')))
		parameters = input()
		if parameters == '':
			self.mainMenu()
			return

		parameters_list = parameters.split(' ')
		if(len(parameters_list) < 3):
			self.ui.messageAndSleep('Set 3 parameters', 'red')
			self.create()
			return

		values = {
			'name': parameters_list[0],
			'password': parameters_list[1],
			'username': parameters_list[2]
		}

		result = self.db.create(values)
		if isinstance(result, Exception):
			cprint('Database error: '+str(result), 'red')
			return

		self.ui.messageAndSleep('Password created successfully', 'green')
		self.mainMenu()


	def update(self):
		self.ui.view('UPDATE')
		self.getPasswords()
		print('Input {} or press enter to back'.format(colored('<id to update> <new name> <new password> <new username>', 'yellow')))
		print("Use '_' to not update parameter")
		parameters = input()
		if parameters == '':
			self.mainMenu()
			return

		parameters_list = parameters.split(' ')
		if len(parameters_list) < 4:
			self.ui.messageAndSleep('Set 4 parameters', 'red')
			self.update()
			return


		values = {
			'id': parameters_list[0],
			'name': parameters_list[1],
			'password': parameters_list[2],
			'username': parameters_list[3]
		}

		first_result = self.db.readone(values['id'])

		if first_result == None:
			self.ui.messageAndSleep('Set a valid ID')
			self.update()
			return

		if isinstance(first_result, Exception):
			cprint('Database error: '+str(first_result), 'red')
			return


		prev_values = {
			'name': first_result[1],
			'password': first_result[2],
			'username': first_result[3]
		}

		result = self.db.update(values, prev_values)
		if isinstance(result, Exception):
			cprint('Database error: '+str(result), 'red')
			return

		self.ui.messageAndSleep('Password updated successfully', 'green')
		self.mainMenu()

	def delete(self):
		self.ui.view('DELETE')
		self.getPasswords()
		print('Input {} (one or more ids) or press enter to back'.format(colored('<id to delete> <id...>', 'yellow')))
		user_input = input()
		if user_input == '':
			self.mainMenu()
			return

		ids = user_input.split(' ')

		for id in ids:
			if not id.isnumeric():
				self.ui.messageAndSleep('Set a numeric ID', 'red')
				self.delete()
				return
				break
				
		result = self.db.delete(ids)
		if isinstance(result, Exception):
			cprint('Database error: '+str(result), 'red')
			return

		self.ui.messageAndSleep('Passwords deleted successfully', 'green')
		self.mainMenu()

	def exit(self):
		cprint('Bye, come back soon!', 'cyan')


	def mainMenu(self):
		self.ui.view('MENU')
		print('Select an option \n')
		options = {'0': 'List', '1': 'Search', '2': 'Create', '3': 'Update', '4': 'Delete', '5': 'Exit'}
		self.ui.printOptions(options)
		selection = {
			'0': self.getList,
			'1': self.search,
			'2': self.create,
			'3': self.update,
			'4': self.delete,
			'5': self.exit}
		choise = input()
		selected = selection.get(choise, False)
		if not selected:
			self.ui.messageAndSleep('Select a valid option', 'red')
			self.mainMenu()
		else:
			selected()


if __name__ == '__main__':
	app = App()


