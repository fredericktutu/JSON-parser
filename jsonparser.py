'''
definition of json value:
'''
class JsonExpr:
    '''
    types:
    0   number     :int float
    1   string     :str
    2   bool       :boolean
    3   array      :JsonArr
    4   object     :JsonObj
    5   null       :None
    '''
    def __init__(self, type:int, value):
        self.type = type
        self.value = value
    
    def eval(self):
        '''
        generate python value
        JsonArr to list
        JsonObj to map
        '''
        if self.type in [0,1,2,5]:
            return self.value
        elif self.type == 3:
            arr = self.value.array
            lst = []
            for item in arr:
                lst.append(item.eval())
                return lst
        elif self.type == 4:
            mp = self.value.map
            dic = {}
            for item in mp:
                dic[item] = mp[item].eval()
            return dic

    def __str__(self):
        switch1 = {0:"number",
                    1:"string",
                    2:"bool",
                    3:"array",
                    4:"object",
                    5:"null"}
        switch2 = {0: lambda x: str(x),
                    1: lambda x: x,
                    2: lambda x: str(x),
                    3: lambda x: x.array,
                    4: lambda x: x.map,
                    5: lambda x: str(x)}
        return "<{0}>: {1}".format(switch1[self.type], switch2[self.type](self.value))
        
class JsonArr:
    '''
    json数组
    '''
    def __init__(self):
        self.array = []

    def add(self, jvalue):
        self.array.append(jvalue)

class JsonObj:
    '''
    json对象
    '''
    def __init__(self):
        self.map = {}

    def add(self, key:str, jvalue):
        self.map[key] = jvalue




'''
json parser begin:
'''

class JsonParser:


    def parse(self, s:str) ->  JsonExpr:
        self.start(s)
        jexpr = self.parse_json()
        self.parse_blank()
        self.check_end()
        return jexpr.eval()


    def start(self, s:str):
        self.input = s
        self.until = len(s) - 1
        self.now = 0

    def error(self, s:str):
        if self.now <= self.until:
            print("error at char:", self.input[self.now], "located at place", self.now)
            exit(0)
        else:
            print("unexpected end of json")

    def check_end(self):
        if self.now != self.until + 1:
            self.error("")
        return


    def advance(self, n):
        self.now += n

    def parse_json(self):
        self.parse_blank()
        if self.match_number() or self.match("-"):
            x = self.parse_number()
            res = JsonExpr(0, x)

        elif self.match('"'):
            s = self.parse_string()
            res = JsonExpr(1, s)

        elif self.match("f") or self.match("t"):
            b = self.parse_bool()
            res = JsonExpr(2, b)

        elif self.match("n"):
            self.parse_null()
            res = JsonExpr(5, None)
        elif self.match("["):
            jarr = self.parse_array()
            res = JsonExpr(3, jarr)
        elif self.match("{"):
            jobj = self.parse_object()
            res = JsonExpr(4, jobj)

        return res

    def parse_blank(self):
        while self.now <= self.until:
            if self.match(" ") or self.match("\n") or self.match("\t"):
                self.advance(1)
            else:
                break

    def parse_object(self):
        if not self.match("{"):
            self.error("")
        self.advance(1)
        jobj = JsonObj()
        while self.now <= self.until:
            self.parse_blank()
            if self.match("}"):
                self.advance(1)
                return jobj
            else:
                key = self.parse_string()
                self.parse_blank()

                if not self.match(":"):
                    self.error("expect ':'.")
                self.advance(1)
            

                value = self.parse_json()

                self.parse_blank()
                if not self.match(","):
                    self.error("expect ','.")
                self.advance(1)
                jobj.add(key, value)
        self.error("")
                

    def parse_array(self):
        if not self.match("["):
            self.error("")
        self.advance(1)
        jarr = JsonArr()

        while self.now <= self.until:
            self.parse_blank()
            if self.match("]"):
                self.advance(1)
                return jarr
            else:
                el = self.parse_json()
                jarr.add(el)
                self.parse_blank()
                if not self.match(","):
                    self.error("")
                self.advance(1)
        self.error("")

    def parse_pos(self):
        numbers = ""
        firstInt = False
        inInt = True
        while self.now <= self.until:
            if inInt:
                if self.match_number():
                    firstInt = True
                    numbers += self.input[self.now]
                    self.advance(1)
                elif self.match("."):
                    if not firstInt:
                        self.error("")
                    numbers += "."
                    self.advance(1)
                    inInt = False
                else:
                    break
            else:
                if self.match_number():
                    numbers += self.input[self.now]
                    self.advance(1)
                else:
                    break

        if inInt:
            return int(numbers)
        else:
            return float(numbers)


    def parse_number(self):
        isPos = True
        if self.match("-"):
            isPos = False
            posval = self.parse_pos()
            return posval * (-1)
        elif self.match_number():
            posval = self.parse_pos()
            return posval
        else:
            error("")


    def parse_bool(self):
        if self.match("false"):
            self.advance(5)
            return False
        elif self.match("true"):
            self.advance(4)
            return True
        else:
            self.error("")
        
    def parse_string(self):
        if not self.match('"'):
           self.error("")
        self.advance(1)
        start = self.now
        while self.now <= self.until:
            if self.match('"'):
                self.advance(1)
                return self.input[start: self.now - 1]
            else:
                self.advance(1)
        error("")



    def parse_null(self):
        if self.match("null"):
            self.advance(4)
            return None
        else:
            self.error("")

    def match(self, s:str):
        if self.until - self.now + 1 < len(s):
            return False
        elif self.input[self.now: self.now + len(s)] == s:
            return True
        else:
            return False
    
    def match_number(self):
        if "0" <= self.input[self.now] <= "9":
            return True
        else:
            return False


jparser = JsonParser()
x = input()
print(jparser.parse(x))
