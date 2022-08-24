from vietnam_number import n2w_single
import re


alphabet={
            'A':'..a..',
            'B':'.bê',
            'C':'xê',
            'D':'dê',
            'E':'e',
            'F':'ép..',
            'G':'gờ.',
            'H':'hát..',
            'I':'..Y..',
            'K':'.ca.',
            'L':'.lờ.',
            'M':'.mờ.',
            'N':'.nờ.',
            'O':'..ô..',
            'P':'..pê..',
            'Q':'..quy..',
            'R':'.rờ..',
            'S':'..ét..',
            'T':'..tê..',
            'U':'..U..',
            'V':'..vi..',
            'W':'.đáp liu..',
            'X':'..ích..',
            'Y':'..Y..',
            'Z':'.dét'
        }

class ConvertBSX():
    def __init__(self) :
        self.ruleFormat={}
        self.loadRuleFormat()
        
    def loadRuleFormat(self):
        with open("text/ruleFormat","r", encoding="utf-8") as f:
            data=f.read().split("\n")
            for line in data:
                rule=" ".join(line.split()).split(" ")
                if (len(rule)==2):
                    self.ruleFormat[rule[0]]=rule[1]

    def convertBienSoXe(self,text):
        output=""
        text=text.upper()      
        texts=text.replace('/','-').replace(' ','-').replace('.','').split("-")
        for text in texts:
            numberText=''
            alphabetText=''
            if len(re.findall('[A-Z]+',text)) >0:   
                output=output+'. '        
                string=re.findall('[A-Z]+',text)[0]
                for i in string:
                    alphabetText=alphabetText+alphabet[i]+' '
            number=re.findall('\d+',text)
            if len(number)>0:
                number=number[0]
            if len(number)==2 and number[1]=='0':
                numberText=n2w_single(number[0])+' mươi '
            elif len(number)>0:
                numberText=n2w_single(number) +' '
            if len(number)>0 and text.find(number)==0:
                output=output+numberText+alphabetText
            else:
                output=output+alphabetText+numberText
            if len(alphabetText)>0:
                output=output+". "
        return output

    def tachBienSoXe(self,string):
        string=re.findall('[A-Z0-9][A-Z0-9 -./]+[A-Z0-9]', string)
        for text in string:
            text=text.strip()
            if len(text)>5 and len(text)<15:
                return text
        return ""

    def FormatTextBSX(self,string):
        text=self.tachBienSoXe(string)
        textConvert=""
        if len(text)>0:
            print("Tìm thấy biển số xe:",text)
            textConvert=self.convertBienSoXe(text)
        string=string.replace(text,textConvert)
        for rule in self.ruleFormat:
            string=string.replace(rule,self.ruleFormat[rule])
        return string.replace("  "," ")


        




