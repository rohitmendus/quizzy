"""The user_id and password of the admin is here as follows:
user_id: admin1
password: 12345"""


#Importing files and packages
from tkinter import *
from tkinter import messagebox
from tkinter import font as tkFont
from PIL import ImageTk, Image
import database
import pygame
import datetime
import time


#Making the class Quiztaker for all applications which the person who takes the quiz uses.
class Quiztaker():
	#Initialising
	def __init__(self, usr_name):
		pygame.mixer.init()
		self.usr_name = usr_name
		self.menu_screen()


	#Making sure that the user wants to logout.
	def log_out(self):
		ask = messagebox.askyesno("Logout?", "Are you sure that you want to logout? Make sure you have saved your changes.")
		if ask == 1:
			quizzy.clear()
			quizzy.check_user()


	#Menuscreen for the quiztaker
	def menu_screen(self):
		quizzy.clear()
		self.user_shown = Label(quizzy.master, padx=10, pady=10, text = "Current User: " + quizzy.current_user, font=('Helvetica', 20))
		self.user_shown.place(x = 1, y = 1)
		self.logout = Button(quizzy.master, text="Log Out", activebackground="red", activeforeground="white", font=('Helvetica', 20), width = 13, bg="red", fg="white", command = self.log_out)
		self.tk_tests = Button(quizzy.master, text="Take Test", activebackground="green", activeforeground="white", font=('Helvetica', 20), width = 15, bg="green", fg="white", command = self.take_tests)
		self.view_res = Button(quizzy.master, text="View Results", activebackground="green", activeforeground="white", font=('Helvetica', 20), width = 15, bg="green", fg="white", command = self.view_results)
		self.logout.place(x = 750, y = 10)
		self.tk_tests.place(x=220, y = 250)
		self.view_res.place(x=500, y = 250)


	#Menu screen for taking tests
	def take_tests(self):
		quizzy.clear()
		self.logout = Button(quizzy.master, text="Log Out", activebackground="red", activeforeground="white", font=('Helvetica', 20), width = 13, bg="red", fg="white", command = self.log_out)
		self.logout.place(x = 750, y = 10)
		self.go_back = Button(quizzy.master, text="Back", activebackground="green", activeforeground="white", font=('Helvetica', 20), width = 13, bg="green", fg="white", command = self.menu_screen)
		self.go_back.place(x = 500, y = 10)
		myframe=Frame(quizzy.master,relief=GROOVE,width=600,height=400,bd=1)
		myframe.place(x=50,y=100)
		canvas=Canvas(myframe, width = 800, height = 400)
		self.test_list_table=Frame(canvas)
		myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
		canvas.configure(yscrollcommand=myscrollbar.set)
		myscrollbar.pack(side="right",fill="y")
		canvas.pack(side="left", fill="both", expand=True)
		canvas.create_window((0,0),window=self.test_list_table,anchor='nw')
		self.test_list_table.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
		self.head1_test_list = Label(self.test_list_table, text = "Test Name", font=('Helvetica', 20))
		self.head2_test_list = Label(self.test_list_table, text = "Total Marks", font=('Helvetica', 20))
		self.head3_test_list = Label(self.test_list_table, text = "Time Limit", font=('Helvetica', 20))
		self.head1_test_list.grid(row = 0, column = 1, padx=10, pady=10)
		self.head2_test_list.grid(row = 0, column = 2, padx=10, pady=10)
		self.head3_test_list.grid(row = 0, column = 3, padx=10, pady=10)
		data_recieved = quizzy.db.fetch_tests1(self.usr_name)
		r = 0
		for i in data_recieved:
			r += 1
			c = 0
			for x in i:
				c += 1
				Label(self.test_list_table, text = x, padx=10, pady=10, font=('Helvetica', 19), fg = "#4d4d4c").grid(row = r, column = c)
			take_tests = Button(self.test_list_table, padx=15, pady=10, text="Take Test", activebackground="green", activeforeground="white", font=('Helvetica', 14), width = 7, bg="green", fg="white", command = lambda b = data_recieved[r-1]: self.confirm_test(b))
			take_tests.grid(row = r, column = 0, padx = 10, pady = 10)


	#Asking the user if he wants to exit 
	def exit(self):
		ask = messagebox.askyesno("Exit", "Are you sure that you want to exit?")
		if ask == 1:
			quizzy.db.close()
			quizzy.master.destroy()


	#Asking the user if he wants to submit and exit. This protocol runs only while the user is taking the test.
	def test_exit(self):
		ask = messagebox.askyesno("Exit", "Are you sure that you want to exit? The test will be submitted!")
		if ask == 1:
			self.submit_answers()
			quizzy.db.close()
			quizzy.master.destroy()


	#Creating the timer and buttons to take the test.
	def test_taker(self, test_name):
		quizzy.clear()
		quizzy.master.protocol("WM_DELETE_WINDOW", self.test_exit)
		self.test = test_name
		test_details_test = quizzy.db.fetch_questions(test_name)
		self.time = int(test_details_test[1])
		self.questions_test = test_details_test[0]
		self.total_ques = len(self.questions_test)
		self.answers = []
		self.current_ques = 1
		self.timer = Label(quizzy.master, text=str(datetime.timedelta(seconds=self.time)), font=('Helvetica', 46))
		self.timer.place(x =780, y=10)
		self.timer.after(1000, self.update_timer)
		self.prev_but = Button(quizzy.master, text="<", activebackground="blue", activeforeground="white", font=('Helvetica', 20), width = 7, bg="blue", fg="white", command = self.prev_ques)
		self.prev_but.place(x = 100, y = 450)
		self.next_but = Button(quizzy.master, text=">", activebackground="green", activeforeground="white", font=('Helvetica', 20), width = 7, bg="green", fg="white", command = self.next_ques)
		self.next_but.place(x = 300, y = 450)
		self.sav_but = Button(quizzy.master, text="Save", activebackground="#33cc33", activeforeground="white", font=('Helvetica', 20), width = 10, bg="#33cc33", fg="white", command = self.save_ans)
		self.sav_but.place(x = 500, y = 450)
		self.sub_but = Button(quizzy.master, text="Submit", activebackground="red", activeforeground="white", font=('Helvetica', 20), width = 10, bg="red", fg="white", command = self.submit_answers)
		self.sub_but.place(x = 750, y = 450)
		self.display_ques(self.current_ques)


	#This function displays the current question on to the screen
	def display_ques(self, crnt):
		myframe=Frame(quizzy.master,relief=GROOVE,width=900,height=300,bd=1)
		myframe.place(x=10,y=120)
		canvas=Canvas(myframe, width = 900, height = 300)
		self.dis_ques_frame=Frame(canvas)
		myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
		myscrollbar_x=Scrollbar(myframe,orient="horizontal",command=canvas.xview)
		canvas.configure(yscrollcommand=myscrollbar.set)
		canvas.configure(xscrollcommand=myscrollbar_x.set)	
		myscrollbar.pack(side="right",fill="y")
		myscrollbar_x.pack(side="bottom", fill = "x")
		canvas.pack(side="left", fill="both", expand=True)
		canvas.create_window((0,0),window=self.dis_ques_frame,anchor='nw')
		self.dis_ques_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
		self.question_lab = Label(self.dis_ques_frame, text = str(crnt) + ". " + self.questions_test[crnt-1][1], font=('Helvetica', 20))
		self.question_lab.grid(row = 0, column = 0, columnspan = 4, sticky = "w", padx = 10, pady = 10)
		lab_lab = Label(self.dis_ques_frame, text = "", font=('Helvetica', 20))
		lab_lab.grid(row = 1, column = 0, columnspan = 4, padx = 10, pady = 10)
		if self.questions_test[crnt-1][2] == "MCQ(Single option choose)":
			options_nxt = self.questions_test[crnt-1][3].split(",")
			self.rb_option_var = StringVar()
			self.rb_option1 = Radiobutton(self.dis_ques_frame, tristatevalue = "x", variable = self.rb_option_var, value = "A", text = options_nxt[0], font=('Helvetica', 20))
			self.rb_option2 = Radiobutton(self.dis_ques_frame, tristatevalue = "x", variable = self.rb_option_var, value = "B", text = options_nxt[1], font=('Helvetica', 20))
			self.rb_option3 = Radiobutton(self.dis_ques_frame, tristatevalue = "x", variable = self.rb_option_var, value = "C", text = options_nxt[2], font=('Helvetica', 20))
			self.rb_option4 = Radiobutton(self.dis_ques_frame, tristatevalue = "x", variable = self.rb_option_var, value = "D", text = options_nxt[3], font=('Helvetica', 20))
			for i in self.answers:
				if i[0] == self.current_ques:
					ans_dis = i[2]
					self.rb_option_var.set(ans_dis)
			self.rb_option1.grid(row = 2, column = 1, sticky = "w", padx = 10, pady = 10)
			self.rb_option2.grid(row = 2, column = 2, sticky = "w", padx = 10, pady = 10)
			self.rb_option3.grid(row = 3, column = 1, sticky = "w", padx = 10, pady = 10)
			self.rb_option4.grid(row = 3, column = 2, sticky = "w", padx = 10, pady = 10)
		elif self.questions_test[crnt-1][2] == "MCQ(Multiple option choose)":
			options_nxt = self.questions_test[crnt-1][3].split(",")
			self.chk_option_var1 = IntVar()
			self.chk_option_var2 = IntVar()
			self.chk_option_var3 = IntVar()
			self.chk_option_var4 = IntVar()
			self.chk_option1 = Checkbutton(self.dis_ques_frame, variable = self.chk_option_var1, onvalue = 1, offvalue = 0, text = options_nxt[0], font=('Helvetica', 20))
			self.chk_option2 = Checkbutton(self.dis_ques_frame, variable = self.chk_option_var2, onvalue = 1, offvalue = 0, text = options_nxt[1], font=('Helvetica', 20))
			self.chk_option3 = Checkbutton(self.dis_ques_frame, variable = self.chk_option_var3, onvalue = 1, offvalue = 0, text = options_nxt[2], font=('Helvetica', 20))
			self.chk_option4 = Checkbutton(self.dis_ques_frame, variable = self.chk_option_var4, onvalue = 1, offvalue = 0, text = options_nxt[3], font=('Helvetica', 20))
			for i in self.answers:
				if i[0] == self.current_ques:
					anns = i[2].split(",")
					options = ["A", "B", "C", "D"]
					ans_dis = []
					for a in options:
						if a in anns:
							ans_dis.append(1)
						else:
							ans_dis.append(0)
					self.chk_option_var1.set(ans_dis[0])
					self.chk_option_var2.set(ans_dis[1])
					self.chk_option_var3.set(ans_dis[2])
					self.chk_option_var4.set(ans_dis[3])
			self.chk_option1.grid(row = 2, column = 1, sticky = "w", padx = 10, pady = 10)
			self.chk_option2.grid(row = 2, column = 2, sticky = "w", padx = 10, pady = 10)
			self.chk_option3.grid(row = 3, column = 1, sticky = "w", padx = 10, pady = 10)
			self.chk_option4.grid(row = 3, column = 2, sticky = "w", padx = 10, pady = 10)
		elif self.questions_test[crnt-1][2] == "One Word":
			self.one_word_lab = Label(self.dis_ques_frame, text = "Ans: ", font=('Helvetica', 20))
			self.one_word_lab.grid(row = 2, column = 0, sticky = "w", padx = 20, pady = 20)
			self.one_word_ans = Entry(self.dis_ques_frame, font=('Helvetica', 20), width = 20)
			self.one_word_ans.grid(row = 2, column = 1, sticky = "w", padx = 20, pady = 20)
			for i in self.answers:
				if i[0] == self.current_ques:
					ans_dis = i[2]
					self.one_word_ans.delete(0,END)
					self.one_word_ans.insert(0, ans_dis)
		elif self.questions_test[crnt-1][2] == "Description":
			self.desc_lab = Label(self.dis_ques_frame, text = "Ans: ", font=('Helvetica', 20))
			self.desc_lab.grid(row = 2, column = 0, sticky = "nw", padx = 20, pady = 20)
			self.desc_ans = Text(self.dis_ques_frame, font=('Helvetica', 16), width = 50, height = 3, cursor = "dot", wrap = WORD, insertbackground = "blue", padx = 10, pady = 10)
			self.desc_ans.grid(row = 2, column = 1, rowspan = 3, columnspan = 2)
			for i in self.answers:
				if i[0] == self.current_ques:
					ans_dis = i[2]
					self.desc_ans.delete(0.1, END)
					self.desc_ans.insert(0.1, ans_dis)


	#This function helps in displaying the next question.
	def next_ques(self):
		if self.current_ques < self.total_ques:
			self.dis_ques_frame.destroy()
			self.current_ques += 1
			self.display_ques(self.current_ques)


	#This function helps in displaying the previous question.
	def prev_ques(self):
		if self.current_ques > 1:
			self.dis_ques_frame.destroy()
			self.current_ques -= 1
			self.display_ques(self.current_ques)


	#Saves the answer and can be seen when move to the next question and come back.
	def save_ans(self):
		answer = []
		sv_ques = self.current_ques
		attempted = False
		for i in self.answers:
			if i[0] == self.current_ques:
				attempted = True
		type_test = self.questions_test[sv_ques-1][2]
		if type_test == "MCQ(Single option choose)":
			ans = self.rb_option_var.get()
			if ans == None:
				blank = True
			else:
				blank = False
		elif type_test == "MCQ(Multiple option choose)":
			user_ans = []
			user_ans.append(self.chk_option_var1.get())
			user_ans.append(self.chk_option_var2.get())
			user_ans.append(self.chk_option_var3.get())
			user_ans.append(self.chk_option_var4.get())
			if 1 in user_ans:
				blank = False
				ans = []
				options = ["A", "B", "C", "D"]
				for x, i in enumerate(user_ans):
					if i == 1:
						ans.append(options[x])
				ans = ",".join(ans)
			else:
				blank = True
		elif type_test == "One Word":
			ans = self.one_word_ans.get()
			if len(ans) != 0:
				blank = False
			else:
				blank = True
		elif type_test == "Description":
			ans = self.desc_ans.get(0.1, END).strip()
			if len(ans) != 0:
				blank = False
			else:
				blank = True
		answer.append(sv_ques)
		answer.append(self.questions_test[sv_ques-1][1])
		if blank == False and attempted == False:
			answer.append(ans)
			self.answers.append(answer)
		elif blank == False and attempted == True:
			for x, i in enumerate(self.answers):
				if i[0] == sv_ques:
					self.answers.pop(x)
					answer.append(ans)
					self.answers.append(answer)
					break
		elif blank == True and attempted == True:
			for i in self.answers:
				if i[0] == sv_ques:
					self.answers.remove(i)
		answer = []


	#Submits the answers by passing the data to the database
	def submit_answers(self):
		quizzy.master.protocol("WM_DELETE_WINDOW", self.exit)
		pygame.mixer.music.stop()
		quizzy.clear()
		quizzy.db.sub_ans(self.test, self.usr_name, self.answers)
		self.menu_screen()


	#Helps in updating the timer and to submit the answer when it stops.
	def update_timer(self):
		if self.time == 0:
			self.submit_answers()
		elif self.time == 60:
			self.timer.config(fg = "red")
			self.time -= 1
			self.timer.config(text=str(datetime.timedelta(seconds=self.time)))
			self.timer.after(1000, self.update_timer)
		elif self.time <= 10:
			pygame.mixer.music.load("Files/beep_submit.mp3")
			pygame.mixer.music.play(loops = 0)
			self.time -= 1
			self.timer.config(text=str(datetime.timedelta(seconds=self.time)))
			self.timer.after(1000, self.update_timer)
		else:
			self.time -= 1
			self.timer.config(text=str(datetime.timedelta(seconds=self.time)))
			self.timer.after(1000, self.update_timer)


	#Asks for confirmation of taking the test.
	def confirm_test(self, test_details):
		reply = messagebox.askyesno("Test confirmation", "Are you sure you that you want to take the test? The timer will start now. ")
		if reply == 1:
			self.test_taker(test_details[0])
		else:
			return


	#Moves to next question while the user view his evaluated test results.
	def next_ques_res(self):
		if self.current_question != self.max_ques_len:
			self.eval_result_frame.destroy()
			self.current_question += 1
			self.dis_eval_results()


	#Moves to prevoius question while the user view his evaluated test results.
	def pre_ques_res(self):
		if self.current_question != 1:
			self.eval_result_frame.destroy()
			self.current_question -= 1
			self.dis_eval_results()


	#Fetches required data and sets up buttons for the user to view his results
	def view_eval(self, user, test):
		self.result_data = quizzy.db.fetch_eval_view(user, test)
		self.max_ques_len = len(self.result_data)
		quizzy.clear()
		self.go_back = Button(quizzy.master, text="Back", activebackground="green", activeforeground="white", font=('Helvetica', 20), width = 13, bg="green", fg="white", command = self.view_results)
		self.go_back.place(x = 700, y = 10)
		self.next_but_res = Button(quizzy.master, text=">", activebackground="green", activeforeground="white", font=('Helvetica', 20), width = 10, bg="green", fg="white", command = self.next_ques_res)
		self.next_but_res.place(x = 400, y = 480)
		self.pre_but_res = Button(quizzy.master, text="<", activebackground="blue", activeforeground="white", font=('Helvetica', 20), width = 10, bg="blue", fg="white", command = self.pre_ques_res)
		self.pre_but_res.place(x = 200, y = 480)
		self.current_question = self.result_data[0][0]
		self.dis_eval_results()


	#Displays the current question
	def dis_eval_results(self):
		self.current_data = self.result_data[self.current_question-1]
		myframe=Frame(quizzy.master,relief=GROOVE,width=900,height=350,bd=1)
		myframe.place(x=50,y=90)
		canvas=Canvas(myframe, width = 900, height = 350)
		self.eval_result_frame=Frame(canvas)
		myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
		myscrollbar_x=Scrollbar(myframe,orient="horizontal",command=canvas.xview)
		canvas.configure(yscrollcommand=myscrollbar.set)
		canvas.configure(xscrollcommand=myscrollbar_x.set)	
		myscrollbar.pack(side="right",fill="y")
		myscrollbar_x.pack(side="bottom", fill = "x")
		canvas.pack(side="left", fill="both", expand=True)
		canvas.create_window((0,0),window=self.eval_result_frame,anchor='nw')
		self.eval_result_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
		if len(self.current_data) == 1:
			self.res_ques_lab = Label(self.eval_result_frame, text = str(self.current_question) + ". " + self.current_data[0], font = ("Helvetica", 18))
			self.res_ques_lab.grid(row = 0, column = 0, columnspan = 4, padx = 10, pady = 20, sticky = "nw")
			self.unattempt_lab = Label(self.eval_result_frame, text = "Not attempted", font = ("Helvetica", 18))
			self.unattempt_lab.grid(row = 1, column = 0, columnspan = 4, padx = 10, pady = 20, sticky = "nw")
		else:
			self.res_ques_lab = Label(self.eval_result_frame, text = str(self.current_question) + ". " + self.current_data[1], font = ("Helvetica", 18))
			self.res_ques_lab.grid(row = 0, column = 0, columnspan = 4, padx = 10, pady = 20, sticky = "nw")
			type_of_ans = self.current_data[7]
			usr_ans = self.current_data[2]
			ans = self.current_data[3]
			opt = self.current_data[8]
			mark = str(self.current_data[5]) + "/" + str(self.current_data[6])
			if type_of_ans == "Description" or type_of_ans == "One Word":
				self.user_ans_res = Label(self.eval_result_frame, text = "User's answer: " + usr_ans, font = ("Helvetica", 18))
				self.ans_res = Label(self.eval_result_frame, text = "Actual answer: " + ans, font = ("Helvetica", 18))
				self.user_ans_res.grid(row = 1, column = 0, columnspan = 4, padx = 10, pady = 20, sticky = "w")
				self.ans_res.grid(row = 2, column = 0, columnspan = 4, padx = 10, pady = 20, sticky = "w")
			elif type_of_ans == "MCQ(Single option choose)":
				opt = opt.split(",")
				self.opt_var_res = StringVar()
				self.user_ans_res = Label(self.eval_result_frame, text = "User's answer: ", font = ("Helvetica", 18))
				self.user_ans_res.grid(row = 1, column = 0, padx = 10)
				self.opt_A_res = Radiobutton(self.eval_result_frame, state = "disabled", tristatevalue = "x", variable = self.opt_var_res, text = "A: " + opt[0], value = "A", padx = 5, pady = 5, font=('Helvetica', 18))
				self.opt_B_res = Radiobutton(self.eval_result_frame, state = "disabled", tristatevalue = "x", variable = self.opt_var_res, text = "B: " + opt[1], value = "B", padx = 5, pady = 5, font=('Helvetica', 18))
				self.opt_C_res = Radiobutton(self.eval_result_frame, state = "disabled", tristatevalue = "x", variable = self.opt_var_res, text = "C: " + opt[2], value = "C", padx = 5, pady = 5, font=('Helvetica', 18))
				self.opt_D_res = Radiobutton(self.eval_result_frame, state = "disabled", tristatevalue = "x", variable = self.opt_var_res, text = "D: " + opt[3], value = "D", padx = 5, pady = 5, font=('Helvetica', 18))
				self.opt_var_res.set(usr_ans)
				self.opt_A_res.grid(row = 2, column = 0, sticky = "w", padx = 10, pady = 10)
				self.opt_B_res.grid(row = 2, column = 2, padx = 10, pady = 10)
				self.opt_C_res.grid(row = 3, column = 0, sticky = "w", padx = 10, pady = 10)
				self.opt_D_res.grid(row = 3, column = 2, padx = 10, pady = 10)
				ans_opt = ["A", "B", "C", "D"]
				ind = ans_opt.index(ans)
				self.ans_res = Label(self.eval_result_frame, text = "Actual answer:   " + ans + ". " + opt[ind], font = ("Helvetica", 18))
				self.ans_res.grid(row = 4, column = 0, columnspan = 2, padx = 10, pady = 20, sticky = "w")
			elif type_of_ans == "MCQ(Multiple option choose)":
				opt = opt.split(",")
				usr_ans = usr_ans.split(",")
				ans = ans.split(",")
				self.optA_var_res = IntVar()
				self.optB_var_res = IntVar()
				self.optC_var_res = IntVar()
				self.optD_var_res = IntVar()
				self.user_ans_res = Label(self.eval_result_frame, text = "User's answer: ", font = ("Helvetica", 18))
				self.user_ans_res.grid(row = 1, column = 0, padx = 10, sticky = "w")
				self.opt_A_res = Checkbutton(self.eval_result_frame, variable = self.optA_var_res, onvalue = 1, offvalue = 0, state = "disabled", text = "A: " + opt[0], padx = 5, pady = 5, font=('Helvetica', 18))
				self.opt_B_res = Checkbutton(self.eval_result_frame, variable = self.optB_var_res, onvalue = 1, offvalue = 0, state = "disabled", text = "B: " + opt[1], padx = 5, pady = 5, font=('Helvetica', 18))
				self.opt_C_res = Checkbutton(self.eval_result_frame, variable = self.optC_var_res, onvalue = 1, offvalue = 0, state = "disabled", text = "C: " + opt[2], padx = 5, pady = 5, font=('Helvetica', 18))
				self.opt_D_res = Checkbutton(self.eval_result_frame, variable = self.optD_var_res, onvalue = 1, offvalue = 0, state = "disabled", text = "D: " + opt[3], padx = 5, pady = 5, font=('Helvetica', 18))
				self.opt_A_res.grid(row = 2, column = 0, sticky = "w", padx = 10, pady = 10)
				self.opt_B_res.grid(row = 2, column = 2, padx = 10, pady = 10)
				self.opt_C_res.grid(row = 3, column = 0, sticky = "w", padx = 10, pady = 10)
				self.opt_D_res.grid(row = 3, column = 2, padx = 10, pady = 10)
				if "A" in usr_ans:
					self.optA_var_res.set(1)
				if "B" in usr_ans:
					self.optB_var_res.set(1)
				if "C" in usr_ans:
					self.optC_var_res.set(1)
				if "D" in usr_ans:
					self.optD_var_res.set(1)
				ans_opt = ["A", "B", "C", "D"]
				ans_text = ""
				for i in ans:
					ind = ans_opt.index(i)
					ans_text += i + ". " + opt[ind] + "    "
				self.ans_res = Label(self.eval_result_frame, text = "Actual answer:   " + ans_text, font = ("Helvetica", 18))
				self.ans_res.grid(row = 4, column = 0, columnspan = 3, padx = 10, pady = 20, sticky = "w")
			if self.current_data[4] == 1:
				self.correct_img = ImageTk.PhotoImage(Image.open("Files/correct.jpg"))
				self.correct_lab = Label(self.eval_result_frame, image = self.correct_img)
				self.correct_lab.grid(row = 5, column = 0, padx = 10, pady = 10, sticky = "w")
			else:
				self.wrong_img = ImageTk.PhotoImage(Image.open("Files/wrong.jpg"))
				self.wrong_lab = Label(self.eval_result_frame, image = self.wrong_img)
				self.wrong_lab.grid(row = 5, column = 0, padx = 10, pady = 10, sticky = "w")
			self.mark_lab_res = Label(self.eval_result_frame, text = "Marks: " + mark, font = ("Helvetica", 18))
			self.mark_lab_res.grid(row = 5, column = 1, pady = 10, padx = 5, sticky = "w")



	#Sets up a table for the user to view his score and marks
	def view_results(self):
		quizzy.clear()
		self.logout = Button(quizzy.master, text="Log Out", activebackground="red", activeforeground="white", font=('Helvetica', 20), width = 13, bg="red", fg="white", command = self.log_out)
		self.logout.place(x = 750, y = 10)
		self.go_back = Button(quizzy.master, text="Back", activebackground="green", activeforeground="white", font=('Helvetica', 20), width = 13, bg="green", fg="white", command = self.menu_screen)
		self.go_back.place(x = 500, y = 10)
		data = quizzy.db.fetch_results(self.usr_name)
		myframe=Frame(quizzy.master,relief=GROOVE,width=600,height=400,bd=1)
		myframe.place(x=10,y=100)
		canvas=Canvas(myframe, width = 800, height = 400)
		self.view_result_table=Frame(canvas)
		myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
		myscrollbar_x=Scrollbar(myframe,orient="horizontal",command=canvas.xview)
		canvas.configure(yscrollcommand=myscrollbar.set)
		canvas.configure(xscrollcommand=myscrollbar_x.set)	
		myscrollbar.pack(side="right",fill="y")
		myscrollbar_x.pack(side="bottom", fill = "x")
		canvas.pack(side="left", fill="both", expand=True)
		canvas.create_window((0,0),window=self.view_result_table,anchor='nw')
		self.view_result_table.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
		self.head1_view_result = Label(self.view_result_table, text = "", font=('Helvetica', 20))
		self.head2_view_result = Label(self.view_result_table, text = "Test", font=('Helvetica', 20))
		self.head3_view_result = Label(self.view_result_table, text = "Marks", font=('Helvetica', 20))
		self.head1_view_result.grid(row = 0, column = 0, padx=10, pady=10)
		self.head2_view_result.grid(row = 0, column = 1, padx=10, pady=10)
		self.head3_view_result.grid(row = 0, column = 2, padx=10, pady=10)
		for x,i in enumerate(data):
			view = Button(self.view_result_table, padx=15, pady=10, text="View", activebackground="green", activeforeground="white", font=('Helvetica', 14), width = 7, bg="green", fg="white", command = lambda y = i[0]: self.view_eval(self.usr_name, y))
			view.grid(row = x+1, column = 0, padx = 20, pady = 10)
			Label(self.view_result_table, text = i[0], font = ("Helvetica", 18)).grid(row = x+1, column = 1, padx = 20, pady = 10)
			Label(self.view_result_table, text = str(i[1]) + "/" + str(i[2]), font = ("Helvetica", 18)).grid(row = x+1, column = 2, padx = 20, pady = 10)


