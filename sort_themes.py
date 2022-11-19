"""In Mad Games Tycoon 2, primary language is German, so files in German have all the data.
But my guide language is English, and I want English themes list to be sorted correctly.
So my idea is to sort the English list, and then rearrange German file in the same order.
"""

def sort_themes(write_files = False):
    """Reads file "themes_en.txt", sorts it in alphabetical order, and then
    rearranges "themes_ge.txt" to be in the same order as "themes_en.txt".
    Sorted lists are then printed to "themes_en_SORTED.txt" and "themes_ge_SORTED.txt" respectively.
    """
    # Reading English and German files
    with open("themes_en.txt", "r", encoding='utf-16-le') as file:
        file.seek(2)  # Skipping first 2 bytes as they are always useless FEFF
        text_themes_en = file.read().split("\n")
    with open("themes_ge.txt", "r", encoding='utf-16-le') as file:
        file.seek(2)  # Skipping first 2 bytes as they are always useless FEFF
        text_themes_ge = file.read().split("\n")

    # Sorting English themes list
    text_themes_en_sorted = text_themes_en.copy()
    text_themes_en_sorted.sort()

    text_themes_ge_sorted = []
    for line in text_themes_en_sorted:
        text_themes_ge_sorted.append(text_themes_ge[text_themes_en.index(line)])

    if (not write_files):
        return text_themes_en_sorted, text_themes_ge_sorted
    # Writing German list in English sorted order
    with open("themes_ge_SORTED.txt", "w", encoding='utf-8') as file:
        file.write("\n".join(text_themes_ge_sorted))

    # Writing sorted English list
    with open("themes_en_SORTED.txt", "w", encoding='utf-8') as file:
        file.write("\n".join(text_themes_en_sorted))

if __name__ == "__main__":
    sort_themes(True)