import json
import random

from lxml import etree


MT_CHAPTERS = 28
MK_CHAPTERS = 16
LK_CHAPTERS = 24
IV_CHAPTERS = 21


def get_number_of_verses(html_sinkopa):
    rows = html_sinkopa.xpath("//span[@class='brojRetka']")
    return int(rows[-1].text)


def parse_html(html):
    parser = etree.HTMLParser(encoding="utf-8")
    html_root = etree.fromstring(html, parser)
    # result = etree.tostring(html_root, pretty_print=True, method="html", encoding="utf-8")
    # print(result.decode("utf-8"))

    # Initialize variables
    paragraphs = []
    current_paragraph = []
    first_paragraph = True

    # Iterate through HTML nodes
    for element in html_root.iter():
        current_paragraph.append(element)
        print("ELEMENT ADDED")
        if first_paragraph:
            if element.tag == 'p' and 'pocetakParagrafa' in element.get('class', ''):
                first_paragraph = False
        else:
            if (element.tag == 'p' and 'pocetakParagrafa' in element.get('class', '')) or (
                    element.get('id') == get_number_of_verses(html_root)):
                paragraphs.append(current_paragraph.copy())
                print(f"PARAGRAPH ADDED, {len(current_paragraph)}")
                current_paragraph.clear()

        # print(element.get('id'))
        # if element.get('id') == get_number_of_verses(html_root):
        #     current_paragraph.append(element)
        #     paragraphs.append(current_paragraph)

    print("Broj paragrafa je ", len(paragraphs))

    para_html = etree.tostring(paragraphs[0][0], method="html", encoding="unicode")
    print(para_html)
    print("----------------------")

    # Print the paragraphs
    # for paragraph in paragraphs:
    #     para_html = etree.tostring(paragraph[0], method="html", encoding="unicode")
    #     print(para_html)
    #     print("----------------------")


def randomize(data):
    """
    Prvi index: 0 - Matej, 1 - Marko, 2 - Luka, 3 - Ivan; data[0] ce dati Mt
    Drugi index: 0 - Naslov, 1 - Tekst; data[0][1] je tekst Mt bez naslova
    Treci index: Broj poglavlja - 1; data[0][1][4] je Mt 5
    Cetvrti index: 0 - Naslov, 1 - Tekst
    """
    gospel_number = random.choice(range(4))
    match gospel_number:
        case 0:
            chapter_number = MT_CHAPTERS
        case 1:
            chapter_number = MK_CHAPTERS
        case 2:
            chapter_number = LK_CHAPTERS
        case 3:
            chapter_number = IV_CHAPTERS
        case _:
            chapter_number = None
    return data[gospel_number][1][random.choice(range(chapter_number))][1]


def main():
    try:
        with open('evangelion.json', 'r', encoding="utf-8") as file:
            data = json.load(file)

        # print(data[3][1][0][1])
        # print(len(data[3][1][0][1]))

        print(randomize(data))

        # parse_html(data[3][1][0][1])

    except Exception as e:
        print("An error occurred:", e)


if __name__ == "__main__":
    main()
