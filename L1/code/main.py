from utils import Assistant


def main():
    import speech_recognition as sr
    for i, micro in enumerate(sr.Microphone.list_microphone_names()):
        print(f'[{i}]: {micro}')
    print('Choose the microphone device index: ')
    dev_index = int(input(' > '))
    
    assistant = Assistant(device_index=dev_index) 
    
    assistant.introduce()
    assistant.work()


if __name__ == "__main__":
    main()