#Creates the class Admin which has the most power in the app to administer it.
class Admin():
	#Initialising
	def __init__(self, usr_name, pwd):
		self.usr_name = usr_name
		self.pwd = pwd
		self.menu_screen()


	#Asks the user for confirmation of logout.
	def log_out(self):
		ask = messagebox.askyesno("Logout?", "Are you sure that you want to logout? Make sure you have saved your changes.")
		if ask == 1:
			quizzy.clear()
			quizzy.check_user()


	#Checking if the deleted is user is valid
	def remove_user(self, usr_id):
		if usr_id == quizzy.current_user:
			messagebox.showerror("Error", "You cannot delete yourself.")
		else:
			ask = messagebox.askyesno("Asking for confirmation", "Are you sure that you want to delete this user?")
			if ask == 1:
				quizzy.db.rm_usr(usr_id)
				self.mng_user()
			else:
				self.mng_user()


	#Checks if the new user is valid
	def create_user(self, usr_id, pwd, power):
		if usr_id == "" or pwd == "":
			messagebox.showinfo("Check you input", "Please check the input you have written.")
			self.crt_new_user()
		else:
			reply = quizzy.db.crt_user(usr_id, pwd, power)
			if reply != "No":
				self.mng_user()
			else:
				messagebox.showwarning("Check your Input", "Please check that your user_id to determine whether there is any other user with the same user_id.")
				self.crt_new_user()


	#Checks new user data
	def chg_user(self, w, x, y, z):
		if w == "" or x == "":
			messagebox.showinfo("Check you input", "Please check the input you have written.")
			self.change_user(z)
		else:
			reply = quizzy.db.chg_user(w, x, y, z)
			if reply != "No":
				self.mng_user()
			else:
				messagebox.showwarning("Check your Input", "Please check that your user_id to determine whether there is any other user with the same user_id.")
				self.change_user(z)


	#Setting widgets to enther the new data of the user
	def change_user(self, a):
		info = quizzy.db.get_user_info(a)
		quizzy.clear()
		self.logout = Button(quizzy.master, text="Log Out", activebackground="red", activeforeground="white", font=('Helvetica', 20), width = 13, bg="red", fg="white", command = self.log_out)
		self.logout.place(x = 775, y = 10)
		self.title_chg_new_user = Label(quizzy.master, text = "Change User", fg = "green", font=('Helvetica', 46), bg = "#ededed")
		self.usr_name = Label(quizzy.master, text="User Name: ", font=('Helvetica', 20), bg = "#ededed")
		self.ent_usr_name = Entry(quizzy.master, font=('Helvetica', 20), width = 15)
		self.ent_usr_name.insert(0, info[0])
		self.pwd = Label(quizzy.master, text="Password: ", font=('Helvetica', 20), bg = "#ededed")
		self.ent_pwd = Entry(quizzy.master, font=('Helvetica', 20), width = 15)
		self.ent_pwd.insert(0, info[1])
		self.power = Label(quizzy.master, text="Power: ", font=('Helvetica', 20), bg = "#ededed")
		opt_list = ["admin", "quiztaker"]
		self.helv35=tkFont.Font(family='Helvetica', size=20)
		self.opt_var = StringVar(quizzy.master)
		self.opt_var.set(info[2])
		self.opt_menu = OptionMenu(quizzy.master, self.opt_var, *opt_list)
		self.opt_menu.config(font=self.helv35)
		menu = quizzy.master.nametowidget(self.opt_menu.menuname)
		menu.config(font=self.helv35)
		self.change = Button(quizzy.master, text="Change", activebackground="green", activeforeground="white", font=('Helvetica', 16), width = 10, bg="green", fg="white", command = lambda: self.chg_user(self.ent_usr_name.get(), self.ent_pwd.get(), self.opt_var.get(), info[0]))
		self.usr_name.place(x=300, y=150)
		self.ent_usr_name.place(x=500, y=150)
		self.pwd.place(x=300, y=230)
		self.ent_pwd.place(x=500, y=230)
		self.change.place(x=480, y=390)
		self.power.place(x=300, y=310)
		self.opt_menu.place(x = 500, y = 310)
		self.title_chg_new_user.place(x=300, y=50)


	#Setting up widgets for creating new user
	def crt_new_user(self):
		quizzy.clear()
		self.logout = Button(quizzy.master, text="Log Out", activebackground="red", activeforeground="white", font=('Helvetica', 20), width = 13, bg="red", fg="white", command = self.log_out)
		self.logout.place(x = 775, y = 10)
		self.title_crt_new_user = Label(quizzy.master, text = "Create New User", fg = "blue", font=('Helvetica', 46), bg = "#ededed")
		self.usr_name = Label(quizzy.master, text="User Name: ", font=('Helvetica', 20), bg = "#ededed")
		self.ent_usr_name = Entry(quizzy.master, font=('Helvetica', 20), width = 15)
		self.pwd = Label(quizzy.master, text="Password: ", font=('Helvetica', 20), bg = "#ededed")
		self.ent_pwd = Entry(quizzy.master, font=('Helvetica', 20), width = 15)
		self.power = Label(quizzy.master, text="Power: ", font=('Helvetica', 20), bg = "#ededed")
		opt_list = ["admin", "quiztaker"]
		self.helv35=tkFont.Font(family='Helvetica', size=20)
		self.opt_var = StringVar(quizzy.master)
		self.opt_var.set(opt_list[1])
		self.opt_menu = OptionMenu(quizzy.master, self.opt_var, *opt_list)
		self.opt_menu.config(font=self.helv35)
		menu = quizzy.master.nametowidget(self.opt_menu.menuname)
		menu.config(font=self.helv35)
		self.create = Button(quizzy.master, text="Create", activebackground="blue", activeforeground="white", font=('Helvetica', 16), width = 10, bg="blue", fg="white", command = lambda: self.create_user(self.ent_usr_name.get(), self.ent_pwd.get(), self.opt_var.get()))
		self.usr_name.place(x=300, y=150)
		self.ent_usr_name.place(x=500, y=150)
		self.pwd.place(x=300, y=230)
		self.ent_pwd.place(x=500, y=230)
		self.create.place(x=480, y=390)
		self.power.place(x=300, y=310)
		self.opt_menu.place(x = 500, y = 310)
		self.title_crt_new_user.place(x=300, y=50)


	#Shows all user and sets up button to apply different functions
	def mng_user(self):
		quizzy.clear()
		self.logout = Button(quizzy.master, text="Log Out", activebackground="red", activeforeground="white", font=('Helvetica', 20), width = 13, bg="red", fg="white", command = self.log_out)
		self.logout.place(x = 750, y = 10)
		self.go_back = Button(quizzy.master, text="Back", activebackground="green", activeforeground="white", font=('Helvetica', 20), width = 13, bg="green", fg="white", command = self.menu_screen)
		self.crt_new = Button(quizzy.master, text="Create new user", activebackground="Blue", activeforeground="white", font=('Helvetica', 20), width = 13, bg="blue", fg="white", command = self.crt_new_user)
		self.go_back.place(x = 500, y = 10)
		self.crt_new.place(x=250, y = 10)
		data_recieved = quizzy.db.fetch_users()
		myframe=Frame(quizzy.master,relief=GROOVE,width=600,height=400,bd=1)
		myframe.place(x=150,y=100)
		canvas=Canvas(myframe, width = 600, height = 400)
		self.table=Frame(canvas)
		myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
		canvas.configure(yscrollcommand=myscrollbar.set)	
		myscrollbar.pack(side="right",fill="y")
		canvas.pack(side="left", fill="both", expand=True)
		canvas.create_window((0,0),window=self.table,anchor='nw')
		self.table.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
		self.head1_mng_user = Label(self.table, padx=10, pady=10, text = "User Name", font=('Helvetica', 20))
		self.head2_mng_user = Label(self.table, padx=10, pady=10, text = "Power", font=('Helvetica', 20))
		self.head3_mng_user = Label(self.table, padx=10, pady=10, text = "Functions", font=('Helvetica', 20))
		self.head1_mng_user.grid(row = 0, column = 2)
		self.head2_mng_user.grid(row = 0, column = 3)
		self.head3_mng_user.grid(row = 0, column = 0, columnspan = 2)
		r = 0
		for i in data_recieved:
			r += 1
			c = 1
			for x in i:
				c += 1
				Label(self.table, text = x, padx=10, pady=10, font=('Helvetica', 19), fg = "#4d4d4c").grid(row = r, column = c)
			hi = Button(self.table, padx=15, pady=10, text="Remove", activebackground="red", activeforeground="white", font=('Helvetica', 14), width = 7, bg="red", fg="white", command = lambda v = i[0]: self.remove_user(v))
			hi.grid(row = r, column = 0)
			bye = Button(self.table, padx=15, pady=10, text="Change", activebackground="green", activeforeground="white", font=('Helvetica', 14), width = 7, bg="green", fg="white", command = lambda v = i[0]: self.change_user(v))
			bye.grid(row = r, column = 1)


	#Asking for confirmation of removing the test
	def rm_test(self, b):
		ask = messagebox.askyesno("Exit", "Are you sure that you want to delete test-" + b + "?")
		if ask == 1:
			quizzy.db.remove_test(b)
			self.mng_test()
		else:
			self.mng_test()


	#Collecting the newy changes test data
	def collect_chg_test_data(self):
		return_to = False
		self.data_list_chg_test = []
		self.data_list_chg_test.append(self.ent_test_name_chg_test.get())
		self.data_list_chg_test.append(self.ent_desc_text_chg_test.get(1.0, END).strip())
		item_num = self.alloted_users_lsbox_chg_test.curselection()
		self.users_chg_test = []
		for i in item_num:
			self.users_chg_test.append(self.alloted_users_lsbox_chg_test.get(i))
		self.data_list_chg_test.append(",".join(self.users_chg_test))
		x = self.time_hours_chg_test.get()
		y = self.time_mins_chg_test.get()
		x = int(x)
		y = int(y)
		if x == 0 and y == 0:
			messagebox.showwarning("Time limit not usable", "Please set the time limit to atleast 15 minutes.")
			return_to = True
		else:
			t = (x*60*60) + (y*60)
			self.data_list_chg_test.append(t)
		if return_to:
			self.mng_test()
		else:
			quizzy.db.chg_test_data(self.data_list_chg_test)
			self.mng_test()


	#Setting up widgets to change test data
	def change_test_data(self, tst_name):
		quizzy.clear()
		data_recieved = quizzy.db.fetch_test_data2(tst_name)
		self.go_back = Button(quizzy.master, text="Back", activebackground="green", activeforeground="white", font=('Helvetica', 20), width = 13, bg="green", fg="white", command = self.mng_test)
		self.go_back.place(x = 750, y = 10)
		self.title_change_test = Label(quizzy.master, text = "Change Test", fg = "blue", font=('Helvetica', 40), bg = "#ededed")
		self.title_change_test.place(x=350, y=70)
		self.test_name_lab_chg_test = Label(quizzy.master, text="Test Name: ", font=('Helvetica', 20), bg = "#ededed")
		self.ent_test_name_chg_test = Entry(quizzy.master, font=('Helvetica', 20), width = 15)
		self.ent_test_name_chg_test.insert(0, tst_name)
		self.ent_test_name_chg_test.config(state = "disabled")
		self.desc_text_chg_test = Label(quizzy.master, text="Test Description: ", font=('Helvetica', 20), bg = "#ededed")
		self.ent_desc_text_chg_test = Text(quizzy.master, font=('Helvetica', 14), width = 20, height = 4, cursor = "dot", wrap = WORD, insertbackground = "blue", padx = 7, pady = 3)
		self.ent_desc_text_chg_test.insert(END, data_recieved[1])
		self.lsframe_chg_test = Frame(quizzy.master)
		self.alloted_users_lab_chg_test = Label(quizzy.master, text="Alloted users: ", font=('Helvetica', 20), bg = "#ededed")
		self.alloted_users_lsbox_chg_test = Listbox(self.lsframe_chg_test, font=('Helvetica', 14), height = 4, width = 20, selectmode = MULTIPLE, selectbackground = "blue", cursor = "dot")
		self.lsframe_chg_test.place(x = 500, y = 310)
		self.alloted_users_lsbox_chg_test.pack(side = "left", fill = "y")
		self.alloted_users_lab_chg_test.place(x = 280, y = 310)
		self.scrollbar_lsbox_chg_test = Scrollbar(self.lsframe_chg_test, orient = "vertical")
		self.scrollbar_lsbox_chg_test.config(command=self.alloted_users_lsbox_chg_test.yview)
		self.scrollbar_lsbox_chg_test.pack(side="right", fill="y")
		self.alloted_users_lsbox_chg_test.config(yscrollcommand=self.scrollbar_lsbox_chg_test.set)
		self.time_limit_lab_chg_test = Label(quizzy.master, text="Time Limit: ", font=('Helvetica', 20), bg = "#ededed")
		self.time_hours_chg_test = Spinbox(quizzy.master, width = 2, from_ = 00, to = 12, format="%02.0f", font=('Helvetica', 20))
		self.time_mins_chg_test = Spinbox(quizzy.master, width = 2, values = ('00', '15', '30', '45'), font=('Helvetica', 20))
		hour = time.strftime("%H", time.gmtime(int(data_recieved[3])))
		minutes = time.strftime("%M", time.gmtime(int(data_recieved[3]))) 
		self.time_hours_chg_test.delete(0, END)
		self.time_mins_chg_test.delete(0, END)
		self.time_hours_chg_test.insert(0, hour)
		self.time_mins_chg_test.insert(0, minutes)
		users = []
		for i in quizzy.db.fetch_users2():
			for a in i:
				users.append(a)
		for i in users:
			self.alloted_users_lsbox_chg_test.insert(END, i)
		selected_users = data_recieved[2].split(",")
		for i in selected_users:
			ind = users.index(i)
			self.alloted_users_lsbox_chg_test.select_set(ind)
		self.change_mng_test = Button(quizzy.master, text="Change", activebackground="green", activeforeground="white", font=('Helvetica', 16), width = 13, bg="green", fg="white", command = self.collect_chg_test_data)
		self.change_mng_test.place(x=480, y=480)
		self.test_name_lab_chg_test.place(x=280, y=150)
		self.ent_test_name_chg_test.place(x=500, y=150)
		self.desc_text_chg_test.place(x=280, y=200)
		self.ent_desc_text_chg_test.place(x=500, y=200)
		self.time_limit_lab_chg_test.place(x = 280, y = 420)
		self.time_hours_chg_test.place(x = 500, y = 420)
		self.time_mins_chg_test.place(x = 550, y = 420)


	#Saving the current user evaluation and moving to the next answer
	def sv_next_ques(self):
		inp_data = []
		inp_data.append(self.eval_data[self.crnt_ques-1][1])
		inp_data.append(self.correct_var.get())
		inp_data.append(self.mark_spin_eval.get())
		self.input_data.append(inp_data)
		self.eval_frame.destroy()
		if self.max_ques == self.crnt_ques + 1:
			self.next_but2.config(text = "Finish")
			self.crnt_ques += 1
			self.display_eval()
		elif self.max_ques == self.crnt_ques:
			quizzy.db.update_eval(self.tst, self.usr, self.input_data)
			self.mng_test()
		else:
			self.crnt_ques += 1
			self.display_eval()


	#Seetting up buttons to evaluate the test
	def evaluate_test(self, user, test):
		self.tst = test
		self.usr = user
		self.eval_data = quizzy.db.fetch_eval_data(test, user)
		self.max_ques = len(self.eval_data)
		quizzy.clear()
		self.next_but2 = Button(quizzy.master, text = "Save and Next", bg = "green", fg = "white", activebackground = "green", activeforeground = "white", font=('Helvetica', 18), width = 13, command = self.sv_next_ques, padx = 10, pady = 10)
		self.next_but2.place(x=200, y=480)
		self.cancel_but = Button(quizzy.master, text = "Cancel", bg = "red", fg = "white", activebackground = "red", activeforeground = "white", font=('Helvetica', 18), width = 13, command = lambda: self.review_test(test), padx = 10, pady = 10)
		self.cancel_but.place(x=500, y=480)
		self.input_data = []
		self.crnt_ques = self.eval_data[0][0]
		self.display_eval()


	#Displays the the user's answer
	def display_eval(self):
		self.crnt_data = self.eval_data[self.crnt_ques-1]
		myframe=Frame(quizzy.master,relief=GROOVE,width=900,height=400,bd=1)
		myframe.place(x=50,y=50)
		canvas=Canvas(myframe, width = 900, height = 400)
		self.eval_frame = Frame(canvas)
		myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
		myscrollbar_x=Scrollbar(myframe,orient="horizontal",command=canvas.xview)
		canvas.configure(yscrollcommand=myscrollbar.set)
		canvas.configure(xscrollcommand=myscrollbar_x.set)	
		myscrollbar.pack(side="right",fill="y")
		myscrollbar_x.pack(side="bottom", fill = "x")
		canvas.pack(side="left", fill="both", expand=True)
		canvas.create_window((0,0),window=self.eval_frame,anchor='nw')
		self.eval_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
		self.eval_ques_lab = Label(self.eval_frame, text = str(self.crnt_ques) + ". " + self.crnt_data[1], font = ("Helvetica", 18))
		self.eval_ques_lab.grid(row = 0, column = 0, columnspan = 4, padx = 10, pady = 20, sticky = "nw")
		type_of_ans = self.crnt_data[4]
		usr_ans = self.crnt_data[2]
		ans = self.crnt_data[3]
		opt = self.crnt_data[5]
		mark = self.crnt_data[6]
		if type_of_ans == "Description" or type_of_ans == "One Word":
			self.user_ans_eval = Label(self.eval_frame, text = "User's answer: " + usr_ans, font = ("Helvetica", 18))
			self.ans_eval = Label(self.eval_frame, text = "Actual answer: " + ans, font = ("Helvetica", 18))
			self.user_ans_eval.grid(row = 1, column = 0, columnspan = 4, padx = 10, pady = 20, sticky = "w")
			self.ans_eval.grid(row = 2, column = 0, columnspan = 4, padx = 10, pady = 20, sticky = "w")
		elif type_of_ans == "MCQ(Single option choose)":
			opt = opt.split(",")
			self.opt_var_eval = StringVar()
			self.user_ans_eval = Label(self.eval_frame, text = "User's answer: ", font = ("Helvetica", 18))
			self.user_ans_eval.grid(row = 1, column = 0, padx = 10)
			self.opt_A_eval = Radiobutton(self.eval_frame, state = "disabled", tristatevalue = "x", variable = self.opt_var_eval, text = "A: " + opt[0], value = "A", padx = 5, pady = 5, font=('Helvetica', 18))
			self.opt_B_eval = Radiobutton(self.eval_frame, state = "disabled", tristatevalue = "x", variable = self.opt_var_eval, text = "B: " + opt[1], value = "B", padx = 5, pady = 5, font=('Helvetica', 18))
			self.opt_C_eval = Radiobutton(self.eval_frame, state = "disabled", tristatevalue = "x", variable = self.opt_var_eval, text = "C: " + opt[2], value = "C", padx = 5, pady = 5, font=('Helvetica', 18))
			self.opt_D_eval = Radiobutton(self.eval_frame, state = "disabled", tristatevalue = "x", variable = self.opt_var_eval, text = "D: " + opt[3], value = "D", padx = 5, pady = 5, font=('Helvetica', 18))
			self.opt_var_eval.set(usr_ans)
			self.opt_A_eval.grid(row = 2, column = 0, sticky = "w", padx = 10, pady = 10)
			self.opt_B_eval.grid(row = 2, column = 2, padx = 10, pady = 10)
			self.opt_C_eval.grid(row = 3, column = 0, sticky = "w", padx = 10, pady = 10)
			self.opt_D_eval.grid(row = 3, column = 2, padx = 10, pady = 10)
			ans_opt = ["A", "B", "C", "D"]
			ind = ans_opt.index(ans)
			self.ans_eval = Label(self.eval_frame, text = "Actual answer:   " + ans + ". " + opt[ind], font = ("Helvetica", 18))
			self.ans_eval.grid(row = 4, column = 0, columnspan = 2, padx = 10, pady = 20, sticky = "w")
		elif type_of_ans == "MCQ(Multiple option choose)":
			opt = opt.split(",")
			usr_ans = usr_ans.split(",")
			ans = ans.split(",")
			self.optA_var_eval = IntVar()
			self.optB_var_eval = IntVar()
			self.optC_var_eval = IntVar()
			self.optD_var_eval = IntVar()
			self.user_ans_eval = Label(self.eval_frame, text = "User's answer: ", font = ("Helvetica", 18))
			self.user_ans_eval.grid(row = 1, column = 0, padx = 10, sticky = "w")
			self.opt_A_eval = Checkbutton(self.eval_frame, variable = self.optA_var_eval, onvalue = 1, offvalue = 0, state = "disabled", text = "A: " + opt[0], padx = 5, pady = 5, font=('Helvetica', 18))
			self.opt_B_eval = Checkbutton(self.eval_frame, variable = self.optB_var_eval, onvalue = 1, offvalue = 0, state = "disabled", text = "B: " + opt[1], padx = 5, pady = 5, font=('Helvetica', 18))
			self.opt_C_eval = Checkbutton(self.eval_frame, variable = self.optC_var_eval, onvalue = 1, offvalue = 0, state = "disabled", text = "C: " + opt[2], padx = 5, pady = 5, font=('Helvetica', 18))
			self.opt_D_eval = Checkbutton(self.eval_frame, variable = self.optD_var_eval, onvalue = 1, offvalue = 0, state = "disabled", text = "D: " + opt[3], padx = 5, pady = 5, font=('Helvetica', 18))
			self.opt_A_eval.grid(row = 2, column = 0, sticky = "w", padx = 10, pady = 10)
			self.opt_B_eval.grid(row = 2, column = 2, padx = 10, pady = 10)
			self.opt_C_eval.grid(row = 3, column = 0, sticky = "w", padx = 10, pady = 10)
			self.opt_D_eval.grid(row = 3, column = 2, padx = 10, pady = 10)
			if "A" in usr_ans:
				self.optA_var_eval.set(1)
			if "B" in usr_ans:
				self.optB_var_eval.set(1)
			if "C" in usr_ans:
				self.optC_var_eval.set(1)
			if "D" in usr_ans:
				self.optD_var_eval.set(1)
			ans_opt = ["A", "B", "C", "D"]
			ans_text = ""
			for i in ans:
				ind = ans_opt.index(i)
				ans_text += i + ". " + opt[ind] + "    "
			self.ans_eval = Label(self.eval_frame, text = "Actual answer:   " + ans_text, font = ("Helvetica", 18))
			self.ans_eval.grid(row = 4, column = 0, columnspan = 3, padx = 10, pady = 20, sticky = "w")
		self.correct_var = IntVar()
		self.correct_rb = Radiobutton(self.eval_frame, variable = self.correct_var, text = "Correct", value = 1, padx = 5, pady = 5, font=('Helvetica', 18), command = lambda: self.change_marks(1, mark))
		self.wrong_rb = Radiobutton(self.eval_frame, variable = self.correct_var, text = "Wrong", value = 0, padx = 5, pady = 5, font=('Helvetica', 18), command = lambda: self.change_marks(0, mark))
		self.correct_rb.grid(row = 5, column = 0, padx = (10,0), pady = 10, sticky = "w")
		self.wrong_rb.grid(row = 5, column = 1, padx = 0, pady = 10, sticky = "w")
		self.mark_lab_eval = Label(self.eval_frame, text = "Marks: ", font = ("Helvetica", 18))
		self.mark_spin_eval = Spinbox(self.eval_frame, from_=0.00, to_ = mark, width = 4, format="%.2f",increment=0.25, font = ("Helvetica", 20))
		self.mark_lab_eval.grid(row = 5, column = 2, pady = 10, padx = (100, 5), sticky = "w")
		self.mark_spin_eval.grid(row = 5, column = 3, pady = 10, padx = 0, sticky = "w")


	#Changes to the appropriate marks while the admin clicks correct or wrong
	def change_marks(self, stat, mark):
		if stat == 1:
			self.mark_spin_eval.delete(0, "end")
			self.mark_spin_eval.insert(0, mark)
		else:
			self.mark_spin_eval.delete(0, "end")
			self.mark_spin_eval.insert(0, "0.00")


	#Showing the status of different users and their marks.
	def review_test(self, test):
		quizzy.clear()
		data = quizzy.db.fetch_usr_status(test)
		self.logout = Button(quizzy.master, text="Log Out", activebackground="red", activeforeground="white", font=('Helvetica', 20), width = 13, bg="red", fg="white", command = self.log_out)
		self.logout.place(x = 750, y = 10)
		self.go_back = Button(quizzy.master, text="Back", activebackground="green", activeforeground="white", font=('Helvetica', 20), width = 13, bg="green", fg="white", command = self.mng_test)
		self.go_back.place(x = 500, y = 10)
		myframe=Frame(quizzy.master,relief=GROOVE,width=600,height=400,bd=1)
		myframe.place(x=10,y=100)
		canvas=Canvas(myframe, width = 800, height = 400)
		self.rev_test_table=Frame(canvas)
		myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
		myscrollbar_x=Scrollbar(myframe,orient="horizontal",command=canvas.xview)
		canvas.configure(yscrollcommand=myscrollbar.set)
		canvas.configure(xscrollcommand=myscrollbar_x.set)	
		myscrollbar.pack(side="right",fill="y")
		myscrollbar_x.pack(side="bottom", fill = "x")
		canvas.pack(side="left", fill="both", expand=True)
		canvas.create_window((0,0),window=self.rev_test_table,anchor='nw')
		self.rev_test_table.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
		self.head1_rev_test = Label(self.rev_test_table, text = "", font=('Helvetica', 20))
		self.head2_rev_test = Label(self.rev_test_table, text = "Users", font=('Helvetica', 20))
		self.head3_rev_test = Label(self.rev_test_table, text = "Status", font=('Helvetica', 20))
		self.head4_rev_test = Label(self.rev_test_table, text = "Marks", font=('Helvetica', 20))
		self.head1_rev_test.grid(row = 0, column = 0, padx=10, pady=10)
		self.head2_rev_test.grid(row = 0, column = 1, padx=10, pady=10)
		self.head3_rev_test.grid(row = 0, column = 2, padx=10, pady=10)
		self.head4_rev_test.grid(row = 0, column = 3, padx=10, pady=10)
		for x, i in enumerate(data):
			status = i[1]
			if status == "finished":
				func = Button(self.rev_test_table, padx=15, pady=10, text="Evaluate", activebackground="green", activeforeground="white", font=('Helvetica', 14), width = 7, bg="green", fg="white", command = lambda y = i[0]: self.evaluate_test(y, test))
				func.grid(row = x+1, column = 0, padx = 10)
			else:
				pass
			Label(self.rev_test_table, text = i[0], padx=10, pady=10, font=('Helvetica', 19)).grid(row = x+1, column = 1, padx = 10)
			Label(self.rev_test_table, text = status, padx=10, pady=10, font=('Helvetica', 19)).grid(row = x+1, column = 2, padx = 10)
			if status == "evaluated":
				Label(self.rev_test_table, text = str(i[2]) + "/" + str(i[3]), padx=10, pady=10, font=('Helvetica', 19)).grid(row = x+1, column = 3, padx = 10)


	#Showing all the tests and listing fuctions which can be applied on them.
	def mng_test(self):
		quizzy.clear()
		self.logout = Button(quizzy.master, text="Log Out", activebackground="red", activeforeground="white", font=('Helvetica', 20), width = 13, bg="red", fg="white", command = self.log_out)
		self.logout.place(x = 750, y = 10)
		self.go_back = Button(quizzy.master, text="Back", activebackground="green", activeforeground="white", font=('Helvetica', 20), width = 13, bg="green", fg="white", command = self.menu_screen)
		self.go_back.place(x = 500, y = 10)
		myframe=Frame(quizzy.master,relief=GROOVE,width=600,height=400,bd=1)
		myframe.place(x=10,y=100)
		canvas=Canvas(myframe, width = 960, height = 400)
		self.mng_test_table=Frame(canvas)
		myscrollbar=Scrollbar(myframe,orient="vertical",command=canvas.yview)
		myscrollbar_x=Scrollbar(myframe,orient="horizontal",command=canvas.xview)
		canvas.configure(yscrollcommand=myscrollbar.set)
		canvas.configure(xscrollcommand=myscrollbar_x.set)	
		myscrollbar.pack(side="right",fill="y")
		myscrollbar_x.pack(side="bottom", fill = "x")
		canvas.pack(side="left", fill="both", expand=True)
		canvas.create_window((0,0),window=self.mng_test_table,anchor='nw')
		self.mng_test_table.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
		self.head1_mng_test = Label(self.mng_test_table, text = "Functions", font=('Helvetica', 20))
		self.head2_mng_test = Label(self.mng_test_table, text = "Test_name", font=('Helvetica', 20))
		self.head3_mng_test = Label(self.mng_test_table, text = "Alloted Users", font=('Helvetica', 20))
		self.head4_mng_test = Label(self.mng_test_table, text = "Time Limit", font=('Helvetica', 20))
		self.head5_mng_test = Label(self.mng_test_table, text = "Mark", font=('Helvetica', 20))
		self.head1_mng_test.grid(row = 0, column = 0, columnspan = 3, padx=10, pady=10)
		self.head2_mng_test.grid(row = 0, column = 3, padx=10, pady=10)
		self.head3_mng_test.grid(row = 0, column = 4, padx=10, pady=10)
		self.head4_mng_test.grid(row = 0, column = 5, padx=10, pady=10)
		self.head5_mng_test.grid(row = 0, column = 6, padx=10, pady=10)
		data_recieved = quizzy.db.fetch_test_data()
		r = 0
		for i in data_recieved:
			r += 1
			c = 2
			for y, x in enumerate(i):
				c += 1
				if y == 2:
					b = str(datetime.timedelta(seconds=int(x)))
					Label(self.mng_test_table, text = b, padx=10, pady=10, font=('Helvetica', 19), fg = "#4d4d4c").grid(row = r, column = c)
				else:
					Label(self.mng_test_table, text = x, padx=10, pady=10, font=('Helvetica', 19), fg = "#4d4d4c").grid(row = r, column = c)
			review = Button(self.mng_test_table, padx=15, pady=10, text="Review", activebackground="green", activeforeground="white", font=('Helvetica', 14), width = 7, bg="green", fg="white", command = lambda x = i[0]: self.review_test(x))
			review.grid(row = r, column = 0)
			remove = Button(self.mng_test_table, padx=15, pady=10, text="Remove", activebackground="red", activeforeground="white", font=('Helvetica', 14), width = 7, bg="red", fg="white", command = lambda x = i[0]: self.rm_test(x))
			remove.grid(row = r, column = 1)
			change = Button(self.mng_test_table, padx=15, pady=10, text="Change", activebackground="blue", activeforeground="white", font=('Helvetica', 14), width = 7, bg="blue", fg="white", command = lambda x = i[0]: self.change_test_data(x))
			change.grid(row = r, column = 2)


	#Shows the appropriate field while the admin switches between different types of questions.
	def show_options(self):
		opt = self.type_ans_rb_var.get()
		for child in self.opt_frame.winfo_children():
			child.destroy()
		self.opt_frame.destroy()
		if opt == 1:
			self.opt_frame = Frame(self.question_frame)
			self.opt_frame.grid(row = 3, column = 2, rowspan = 2, columnspan = 4)
			self.answer_lab.grid(row = 3, column = 0, columnspan = 2)
			self.optA_lab = Label(self.opt_frame, text="A: ", padx = 5, pady = 5, font=('Helvetica', 20), bg = "#ededed")
			self.optA_ent = Entry(self.opt_frame, font=('Helvetica', 16), width = 20)
			self.correct_ans = IntVar()
			self.correct_ans.set(1)
			self.optA_correct = Radiobutton(self.opt_frame, variable = self.correct_ans, value = 1, text = "")
			self.optA_lab.grid(row = 0, column = 0)
			self.optA_correct.grid(row = 0, column = 1)
			self.optA_ent.grid(row = 0, column = 2)
			self.optB_lab = Label(self.opt_frame, text="B: ", padx = 5, pady = 5, font=('Helvetica', 20), bg = "#ededed")
			self.optB_ent = Entry(self.opt_frame, font=('Helvetica', 16), width = 20)
			self.optB_correct = Radiobutton(self.opt_frame, variable = self.correct_ans, value = 2, text = "")
			self.optB_lab.grid(row = 0, column = 3)
			self.optB_correct.grid(row = 0, column = 4)
			self.optB_ent.grid(row = 0, column = 5)
			self.optC_lab = Label(self.opt_frame, text="C: ", padx = 5, pady = 5, font=('Helvetica', 20), bg = "#ededed")
			self.optC_ent = Entry(self.opt_frame, font=('Helvetica', 16), width = 20)
			self.optC_correct = Radiobutton(self.opt_frame, variable = self.correct_ans, value = 3, text = "")
			self.optC_lab.grid(row = 1, column = 0)
			self.optC_correct.grid(row = 1, column = 1)
			self.optC_ent.grid(row = 1, column = 2)
			self.optD_lab = Label(self.opt_frame, text="D: ", padx = 5, pady = 5, font=('Helvetica', 20), bg = "#ededed")
			self.optD_ent = Entry(self.opt_frame, font=('Helvetica', 16), width = 20)
			self.optD_correct = Radiobutton(self.opt_frame, variable = self.correct_ans, value = 4, text = "")
			self.optD_lab.grid(row = 1, column = 3)
			self.optD_correct.grid(row = 1, column = 4)
			self.optD_ent.grid(row = 1, column = 5)
		elif opt == 2:
			self.opt_frame = Frame(self.question_frame)
			self.opt_frame.grid(row = 3, column = 2, rowspan = 2, columnspan = 4)
			self.answer_lab.grid(row = 3, column = 0, columnspan = 2)
			self.optA_lab = Label(self.opt_frame, text="A: ", padx = 5, pady = 5, font=('Helvetica', 20), bg = "#ededed")
			self.optA_ent = Entry(self.opt_frame, font=('Helvetica', 16), width = 20)
			self.correct_ans1 = IntVar()
			self.correct_ans2 = IntVar()
			self.correct_ans3 = IntVar()
			self.correct_ans4 = IntVar()
			self.optA_correct = Checkbutton(self.opt_frame, variable = self.correct_ans1, onvalue = 1, offvalue = 0, text = "")
			self.optA_lab.grid(row = 0, column = 0)
			self.optA_correct.grid(row = 0, column = 1)
			self.optA_ent.grid(row = 0, column = 2)
			self.optB_lab = Label(self.opt_frame, text="B: ", padx = 5, pady = 5, font=('Helvetica', 20), bg = "#ededed")
			self.optB_ent = Entry(self.opt_frame, font=('Helvetica', 16), width = 20)
			self.optB_correct = Checkbutton(self.opt_frame, variable = self.correct_ans2, onvalue = 1, offvalue = 0, text = "")
			self.optB_lab.grid(row = 0, column = 3)
			self.optB_correct.grid(row = 0, column = 4)
			self.optB_ent.grid(row = 0, column = 5)
			self.optC_lab = Label(self.opt_frame, text="C: ", padx = 5, pady = 5, font=('Helvetica', 20), bg = "#ededed")
			self.optC_ent = Entry(self.opt_frame, font=('Helvetica', 16), width = 20)
			self.optC_correct = Checkbutton(self.opt_frame, variable = self.correct_ans3, onvalue = 1, offvalue = 0, text = "")
			self.optC_lab.grid(row = 1, column = 0)
			self.optC_correct.grid(row = 1, column = 1)
			self.optC_ent.grid(row = 1, column = 2)
			self.optD_lab = Label(self.opt_frame, text="D: ", padx = 5, pady = 5, font=('Helvetica', 20), bg = "#ededed")
			self.optD_ent = Entry(self.opt_frame, font=('Helvetica', 16), width = 20)
			self.optD_correct = Checkbutton(self.opt_frame, variable = self.correct_ans4, onvalue = 1, offvalue = 0, text = "")
			self.optD_lab.grid(row = 1, column = 3)
			self.optD_correct.grid(row = 1, column = 4)
			self.optD_ent.grid(row = 1, column = 5)
		elif opt == 3:
			self.opt_frame = Frame(self.question_frame)
			self.opt_frame.grid(row = 3, column = 2, rowspan = 2, columnspan = 4)
			self.description_text = Text(self.opt_frame, font=('Helvetica', 16), width = 50, height = 3, cursor = "dot", wrap = WORD, insertbackground = "blue", padx = 10, pady = 10)
			self.description_text.pack()
		elif opt == 4:
			self.opt_frame = Frame(self.question_frame)
			self.opt_frame.grid(row = 3, column = 2, rowspan = 2, columnspan = 4)
			self.one_word_ent = Entry(self.opt_frame, font=('Helvetica', 16), width = 20)
			self.one_word_ent.pack()


	#Asking for confirmation if the admin wants to go back while creating a new test
	def go_back_ques_mng(self):
		ask = messagebox.askyesno("Go back?", "Are you sure that you want to go back? Note that your changes won't be saved unless you click the finish button and then save.")
		if ask == 1:
			self.data_list = []
			self.question = []
			self.questions = []
			self.create_test()


	#Collecting the question data and saving it
	def collect_ques_data(self):
		self.question = []
		self.ques_order += 1
		self.question.append(self.ques_order)
		ques = self.question_ent.get(1.0, END).strip()
		if ques == "":
			messagebox.showwarning("Check your Input", "Please provide the question before you proceed.")
			self.question_manager()
		else:
			self.question.append(ques)
		type_ans = self.type_ans_rb_var.get()
		if type_ans == 1:
			type_ans = "MCQ(Single option choose)"
			self.question.append(type_ans)
			opt = []
			opt.append(self.optA_ent.get())
			opt.append(self.optB_ent.get())
			opt.append(self.optC_ent.get())
			opt.append(self.optD_ent.get())
			for i in opt:
				if i == "":
					messagebox.showwarning("Check your Input", "Please provide the options before you proceed.")
					return
			self.question.append(opt)
			opt_ans = self.correct_ans.get()
			if opt_ans == 1:
				opt_ans = "A"
			elif opt_ans == 2:
				opt_ans = "B"
			elif opt_ans == 3:
				opt_ans = "C"
			elif opt_ans == 4:
				opt_ans = "D"
			self.question.append(opt_ans)
		elif type_ans == 2:
			type_ans = "MCQ(Multiple option choose)"
			self.question.append(type_ans)
			opt = []
			opt.append(self.optA_ent.get())
			opt.append(self.optB_ent.get())
			opt.append(self.optC_ent.get())
			opt.append(self.optD_ent.get())
			for i in opt:
				if i == "":
					messagebox.showwarning("Check your Input", "Please provide the options before you proceed.")
					return
			self.question.append(opt)
			opt_ans_list = []
			opt_list = [self.correct_ans1.get(), self.correct_ans2.get(), self.correct_ans3.get(), self.correct_ans4.get()]
			options = ["A", "B", "C", "D"]
			for x, y in enumerate(opt_list):
				if y == 1:
					opt_ans_list.append(options[x])
			self.question.append(opt_ans_list)
		elif type_ans == 3:
			type_ans = "Description"
			self.question.append(type_ans)
			ans = self.description_text.get(1.0, END).strip()
			if ans == "":
				messagebox.showwarning("Check your Input", "Please provide the answer before you proceed.")
				return
			else:
				self.question.append(ans)
		elif type_ans == 4:
			type_ans ="One Word"
			self.question.append(type_ans)
			ans = self.one_word_ent.get()
			if ans == "":
				messagebox.showwarning("Check your Input", "Please provide the answer before you proceed.")
				return
			else:
				self.question.append(ans)
		self.question.append(float(self.marks_spin.get()))
		self.questions.append(self.question)
		self.question_manager()


	#Removing the question
	def remove_rev(self, elem):
		for x, y in enumerate(self.questions):
			if y[0] == elem:
				self.questions.pop(x)
		self.question_reviewing()


	#Checking if the admin creates a test with no questions
	def question_check(self):
		self.collect_ques_data()
		if len(self.questions) == 0:
			messagebox.showwarning("No questions", "You can't create a test without no questions.")
			self.question_manager()
			return
		else:
			self.question_reviewing()


	#Saving the test in the database
	def save_test(self):
		self.data_list.append(self.ask_var.get())
		self.data_list.append(self.shuffle_var.get())
		total_marks = 0
		for i, x in zip(self.questions, self.order_list):
			total_marks += i[-1]
			i[0] = x.get()
		self.data_list.append(total_marks)
		for i in self.questions:
			if i[2][:3] == "MCQ":
				i[3] = ",".join(i[3])
				if i[2] == "MCQ(Multiple option choose)":
					i[4] = ",".join(i[4])
		self.data_list[2] = ",".join(self.data_list[2])
		a = quizzy.db.crt_test(self.data_list, self.questions, self.users)
		if a == "ERROR":
			self.question = []
			self.questions = []
			self.data_list = []
			self.menu_screen()
			messagebox.showerror("ERROR!", "An ERROR occured while save this test. Please note that the test name does not contain words such as CREATE, class etc.")
		self.question = []
		self.questions = []
		self.data_list = []
		self.menu_screen()


	#Reviewing the questions one final time before save all of it
	def question_reviewing(self):
		quizzy.clear()
		myframe_rev=Frame(quizzy.master,relief=GROOVE,width=600,height=400,bd=1)
		myframe_rev.place(x=20,y=20)
		canvas=Canvas(myframe_rev, width = 750, height = 400)
		self.table_rev=Frame(canvas)
		myscrollbar=Scrollbar(myframe_rev,orient="vertical",command=canvas.yview)
		canvas.configure(yscrollcommand=myscrollbar.set)	
		myscrollbar.pack(side="right",fill="y")
		canvas.pack(side="left", fill="both", expand=True)
		canvas.create_window((0,0),window=self.table_rev,anchor='nw')
		self.table_rev.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
		self.head_rev1 = Label(self.table_rev, text="Order: ", font=('Helvetica', 20))
		self.head_rev2 = Label(self.table_rev, text="Question: ", font=('Helvetica', 20))
		self.head_rev3 = Label(self.table_rev, text="Type: ", font=('Helvetica', 20))
		self.head_rev1.grid(row = 0, column = 0, sticky = W, padx = 10, pady = 10)
		self.head_rev2.grid(row = 0, column = 1, columnspan=2, sticky = W, padx = 10, pady = 10)
		self.head_rev3.grid(row = 0, column = 3, sticky = W, padx = 10, pady = 10)
		count = 0
		col = 0
		self.order_list = []
		for x in self.questions:
			count += 1
			lab = Spinbox(self.table_rev, width = 3, from_ = 1, to = len(self.questions), font=('Helvetica', 20))
			lab.delete(0, "end")
			lab.insert(0, count)
			lab.grid(row=count, column = col, sticky = W, padx = 10, pady = 10)
			self.order_list.append(lab)
			q = x[1]
			ques = Label(self.table_rev, text = q[:10] + "....", font=('Helvetica', 20)).grid(row=count, column = col+1, sticky = W, padx = 10, pady = 10)
			t = x[2]
			typr = Label(self.table_rev, text = t[:6] + "...", font=('Helvetica', 20)).grid(row=count, column = col+3, sticky = W, padx = 10, pady = 10)
			hi = Button(self.table_rev, padx=15, pady=10, text="Remove", activebackground="red", activeforeground="white", font=('Helvetica', 14), width = 7, bg="red", fg="white", command = lambda elem = x[0]: self.remove_rev(elem))
			hi.grid(row = count, column = 4, sticky = W, padx = 10, pady = 10)
		self.ask_auto_eval = Label(quizzy.master, text="Auto Evaluate: ", padx = 10, pady = 10, font=('Helvetica', 20), bg = "#ededed")
		self.ask_var = IntVar()
		self.ask_var.set(1)
		self.ask_yes = Radiobutton(quizzy.master, variable = self.ask_var, value = 1, text = "Yes", padx = 10, pady = 10, font=('Helvetica', 20))
		self.ask_no = Radiobutton(quizzy.master, variable = self.ask_var, value = 0, text = "No", padx = 10, pady = 10, font=('Helvetica', 20))
		self.shuffle_var = IntVar()
		self.shuffle_chk_btn = Checkbutton(quizzy.master, variable = self.shuffle_var, onvalue = 1, offvalue = 0, text = "Shuffle", font=('Helvetica', 20), padx = 10, pady = 10)
		self.ask_auto_eval.place(x = 25, y = 430)
		self.ask_yes.place(x = 300, y = 430)
		self.ask_no.place(x = 400, y = 430)
		self.shuffle_chk_btn.place(x = 650, y = 430)
		self.add_more_ques = Button(quizzy.master, text="Add more Questions", activebackground="blue", activeforeground="white", font=('Helvetica', 16), width = 20, bg="blue", fg="white", command = self.question_manager)
		self.save_btn = Button(quizzy.master, text="Save", activebackground="green", activeforeground="white", font=('Helvetica', 16), width = 13, bg="green", fg="white", command = self.save_test)
		self.add_more_ques.place(x = 700, y = 500)
		self.save_btn.place(x = 300, y = 500)


	#Seetting up widgets to enter question data
	def question_manager(self):
		quizzy.clear()
		self.go_back = Button(quizzy.master, text="Back", activebackground="green", activeforeground="white", font=('Helvetica', 20), width = 10, bg="green", fg="white", command = self.go_back_ques_mng)
		self.go_back.place(x = 800, y = 10)
		self.question_frame = Frame(quizzy.master, bd = 0, padx = 10, pady = 10, highlightthickness= 5, highlightcolor = "#000066", highlightbackground = "#000066")
		self.question_frame.place(x = 30, y = 80)		
		self.question_lab = Label(self.question_frame, text="Question: ", padx = 10, pady = 10, font=('Helvetica', 20), bg = "#ededed")
		self.question_ent = Text(self.question_frame, font=('Helvetica', 16), width = 50, height = 2, cursor = "dot", wrap = WORD, insertbackground = "blue", padx = 10, pady = 10)
		self.type_ans_lab = Label(self.question_frame, text="Type of Answer: ", padx = 10, pady = 10, font=('Helvetica', 20), bg = "#ededed")
		self.type_ans_rb_var = IntVar(quizzy.master)
		self.type_ans_rb_var.set(1)
		self.answer_lab = Label(self.question_frame, text="Answer or Options: ", padx = 10, pady = 10, font=('Helvetica', 20), bg = "#ededed")
		self.opt_frame = Frame(self.question_frame)
		self.opt_frame.grid(row = 3, column = 2, rowspan = 2, columnspan = 4)
		self.answer_lab.grid(row = 3, column = 0, columnspan = 2)
		self.optA_lab = Label(self.opt_frame, text="A: ", padx = 5, pady = 5, font=('Helvetica', 20), bg = "#ededed")
		self.optA_ent = Entry(self.opt_frame, font=('Helvetica', 16), width = 20)
		self.correct_ans = IntVar()
		self.correct_ans.set(1)
		self.optA_correct = Radiobutton(self.opt_frame, variable = self.correct_ans, value = 1, text = "")
		self.optA_lab.grid(row = 0, column = 0)
		self.optA_correct.grid(row = 0, column = 1)
		self.optA_ent.grid(row = 0, column = 2)
		self.optB_lab = Label(self.opt_frame, text="B: ", padx = 5, pady = 5, font=('Helvetica', 20), bg = "#ededed")
		self.optB_ent = Entry(self.opt_frame, font=('Helvetica', 16), width = 20)
		self.optB_correct = Radiobutton(self.opt_frame, variable = self.correct_ans, value = 2, text = "")
		self.optB_lab.grid(row = 0, column = 3)
		self.optB_correct.grid(row = 0, column = 4)
		self.optB_ent.grid(row = 0, column = 5)
		self.optC_lab = Label(self.opt_frame, text="C: ", padx = 5, pady = 5, font=('Helvetica', 20), bg = "#ededed")
		self.optC_ent = Entry(self.opt_frame, font=('Helvetica', 16), width = 20)
		self.optC_correct = Radiobutton(self.opt_frame, variable = self.correct_ans, value = 3, text = "")
		self.optC_lab.grid(row = 1, column = 0)
		self.optC_correct.grid(row = 1, column = 1)
		self.optC_ent.grid(row = 1, column = 2)
		self.optD_lab = Label(self.opt_frame, text="D: ", padx = 5, pady = 5, font=('Helvetica', 20), bg = "#ededed")
		self.optD_ent = Entry(self.opt_frame, font=('Helvetica', 16), width = 20)
		self.optD_correct = Radiobutton(self.opt_frame, variable = self.correct_ans, value = 4, text = "")
		self.optD_lab.grid(row = 1, column = 3)
		self.optD_correct.grid(row = 1, column = 4)
		self.optD_ent.grid(row = 1, column = 5)
		self.mcq_1 = Radiobutton(self.question_frame, variable = self.type_ans_rb_var, value = 1, text = "MCQ(One option)", padx = 5, pady = 5, font=('Helvetica', 20), command=self.show_options)
		self.mcq_2 = Radiobutton(self.question_frame, variable = self.type_ans_rb_var, value = 2, text = "MCQ(More than one option)", padx = 5, pady = 5, font=('Helvetica', 20), command=self.show_options)
		self.desc = Radiobutton(self.question_frame, variable = self.type_ans_rb_var, value = 3, text = "Descriptive", padx = 5, pady = 5, font=('Helvetica', 20), command=self.show_options)
		self.one_word = Radiobutton(self.question_frame, variable = self.type_ans_rb_var, value = 4, text = "One Word", padx = 5, pady = 5, font=('Helvetica', 20), command=self.show_options)
		self.crt_another_question = Button(self.question_frame, text="Create Another Question", activebackground="blue", activeforeground="white", font=('Helvetica', 16), width = 20, bg="blue", fg="white", command = self.collect_ques_data)
		self.crt_another_question.grid(row = 6, column = 2, columnspan = 2, padx=10, pady = 10)
		self.finish_btn = Button(self.question_frame, text="Finish", activebackground="#ff8000", activeforeground="white", font=('Helvetica', 16), width = 13, bg="#ff8000", fg="white", command = self.question_check)
		self.finish_btn.grid(row = 6, column = 4, columnspan = 2, padx=10, pady = 10)
		self.marks_label = Label(self.question_frame, text="Marks: ", padx = 10, pady = 10, font=('Helvetica', 20), bg = "#ededed")
		self.marks_spin = Spinbox(self.question_frame, from_=0.25, to_ = 100, width = 4, format="%.2f",increment=0.25, font = ("Helvetica", 20))
		self.marks_label.grid(row = 5, column = 0, columnspan = 2)
		self.marks_spin.grid(row = 5, column = 2, columnspan = 2)
		self.question_lab.grid(row = 0, column = 0, columnspan=2)
		self.question_ent.grid(row=0, column=2, columnspan = 4)
		self.type_ans_lab.grid(row = 1, column = 0, columnspan = 2)
		self.mcq_1.grid(row = 1, column = 2, columnspan = 2)
		self.mcq_2.grid(row = 1, column = 4, columnspan = 2)
		self.desc.grid(row = 2, column = 2, columnspan = 2)
		self.one_word.grid(row = 2, column = 4, columnspan = 2)


	#Collecting test data
	def collect_test_data(self):
		return_to = False
		self.data_list = []
		a = self.ent_test_name.get()
		if a == "":
			messagebox.showwarning("No Test Name", "Please provide a name to the test.")
			return_to = True
		else:
			self.data_list.append(a)
		self.data_list.append(self.ent_desc_text.get(1.0, END).strip())
		item_num = self.alloted_users_lsbox.curselection()
		self.users = []
		for i in item_num:
			self.users.append(self.alloted_users_lsbox.get(i))
		self.data_list.append(self.users)
		x = self.time_hours.get()
		y = self.time_mins.get()
		x = int(x)
		y = int(y)
		if x == 0 and y == 0:
			messagebox.showwarning("Time limit not usable", "Please set the time limit to atleast 15 minutes.")
			return_to = True
		else:
			t = (x*60*60) + (y*60)
			self.data_list.append(t)
		if return_to:
			self.create_test()
		else:
			self.ques_order = 0
			self.question_manager()


	#Setting up widgets to enter test data
	def create_test(self):
		quizzy.clear()
		self.questions = []
		self.logout = Button(quizzy.master, text="Log Out", activebackground="red", activeforeground="white", font=('Helvetica', 20), width = 10, bg="red", fg="white", command = self.log_out)
		self.logout.place(x = 800, y = 10)
		self.go_back = Button(quizzy.master, text="Back", activebackground="green", activeforeground="white", font=('Helvetica', 20), width = 10, bg="green", fg="white", command = self.menu_screen)
		self.go_back.place(x = 600, y = 10)
		self.title_crt_new_test = Label(quizzy.master, text = "Create Test", fg = "blue", font=('Helvetica', 40), bg = "#ededed")
		self.title_crt_new_test.place(x=350, y=70)
		self.test_name_lab = Label(quizzy.master, text="Test Name: ", font=('Helvetica', 20), bg = "#ededed")
		self.ent_test_name = Entry(quizzy.master, font=('Helvetica', 20), width = 15)
		self.desc_text = Label(quizzy.master, text="Test Description: ", font=('Helvetica', 20), bg = "#ededed")
		self.ent_desc_text = Text(quizzy.master, font=('Helvetica', 14), width = 20, height = 4, cursor = "dot", wrap = WORD, insertbackground = "blue", padx = 7, pady = 3)
		self.lsframe = Frame(quizzy.master)
		self.alloted_users_lab = Label(quizzy.master, text="Alloted users: ", font=('Helvetica', 20), bg = "#ededed")
		self.alloted_users_lsbox = Listbox(self.lsframe, font=('Helvetica', 14), height = 4, width = 20, selectmode = MULTIPLE, selectbackground = "blue", cursor = "dot")
		self.lsframe.place(x = 500, y = 310)
		self.alloted_users_lsbox.pack(side = "left", fill = "y")
		self.alloted_users_lab.place(x = 280, y = 310)
		self.scrollbar_lsbox = Scrollbar(self.lsframe, orient = "vertical")
		self.scrollbar_lsbox.config(command=self.alloted_users_lsbox.yview)
		self.scrollbar_lsbox.pack(side="right", fill="y")
		self.alloted_users_lsbox.config(yscrollcommand=self.scrollbar_lsbox.set)
		self.time_limit_lab = Label(quizzy.master, text="Time Limit: ", font=('Helvetica', 20), bg = "#ededed")
		self.time_hours = Spinbox(quizzy.master, width = 2, from_ = 00, to = 12, format="%02.0f", font=('Helvetica', 20))
		self.time_mins = Spinbox(quizzy.master, width = 2, values = ('00', '15', '30', '45'), font=('Helvetica', 20))
		self.add_questions_btn = Button(quizzy.master, text="Add Questions", activebackground="green", activeforeground="white", font=('Helvetica', 16), width = 13, bg="green", fg="white", command = self.collect_test_data)
		users = []
		for i in quizzy.db.fetch_users2():
			for a in i:
				users.append(a)
		for i in users:
			self.alloted_users_lsbox.insert(END, i)
		self.test_name_lab.place(x=280, y=150)
		self.ent_test_name.place(x=500, y=150)
		self.desc_text.place(x=280, y=200)
		self.ent_desc_text.place(x=500, y=200)
		self.time_limit_lab.place(x = 280, y = 420)
		self.time_hours.place(x = 500, y = 420)
		self.time_mins.place(x = 550, y = 420)
		self.add_questions_btn.place(x=480, y=480)


	#Setting up the menuscreen for the admin
	def menu_screen(self):
		quizzy.clear()
		self.user_shown = Label(quizzy.master, padx=10, pady=10, text = "Current User: " + quizzy.current_user, font=('Helvetica', 20))
		self.user_shown.place(x = 1, y = 1)
		self.logout = Button(quizzy.master, text="Log Out", activebackground="red", activeforeground="white", font=('Helvetica', 20), width = 13, bg="red", fg="white", command = self.log_out)
		self.mng_usr_btn = Button(quizzy.master, text="Manage Users", activebackground="green", activeforeground="white", font=('Helvetica', 20), width = 15, bg="green", fg="white", command = self.mng_user)
		self.mng_test_btn = Button(quizzy.master, text="Manage Tests", activebackground="green", activeforeground="white", font=('Helvetica', 20), width = 15, bg="green", fg="white", command = self.mng_test)
		self.crt_test_btn = Button(quizzy.master, text="Create Test", activebackground="green", activeforeground="white", font=('Helvetica', 20), width = 15, bg="green", fg="white", command = self.create_test)
		self.logout.place(x = 750, y = 10)
		self.mng_usr_btn.place(x=100, y = 250)
		self.mng_test_btn.place(x=380, y = 250)
		self.crt_test_btn.place(x=660, y = 250)


