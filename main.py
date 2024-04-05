import json

from lxml import etree


def get_number_of_verses(html_sinkopa):
    rows = html_sinkopa.xpath("//span[@class='brojRetka']")
    return int(rows[-1].text)


def main():
    try:
        with open('evangelion.json', 'r', encoding="utf-8") as file:
            data = json.load(file)

        # Prvi index: 0 - Matej, 1 - Marko, 2 - Luka, 3 - Ivan; data[0] ce dati Mt
        # Drugi index: 0 - Naslov, 1 - Tekst; data[0][1] je tekst Mt bez naslova
        # Treci index: Broj poglavlja - 1; data[0][1][4] je Mt 5
        # Cetvrti index: 0 - Naslov, 1 - Tekst
        print(data[3][1][0][1])
        print(len(data[3][1][0][1]))

        parser = etree.HTMLParser(encoding="utf-8")
        html_root = etree.fromstring(data[3][1][0][1], parser)
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
                    # current_paragraph.append(element)
                    # paragraph = current_paragraph
                    paragraphs.append(current_paragraph.copy())
                    print(f"PARAGRAPH ADDED, {len(current_paragraph)}")
                    current_paragraph.clear()

            # print(element.get('id'))
            # if element.get('id') == get_number_of_verses(html_root):
            #     current_paragraph.append(element)
            #     paragraphs.append(current_paragraph)

        print("Broj paragrafa je ", len(paragraphs))

        # para_html = etree.tostring(paragraphs[2][0], method="html", encoding="unicode")
        # print(para_html)
        # print("----------------------")

        # Print the paragraphs
        for paragraph in paragraphs:
            para_html = etree.tostring(paragraph[0], method="html", encoding="unicode")
            print(para_html)
            print("----------------------")

    except Exception as e:
        print("An error occurred:", e)


if __name__ == "__main__":
    main()
