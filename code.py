from adbkit import ADBTools
from cv2imshow.cv2imshow import cv2_imshow_multi
from kthread_sleep import sleep
from tserial import deviceserial
import numpy as np
from win10ctypestoast import show_toast

import cv2
from locate_pixelcolor_c import search_colors
def get_uiautomator_frame(screenshotfolder='c:\\ttscreenshots'):
	if screenshotfolder:
		adb.aa_update_screenshot()
	df = adb.aa_get_all_displayed_items_from_uiautomator(
		screenshotfolder=screenshotfolder,  # screenshots will be saved here
		max_variation_percent_x=10,
		# used for one of the click functions, to not click exactly in the center - more information below
		max_variation_percent_y=10,  # used for one of the click functions, to not click exactly in the center
		loung_touch_delay=(
			1000,
			1500,
		),  # with this settings longtouch will take somewhere between 1 and 1,5 seconds
		swipe_variation_startx=10,  # swipe coordinate variations in percent
		swipe_variation_endx=10,
		swipe_variation_starty=10,
		swipe_variation_endy=10,
		sdcard="/storage/emulated/0/",
		# sdcard will be used if you use the sendevent methods, don't pass a symlink - more information below
		tmp_folder_on_sd_card="AUTOMAT",  # this folder will be created in the sdcard folder for using sendevent actions
		bluestacks_divider=32767,
		# coordinates must be recalculated for BlueStacks https://stackoverflow.com/a/73733261/15096247 when using sendevent
	)
	return df

ADBTools.aa_kill_all_running_adb_instances()
adb_path = r'C:\ProgramData\chocolatey\bin\adb.exe'
adb = ADBTools(adb_path=adb_path, deviceserial=deviceserial)
adb.aa_start_server() # creates a new process which is not a child process
sleep(3)
adb.aa_connect_to_device()
sleep(3)
adb.aa_activate_scrcpy_screenshots_usb(adb_host_address="127.0.0.1",
                        adb_host_port=5037, lock_video_orientation=0)
adb.aa_show_screenshot()
sleep(3)
df = get_uiautomator_frame()
df.dropna(subset='bb_screenshot').ff_bb_save_screenshot.apply(lambda x:x())


def cropimage(img, coords):
	if sum(coords) != 0:
		return img[coords[1]: coords[3], coords[0]: coords[2]].copy()
	return img


coords = (190, 197, 721, 243)
color_ = list(reversed((10,140,104))) #104,140,10
color = np.array([color_],dtype=np.uint8)
while True:
	try:
		adb.aa_update_screenshot()
		sleep(0.01)
		crim = cropimage(img=adb.screenshot, coords=coords)
		cv2_imshow_multi(
			title="picx",
			image=crim,
			killkeys="ctrl+alt+z", 
		)
		sleep(0.01)
		howmany = search_colors(pic=crim.copy(), colors=[color])
		if (howmany.shape[0]) > 20000:

			show_toast(
				title="Filha online",
				message="Mande uma mensagem",

				duration=1,
				repeat=2,
				pause=2,
				threaded=False,
			)
	except Exception as fe:
		print(fe)
	except KeyboardInterrupt:
		break



















