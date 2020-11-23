from pysqlcipher3 import dbapi2 as sqlite3

class Database:
	def __init__(self, file, key):
		self.connection = sqlite3.connect(file)
		self.cursor = self.connection.cursor()
		self.cursor.execute("PRAGMA key='{}'".format(key.decode()))
		self.cursor.execute("""
			CREATE TABLE IF NOT EXISTS password
			(
			id INTEGER PRIMARY KEY AUTOINCREMENT,
			name TEXT NOT NULL,
			password TEXT NOT NULL,
			username TEXT,
			updated TEXT,
			created TEXT
			)
			""")
		self.connection.commit()

	def create(self, values):
		try:
			self.cursor.execute("""INSERT INTO password(name, password, username, updated, created)
				VALUES (?, ?, ?, datetime('now', 'localtime'), datetime('now', 'localtime'))
			""", (values['name'], values['password'], values['username']))
			self.connection.commit()
		except Exception as e:
			return e

	def read(self):
		try:
			result = self.cursor.execute("SELECT * FROM password")
			return result.fetchall()
		except Exception as e:
			return e

	def readone(self, id):
		try:
			result = self.cursor.execute("SELECT * FROM password WHERE id=?", (id,))
			return result.fetchone() 
		except Exception as e:
			return e

	def search(self, to_search):
		try:
			result = self.cursor.execute("SELECT * FROM password WHERE name LIKE ?", ('%'+to_search+'%',))
			return result.fetchall()
		except Exception as e:
			return e 

	def update(self, values, prev_values):
		try:
			values['name'] = values['name'] if values['name'] != '_' else prev_values['name']
			values['password'] = values['password'] if values['password'] != '_' else prev_values['password']
			values['username'] = values['username'] if values['username'] != '_' else prev_values['username']

			self.cursor.execute("""UPDATE password SET 
					name=?,
					password=?,
					username=?,
					updated=datetime('now', 'localtime')
					WHERE id=?
				""", (values['name'], values['password'], values['username'], values['id']))
			self.connection.commit()
		except Exception as e:
			return e 

	def delete(self, ids):
		string_ids = map(str, ids)
		string_ids = ", ".join(string_ids)

		try:
			self.cursor.execute('DELETE FROM password WHERE id IN (%s)' % (string_ids,))
			self.connection.commit()
		except Exception as e:
			print(e)
			return e 


