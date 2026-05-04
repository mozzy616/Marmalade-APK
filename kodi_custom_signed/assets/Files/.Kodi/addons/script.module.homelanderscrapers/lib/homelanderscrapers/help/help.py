# -*- coding: utf-8 -*-
"""
	Fenomscrapers Module
"""

from homelanderscrapers.modules.control import addonPath, addonVersion, joinPath
from homelanderscrapers.windows.textviewer import TextViewerXML


def get(file):
	homelanderscrapers_path = addonPath()
	homelanderscrapers_version = addonVersion()
	helpFile = joinPath(homelanderscrapers_path, 'lib', 'homelanderscrapers', 'help', file + '.txt')
	r = open(helpFile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]homelanderscrapers -  v%s - %s[/B]' % (homelanderscrapers_version, file)
	windows = TextViewerXML('textviewer.xml', homelanderscrapers_path, heading=heading, text=text)
	windows.run()
	del windows