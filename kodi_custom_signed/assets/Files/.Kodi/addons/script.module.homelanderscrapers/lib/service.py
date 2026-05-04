# -*- coding: utf-8 -*-
"""
	Fenomscrapers Module
"""

import xbmc
from homelanderscrapers.modules import control
from homelanderscrapers.modules.Thread_pool import shutdown_executor
window = control.homeWindow
LOGINFO = 1 # (LOGNOTICE(2) deprecated in 19, use LOGINFO(1))

class CheckSettingsFile:
	def run(self):
		try:
			xbmc.log('[ script.module.homelanderscrapers ]  CheckSettingsFile Service Starting...', LOGINFO)
			window.clearProperty('homelanderscrapers')
			profile_dir = control.dataPath
			if not control.existsPath(profile_dir):
				success = control.makeDirs(profile_dir)
				if success: xbmc.log('%s : created successfully' % profile_dir, LOGINFO)
			else: xbmc.log('%s : already exists' % profile_dir, LOGINFO)
			settings_xml = control.joinPath(profile_dir, 'settings.xml')
			if not control.existsPath(settings_xml):
				control.setSetting('module.provider', 'homelanderscrapers')
				xbmc.log('%s : created successfully' % settings_xml, LOGINFO)
			else: xbmc.log('%s : already exists' % settings_xml, LOGINFO)
			return xbmc.log('[ script.module.homelanderscrapers ]  Finished CheckSettingsFile Service', LOGINFO)
		except:
			import traceback
			traceback.print_exc()

class SettingsMonitor(control.monitor_class):
	def __init__ (self):
		control.monitor_class.__init__(self)
		window.setProperty('homelanderscrapers.debug.reversed', control.setting('debug.reversed'))
		xbmc.log('[ script.module.homelanderscrapers ]  Settings Monitor Service Starting...', LOGINFO)

	def onSettingsChanged(self): # Kodi callback when the addon settings are changed
		window.clearProperty('homelanderscrapers')
		control.sleep(50)
		refreshed = control.make_settings_dict()
		control.refresh_debugReversed()

class CheckUndesirablesDatabase:
	def run(self):
		xbmc.log('[ script.module.homelanderscrapers ]  "CheckUndesirablesDatabase" Service Starting...', LOGINFO)
		from homelanderscrapers.modules import undesirables
		try:
			old_database = undesirables.Undesirables().check_database()
			if old_database: undesirables.add_new_default_keywords()
		except:
			import traceback
			traceback.print_exc()
		return xbmc.log('[ script.module.homelanderscrapers ]  Finished "CheckUndesirablesDatabase" Service', LOGINFO)

def main():
	while not control.monitor.abortRequested():
		xbmc.log('[ script.module.homelanderscrapers ]  Service Started', LOGINFO)
		CheckSettingsFile().run()
		CheckUndesirablesDatabase().run()
		if control.isVersionUpdate():
			control.clean_settings()
			xbmc.log('[ script.module.homelanderscrapers ]  Settings file cleaned complete', LOGINFO)
		break
	SettingsMonitor().waitForAbort()
	shutdown_executor()
	xbmc.log('[ script.module.homelanderscrapers ]  Service Stopped', LOGINFO)

main()