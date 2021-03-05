# Close Window
# ============
#
# Copyright 2021 Florian Pircher
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import objc
from AppKit import (
    NSEventModifierFlagCommand,
    NSEventModifierFlagShift,
    NSMenuItem,
)
from GlyphsApp import (Glyphs, FILE_MENU, VIEW_MENU)
from GlyphsApp.plugins import GeneralPlugin


class CloseWindow(GeneralPlugin):
    @objc.python_method
    def settings(self):
        self.name = Glyphs.localize({
            "ar": "إغلاق نافذ",
            "cs": "Zavřít okno",
            "de": "Fenster schließen",
            "en": "Close Window",
            "es": "Cerrar ventana",
            "fr": "Fermer la fenêtre",
            "it": "Chiudi la finestra",
            "ja": "ウインドウを閉じる",
            "ko": "창 닫기",
            "pt": "Fechar Janela",
            "ru": "Закрыть окно",
            "tr": "Pencereyi kapat",
            "zh-Hans": "关闭窗口",
            "zh-Hant": "關閉視窗",
        })

    @objc.python_method
    def start(self):
        closeWindowMenuItem = CloseWindowMenuItem.new()
        closeWindowMenuItem.setTitle_(self.name)
        closeWindowMenuItem.setTarget_(self)
        closeWindowMenuItem.setAction_(self.closeWindow_)

        if not Glyphs.defaults["com.FlorianPircher.CloseWindow.retainKeyboardEquivalent"]:
            viewMenuItem = Glyphs.menu[VIEW_MENU]
            viewMenu = viewMenuItem.submenu()
            closeTabMenuItemIndex = viewMenu.indexOfItemWithTarget_andAction_(None, "closeEditPage:")

            if closeTabMenuItemIndex != -1:
                closeTabMenuItem = viewMenu.itemAtIndex_(closeTabMenuItemIndex)
                closeTabMenuItem.setKeyEquivalent_("")
                closeTabMenuItem.setKeyEquivalentModifierMask_(0)

            closeWindowMenuItem.setKeyEquivalent_("W")
            closeWindowMenuItem.setKeyEquivalentModifierMask_(NSEventModifierFlagShift | NSEventModifierFlagCommand)

        fileMenuItem = Glyphs.menu[FILE_MENU]
        fileMenu = fileMenuItem.submenu()
        closeMenuItemIndex = fileMenu.indexOfItemWithTarget_andAction_(None, "performClose:")

        if closeMenuItemIndex != -1:
            fileMenu.insertItem_atIndex_(closeWindowMenuItem, closeMenuItemIndex + 1)
        else:
            fileMenu.addItem_(closeWindowMenuItem)

    def closeWindow_(self, sender):
        if Glyphs.font:
            Glyphs.font.close()

    @ objc.python_method
    def __file__(self):
        """Please leave this method unchanged"""
        return __file__


class CloseWindowMenuItem(NSMenuItem):
    def isEnabled(self):
        return Glyphs.font is not None
