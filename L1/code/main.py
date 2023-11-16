import speech_recognition as sr
from enum import Enum


# Grammar lists
start_operation_grammar_list = [
    "oblicz"
]

stop_operation_grammar_list = [
    "stop",
    "zatrzymaj"
]

calc_operation_grammar_list = [
    "dodać",
    "odjąć",
    "razy",
    "podzielić"
]

class Command(Enum):
    ADD = 0,
    SUB = 1,
    MUL = 2,
    DIV = 3
    
    @staticmethod
    def get_by_value(value : int):
        match(value):
            case 0:
                return Command.ADD
            case 1:
                return Command.SUB
            case 2:
                return Command.MUL
            case 3:
                return Command.DIV


class Interpreter:
    @staticmethod
    def interpret_cmd(text : str) -> None:
        Command.get_by_value(calc_operation_grammar_list.index(text))
    
    @staticmethod    
    def interpret_number(text : str) -> None:
        return 0


class Assistant:
    def __init__(self) -> None:
        self._engine : sr.Recognizer = sr.Recognizer()

    def __log(self, who : str, msg : str) -> None:
        print(f'{who} : {msg}')

    def __log_user(self, msg : str) -> None:
        self.__log("USER     ", msg)
    
    def __log_assistant(self, msg : str) -> None:
        self.__log("ASSISTANT", msg)

    def listen(self) -> str:
        with sr.Microphone() as source:
            while True:
                
                try:
                    audio = self._engine.listen(source)
                    recognized_text = self._engine.recognize_google(audio, language='pl-PL')
                    self.__log_user(recognized_text)
                    
                except sr.UnknownValueError or sr.RequestError as e:
                    self.__log_assistant("Nie rozumiem, możesz powtórzyć?")
                
                else:
                    text = ' '.join(recognized_text).lower()
                    if text in stop_operation_grammar_list:
                        raise SystemError("STOP command recognized")
                    else:
                        return text
                
    def perform_calculation(self) -> None:
        nums = set()
        
        try:
            while True:
                # Recognize START
                if not self.listen() in start_operation_grammar_list:
                    continue
                
                # Recognize number 1
                nums[0] = int(self.listen())

                # Recognize operation
                while True:
                    cmd_str : str = self.listen()
                    if not cmd_str in calc_operation_grammar_list:
                        continue                    
                    
                    cmd : Command = Interpreter.interpret_cmd(cmd_str)
                    break

                # Recognize number 2
                nums[1] = int(self.listen())
                break
        except SystemError as e:
            # Recognized STOP
            return
        
        result : int = 0
        match(cmd):
            case Command.ADD:
                result = nums[0] + nums[1]
            case Command.SUB:
                result = nums[0] - nums[1]
            case Command.MUL:
                result = nums[0] * nums[1]
            case Command.DIV:
                if nums[1] == 0:
                    self.__log_assistant("Nie dzielimy przez 0")
                else:
                    result = nums[0] / nums[1]
        
        self.__log_assistant(f"Wynik to {result}")
        
                
    def introduce(self) -> None:
        self.__log_assistant("Slucham...")


def main():
    assistant = Assistant() 
    assistant.introduce()
    assistant.perform_calculation()
            

if __name__ == "__main__":
    main()
