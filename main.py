import json
import random

from lxml import etree


MT_CHAPTERS = 28
MK_CHAPTERS = 16
LK_CHAPTERS = 24
IV_CHAPTERS = 21


def get_number_of_verses_in_paragraph(html_paragraph) -> int:
    """ Returns number of verses of a given paragraph """
    rows = html_paragraph.xpath("//span[@class='brojRetka']")
    return int(rows[-1].text)


def get_random_paragraph(html_chapter):
    """ Returns random paragraph of a given chapter """
    parser = etree.HTMLParser(encoding="utf-8")
    html_root = etree.fromstring(html_chapter, parser)

    # Initialize variables
    paragraphs = []
    current_paragraph = []
    first_paragraph = True

    # Iterate through HTML nodes
    for element in html_root.iter():

        if first_paragraph:
            if element.tag == 'p' and 'pocetakParagrafa' in element.get('class', ''):
                first_paragraph = False
        else:
            if element.tag == 'p' and 'pocetakParagrafa' in element.get('class', ''):
                paragraphs.append(current_paragraph.copy())
                print(f"PARAGRAPH ADDED, {len(current_paragraph)}")
                current_paragraph.clear()
            # else:
            #     if element.get('id') == get_number_of_verses_in_paragraph(html_root):
            #         # paragraphs.append(current_paragraph.copy())
            #         # print(f"PARAGRAPH ADDED, {len(current_paragraph)}")
            #         # current_paragraph.clear()
            #         print("LAST LINE")

        current_paragraph.append(element)
        print("ELEMENT ADDED")

    paragraphs.append(current_paragraph.copy())
    print(f"PARAGRAPH ADDED, {len(current_paragraph)}")

    print("Broj paragrafa je ", len(paragraphs))

    random_paragraph_number = random.choice(range(len(paragraphs)))
    print(f"{random_paragraph_number=}")

    return paragraphs[random_paragraph_number], random_paragraph_number, len(paragraphs)


def get_random_chapter(data):
    """
    Prvi index: 0 - Matej, 1 - Marko, 2 - Luka, 3 - Ivan; data[0] ce dati Mt
    Drugi index: 0 - Naslov, 1 - Tekst; data[0][1] je tekst Mt bez naslova
    Treci index: Broj poglavlja - 1; data[0][1][4] je Mt 5
    Cetvrti index: 0 - Naslov, 1 - Tekst
    """
    gospel_number = random.choice(range(4))
    match gospel_number:
        case 0:
            num_of_chapters = MT_CHAPTERS
            gospel_sig = "Mt"
        case 1:
            num_of_chapters = MK_CHAPTERS
            gospel_sig = "Mk"
        case 2:
            num_of_chapters = LK_CHAPTERS
            gospel_sig = "Lk"
        case 3:
            num_of_chapters = IV_CHAPTERS
            gospel_sig = "Iv"
        case _:
            num_of_chapters = None
            gospel_sig = None
    selected_chapter = random.choice(range(num_of_chapters))

    return data[gospel_number][1][selected_chapter][1], gospel_sig, selected_chapter + 1


def main():

    final_gospel = None
    final_chapter = None
    total_paragraphs = None
    final_paragraph = None

    try:
        with open('evangelion.json', 'r', encoding="utf-8") as file:
            data = json.load(file)

        # Get a random chapter and print it
        random_chapter, final_gospel, final_chapter = get_random_chapter(data)
        print(random_chapter)
        print("-----------------------")

        # Get a random paragraph from a random chapter
        raw_paragraph, final_paragraph, total_paragraphs = get_random_paragraph(random_chapter)

        # Convert the paragraph to HTML and print it
        result = ""
        for element in raw_paragraph:
            result += etree.tostring(element, method="html", encoding="utf-8").decode("utf-8")

        # TODO: zadnji paragraf daje dvostruke redove
        print(result)

        print(f"{final_gospel} {final_chapter}, {final_paragraph + 1}/{total_paragraphs}")

    except Exception as e:
        print("An error occurred:", e)


if __name__ == "__main__":
    main()
