# -*- coding: utf-8 -*-
"""
	Fenomscrapers Module
"""

from homelanderscrapers.modules.control import addonPath, addonVersion, joinPath
from homelanderscrapers.windows.textviewer import TextViewerXML


def get():
	homelanderscrapers_path = addonPath()
	homelanderscrapers_version = addonVersion()
	changelogfile = joinPath(homelanderscrapers_path, 'changelog.txt')
	r = open(changelogfile, 'r', encoding='utf-8', errors='ignore')
	text = r.read()
	r.close()
	heading = '[B]homelanderscrapers -  v%s - ChangeLog[/B]' % homelanderscrapers_version
	windows = TextViewerXML('textviewer.xml', homelanderscrapers_path, heading=heading, text=text)
	windows.run()
	del windows