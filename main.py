import pygame
import pygame.midi
import time
import string

# Настройки MIDI
VIRETUAL_PORT_NAME = "TEXTtoMIDI"
NOTE_DURATION = 0.4
VELOCITY = 100  

def create_note_mapping():
    mapping = {}
    for i, char in enumerate(string.ascii_uppercase):
        mapping[char] = 60 + i
    
    russian_letters = [chr(c) for c in range(1040, 1040+32)]  # А-Я
    for i, char in enumerate(russian_letters):
        mapping[char] = 60 + 26 + i

    return mapping

NOTE_MAPPING = create_note_mapping()

def connect_to_midi():
    pygame.midi.init()
    port_id = None
    
    for i in range(pygame.midi.get_count()):
        interface, name, is_input, is_output, opened = pygame.midi.get_device_info(i)
        if name.decode() == VIRTUAL_PORT_NAME and is_output:
            port_id = i
            break
    
    if port_id is None:
        raise Exception(f"Порт '{VIRTUAL_PORT_NAME}' не найден!")
    
    return pygame.midi.Output(port_id)

def send_note(output, midi_num):
    output.note_on(midi_num, VELOCITY)
    time.sleep(NOTE_DURATION)
    output.note_off(midi_num, VELOCITY)
def get_input() -> str:
    return input("Введите последовательность символов: ")

def process_text(text: str) -> list:
    filtered = []
    for char in text.upper(): 
        if char in NOTE_MAPPING:
            filtered.append((char, NOTE_MAPPING[char]))
    return filtered

def ask_continue() -> bool:
    while True:
        answer = input("\nПродолжить? (y/n): ").lower().strip()
        if answer == 'y': return True
        if answer == 'n': return False
        print("Ошибка: введите 'y' или 'n'")

def main():
    # Подключаемся к MIDI
    try:
        midi_output = connect_to_midi()
        print(f"Успешно подключено к порту: {VIRTUAL_PORT_NAME}")
    except Exception as e:
        print(f"Ошибка: {e}")
        return

    print("Текст:")
    while True:
        text = input("> ").strip().upper()
        
        valid_notes = []
        for char in text:
            if char in NOTE_MAPPING:
                midi_num = NOTE_MAPPING[char]
                valid_notes.append(midi_num)
                print(f"{char} → MIDI-нота {midi_num}")
        
        for midi_num in valid_notes:
            send_note(midi_output, midi_num)
        
        if input("Продолжить? (y/n): ").lower() != 'y':
            break
    
    midi_output.close()
    pygame.midi.quit()
    print("Работа завершена.")

if __name__ == "__main__":
    main()