#Creating the App Class
class App():
	def __init__(self, master, db):
		self.master = master
		self.db = db
		master.config(bg="#ededed")
		master.geometry('1000x550+100+100')
		master.maxsize(1000, 550)
		master.minsize(1000, 550)
		master.title("Quizzy")
		master.iconbitmap("Files/app.ico")
		master.protocol("WM_DELETE_WINDOW", self.exit)


	#Clearing the widgets from the Tkinter window.
	def clear(self):
		lis = self.master.winfo_children()
		for i in lis:
			i.destroy()


	#Closing the connection to the database and closing the application
	def exit(self):
		ask = messagebox.askyesno("Exit", "Are you sure that you want to exit?")
		if ask == 1:
			self.db.close()
			self.master.destroy()


	#Checking if the login was valid
	def check_login(self):
		check = self.db.login_check(self.ent_usr_name.get(), self.ent_pwd.get())
		if check != None:
			if check[2] == "admin":
				messagebox.showinfo("Successfully Loged In", "You have successfully loged in as "+"ADMIN.")
				self.current_user = check[0]
				adm = Admin(check[0], check[1])
			elif check[2] == "quiztaker":
				messagebox.showinfo("Successfully Loged In", "You have successfully loged in as a "+"QUIZTAKER.")
				self.current_user = check[0]
				qzt = Quiztaker(check[0])
		else:
			ask = messagebox.askretrycancel("Login Unsuccessful", "Please check if you had entered the correct user name or password.")
			if ask == True:
				self.ent_pwd.delete(0, 'end')
				self.ent_usr_name.delete(0, 'end')
			else:
				self.exit()


	#Creating widgets for the login screen
	def check_user(self):
		self.title_chk_usr = Label(self.master, text = "Sign In", fg = "red", font=('Helvetica', 46), bg = "#ededed")
		self.usr_name = Label(self.master, text="User Name: ", font=('Helvetica', 20), bg = "#ededed")
		self.ent_usr_name = Entry(self.master, font=('Helvetica', 20), width = 15)
		self.pwd = Label(self.master, text="Password: ", font=('Helvetica', 20), bg = "#ededed")
		self.ent_pwd = Entry(self.master, font=('Helvetica', 20), width = 15, show="*")
		self.submit = Button(self.master, text="Sign In", activebackground="green", activeforeground="white", font=('Helvetica', 16), width = 10, bg="green", fg="white", command=self.check_login)
		self.title_chk_usr.place(x=430, y=80)
		self.usr_name.place(x=300, y=180)
		self.ent_usr_name.place(x=500, y=180)
		self.pwd.place(x=300, y=250)
		self.ent_pwd.place(x=500, y=250)
		self.submit.place(x=480, y=320)


	#Running the application and the mainloop
	def run(self):
		self.check_user()
		self.master.mainloop()


#Creating a window for Tkinter
win = Tk()
#Giving the class "DB_manager" to the instance dbm
dbm = database.DB_manager()
#Giving the class "App" to the instance quizzy
quizzy = App(win, dbm)
#Running the quizzy program
quizzy.run()
