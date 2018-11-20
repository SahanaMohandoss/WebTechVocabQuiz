from flask import Flask, redirect, render_template, request, make_response
import time
from GenerateQuestion import *


class Word(object):

    MAX_SCORE = 4
    MIN_SCORE = -4

    def __init__(self, word, definition):

        self.word = word
        self.definition = definition
        self.score = 0

    def set_score(self, score):
        self.score = int(score)

    def get_score_str(self):
        return "%s\t%s\n" % (self.word, self.score)

    def is_learned(self):
        return self.score == Word.MAX_SCORE

    def update_correct(self):
        self.score = min(self.score + 1, Word.MAX_SCORE)

    def update_wrong(self):
        self.score = max(self.score - 1, Word.MIN_SCORE)


class Card(object):
    """[summary]
    This class represents a vocabulary card

    Arguments:
        object {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """

    def __init__(self, front = "", back = ""):
        self.__front = front
        self.__back = back
        self.__timestamp = time.time()
        self.__known = False
    def get_front(self):
        return self.__front
    def get_back(self):
        return self.__back
    def set_front(self, front):
        self.__front = front
    def set_back(self, back):
        self.__back = back
    def reset(self):
        self.__timestamp = time.time()
    def get_timestamp(self):
        return self.__timestamp
    def set_timestamp(self, value):
        self.__timestamp = value
    def set_known(self, flag):
        self.__known = flag
    def get_known(self):
        return self.__known

class Compartment(object):
    def __init__(self, i):
        self.__cards = []
        self.id = i
        self.__iter = iter(self.__cards)
        self.C = 1.1
    def add_card(self, cd):
        assert isinstance(cd, Card), "Obj must be Card"
        for c in self.__cards:
            if c.get_front() == cd.get_front() and c.get_back() == cd.get_back():
                raise Exception("add_card: Duplicate!")
        self.__cards.append(cd)
    def remove_card(self, cd):
        assert isinstance(cd, Card), "Obj must be Card"
        for c in self.__cards:
            if c.get_front() == cd.get_front() and c.get_back() == cd.get_back():
                self.__cards.remove(c)
                return
        raise Exception("remove_card : The card don't exists")
    def get_cards(self):
        return self.__cards
    def get_card(self, front, back):
        for cd in self.__cards:
            if cd.get_front() == front and cd.get_back() == back:
                return cd
        return None
    def size(self):
        return len(self.__cards)
    def next_card(self):
        print("in next")
        try:
            print(self.__iter.next())
            return self.__iter.next()
        except:
            print("in except")
            self.__iter = iter(self.__cards)
            return next(self.__iter)
    def reset(self):
        self.__cards = []

class FillingBox(object):
    def __init__(self):
        self.__compartments = []
        for i in range(5):
            self.__compartments.append(Compartment(i+1))
        self.__selected = 0
        self.__MAIN = 0
    def add_card(self,cd):
        self.__compartments[self.__MAIN].add_card(cd)
    def remove(self,i, cd):
        assert i >= 0 and i < 5
        self.__compartments[i].remove_card(cd)
    def select(self, i):
        assert i >= 0 and i < len(self.__compartments)
        self.__selected = i
    def __str__(self):
        ans = ""
        for i in range(5):
            ans += "\n\tBox {0}\n\n".format(i)
            for cd in self.__compartments[i].get_cards():
                ans += "{0}, {1} \n".format(cd.get_front(), cd.get_back())
        return ans
    def get_compartments(self):
        return self.__compartments
    def is_empty(self):
        for com in self.__compartments:
            if com.size() > 0:
                return False
        return True
    def learn(self):
        print("in second learn")
        print(self.__selected, self.__compartments[self.__selected].get_cards())
        cd = self.__compartments[self.__selected].next_card()
        
        assert cd
        # counter = 0
        # while (time.time() - cd.get_timestamp()) < (86400 * (self.__selected + 1)):
        #     cd = self.__compartments[self.__selected].next_card()
        #     counter += 1
        #     if counter > self.__compartments[self.__selected].size():
        #         return None
        return cd
    def is_known(self, cd):
        cd.reset()
        cd.set_known(False)
        self.__compartments[self.__selected + 1].get_cards().append(cd)
        self.__compartments[self.__selected].get_cards().remove(cd)
    def is_unknown(self, cd):
        cd.reset()
        cd.set_known(False)
    def reset(self):
        for com in self.__compartments:
            com.reset()
    def save(self, path):
        file = open(path,"w")
        content = ""

        for i in range(5):
            for cd in self.__compartments[i].get_cards():
                content += "{0};{1};{2};{3}\n".format(i, cd.get_front(), cd.get_back(), cd.get_timestamp())
        
        file.write(content)

        file.close()
    def load(self, path):
        self.reset()
        words = []
        file = open(path)
        for line in file:
            words = line.split('\t')
            cd = Card(words[1], words[2])
            cd.set_timestamp(time.time())
            self.__compartments[int(words[0])].add_card(cd)
        file.close()
    def create_CSV(self):
        content = ""

        for i in range(5):
            for cd in self.__compartments[i].get_cards():
                content += "{0};{1};{2};{3}\n".format(i, cd.get_front(), cd.get_back(), cd.get_timestamp())
        
        return content

    
    


