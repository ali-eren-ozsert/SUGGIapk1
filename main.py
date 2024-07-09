from kivymd.app import MDApp
import random
import csv
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.floatlayout import FloatLayout
from kivy.clock import Clock
from functools import partial

global verb_num
global verb
global question_caunt
global time_var
global name
global score_count
name = ""
question_caunt = 0
stable = "Question "
time_var = 0

score_count = 0

irg_list = []

with open('irregular_verbs.csv', 'r') as irg_csv:
    irg_reader = csv.reader(irg_csv, delimiter=';')
    
    for verbs in irg_reader:
        irg_list.append(verbs)

def multiple_answers(object):
    list = object.split("/")
    return list

def random_verb(self):
    x = random.randint(0, 96)
    return self[x]

def save_score(x, y):
    with open("high_scores.csv", "a", newline = "" ) as high_scores_file:
        high_scores_writer = csv.writer(high_scores_file, delimiter = ";")
        list = [x, y]
        high_scores_writer.writerow(list)

def read_score():
    with open("high_scores.csv", "r") as high_scores_file_2:
        high_scores_reader = csv.reader(high_scores_file_2, delimiter = ";")
        list = []
        for line in high_scores_reader:
            list.append(line)
        return list

def get_top_3(list):
    global count_var
    list_2 = []
    list_3 = []
    best = []
    count_var = 0
    for k in list:
        list_2.append(k[1])

    while count_var < 3:
        for j in list:
            if j[1] == max(list_2):
                best.append(j)
                list.remove(j)
                break
            else:
                continue
        if len(list) == 1:
            count_var += 3
        elif len(list) == 2:
            count_var += 2
        elif len(list) >= 3:
            count_var += 1

    return best

class StartUp(Screen):
    score = ObjectProperty(None)
    high_score = ObjectProperty(None)
    name_input = ObjectProperty(None)

    def start_game(self):
        global name
        if self.name_input.text == '':
            name = "NoName"
        else:
            name = self.name_input.text
        sm.current = "main"

class MainWindow(Screen):
    answer_input = ObjectProperty(None)
    question_num = ObjectProperty(None)
    question = ObjectProperty(None)
    time_counter = ObjectProperty(None)
    answer_button = ObjectProperty(None)
    
    def on_enter(self, *args):
        global time_var
        time_var = 0
        self.time_counter.text = f"Time: {str(60)}"
        self.interval_countdown = Clock.schedule_interval(self.time_countdown,1)
        Clock.schedule_once(self.change_text,0)


    def test_funct(self, c_or_w, dt):
        if c_or_w == "Correct":
            self.question.text = "Correct!"
           
        elif c_or_w == "Wrong":
            self.question.text = "Wrong the correct answer is " + verb[verb_num]

    def time_countdown(self, dt):
        global time_var
        global name
        time_var += 1 
        self.time_counter.text = f"Time: {str(60 - time_var)}"
        if time_var == 60:
            save_score(name,str(score_count))
            sm.transition.direction = "left"
            sm.current = "results"
            self.stop_interval(2)


    def stop_interval(self,x,*args):
        if x == 1:
            self.function_interval.cancel()
            self.answer_button.disabled = False
        if x == 2:
            self.interval_countdown.cancel()

    def display_answer(self,x):
        self.answer_button.disabled = True
        self.function_interval = Clock.schedule_interval(partial(self.test_funct, x), 0)
        Clock.schedule_once(partial(self.stop_interval, 1), 2)

    def change_text(self, dt):
        global verb_num
        global verb
        verb_num = random.randint(1,2)
        verb = random_verb(irg_list)
        self.answer_input.text = ''
        self.score.text = f"Score: {score_count}"
        

        if verb_num == 1:
            self.question.text =  "What is the past simple of the " + verb[0]

        elif verb_num == 2:
            self.question.text =  "What is the past perfect of the " + verb[0]


    def check_answer(self):
        global question_caunt
        global score_count 
        answer = self.answer_input.text
        if verb_num == 1:
            if answer == verb[verb_num] or answer in multiple_answers(verb[verb_num]):                
                self.display_answer("Correct")
                score_count += 1
            else:
                self.display_answer("Wrong")

        elif verb_num == 2:
            if answer == verb[verb_num] or answer in multiple_answers(verb[verb_num]):
                self.display_answer("Correct")
                score_count += 1
            else:
                self.display_answer("Wrong")
                

        Clock.schedule_once(self.change_text, 2)

        question_caunt += 1
        self.question_num.text = stable + str(question_caunt)

class ResultWindow(Screen):

    score = ObjectProperty(None)
    high_score = ObjectProperty(None)

    def on_enter(self, *args):
        global high_score_list
        global top_3
        self.score.text = f"Your Score: {score_count}"
        high_score_list = read_score()
        top_3 = get_top_3(high_score_list) 
        self.high_score.text = f'''High Score: {top_3[0][0]} - {top_3[0][1]}
                      {top_3[1][0]} - {top_3[1][1]}
                      {top_3[2][0]} - {top_3[2][1]}'''

                                                                

class WindowManager(ScreenManager):
    pass

kv = Builder.load_file("my.kv")

sm = WindowManager()

screens = [StartUp(name = "startup"),MainWindow(name="main"), ResultWindow(name="results")]
for screen in screens:
    sm.add_widget(screen)

class MyMainApp(App):
    def build(self):
        return sm
          
if __name__ == "__main__":
    MyMainApp().run()
