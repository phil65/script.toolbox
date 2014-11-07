import sys
import os
import xbmc
import xbmcgui
import xbmcaddon
import urlparse
import urllib

__addon__ = xbmcaddon.Addon()
__addonid__ = __addon__.getAddonInfo('id')
__addonversion__ = __addon__.getAddonInfo('version')
__language__ = __addon__.getLocalizedString
__cwd__ = __addon__.getAddonInfo('path').decode("utf-8")
__resource__ = xbmc.translatePath(os.path.join(__cwd__, 'resources', 'lib')).decode("utf-8")
sys.path.append(__resource__)

from Utils import *

homewindow = xbmcgui.Window(10000)
Addon_Data_Path = os.path.join(xbmc.translatePath("special://profile/addon_data/%s" % __addonid__).decode("utf-8"))
Skin_Data_Path = os.path.join(xbmc.translatePath("special://profile/addon_data/%s" % xbmc.getSkinDir()).decode("utf-8"))


class Main:

    def __init__(self):
        log("version %s started" % __addonversion__)
        xbmc.executebuiltin('SetProperty(toolbox_running,True,home)')
        self._init_vars()
        self._parse_argv()
        if self.infos:
            self._StartInfoActions()
  #       elif self.exportsettings:
  #           export_skinsettings()
  #       elif self.importsettings:
  #           import_skinsettings()
  #       elif self.importextrathumb:
  #           AddArtToLibrary("extrathumb", "Movie", "extrathumbs", extrathumb_limit, True)
  #       elif self.importextrafanart:
  #           AddArtToLibrary("extrafanart", "Movie", "extrafanart", extrafanart_limit, True)
  #  #     elif self.importextrathumbtv:
  # #          AddArtToLibrary("extrathumb","TVShow","extrathumbs")
  #       elif self.importextrafanarttv:
  #           AddArtToLibrary("extrafanart", "TVShow", "extrafanart", extrafanart_limit, True)
  #       elif self.importallartwork:
  #           AddArtToLibrary("extrathumb", "Movie", "extrathumbs", extrathumb_limit, True)
  #           AddArtToLibrary("extrafanart", "Movie", "extrafanart", extrafanart_limit, True)
  #           AddArtToLibrary("extrafanart", "TVShow", "extrafanart", extrafanart_limit, True)
        elif not len(sys.argv) > 1:
            self._selection_dialog()
        if self.control == "plugin":
            xbmcplugin.endOfDirectory(self.handle)
        xbmc.executebuiltin('ClearProperty(toolbox_running,home)')

    def _StartInfoActions(self):
        for info in self.infos:
            if info == 'channels':
                channels = create_channel_list()
                prettyprint(channels)
            elif info == 'favourites':
                if self.id:
                    favourites = GetFavouriteswithType(self.id)
                else:
                    favourites = GetFavourites()
                    homewindow.setProperty('favourite.count', str(len(favourites)))
                    if len(favourites) > 0:
                        homewindow.setProperty('favourite.1.name', favourites[-1]["Label"])
                passDataToSkin('Favourites', favourites, self.prop_prefix, self.window, self.control, self.handle)
            elif info == 'playliststats':
                GetPlaylistStats(self.id)
            elif info == 'selectdialog':
                CreateDialogSelect(self.header)
            elif info == 'okdialog':
                CreateDialogOK(self.header, self.text)
            elif info == 'yesnodialog':
                CreateDialogYesNo(self.header, self.text, self.nolabel, self.yeslabel, self.noaction, self.yesaction)
            elif info == 'notification':
                CreateNotification(self.header, self.text, self.icon, self.time, self.sound)
            elif info == "sortletters":
                listitems = GetSortLetters(self.path, self.id)
                passDataToSkin('SortLetters', listitems, self.prop_prefix, self.window, self.control, self.handle)
            # elif info == 'slideshow':
            #     windowid = xbmcgui.getCurrentWindowId()
            #     Window = xbmcgui.Window(windowid)
            #     focusid = Window.getFocusId()
            #     itemlist = Window.getFocus()
            #     numitems = itemlist.getSelectedPosition()
            #     log("items:" + str(numitems))
            #     for i in range(0, numitems):
            #         pass
            elif info == 'jumptoletter':
                JumpToLetter(self.id)
            elif info == 'blur':
                homewindow.clearProperty('ImageFilter')
                image = Filter_Image(self.id)
                homewindow.setProperty('ImageFilter', image)

    def _init_vars(self):
        self.window = xbmcgui.Window(10000)  # Home Window
        self.control = None
        self.infos = []
        self.id = ""
        self.header = ""
        self.text = ""
        self.yeslabel = ""
        self.yesaction = ""
        self.nolabel = ""
        self.noaction = ""
        self.icon = ""
        self.sound = True
        self.time = 5000
        self.autoclose = ""

    def _parse_argv(self):
        args = sys.argv
        for arg in args:
            log(arg)
            if arg == 'script.toolbox':
                continue
            elif arg.startswith('info='):
                self.infos.append(arg[5:])
            elif arg.startswith('id='):
                self.id = arg[3:]
            elif arg.startswith('header='):
                self.header = arg[7:]
            elif arg.startswith('text='):
                self.text = arg[5:]
            elif arg.startswith('yeslabel='):
                self.yeslabel = arg[9:]
            elif arg.startswith('nolabel='):
                self.nolabel = arg[8:]
            elif arg.startswith('yesaction='):
                self.yesaction = arg[10:]
            elif arg.startswith('noaction='):
                self.noaction = arg[9:]
            elif arg.startswith('icon='):
                self.icon = arg[5:]
            elif arg.startswith('sound='):
                if "false" in arg or "False" in arg:
                    self.sound = False
            elif arg.startswith('time='):
                self.time = int(arg[5:])
            elif arg.startswith('window='):
                if arg[7:] == "currentdialog":
                    xbmc.sleep(300)
                    self.window = xbmcgui.Window(xbmcgui.getCurrentWindowDialogId())
                elif arg[7:] == "current":
                    xbmc.sleep(300)
                    self.window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
                else:
                    self.window = xbmcgui.Window(int(arg[7:]))
            elif arg.startswith('control='):
                self.control = int(arg[8:])

    def _selection_dialog(self):
        modeselect = []
        modeselect.append(__language__(32001))
        modeselect.append(__language__(32002))
        modeselect.append(__language__(32003))
        modeselect.append(__language__(32014))
        modeselect.append(__language__(32015))
     #   modeselect.append( __language__(32014) + " (TV)" )
        modeselect.append(__language__(32015) + " (TV)")
        modeselect.append("Update All")
        dialogSelection = xbmcgui.Dialog()
        selection = dialogSelection.select(__language__(32004), modeselect)
        if selection == 0:
            export_skinsettings()
        elif selection == 1:
            import_skinsettings()
        elif selection == 2:
            xbmc.executebuiltin("Skin.ResetSettings")
        elif selection == 3:
            AddArtToLibrary("extrathumb", "Movie", "extrathumbs", extrathumb_limit)
        elif selection == 4:
            AddArtToLibrary("extrafanart", "Movie", "extrafanart", extrafanart_limit)
   #     elif selection == 5:
    #        AddArtToLibrary("extrathumb","TVShow", "extrathumbs")
        elif selection == 5:
            AddArtToLibrary("extrafanart", "TVShow", "extrafanart", extrafanart_limit)
        elif selection == 6:
            AddArtToLibrary("extrathumb", "Movie", "extrathumbs", extrathumb_limit)
            AddArtToLibrary("extrafanart", "Movie", "extrafanart", extrafanart_limit)
            AddArtToLibrary("extrafanart", "TVShow", "extrafanart", extrafanart_limit)


if (__name__ == "__main__"):
    Main()
log('finished')
