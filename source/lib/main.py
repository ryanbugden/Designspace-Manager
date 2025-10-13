# menuTitle: Designspace Manager

import ezui
from mojo.UI import CurrentFontWindow, GetFile
from mojo.subscriber import Subscriber, registerRoboFontSubscriber
from mojo.extensions import ExtensionBundle
from mojo.roboFont import version


'''
Ryan Bugden
2025.10.13
'''


BUNDLE = ExtensionBundle("Designspace Manager")
ICON_NAME = "icon-old" if version < "5" else "icon-new"
TOOLBAR_ICON = BUNDLE.getResourceImage(ICON_NAME)
LIB_KEY = "public.designspaces"


class DesignspaceManagerController(ezui.WindowController):
    '''
    This is a sheet that contains a table consisting of all 
    designspace file paths that are associated with your UFO.
    '''

    def build(self, parent):
        window = parent.w
        self.f = RFont(parent._font, showInterface=False)
        content = """
        |-files----| @fileTable
        |          |
        |----------|
        > (+-)       @fileTableAddRemoveButton
        
        ---
        ===
        
        (?)          @helpButton
        (Apply)      @applyButton
        (Close)      @closeButton
        """
        descriptionData = dict(
            fileTable=dict(
                width='fill',
                height='fill',
                itemType="dict",
                showColumnTitles=True,
                enableDelete=True,
                allowsDropBetweenRows=True,
                allowsInternalDropReordering=True,
                acceptedDropFileTypes=[".designspace"],
                columnDescriptions=[
                    dict(
                        identifier="path",
                        title="Designspace Paths",
                        cellClassArguments=dict(
                            showFullPath=True
                        )
                    )
                ]
            ),
            helpButton=dict(
                gravity="leading",
            )
        )
        self.w = ezui.EZSheet(
            content=content,
            size=(300, 300),
            minSize=(300, 200),
            maxSize=(600, 600),
            descriptionData=descriptionData,
            parent=window,
            controller=self,
            defaultButton="applyButton"
        )
        
    def started(self):
        self.load_stored_paths()
        self.w.open()
        
    def applyButtonCallback(self, sender):
        self.update_stored_paths()
        self.w.close()
        
    def closeButtonCallback(self, sender):
        self.w.close()
        
    def helpButtonCallback(self, sender):
        BUNDLE.openHelp()
        
    def load_stored_paths(self):
        if LIB_KEY not in self.f.lib:
            return
        stored_paths = self.f.lib[LIB_KEY]
        table = self.w.getItem("fileTable")
        items = [table.makeItem(path=path) for path in stored_paths]
        table.appendItems(items)
        
    def update_stored_paths(self):
        paths_dicts = self.w.getItem("fileTable").get()
        paths = [paths_dict["path"] for paths_dict in paths_dicts] 
        self.f.lib[LIB_KEY] = paths
        
    def fileTableCreateItemsForDroppedPathsCallback(self, sender, paths):
        items = []
        for path in paths:
            with open(path, "r") as f:
                lines = len(f.read().splitlines())
                item = dict(
                    path=path,
                    lines=lines
                )
                items.append(item)
        return items
        
    def fileTableAddRemoveButtonAddCallback(self, sender):
        table = self.w.getItem("fileTable")
        # get items from GetFile
        directory = self.f.path
        paths = GetFile(
            message="Add designspace file references to your UFO.", 
            directory=directory, 
            allowsMultipleSelection=True, 
            fileTypes=["designspace"]
        )
        existing_items = table.get() or []
        items = [table.makeItem(path=path) for path in paths if table.makeItem(path=path) not in existing_items]
        if items: table.appendItems(items)

    def fileTableAddRemoveButtonRemoveCallback(self, sender):
        table = self.w.getItem("fileTable")
        table.removeSelectedItems()
        
    def fileTableDeleteCallback(self, sender):
        table = self.w.getItem("fileTable")
        table.removeSelectedItems()
        
    def fileTableDoubleClickCallback(self, sender):
        table = self.w.getItem("fileTable")
        paths = [path_dict["path"] for path_dict in table.getSelectedItems()]
        for path in paths:
            OpenDesignspace(path)



class AddDMToolbarItem(Subscriber):
    '''
    Adds a button for Designspace Manager into the toolbar.
    '''

    def fontDocumentWantsToolbarItems(self, info):
        # Get the font document window
        self.fw = CurrentFontWindow()
        # Create the button and add it to the toolbar
        new_item = {'itemIdentifier': 'designspaceManager',
                   'label':           'Designspaces',
                   'toolTip':         'Designspaces',
                   'imageObject':     TOOLBAR_ICON,
                   'imageTemplate':   True,
                   'callback':        self.dm_button_callback}
        info['itemDescriptions'].insert(2, new_item)

    def dm_button_callback(self, sender):
        '''The button opens a sheet atop the Font Overview.'''
        parent = CurrentFontWindow()
        DesignspaceManagerController(parent)
        


if __name__ == '__main__':
    registerRoboFontSubscriber(AddDMToolbarItem)