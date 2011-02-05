# -*- coding: utf-8 -*-
#
# Author: Ingelrest François (Francois.Ingelrest@gmail.com)
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Library General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA

import gtk

from tools import consts, prefs


DEFAULT_VIEW_MODE       = consts.VIEW_MODE_FULL
DEFAULT_PANED_POS       = 320
DEFAULT_WIN_WIDTH       = 930
DEFAULT_WIN_HEIGHT      = 568
DEFAULT_MAXIMIZED_STATE = False


class MainWindow:

    def __init__(self, wtree, window):
        """ Constructor """
        self.wtree  = wtree
        self.paned  = wtree.get_widget('pan-main')
        self.window = window

        # Enable the right radio menu button
        viewmode = prefs.get(__name__, 'view-mode', DEFAULT_VIEW_MODE)

        if viewmode == consts.VIEW_MODE_FULL:       self.wtree.get_widget('menu-mode-full').set_active(True)
        elif viewmode == consts.VIEW_MODE_LEAN:     self.wtree.get_widget('menu-mode-lean').set_active(True)
        elif viewmode == consts.VIEW_MODE_MINI:     self.wtree.get_widget('menu-mode-mini').set_active(True)
        elif viewmode == consts.VIEW_MODE_PLAYLIST: self.wtree.get_widget('menu-mode-playlist').set_active(True)

        # Restore the size and the state of the window
        if prefs.get(__name__, 'win-is-maximized', DEFAULT_MAXIMIZED_STATE):
            self.window.maximize()

        savedWidth  = prefs.get(__name__, 'win-width', DEFAULT_WIN_WIDTH)
        savedHeight = prefs.get(__name__, 'win-height', DEFAULT_WIN_HEIGHT)
        savedPanPos = prefs.get(__name__, 'paned-pos', DEFAULT_PANED_POS)

        self.window.resize(savedWidth, savedHeight)
        self.paned.set_position(savedPanPos)
        self.window.show_all()

        # Restore the view mode
        # We set the mode to VIEW_MODE_FULL in the preferences because the window is currently in this mode (initial startup state)
        prefs.set(__name__, 'view-mode', consts.VIEW_MODE_FULL)
        self.setViewMode(viewmode)

        # Restore once again the size (may have been modified while restoring the view mode)
        self.window.resize(savedWidth, savedHeight)
        self.paned.set_position(savedPanPos)

        # Finally connect the event handlers
        self.window.connect('delete-event', self.onDelete)
        self.window.connect('size-allocate', self.onResize)
        self.window.connect('window-state-event', self.onState)

        self.wtree.get_widget('menu-mode-mini').connect('activate', self.onViewMode, consts.VIEW_MODE_MINI)
        self.wtree.get_widget('menu-mode-full').connect('activate', self.onViewMode, consts.VIEW_MODE_FULL)
        self.wtree.get_widget('menu-mode-lean').connect('activate', self.onViewMode, consts.VIEW_MODE_LEAN)
        self.wtree.get_widget('menu-mode-playlist').connect('activate', self.onViewMode, consts.VIEW_MODE_PLAYLIST)

        self.wtree.get_widget('menu-help').connect('activate', self.onHelp)
        self.wtree.get_widget('menu-about').connect('activate', self.onAbout)
        self.wtree.get_widget('menu-preferences').connect('activate', self.onShowPreferences)
        self.wtree.get_widget('menu-quit').connect('activate', lambda item: self.onDelete(window, None))
        self.wtree.get_widget('pan-main').connect('size-allocate', lambda win, rect: prefs.set(__name__, 'paned-pos', self.paned.get_position()))


    def setViewMode(self, mode):
        """ Change the view mode to the given one """
        currMode = prefs.get(__name__, 'view-mode', DEFAULT_VIEW_MODE)

        # Give up if the new mode is the same as the current one
        if currMode == mode:
            return

        # First restore the initial window state (e.g., VIEW_MODE_FULL)
        if currMode == consts.VIEW_MODE_LEAN:       self.__fromModeLean()
        elif currMode == consts.VIEW_MODE_MINI:     self.__fromModeMini()
        elif currMode == consts.VIEW_MODE_PLAYLIST: self.__fromModePlaylist()

        # Now we can switch to the new mode
        if mode == consts.VIEW_MODE_LEAN:       self.__toModeLean()
        elif mode == consts.VIEW_MODE_MINI:     self.__toModeMini()
        elif mode == consts.VIEW_MODE_PLAYLIST: self.__toModePlaylist()

        # Save the new mode
        prefs.set(__name__, 'view-mode', mode)


    # --== Lean Mode ==--

    def __fromModeLean(self):
        """ Switch from lean mode to full mode """
        self.wtree.get_widget('box-btn-tracklist').show()


    def __toModeLean(self):
        """ Switch from full mode to lean mode """
        self.wtree.get_widget('box-btn-tracklist').hide()


    # --== Mini Mode ==--

    def __fromModeMini(self):
        """ Switch from playlist mode to mini mode """
        self.paned.get_child1().show()
        self.wtree.get_widget('statusbar').show()
        self.wtree.get_widget('box-btn-tracklist').show()
        self.wtree.get_widget('scrolled-tracklist').show()

        (winWidth, winHeight) = self.window.get_size()
        self.window.resize(winWidth + self.paned.get_position(), prefs.get(__name__, 'full-win-height', 470))


    def __toModeMini(self):
        """ Switch from full mode to mini mode """
        self.paned.get_child1().hide()
        self.wtree.get_widget('statusbar').hide()
        self.wtree.get_widget('box-btn-tracklist').hide()
        self.wtree.get_widget('scrolled-tracklist').hide()

        (winWidth, winHeight) = self.window.get_size()
        self.window.resize(winWidth - self.paned.get_position(), 1)


    # --== Playlist Mode ==--

    def __fromModePlaylist(self):
        """ Switch from playlist mode to full mode """
        (winWidth, winHeight) = self.window.get_size()
        winWidth = winWidth + self.paned.get_position()
        self.window.resize(winWidth, winHeight)

        self.paned.get_child1().show()
        self.wtree.get_widget('box-btn-tracklist').show()


    def __toModePlaylist(self):
        """ Switch from full mode to playlist mode """
        (winWidth, winHeight) = self.window.get_size()
        winWidth = winWidth - self.paned.get_position()
        self.window.resize(winWidth, winHeight)

        self.paned.get_child1().hide()
        self.wtree.get_widget('box-btn-tracklist').hide()


    # --== GTK Handlers ==--


    def onResize(self, win, rect):
        """ Save the new size of the window """
        # The first status label gets more or less a third of the window's width
        self.wtree.get_widget('hbox-status1').set_size_request(rect.width / 3 + 15, -1)

        # Save size and maximized state
        if win.window is not None and not win.window.get_state() & gtk.gdk.WINDOW_STATE_MAXIMIZED:
            prefs.set(__name__, 'win-width',  rect.width)
            prefs.set(__name__, 'win-height', rect.height)

            if prefs.get(__name__, 'view-mode', DEFAULT_VIEW_MODE) != consts.VIEW_MODE_MINI:
                prefs.set(__name__, 'full-win-height', rect.height)


    def onState(self, win, evt):
        """ Save the new state of the window """
        prefs.set(__name__, 'win-is-maximized', bool(evt.new_window_state & gtk.gdk.WINDOW_STATE_MAXIMIZED))


    def onViewMode(self, item, mode):
        """ Wrapper for setViewMode() """
        if item.get_active():
            self.setViewMode(mode)


    def onDelete(self, win, event):
        """ Use our own quit sequence, that will itself destroy the window """
        import modules

        win.hide()
        modules.postQuitMsg()

        return True


    def onShowPreferences(self, item):
        """ Show preferences """
        import modules

        modules.showPreferences()


    def onAbout(self, item):
        """ Show the about dialog box """
        import gui.about

        gui.about.show(self.window)


    def onHelp(self, item):
        """ Show help page in the web browser """
        import webbrowser

        webbrowser.open(consts.urlHelp)
