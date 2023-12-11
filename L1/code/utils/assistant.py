import sys
import pyttsx3
import speech_recognition as sr
from enum import Enum

class Operation(Enum):
    ADD         = 1
    SUBSTRACT   = 2
    MULTIPLY    = 3
    DIVIDE      = 4
    UNKNOWN     = 0


class Assistant(sr.Recognizer):
    _start_operation_list : list[str] = [
        "ile jest",
        "oblicz"
    ]

    _help_operation_list : list[str] = [
        "pomoc"
    ]

    _stop_operation_list : list[str] = [
        "stop",
        "zatrzymaj"
    ]

    _calc_operation_list : dict = {
        "add" : {
            "operation" : Operation.ADD,
            "words" : [
                "dodać",
                "plus",
                "+"
            ],
        },
        "sub" : {
            "operation" : Operation.SUBSTRACT,
            "words" : [
                "odjąć",
                "minus",
                "-"
            ],
        },
        "mul" : {
            "operation" : Operation.MULTIPLY,
            "words" : [
                "razy",
                "pomnożyć przez",
                "mnożone przez",
                "*",
                "x"
            ],
        },
        "div" : {
            "operation" : Operation.DIVIDE,
            "words" : [
                "podzielić przez",
                "dzielone przez",
                "dzielone",
                "/"
            ],
        },
    }
    
    def __init__(self, device_index : int = 0) -> None:
        self._dev_index = device_index
        
        self._engine = pyttsx3.init()

        _voices = self._engine.getProperty('voices')
        for voice in _voices:
            if 'polish' in voice.name.lower():
                self._engine.setProperty('voice', voice.id)

        super().__init__()


    def __log(self, who : str, msg : str) -> None:
        print(f'{who} : {msg}')

    def __log_user(self, msg : str) -> None:
        self.__log("USER     ", msg)
    
    def __log_assistant(self, msg : str) -> None:
        self._engine.say(msg)
        self.__log("ASSISTANT", msg)
        self._engine.runAndWait()

    def __log_core(self, msg : str) -> None:
        who = "  [*] CORE     "
        print(f'{who} : {msg}')


    def __is_start_cmd(self, text: list[str]) -> (bool, int):
        for start_op in Assistant._start_operation_list:
            l = len(start_op.split())
            phrase = ' '.join(text[:l])
            print(f'    - {phrase=} | {start_op=}', file=sys.stderr)
            if phrase == start_op:
                return True, l
        return False, 0
    
    def __get_num(self, text: list[str]) -> float | None:
        try:
            phrase = text[0].replace(',', '.')
            print(f'    - {phrase= }', file=sys.stderr)
            if phrase == '0' or phrase == '0.0':
                return 0
            num = float(phrase)
        except Exception as err:
            print(f"[ERROR]: {err}")
            return None
        else:
            return num
    
    def __get_op(self, text: list[str]) -> (Operation | None, int):
        for key, value in Assistant._calc_operation_list.items():
            for calc_op in value["words"]:
                l = len(calc_op.split())
                phrase = ' '.join(text[:l])
                print(f'    - {phrase= } | {calc_op= }', file=sys.stderr)
                if phrase == calc_op:
                    return value["operation"], l
        return None, 0
        
    
    def __calculate(self, num_1: float, op: Operation, num_2: float) -> float:
        self.__log_core("Calculating...")
        if op == Operation.ADD:
            result = num_1 + num_2
        elif op == Operation.SUBSTRACT:
            result = num_1 - num_2
        elif op == Operation.MULTIPLY:
            result = num_1 * num_2
        elif op == Operation.DIVIDE:
            if num_2 == 0:
                raise ZeroDivisionError("Nie można dzielić przez 0.")
            result = num_1 / num_2
        return result
    

    def work(self) -> None:
        with sr.Microphone(device_index=self._dev_index) as source: 
            while True:
                self.__log_assistant("Jak mogę Ci pomóc?")
                
                try:
                    self.__log_core("Listening...")
                    audio = self.listen(source=source, timeout=8, phrase_time_limit=4)
                except sr.WaitTimeoutError:
                    continue
                
                try:
                    self.__log_core("Recognizing...")
                    text = self.recognize_google(audio, language="pl-PL")
                    if type(text) == str:
                        self.__log_core("Splitting...")
                        text = text.lower().split()
                except sr.UnknownValueError:
                    self.__log_core("UnknownValueError detected")
                    self.__log_assistant("Nie zrozumiałem. Możesz powtórzyć?")
                    continue
                except sr.RequestError as err:
                    print(f' [ERROR] : Google Speech Recognition : błąd usługi; {err}')
                    continue
                
                self.__log_user(' '.join(text))
                
                self.__log_core("Checking HELP command...")
                if text[0] in self._help_operation_list:
                    self.help_user()
                    continue
                
                self.__log_core("Checking STOP command...")
                if text[0] in self._stop_operation_list:
                    self.bye()
                    break
            
                self.__log_core("Checking CALCULATE format...")
                self.__log_core(f"Checking words count [{len(text)}]...")
                if len(text) < 4:
                    self.__log_assistant("Nie zrozumiałem. Możesz powtórzyć?")
                    continue
                
                self.__log_core("Checking START command...")
                start, ind = self.__is_start_cmd(text)
                if start:
                    text = text[ind:]
                    
                    self.__log_core("Getting NUM_1...")
                    num_1 = self.__get_num(text)
                    if not num_1:
                        self.__log_assistant("Nie zrozumiałem. Możesz powtórzyć?")
                        continue
                    text = text[1:]
                    
                    self.__log_core("Getting Operation type...")
                    op, ind = self.__get_op(text)
                    if not op:
                        self.__log_assistant("Nie zrozumiałem. Możesz powtórzyć?")
                        continue
                    text = text[ind:]
                    
                    self.__log_core("Getting NUM_2...")
                    num_2 = self.__get_num(text)
                    if not num_2:
                        self.__log_assistant("Nie zrozumiałem. Możesz powtórzyć?")
                        continue
                    
                    try:
                        result = self.__calculate(num_1, op, num_2)
                    except ZeroDivisionError as err:
                        self.__log_assistant(str(err.args[0]))
                    else:
                        self.__log_assistant(f"Wynik to {result}")


    def help_user(self) -> None:
        self.__log_assistant(f"Podaj polecenie w formacie: [{self._start_operation_list[0]}], liczba, rodzaj operacji, liczba.")
        
        print(" * Rodzaje operacji: ")
        print(f"    - dodawanie   : {self._calc_operation_list['add']['words']}")
        print(f"    - odejmowanie : {self._calc_operation_list['sub']['words']}")
        print(f"    - mnożenie    : {self._calc_operation_list['mul']['words']}")
        print(f"    - dzielenie   : {self._calc_operation_list['div']['words']}")
        
        self.__log_assistant(f"Albo podaj polecenie {self._stop_operation_list[0]}, żeby zakończyć pracę.")
        
    
    def introduce(self) -> None:
        # self.__log_assistant("Witaj! Tutaj twój głosowy kalkulator.")
        self.__log_assistant("Podaj polecenie do wykonania, albo powiedz 'POMOC'.")


    def bye(self) -> None:
        self.__log_assistant("Daj znać jakbyś czegoś potrzebował.")
