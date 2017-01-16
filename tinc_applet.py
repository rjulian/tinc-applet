#!/usr/bin/python3
# tinc-vpn applet
# Creates a taskbar applet that lists all connected nodes in the menu and provides information for each node in Notifications.
# Copyright 2017, rjulian (https://github.com/rjulian)
#
# tinc-applet is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by the Free Software
# Foundation, either version 3 of the License, or (at your option) any later version.
#
# tinc-applet is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
# without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along with tinc-applet.
# If not, see <http://www.gnu.org/licenses/>.

import signal
import json
import os
import sys

from gi.repository import GLib as glib
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify

APPINDICATOR_ID = 'tinc-applet'

ICON_PATH = os.path.dirname(os.path.abspath(__file__)) + '/img/helicopter-green-icon.svg'
# helicopter icon courtesy of wikipedia user André437 !

if not os.geteuid() == 0:
    sys.exit('Must be root!')

class TincAppletIndicator(object):
    def __init__(self):
        self.first_run = True
        indicator = appindicator.Indicator.new(APPINDICATOR_ID, ICON_PATH, appindicator.IndicatorCategory.SYSTEM_SERVICES)
        indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
        indicator.set_menu(self.build_menu())

        ## Update indicator every x seconds with newly discovered/removed nodes.
        glib.timeout_add_seconds(300, self.indicator_refresh, indicator)
        notify.init(APPINDICATOR_ID)
        gtk.main()

    def indicator_refresh(self, indicator):
        indicator.set_menu(self.build_menu())
        return True

    def build_menu(self):
        menu = gtk.Menu()
        node_menu = gtk.Menu()
        item_nodes = gtk.MenuItem('Connected Nodes')
        item_nodes.set_submenu(node_menu)
        menu.append(item_nodes)
        self.update_nodes_menu(node_menu)
        item_restart = gtk.MenuItem('Restart')
        item_restart.connect('activate', self.restart)
        menu.append(item_restart)
        item_quit = gtk.MenuItem('Quit')
        item_quit.connect('activate', self.quit)
        menu.append(item_quit)
        menu.show_all()
        return menu

    def update_nodes_menu(self,menu):
        print("Updating nodes!")
        new_nodes = self.get_reachable_nodes()
        for new_node in new_nodes:
            item_node = gtk.MenuItem(new_node)
            menu.append(item_node)
        if self.first_run == True:
            self.first_run = False
        else:
            intro_nodes, removed_nodes = self.diff_updated_nodes(new_nodes,self.old_nodes)
            self.notify_new_or_removed_nodes(intro_nodes, removed_nodes)
        self.old_nodes = new_nodes
        return True

    def diff_updated_nodes(self, new_nodes, old_nodes):
        if old_nodes:
            newer_nodes = [new_node for new_node in new_nodes if new_node not in old_nodes]
            removed_nodes = [removed_node for removed_node in old_nodes if removed_node not in new_nodes]
            return (newer_nodes, removed_nodes)

    def notify_new_or_removed_nodes(self, intro_nodes, removed_nodes):
        for node in intro_nodes:
            notify.Notification.new("New Node Reachable", node, None).show()
        for node in removed_nodes:
            notify.Notification.new("Node Now Unreachable", node, None).show()

    def get_reachable_nodes(self):
        reachable_stream = os.popen("tinc dump reachable nodes | cut -d' ' -f1")
        nodes = reachable_stream.read().splitlines()
        return nodes

    def restart(self, state):
        """ Has tinc restart itself """
        notify.uninit()
        print("Restarting Tinc: exec tincd restart")

    def quit(self, state):
        notify.uninit()
        print("Quitting!")
        gtk.main_quit()


def main():
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    TincAppletIndicator()

if __name__ == "__main__":
    main()
