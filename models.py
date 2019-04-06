import sqlite3
from datetime import datetime

class Model_Comment():
	def __init__(self):
		self.conn = sqlite3.connect('sql.db')
		self.cursor = self.conn.cursor()
		try:
			self.cursor.execute('''CREATE TABLE comments (name varchar, body varchar,id INTEGER PRIMARY KEY,article_id INTEGER,FOREIGN KEY(article_id) REFERENCES articles(id) )''')
			self.conn.commit()
		except:
			pass
	def get_all_comments(self,id):
		self.cursor.execute('SELECT * FROM comments WHERE article_id=? ORDER BY id DESC;',id)
		return self.cursor.fetchall()
	def add_comment(self,name,body,id):
		self.cursor.execute('INSERT INTO comments (name,body,article_id) VALUES (?,?,?)' ,(name,body,id))
		self.conn.commit()

class Model_User():
	def __init__(self):
		self.conn = sqlite3.connect('sql.db')
		self.cursor = self.conn.cursor()
		try:
			self.cursor.execute('''CREATE TABLE users (username varchar, password varchar, email varchar, name varchar, surename varchar)''')
			self.conn.commit()
		except:
			pass
	def get_all_users(self):
		self.cursor.execute('SELECT * FROM users')
		return self.cursor.fetchall()
	def info(self,username):
		self.cursor.execute('SELECT * FROM users WHERE username=?',[username]) 
		return self.cursor.fetchone()
	def isset_user(self,username,password):
		self.cursor.execute('SELECT * FROM users WHERE username=? AND password=?',(username,password)) 
		return self.cursor.fetchone()
	def create_user(self,username,password,email,name,surename):
		self.cursor.execute('INSERT INTO users (username,password,email,name,surename) VALUES ("%s","%s","%s","%s","%s")' % (username,password,email,name,surename))
		self.conn.commit()



class Model_Article():
	def __init__(self):
		self.conn = sqlite3.connect('sql.db')
		self.cursor = self.conn.cursor()
		try:
			self.cursor.execute('''CREATE TABLE articles (title varchar, body varchar,baz timestamp,id INTEGER PRIMARY KEY)''')
			self.conn.commit()
		except:
			pass
	def get_all_articles(self):
		self.cursor.execute('SELECT * FROM articles ORDER BY id DESC')
		return self.cursor.fetchall()
	def get_by_id(self,id):
		self.cursor.execute('SELECT * FROM articles WHERE id=?',id)
		return self.cursor.fetchone()
	def search(self,searchstr):
		self.cursor.execute("SELECT * FROM articles WHERE title LIKE ?",['%'+searchstr+'%'])
		return self.cursor.fetchall()
	def delete_by_id(self,id):
		self.cursor.execute('DELETE FROM articles WHERE id=?',id)
		self.conn.commit()
	def update_by_id(self,title,body,id):
		self.cursor.execute('UPDATE articles SET title=? , body=? WHERE id=?',(title,body,id))
		self.conn.commit()
	def add_article(self,title,body):
		now = datetime.now()
		self.cursor.execute('INSERT INTO articles (title,body,baz) VALUES (?,?,?)' , (title,body,now))
		self.conn.commit()