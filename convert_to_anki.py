import os
import csv
import re
import markdown
from bs4 import BeautifulSoup

OUTPUT_DIR = './anki-csv'
INPUT_DIR = './practice-exam'

def write_csv(cards, exam_name):
    csv_path = os.path.join(OUTPUT_DIR, f"{exam_name}.csv")
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile, delimiter='\t')
        for card in cards:
            writer.writerow([card['front'], card['back'], exam_name])

def main():
    for filename in sorted(os.listdir(INPUT_DIR)):
        if not filename.endswith('.md'):
            continue

        if filename == 'exams.md':
            continue

        filepath = os.path.join(INPUT_DIR, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()

        html = markdown.markdown(text)
        soup = BeautifulSoup(html, 'html.parser')

        exam_name = os.path.splitext(filename)[0]

        questions = soup.select("ol > li")

        cards = []

        for question in questions:
            title = question.select("p:nth-of-type(1)")[0].text
            choice_list = question.select("ul")[0]

            # Convert <ul> to <ol type="A"> for A, B, C... numbering
            choice_list.name = 'ol'
            choice_list['type'] = 'A'

            choices = choice_list.select('li')
            for choice in choices:
                text = choice.text[3:]        # strip leading "A. "
                text = text.rstrip('.')       # strip trailing period
                choice.string = text

            answer = question.select("p:nth-of-type(2)")[0].text

            front = title + '\n' + str(choice_list)
            back = answer
            cards.append({"front": front, "back": back})
        
        write_csv(cards, exam_name)

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    main()