app = Flask(__name__)

box = FillingBox()
cd = None # global card for the learn() and know() function

@app.route("/")
def index():
    box.load("words.csv")
    return render_template("index.html")

@app.route("/add", methods = ['POST', 'GET'])
def add():
    flag = False
    flag2 = False
    if request.method == "POST":
        front = request.form["front"]
        back = request.form["back"]

        # check for empty inputs 
        if len(front) > 1 and len(back) > 1:
            card = Card(front, back)
            try:
                box.add_card(card)
            except:
                flag = True
        else:
            flag2 = True
        return render_template("add.html", status = flag, status2 = flag2)
    else:
        return render_template("add.html", status = flag)

@app.route("/display")
def display():
    flag = box.is_empty()
    return render_template("display.html", data = box.get_compartments(), status = flag)

@app.route("/remove", methods = ["POST", "GET"])
def remove():
    flag = False
    if request.method == "POST":
        front = request.form["front"]
        back = request.form["back"]
        deck = int(request.form["deck"]) -1
        try:
            box.remove(deck, Card(front, back))
        except:
            flag = True
        return render_template("remove.html", status = flag)
    else:
        return render_template("remove.html")

@app.route("/learn", methods = ["POST", "GET"])
def learn():
    global cd
    data = ""
    flag = False
    deck = 1
    if request.method == "POST":
        deck = int(request.form["deck"]) -1
        box.select(deck)
        com = box.get_compartments()[deck]
        cs = com.get_cards()
        words={}
        for x in cs:
            words[x.get_front()]= Word(x.get_front(), x.get_back())
        question , options , answer = getQuestion(words)
        print(question , options , options[answer])
        # cs = box.get_cards()
        print(cs)
        # try:
        #     print(cd)
        #     cd = box.learn()
        #     # cs = box.get_cards()
        #     # print(cs)
        #     # question , options , answer = getQuestion()
        #     # print(question , options, answer)
        # except:
        #     return render_template("learn.html", word = data, status = True, status2 = False)
        # if cd == None:
        #     print("here")
        #     data = ""
        #     # data="hello"
        #     flag = True
        # else:
        #     print("actually here")
        #     data = cd.get_front()
        #     answer = cd.get_back()
        #     # data="hello"
        return render_template("learn.html", word = question, answer=answer, options = options, status = flag, status2 = False, deck= deck+1 )
    else:
        return render_template("learn.html", word = data, status = flag, status2 = False)

@app.route("/learn/know", methods = ["POST", "GET"])
def know():
    flag = False
    print("in knoww")
    if request.method == "POST":
        print("in knoww")
        if cd == None:
            print("flag true")
            flag = True
        else:
            print("flag false")
            box.is_known(cd)
        return render_template("learn.html", word = "", status = False, status2 = flag)
    else:
        return render_template("learn.html", word = "", status = False, status2 = flag)

@app.route("/io")
def io():
    return render_template("io.html")

@app.route("/io/save", methods = ["POST", "GET"])
def save():
    response = make_response(box.create_CSV())
    response.headers['Content-Disposition'] = 'attachment; filename=words.csv'
    response.mimetype='text/csv'
    return response

@app.route("/io/load", methods = ["POST", "GET"])
def load():
    if request.method == "POST":
        path = request.form["file"]
        box.load(path)
    
    return render_template("io.html")

@app.route("/edit", methods = ["POST", "GET"])
def edit():
    flag = False
    if request.method == "POST":
        deck = int(request.form["deck"]) -1
        com = box.get_compartments()[deck]
        flag = True
        if "front" in request.form:
            if len(request.form["front"]) > 0 and len(request.form["back"]) > 0:
                id = int(request.form["card"]) -1
                com = box.get_compartments()[deck]
                cs = com.get_cards()
                cs[id].set_front(request.form["front"])
                cs[id].set_back(request.form["back"])
        return render_template("edit.html", cards = com.get_cards(), status = flag)
    else:
        return render_template("edit.html", status = flag)

if __name__ == "__main__":
    app.run(debug= True, port=5004)
    # app.run(debug = True)