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
                "plus"
            ],
        },
        "sub" : {
            "operation" : Operation.SUBSTRACT,
            "words" : [
                "odjąć",
                "minus"
            ],
        },
        "mul" : {
            "operation" : Operation.MULTIPLY,
            "words" : [
                "razy",
                "pomnożyć przez",
                "mnożone przez"
            ],
        },
        "div" : {
            "operation" : Operation.DIVIDE,
            "words" : [
                "podzielić przez",
                "dzielone przez"
            ],
        },
    }
    
    def __init__(self) -> None:
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
        self._engine.runAndWait()
        self.__log("ASSISTANT", msg)


    def work(self) -> None:            
        with sr.Microphone() as source: 
            while True:
                self.__log_assistant("Jak mogę Ci pomóc?")
                
                try:
                    audio = self.listen(source=source, timeout=5)
                except sr.WaitTimeoutError:
                    continue
                
                try:
                    text = ' '.join(self.recognize_google(audio, language="pl-PL")).lower()
                except sr.UnknownValueError:
                    self.__log_assistant("Nie zrozumiałem. Możesz powtórzyć?")
                    continue
                except sr.RequestError as err:
                    print(f' [ERROR] : Google Speech Recognition : błąd usługi; {err}')
                    continue
                
                self.__log_user(text)
                
                if text in self._help_operation_list:
                    self.help_user()
                    continue
                
                elif text in self._stop_operation_list:
                    self.bye()
                    break
      
                else:
                    if len(text.split() < 4):
                        self.__log_assistant("Nie zrozumiałem. Możesz powtórzyć?")
                        continue
                    
                    if text.split()[0] in self._start_operation_list:
                        words = text.split()
                        if ' '.join(words[0:1]) == self._start_operation_list[0]:
                            words.pop(0)
                            words.pop(0)
                        else:
                            words.pop(0)
                            
                        try:
                            num_1 = float(words[0])
                        except TypeError:
                            self.__log_assistant("Nie zrozumiałem. Możesz powtórzyć?")
                            continue
                        
                        for key, value in self._calc_operation_list.items():
                            if words[1] in value["words"]:
                                op = value["operation"]
                                break
                        else:
                            self.__log_assistant("Nie zrozumiałem. Możesz powtórzyć?")
                            continue
                        
                        try:
                            num_2 = float(words[2])
                        except TypeError:
                            try:
                                num_2 = float(words[3])
                            except TypeError | IndexError:
                                self.__log_assistant("Nie zrozumiałem. Możesz powtórzyć?")
                                continue
                        
                        if op == Operation.ADD:
                            result = num_1 + num_2
                        elif op == Operation.SUBSTRACT:
                            result = num_1 - num_2
                        elif op == Operation.MULTIPLY:
                            result = num_1 * num_2
                        elif op == Operation.DIVIDE:
                            if num_2 == 0:
                                self.__log_assistant("Nie można dzielić przez 0.")
                                continue
                            result = num_1 / num_2

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