import pytesseract
import os
import time
from PIL import ImageGrab
import keyboard
import csv
import threading
import os
import sys


tesseract_path = os.path.join(os.path.dirname(os.path.abspath(sys.executable)), 'Tesseract-OCR')
pytesseract.pytesseract.tesseract_cmd = os.path.join(tesseract_path, 'tesseract.exe')

def grab_image_from_clipboard(output_file, prev_img_hash):

    #setze den hash falls schon ein Bild in der zwischenablage existiert
    img = ImageGrab.grabclipboard()
    if img is not None:
        prev_img_hash[0] = hash(img.tobytes())
    while True:
        # Bild aus Zwischenablage holen
        img = ImageGrab.grabclipboard()

        if img is not None:
            # Bild-Hash berechnen, um Änderungen in der Zwischenablage zu erkennen
            img_hash = hash(img.tobytes())

            if prev_img_hash[0] != img_hash:
                prev_img_hash[0] = img_hash
                # OCR-Anwendung auf das Bild
                text = pytesseract.image_to_string(img, lang='deu')
                print("Erkannter Text: ", text)

                # Speichern des erkannten Textes in der Textdatei
                with open(output_file, 'a', encoding='utf-8') as f:
                    f.write(text)
                    f.write('\n')
            # else:
            #     print("Keine Änderung in der Zwischenablage erkannt.")
        # else:
        #     print("Kein Bild in der Zwischenablage gefunden.")

        time.sleep(2)

def main():
    output_file_base = "documents/" + input("Geben Sie den Basisdateinamen für das Text-Dokument ein (ohne Dateierweiterung): ")
    # csv_file = "documents/" + input("Geben Sie den Dateinamen für die CSV-Datei ein (ohne Dateierweiterung): ") + '.csv'
    

    prev_img_hash = [None]
    file_count = 1
    output_file = output_file_base + "_" + str(file_count) + '.txt'

    print("Drücken Sie 'Ctrl+C' oder 'Ctrl+Break', um das Programm zu beenden.")
    print("mache screenshots und der Text wird automatisch in das Textdokument geschrieben\n")
    print("zusatzoption: drücke # um ein neues dokument zu erzeugen\n(du hast ein unterkapitel gelesen)\n")
    # print("Drücke + um die speicherung in csv zu starten\n(einfach den Text von chatgpt in die Konsole anfügen und anschließend enter drücken)\n")

        # Anfangstext zum Textdokument hinzufügen
    anfangs_text =  """\
Lieber ChatGPT,

ich habe folgende aufgaben für dich:

-bitte erstelle mir Karteikarten für anki
-bitte im csv format
-bitte mit semikolon als trennzeichen
-bitte so das man es in anki importieren kann:)
-bitte in einem codeblock

vielen dank :)
der Text:\
    
"""
    with open(output_file, 'a', encoding='utf-8') as f:
        f.write(anfangs_text + '\n')

    # Füge hier den restlichen Code ein, der parallel ausgeführt werden soll

    t = threading.Thread(target=grab_image_from_clipboard, args=(output_file, prev_img_hash))
    t.start()

    try:
        while True:
            # Wenn die 1 gedrückt wird, erstellen Sie eine neue Datei
            if keyboard.is_pressed('#'):
                file_count += 1
                output_file = output_file_base + str(file_count) + '.txt'
                with open(output_file, 'a', encoding='utf-8') as f:
                    f.write(anfangs_text + '\n')
                print(f"Neue Datei erstellt: {output_file}")
                time.sleep(0.5)

            # # Wenn die Taste "2" gedrückt wird, warten Sie auf eine Eingabe und speichern Sie sie in der CSV-Datei
            # if keyboard.is_pressed('+'):
            #     time.sleep(0.5)
            #     input_lines = []
            #     while True:
            #         user_input = input("Bitte geben Sie eine Frage und Antwort ein (oder 'q' zum Beenden): ")
            #         if user_input.lower() == 'q':
            #             break
            #         input_lines.append(user_input.split(";"))

            #     with open(csv_file, 'a', encoding='utf-8') as csvfile:
            #         writer = csv.writer(csvfile)
            #         for line in input_lines:
            #             writer.writerow([line])
            #     print("Daten in die CSV-Datei geschrieben.")


    except KeyboardInterrupt:
        print("Skript beendet.")

if __name__ == '__main__':
    main_thread = threading.Thread(target=main)
    main_thread.start()
    main_thread.join()