#Importing files and packages
import sqlite3
import datetime
import random


#Creating the class Dtabase manager for all database operations
class DB_manager():
	#Initialising an creating the basic tables
	def __init__(self):
		self.con = sqlite3.connect("quizzy.db")
		self.cur = self.con.cursor()
		try:
		 	self.cur.execute("CREATE TABLE Users(id INTEGER PRIMARY KEY AUTOINCREMENT, user_id TEXT, pwd TEXT, power TEXT);")
		 	self.cur.execute("INSERT INTO Users(user_id, pwd, power) VALUES('admin1', '12345', 'admin');")
		 	self.con.commit()
		except:
		 	pass
		try:
			self.cur.execute("CREATE TABLE Tests(id INTEGER PRIMARY KEY AUTOINCREMENT, test_name TEXT, test_description TEXT, alloted_users TEXT, time_limit TEXT, auto_evaluate INTEGER, shuffle INTEGER, total_marks REAL);")
			self.con.commit()
		except:
			pass


	def fetch_eval_view(self, user, test):
		sql_query = "SELECT * FROM [" + test + "_" + user + "]"
		result = self.cur.execute(sql_query).fetchall()
		result = [list(a) for a in result]
		for i in range(len(result)):
			result[i].insert(0, i+1)
		for y, x in enumerate(result):
			ques = x[1]
			sql_query1 = "SELECT mark, type_of_answer, options FROM [" + test + "] WHERE question = ?"
			result1 = self.cur.execute(sql_query1,(ques,)).fetchone()
			result[y].append(result1[0])
			result[y].append(result1[1])
			result[y].append(result1[2])
		sql_query2 = "SELECT question FROM [" + test + "]"
		result2 = self.cur.execute(sql_query2).fetchall()
		if len(result2) != len(result):
			question= []
			for i in result:
				question.append(i[1])
			unattempted = []
			for a,b in enumerate(result2):
				if b[0] in question:
					pass
				else:
					c = []
					c.append(b[0])
					unattempted.append(c)
			result = result + unattempted
		return result


	def fetch_results(self, user):
		result1 = self.cur.execute("SELECT test_name FROM Tests").fetchall()
		test_marks = []
		for i in result1:
			test = i[0]
			sql_query = "SELECT total_marks, max_marks FROM [" + test + "_" + "results] WHERE user_name = ? AND status = ?"
			result = self.cur.execute(sql_query, (user, "evaluated")).fetchone()
			if result != None:
				li_st = []
				li_st.append(test)
				li_st.append(result[0])
				li_st.append(result[1])
				test_marks.append(li_st)
		return test_marks


	def evaluate(self, tst, usr, data):
		user_marks = 0
		for i in data:
			if i[2] == i[3]:
				sql_query4 = "SELECT mark FROM [" + tst + "] WHERE question = ?"
				result3 = self.cur.execute(sql_query4, (i[1],))
				result3 = result3.fetchone()
				user_marks += result3[0]
				sql_query5 = "INSERT INTO [" + tst + "_" + usr + "](question, user_answer, actual_answer, mark, correct) VALUES(?, ?, ?, ?, ?);"
				self.cur.execute(sql_query5, (i[1], i[2], i[3], result3[0], 1))
			else:
				sql_query6 = "INSERT INTO [" + tst + "_" + usr + "](question, user_answer, actual_answer, mark, correct) VALUES(?, ?, ?, ?, ?);"
				self.cur.execute(sql_query6, (i[1], i[2], i[3], 0, 0))
		return user_marks


	def update_eval(self, test, user, data):
		marks = 0
		for i in data:
			marks += float(i[2])
			sql_query1 = "UPDATE [" + test + "_" + user + "] set correct = ?, mark = ? WHERE question = ?"
			self.cur.execute(sql_query1, (i[1], float(i[2]), i[0]))
		sql_query2 = "UPDATE [" + test + "_results] set total_marks = ?, status = ? WHERE user_name = ?"
		self.cur.execute(sql_query2, (marks, "evaluated", user))
		self.con.commit()


	def fetch_eval_data(self, test, user):
		sql_query1 = "SELECT question, user_answer, actual_answer FROM [" + test + "_" + user + "]"
		result1 = self.cur.execute(sql_query1)
		result1 = result1.fetchall()
		result1 = [list(a) for a in result1]
		for x, i in enumerate(result1):
			ques = i[0]
			sql_query2 = "SELECT type_of_answer, options, mark FROM [" + test + "] WHERE question = ?"
			result2 = self.cur.execute(sql_query2, (ques,))
			result2 = result2.fetchone()
			result1[x].append(result2[0])
			result1[x].append(result2[1])
			result1[x].append(result2[2])
			result1[x].insert(0, x+1)
		return result1




	def fetch_usr_status(self, test_name):
		sql_query = "SELECT user_name, status, total_marks, max_marks FROM [" + test_name + "_results] " 
		result = self.cur.execute(sql_query)
		return result.fetchall()
		

	def sub_ans(self, test, user, answers):
		for x,i in enumerate(answers):
			que = i[1]
			sql_query1 = "SELECT answer FROM [" +  test + "] WHERE question = ?"
			result = self.cur.execute(sql_query1, (que,))
			result = result.fetchone()
			result = result[0]
			answers[x].append(result)
		result2 = self.cur.execute("SELECT auto_evaluate FROM Tests WHERE test_name = ?", (test,))
		result2 = result2.fetchone()
		if result2[0] == 1:
			marks = self.evaluate(test, user, answers)
			sql_query7 = "UPDATE [" + test + "_results] SET total_marks = ?, status = 'evaluated' WHERE user_name = ?"
			self.cur.execute(sql_query7, (marks, user))		
		else:
			for a in answers:
				sql_query2 = "INSERT INTO [" + test + "_" + user + "](question, user_answer, actual_answer) VALUES(?, ?, ?);"
				self.cur.execute(sql_query2, (a[1], a[2], a[3]))
			sql_query3 = "UPDATE [" + test + "_results] SET status = 'finished' WHERE user_name = ?"
			self.cur.execute(sql_query3, (user,))
		self.con.commit()


	def fetch_questions(self, a):
		sql1 = "SELECT ques_order, question, type_of_answer, options FROM [" + a + "]"
		result1 = self.cur.execute(sql1)
		result1 =  result1.fetchall()
		sql2 = "SELECT time_limit, shuffle FROM Tests Where test_name = ?"
		result2 = self.cur.execute(sql2, (a,))
		result2 =  result2.fetchone()
		time_limit = result2[0]
		if result2[1] == 1:
			random.shuffle(result1)
		else:
			result1.sort()
		return result1, time_limit




	def fetch_tests1(self, user):
		result1 = self.cur.execute("SELECT test_name FROM Tests")
		result1 =  result1.fetchall()
		test_status = []
		for i in result1:
			query = "SELECT status FROM [" + i[0] + "_results] WHERE user_name = ?"
			result2 = self.cur.execute(query, (user,)) 
			result2 = result2.fetchone()
			if result2 != None:
				if result2[0] == "not completed":
					test_status.append(i[0])
		results = []
		for i in test_status:
			query = "SELECT test_name, total_marks, time_limit FROM Tests WHERE test_name = ?"
			result = self.cur.execute(query, (i,))
			result = list(result.fetchone())
			result[2] = str(datetime.timedelta(seconds=int(result[2])))
			results.append(result)
		return results



	def login_check(self, usr, pwd):
		result = self.cur.execute("SELECT user_id, pwd, power FROM Users WHERE user_id = ? AND pwd = ?", (usr, pwd))
		return result.fetchone()


	def get_user_info(self, a):
		result = self.cur.execute("SELECT user_id, pwd, power FROM Users WHERE user_id = ?", (a,))
		return result.fetchone()


	def fetch_users(self):
		hello = self.cur.execute("SELECT user_id, power FROM Users")
		x = hello.fetchall()
		return x


	def fetch_users2(self):
		result = self.cur.execute("SELECT user_id FROM Users WHERE power='quiztaker'")
		res = result.fetchall()
		return res


	def rm_usr(self, usr):
		self.cur.execute("DELETE FROM Users WHERE user_id = ?", (usr,))
		self.con.commit()


	def chg_user(self, a, b, c, d):
		result = self.cur.execute("SELECT user_id, pwd, power FROM Users WHERE user_id = ?", (a,))
		res = result.fetchone()
		if res == None or res[0] == d:
			self.cur.execute("UPDATE Users SET user_id = ?, pwd = ?, power = ? WHERE user_id = ?", (a, b, c, d))
			self.con.commit()
		else:
			return "No"


	def crt_user(self, a, b, c):
		result = self.cur.execute("SELECT user_id, pwd, power FROM Users WHERE user_id = ?", (a,))
		res = result.fetchall()
		if len(res) == 0:
			self.cur.execute("INSERT INTO Users(user_id, pwd, power) VALUES(?, ?, ?);", (a, b, c))
			self.con.commit()
		else:
			return "No"


	def crt_test(self, test_data, test_questions, users):
		self.cur.execute("INSERT INTO Tests(test_name, test_description, alloted_users, time_limit, auto_evaluate, shuffle, total_marks) VALUES(?, ?, ?, ?, ?, ?, ?);", (test_data[0], test_data[1], test_data[2], test_data[3], test_data[4], test_data[5], test_data[6]))
		query = "CREATE TABLE ["+ test_data[0] + "](ques_order INTEGER, question TEXT, type_of_answer TEXT, options TEXT, answer TEXT, mark REAL);"
		self.cur.execute(query)
		for i in test_questions:
			if i[2][:3] == "MCQ": 
				sql_query = "INSERT INTO ["+test_data[0]+"](ques_order, question, type_of_answer, options, answer, mark) VALUES (?, ?, ?, ?, ?, ?)"
				self.cur.execute(sql_query, (i[0], i[1], i[2], i[3], i[4], i[5]))
			else:
				sql_query = "INSERT INTO ["+test_data[0]+"](ques_order, question, type_of_answer, answer, mark) VALUES (?, ?, ?, ?, ?)"
				self.cur.execute(sql_query, (i[0], i[1], i[2], i[3], i[4]))
		tables = []
		for i in users:
			tables.append(test_data[0] + "_" + i)
		for i in tables:
			table_query = "CREATE TABLE ["+ i + "](question TEXT, user_answer TEXT, actual_answer TEXT, correct INTEGER, mark REAL);"
			self.cur.execute(table_query)
		result = test_data[0] + "_results"
		result_query = "CREATE TABLE ["+ result + "](user_name TEXT, total_marks REAL, max_marks REAL, status TEXT);"
		self.cur.execute(result_query)
		for i in users:
			sql_query = "INSERT INTO ["+result+"](user_name, total_marks, max_marks, status) VALUES (?, ?, ?, ?)"
			self.cur.execute(sql_query, (i, 0, test_data[6], "not completed"))
		self.con.commit()


	def fetch_test_data(self):
		result = self.cur.execute("SELECT test_name, alloted_users, time_limit, total_marks FROM Tests")
		return result.fetchall()


	def fetch_test_data2(self, tst_name):
		result = self.cur.execute("SELECT test_name, test_description, alloted_users, time_limit FROM Tests WHERE test_name = ?", (tst_name,))
		return result.fetchone()


	def fetch_test_marks(self, a):
		result = self.cur.execute("SELECT total_marks FROM Tests WHERE test_name = ?", (a,))
		return result.fetchone()


	def chg_test_data(self, chg_data):
		result = self.cur.execute("SELECT alloted_users FROM Tests WHERE test_name = ?", (chg_data[0],))
		result = result.fetchone()
		self.cur.execute("UPDATE Tests SET test_description = ?, alloted_users = ?, time_limit = ? WHERE test_name = ?", (chg_data[1], chg_data[2], chg_data[3], chg_data[0]))
		users = chg_data[2].split(",")
		real_users = result[0].split(",")
		add_users = []
		del_users = []
		for i in real_users:
			if i not in users:
				del_users.append(i)
		for i in users:
			if i not in real_users:
				add_users.append(i)
		for i in del_users:
			query = "DELETE FROM [" + chg_data[0] + "_results] WHERE user_name = ?"
			self.cur.execute(query, (i,))
			query2 = "DROP TABLE [" + chg_data[0] + "_" + i + "]"
			self.cur.execute(query2)
		data_rec = self.fetch_test_marks(chg_data[0])
		for i in add_users:
			query = "INSERT INTO [" + chg_data[0] + "_results](user_name, total_marks, max_marks, status) VALUES(?, ?, ?, ?)"
			self.cur.execute(query, (i, 0, data_rec[0], "not completed"))
			query2 = "CREATE TABLE ["+ chg_data[0] + "_" + i + "](question TEXT, user_answer TEXT, actual_answer TEXT, correct INTEGER, mark REAL);"
			self.cur.execute(query2)
		self.con.commit()


	def remove_test(self, tst_name):
		result = self.cur.execute("SELECT test_name, alloted_users FROM Tests WHERE test_name = ?", (tst_name,))
		result = result.fetchone()
		testname = result[0]
		users = result[1].split(",")
		query_drop_table1 = "DROP TABLE [" + testname + "]"
		self.cur.execute(query_drop_table1)
		query_drop_table2 = "DROP TABLE [" + testname + "_results]"
		self.cur.execute(query_drop_table2)
		for i in users:
			query = "DROP TABLE [" + testname + "_" + i + "]"
			self.cur.execute(query)
		self.cur.execute("DELETE FROM Tests WHERE test_name = ?", (testname,))
		self.con.commit()


	#Closing the database connection
	def close(self):
		self.con.close()

#Giving the instance 'db' the class DB_manager
db = DB_manager()