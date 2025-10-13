<img src="source/resources/mechanic_icon.png"  width="80">

# Designspace Manager
A simple RoboFont extension to help link designspaces to your UFO.

![](source/resources/ui-main.png)

## Functionality

This extension is a user interface for storing paths to .designspace files in a UFO’s `public.designspaces` lib key. The paths stored in that lib key may be used by other tools for limitless purposes! For example, are you tired of making sure the designspace file corresponding to your UFO is open in Designspace Editor before you run a tool like, say, Prepolator? Using this key, a tool can intuit which designspace to reference based on the associations you set up in your UFO.

### User Interface
- A button is added to your **Font Overview** toolbar.
- Clicking the button opens up a sheet with a table showing all of the Designspace files linked to your UFO.
- You can:
	- Drag and drop designspace files from **Finder** into this table.
	- Add or remove items with the (+/-) buttons.
	- Remove items by selecting them and hitting the **Delete** key on your keyboard.
	- Reorder items in the table to show priority, in case external tools only look at the first item in the list, for example.
	- Double-click items to open them in **[Designspace Editor](https://github.com/LettError/designSpaceRoboFontExtension)**.
- Changes are only applied if you click **Apply**.


## Acknowledgements

- RoboFont, Frederik Berlaen
- EZUI, Tal Leming
- Designspace Editor, Erik van Blokland
