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


__lbl               = None
__dirBtnIcon        = None
__dirMenuIcon       = None
__prefsBtnIcon      = None
__nullMenuIcon      = None
__playMenuIcon      = None
__pauseMenuIcon     = None
__cdromMenuIcon     = None
__errorMenuIcon     = None
__mediaDirMenuIcon  = None
__mediaFileMenuIcon = None


def __render(stock, size):
    """ Return the given stock icon rendered at the given size """
    global __lbl

    if __lbl is None:
        __lbl = gtk.Label()

    return __lbl.render_icon(stock, size)


def dirMenuIcon():
    """ Directories """
    global __dirMenuIcon

    if __dirMenuIcon is None:
        __dirMenuIcon = __render(gtk.STOCK_DIRECTORY, gtk.ICON_SIZE_MENU)

    return __dirMenuIcon


def dirBtnIcon():
    """ Directories """
    global __dirBtnIcon

    if __dirBtnIcon is None:
        __dirBtnIcon = __render(gtk.STOCK_DIRECTORY, gtk.ICON_SIZE_BUTTON)

    return __dirBtnIcon


def prefsBtnIcon():
    """ Preferences """
    global __prefsBtnIcon

    if __prefsBtnIcon is None:
        __prefsBtnIcon = __render(gtk.STOCK_PREFERENCES, gtk.ICON_SIZE_BUTTON)

    return __prefsBtnIcon


def playMenuIcon():
    """ Play """
    global __playMenuIcon

    if __playMenuIcon is None:
        __playMenuIcon = __render(gtk.STOCK_MEDIA_PLAY, gtk.ICON_SIZE_MENU)

    return __playMenuIcon


def pauseMenuIcon():
    """ Pause """
    global __pauseMenuIcon

    if __pauseMenuIcon is None:
        __pauseMenuIcon = __render(gtk.STOCK_MEDIA_PAUSE, gtk.ICON_SIZE_MENU)

    return __pauseMenuIcon


def cdromMenuIcon():
    """ CD-ROM """
    global __cdromMenuIcon

    if __cdromMenuIcon is None:
        __cdromMenuIcon = __render(gtk.STOCK_CDROM, gtk.ICON_SIZE_MENU)

    return __cdromMenuIcon


def errorMenuIcon():
    """ Error """
    global __errorMenuIcon

    if __errorMenuIcon is None:
        __errorMenuIcon = __render(gtk.STOCK_CANCEL, gtk.ICON_SIZE_MENU)

    return __errorMenuIcon


def nullMenuIcon():
    """ Transparent icon """
    global __nullMenuIcon

    if __nullMenuIcon is None:
        __nullMenuIcon = gtk.gdk.Pixbuf(gtk.gdk.COLORSPACE_RGB, True, 8, 16, 16)
        __nullMenuIcon.fill(0x00000000)

    return __nullMenuIcon


def mediaDirMenuIcon():
    """ Media directory """
    global __mediaDirMenuIcon

    if __mediaDirMenuIcon is None:
        __mediaDirMenuIcon = dirMenuIcon().copy()  # We need a copy to modify it
        cdromMenuIcon().composite(__mediaDirMenuIcon, 5, 5, 11, 11, 5, 5, 0.6875, 0.6875, gtk.gdk.INTERP_HYPER, 255)

    return __mediaDirMenuIcon


def mediaFileMenuIcon():
    """ Media file """
    global __mediaFileMenuIcon

    if __mediaFileMenuIcon is None:
        __mediaFileMenuIcon = __render(gtk.STOCK_FILE, gtk.ICON_SIZE_MENU).copy()  # We need a copy to modify it
        cdromMenuIcon().composite(__mediaFileMenuIcon, 5, 5, 11, 11, 5, 5, 0.6875, 0.6875, gtk.gdk.INTERP_HYPER, 255)

    return __mediaFileMenuIcon