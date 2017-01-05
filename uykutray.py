# encoding: utf-8
# Some of codes from happyMaker (https://github.com/happyMaker/mutuke/blob/master/win-client/win32gui_taskbar.py)
import win32api, win32gui
import win32con, winerror
import sys, os

class MainWindow:
	def __init__(self):
		msg_TaskbarRestart = win32gui.RegisterWindowMessage("TaskbarOlustur");
		message_map = {
				msg_TaskbarRestart: self.OnRestart,
				win32con.WM_DESTROY: self.OnDestroy,
				win32con.WM_COMMAND: self.OnCommand,
				win32con.WM_USER+20 : self.OnTaskbarNotify,
		}

		wc = win32gui.WNDCLASS()
		hinst = wc.hInstance = win32api.GetModuleHandle(None)
		wc.lpszClassName = "murat"
		wc.style = win32con.CS_VREDRAW | win32con.CS_HREDRAW;
		wc.hCursor = win32api.LoadCursor( 0, win32con.IDC_ARROW )
		wc.hbrBackground = win32con.COLOR_WINDOW
		wc.lpfnWndProc = message_map 

		try:
			classAtom = win32gui.RegisterClass(wc)
		except win32gui.error, err_info:
			if err_info.winerror!=winerror.ERROR_CLASS_ALREADY_EXISTS:
				raise

		style = win32con.WS_OVERLAPPED | win32con.WS_SYSMENU
		self.hwnd = win32gui.CreateWindow( wc.lpszClassName, u"muratwin", style, \
				0, 0, win32con.CW_USEDEFAULT, win32con.CW_USEDEFAULT, \
				0, 0, hinst, None)
		win32gui.UpdateWindow(self.hwnd)
		self._DoCreateIcons()
	def _DoCreateIcons(self):
		hinst =  win32api.GetModuleHandle(None)
		iconPathName = os.path.realpath("icon.ico")
		#iconPathName = os.path.abspath(os.path.join( os.path.split(sys.executable)[0], "pyc.ico" ))
		'''
		if not os.path.isfile(iconPathName):
			iconPathName = os.path.abspath(os.path.join( os.path.split(sys.executable)[0], "DLLs", "pyc.ico" ))
		if not os.path.isfile(iconPathName):
			iconPathName = os.path.abspath(os.path.join( os.path.split(sys.executable)[0], "..\\PC\\pyc.ico" ))
		'''
		#if os.path.isfile(iconPathName):
		icon_flags = win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
		hicon = win32gui.LoadImage(hinst, iconPathName, win32con.IMAGE_ICON, 0, 0, icon_flags)
		'''
		else:
			print "ikon bulunamadı, default ikon kullanılıyor"
			hicon = win32gui.LoadIcon(0, win32con.IDI_APPLICATION)
		'''
		flags = win32gui.NIF_ICON | win32gui.NIF_MESSAGE | win32gui.NIF_TIP
		nid = (self.hwnd, 0, flags, win32con.WM_USER+20, hicon, u"Uyku Modu")
		try:
			win32gui.Shell_NotifyIcon(win32gui.NIM_ADD, nid)
			win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, \
                         (self.hwnd, 0, win32gui.NIF_INFO, win32con.WM_USER+20,\
                          hicon, "Balloon  tooltip",u"Kullanmak için sağ tıklayın",200,u"Uyku Modu Değiştirici"))
		except win32gui.error:
			print u"İkon eklenemedi - explorer çalışıyor mu?"

	def OnRestart(self, hwnd, msg, wparam, lparam):
		self._DoCreateIcons()

	def OnDestroy(self, hwnd, msg, wparam, lparam):
		nid = (self.hwnd, 0)
		win32gui.Shell_NotifyIcon(win32gui.NIM_DELETE, nid)
		win32gui.PostQuitMessage(0)

	def OnTaskbarNotify(self, hwnd, msg, wparam, lparam):
		if lparam==win32con.WM_LBUTTONUP:
			print u"Tık"
		elif lparam==win32con.WM_LBUTTONDBLCLK:
			print u"Çift Tık"
			nid = (self.hwnd, 0)
			hicon = win32gui.LoadImage(win32api.GetModuleHandle(None), os.path.realpath("icon.ico"), win32con.IMAGE_ICON, 0, 0, win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE)
			win32gui.Shell_NotifyIcon(win32gui.NIM_MODIFY, \
                         (self.hwnd, 0, win32gui.NIF_INFO, win32con.WM_USER+20,\
                          hicon, "Balloon  tooltip",u"Bu ikona sağ tıklayın.",200,u"Kullanım"))
			
		elif lparam==win32con.WM_RBUTTONUP:
			print u"Sağ Tık"
			menu = win32gui.CreatePopupMenu()
			win32gui.AppendMenu( menu, win32con.MF_STRING, 1023, u"Hiçbir zaman")
			win32gui.AppendMenu( menu, win32con.MF_STRING, 1024, u"20 dakika")
			win32gui.AppendMenu (menu, win32con.MF_SEPARATOR, 0, '')
			win32gui.AppendMenu( menu, win32con.MF_STRING, 1025, u"Çıkış" )
			pos = win32gui.GetCursorPos()
			win32gui.SetForegroundWindow(self.hwnd)
			win32gui.TrackPopupMenu(menu, win32con.TPM_LEFTALIGN, pos[0], pos[1], 0, self.hwnd, None)
			win32gui.PostMessage(self.hwnd, win32con.WM_NULL, 0, 0)
		return 1

	def OnCommand(self, hwnd, msg, wparam, lparam):
		id = win32api.LOWORD(wparam)
		if id == 1023:
                        os.system("powercfg -x standby-timeout-ac 0")
		elif id == 1024:
			os.system("powercfg -x standby-timeout-ac 20")
		elif id == 1025:
			print u"Kapat"
			win32gui.DestroyWindow(self.hwnd)
		else:
			print "Bilinmeyen komut -", id
		
def winmain():
	w=MainWindow()
	win32gui.PumpMessages()

if __name__=='__main__':
	winmain()
