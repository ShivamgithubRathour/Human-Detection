import matplotlib.font_manager

for font in matplotlib.font_manager.findSystemFonts(fontpaths=None, fontext='ttf'):
    if 'Rog' in font:
        print(font)
