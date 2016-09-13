#!/usr/bin/env python

import sys
import pickle
from gimpfu import *
#from subprocess import call
from os.path import expanduser
import time

from array import array

home = expanduser("~")
#kdctools_path = sys.path[0] + "/KDCTools"
sys.stderr = open(home + '/gimpstderr.txt', 'w')
sys.stdout = open(home + '/gimpstdout.txt', 'w')

BLOCK_COUNT = 2 # 128x128*2
block = 1

CMAPS = [
	(0,128,0,31,31,31,47,47,47,63,63,63,79,79,79,95,95,95,111,111,111,127,127,127,143,143,143,159,159,159,175,175,175,191,191,191,207,207,207,223,223,223,239,239,239,255,255,255) + (0,0,0)*240,
	(173,165,239,255,255,255,255,165,66,74,41,16,255,214,57,198,173,123,206,148,66,255,189,66,255,156,41,222,107,41,156,107,82,148,82,24,255,255,255,148,173,173,74,82,82,0,0,0) + (0,0,0)*240,
	(0,0,214,255,255,255,239,239,239,132,41,33,74,57,57,16,16,16,0,0,0,255,165,198,239, 156, 173,222,140,156,239,90,140,181,132,140,132,90,107,41,33,140,189,33,41,214,0,33) + (0,0,0)*240,
	(107,255,107,115,189,82,255,255,255,247,247,247,198,148,140,165,99,90,247,66,66,255,107,107,214,49,49,99,24,16,33,8,8,0,255,0,165,222,214,140,156,156,107,90,90,0,0,0) + (0,0,0)*240
]
#titlescreen
#scoreboard
#kirby-1
STUFF = {
	'0x076478': [0, "\xC7\x00\x6C\x00\x6C\x00\xE7\x00\xE1\x00\xE1\x00\xC1\x00\x00\x00\x87\x00\xCD\x00\xD9\x00\xD9\x00\xDF\x00\xC3\x00\x83\x00\x00\x00\x80\x00\x80\x00\x80\x00\x80\x00\xC0\x00\x80\x00\x80\x00\x00\x00\xFF\xFF\xFF\x81\xFF\xBD\xFF\xBD\xFF\xBD\xFF\xBD\xFF\x81\xFF\xFF\xFF\xFF\xFF\x81\xFF\xBD\xFF\xBD\xFF\xBD\xFF\xBD\xFF\x81\xFF\xFF\xFF\xFF\xFF\x81\xFF\xBD\xFF\xBD\xFF\xBD\xFF\xBD\xFF\x81\xFF\xFF\xFF\xFF\xFF\x81\xFF\xBD\xFF\xBD\xFF\xBD\xFF\xBD\xFF\x81\xFF\xFF\xFF\xFF\xFF\x81\xFF\xBD\xFF\xBD\xFF\xBD\xFF\xBD\xFF\x81\xFF\xFF\xFF\xFF\xFF\x81\xFF\xBD\xFF\xBD\xFF\xBD\xFF\xBD\xFF\x81\xFF\xFF\xFF\xFF\xFF\x81\xFF\xBD\xFF\xBD\xFF\xBD\xFF\xBD\xFF\x81\xFF\xFF\xFF\xFF\xFF\x81\xFF\xBD\xFF\xBD\xFF\xBD\xFF\xBD\xFF\x81\xFF\xFF\xFF\xFF\xFF\x81\xFF\xBD\xFF\xBD\xFF\xBD\xFF\xBD\xFF\x81\xFF\xFF\xFF\xFF\xFF\x81\xFF\xBD\xFF\xBD\xFF\xBD\xFF\xBD\xFF\x81\xFF\xFF\xFF\xFF\xFF\x81\xFF\xBD\xFF\xBD\xFF\xBD\xFF\xBD\xFF\x81\xFF\xFF\xFF\xFF\xFF\x81\xFF\xBD\xFF\xBD\xFF\xBD\xFF\xBD\xFF\x81\xFF\xFF"],
	'0x078000': [0, ''], # scoreboard
	'0x080000': [0, ''], # kirby normal
	'0x07E0EF': [0, ''], # in game stuff (various sprites)
	'0x0A507C': [0, ''], # kirby electrified, kracko
	'0x08AC87': [0, ''], # rock, umbrella
	'0x095AA4': [0, ''], # umbrella, ball (top spin)
	'0x060000': [0, ''], # transforming to ball
	'0x09166F': [0, ''], # tornado
	'0x090000': [0, ''], # using umbrella
	'0x0A2704': [3200, ''], # cutscene screen
	'0x09F4A8': [0, ''], # Course end start
	'0x0AA7EB': [0, ''], # idle ability card, kirby wave, stuff
	'0x0A05AB': [0, ''], # Kirby poked, Kabu
	'0x07BD0A': [0, ''], # spike ability
	'0x07CF0A': [8192, ''], # course select screen
	'0x0B8888': [0, ''], # stars, switches, power bar, water splash
	'0x09E8B3': [2560, ''], # Win screen
	'0x0A3C3A': [2816, ''], # Course select and in game score tables
	'0x073478': [0, ''], # Ability cards
	'0x0B7142': [0, ''], # Dreams
	'0x0B2601': [1536, ''], # Bronto Burt
	'0x064EC0': [18416, '\xF9\xFF\xF0\xFF\xF0\xFF\xF9\xFF\x9F\xFF\x0F\xFF\x0F\xFF\x9F\xFF\xF9\xFF\xF0\xFF\xF0\xFF\xF9\xFF\xDF\xAA\xAF\x55\x5F\xAA\xFF\x00\xF9\x5F\xF0\x2F\xF0\x5F\xF9\x2F\xBF\x5F\xDF\x2F\xAF\x5F\xDF\x2F\xF9\xFF\xF0\xFF\xF0\xFF\xF9\xFF\x9F\xFE\x0F\xFD\x0F\xFA\x9F\xF4\xF9\xFF\xF0\xFF\xF0\xFF\xF9\xFF\x9F\x7F\x4F\xBF\xAF\x5F\xDF\x2F\xFB\xF4\xF5\xFA\xF2\xFD\xF9\xFE\x9F\xFF\x0F\xFF\x0F\xFF\x9F\xFF\xF9\x2F\xF0\x5F\xF0\xBF\xF9\x7F\x9F\xFF\x0F\xFF\x0F\xFF\x9F\xFF\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'], # Story sprites
	'0x09B594': [0, ''], # Kirby dance move
	'0x084178': [4032, ''], # Kirby walking (Cut out two tiles of data)
	'0x0AE914': [1728, ''], # Kirby look out in the story (also dance, not used)
	'0x0AEC80': [3528, ''], # Broom hatter, Kirby sleeping and tired, big eyes (surprised)
	'0x0B285D': [6336, ''], # Enemies, Kirby hurt eye
	'0x092B0F': [3072, ''], # Background (Course end fill-star)
	'0x093EB1': [3072, ''], # Whispy Woods Background
	'0x09518C': [3072, ''], # Background (Course end fill-star)
	'0x0998A1': [3072, ''], # Background (Course end fill-star)
	'0x09A043': [3072, ''], # Background (Course end fill-star)
	'0x09E286': [3072, ''], # Background (Course end fill-star)
	'0x0ADE67': [2048, ''], # Background (Course end fill-star) & LEAVES
	'0x0B9278': [512, ''], # Debug menu
	'0x0AC7D7': [6464, ''], # Nintendo logo, Halken logo
}

ROM_INFO = {
	'0x076478': [0, "\xC7\x00\x6C\x00\x6C\x00\xE7\x00\xE1\x00\xE1\x00\xC1\x00\x00\x00\x87\x00\xCD\x00\xD9\x00\xD9\x00\xDF\x00\xC3\x00\x83\x00\x00\x00\x80\x00\x80\x00\x80\x00\x80\x00\xC0\x00\x80\x00\x80\x00\x00\x00\xFF\xFF\xFF\x81\xFF\xBD\xFF\xBD\xFF\xBD\xFF\xBD\xFF\x81\xFF\xFF\xFF\xFF\xFF\x81\xFF\xBD\xFF\xBD\xFF\xBD\xFF\xBD\xFF\x81\xFF\xFF\xFF\xFF\xFF\x81\xFF\xBD\xFF\xBD\xFF\xBD\xFF\xBD\xFF\x81\xFF\xFF\xFF\xFF\xFF\x81\xFF\xBD\xFF\xBD\xFF\xBD\xFF\xBD\xFF\x81\xFF\xFF\xFF\xFF\xFF\x81\xFF\xBD\xFF\xBD\xFF\xBD\xFF\xBD\xFF\x81\xFF\xFF\xFF\xFF\xFF\x81\xFF\xBD\xFF\xBD\xFF\xBD\xFF\xBD\xFF\x81\xFF\xFF\xFF\xFF\xFF\x81\xFF\xBD\xFF\xBD\xFF\xBD\xFF\xBD\xFF\x81\xFF\xFF\xFF\xFF\xFF\x81\xFF\xBD\xFF\xBD\xFF\xBD\xFF\xBD\xFF\x81\xFF\xFF\xFF\xFF\xFF\x81\xFF\xBD\xFF\xBD\xFF\xBD\xFF\xBD\xFF\x81\xFF\xFF\xFF\xFF\xFF\x81\xFF\xBD\xFF\xBD\xFF\xBD\xFF\xBD\xFF\x81\xFF\xFF\xFF\xFF\xFF\x81\xFF\xBD\xFF\xBD\xFF\xBD\xFF\xBD\xFF\x81\xFF\xFF\xFF\xFF\xFF\x81\xFF\xBD\xFF\xBD\xFF\xBD\xFF\xBD\xFF\x81\xFF\xFF"],
	'0x078000': [0, ''], # scoreboard
	'0x080000': [35, ''], # kirby normal
	'0x07E0EF': [80, ''], # in game stuff (various sprites)
	'0x0A4B7C': [80, ''], # bosses (kraco etc) electrified
	'0x08AC87': [35, ''], # rock, umbrella
	'0x095AA4': [63, ''], # umbrella, ball (top spin)
	'0x060000': [41, ''], # transforming to ball
	'0x09166F': [35, ''], # tornado
	'0x090000': [35, ''], # using umbrella
	
}

trash_y = 99

def save(timg, tdrawable, nope):
	gimp.progress_init("Searching...")

	kdctools_path = pdb.gimp_gimprc_query("plug-in-path").split(";")[0] + "/../KDCTools"
	tmp_path = pdb.gimp_gimprc_query("temp-path")
	
	sheet_img = pdb.gimp_image_duplicate(timg)
	sheet_img.flatten()
	pdb.gimp_image_set_colormap(sheet_img, len(CMAPS[0]), CMAPS[0])
	sheet_layer = sheet_img.layers[0]
	
	sheet_w = sheet_layer.width
	sheet_h = sheet_layer.height
	sheet_pr = sheet_layer.get_pixel_rgn(0, 0, sheet_w, sheet_h, False)
	sheet_tiles = []
	Tostart = time.clock()
	for sheet_y in xrange(0, sheet_h, 8):
		for sheet_x in xrange(0, sheet_w, 8):
			tile = int(sheet_pr[sheet_x:sheet_x + 8, sheet_y : sheet_y + 8].encode('hex'), 16)
			sheet_tiles.append(tile)
	
	#rom_imgs = []
	#rom_addrs = []
	#rom_extra = []
	#rom_start_y = []
	#rom_end_y = []
	#rom_compress = []
	rom_done_count = 0
	data = []
	sheet_used = []
	
	rom_total_count = 0
	for img in gimp.image_list():
		img_d = img.name[0:-4].split("_")
		if (img_d[0] == "rom"):
			rom_total_count += 1
			
			
	for img in gimp.image_list():
	#while (rom_count < rom_total_count):
		img_d = img.name[0:-4].split("_")
		if (img_d[0] == "rom"):
			addr = img_d[1]
			if (img_d[2] == "c"):
				compress = 1
			else:
				compress = 0
				
			if (img_d[3] == "2bpp"):
				rom_2bpp = 1
			else:
				rom_2bpp = 0
				
			max_size = STUFF[addr][0]
			extra = STUFF[addr][1]
			#start_y = STUFF[addr][0]
			#end_y = STUFF[addr][1]
		
			rom_img = pdb.gimp_image_duplicate(img)
			rom_img.flatten()
			pdb.gimp_image_set_colormap(rom_img, len(CMAPS[0]), CMAPS[0])
			rom_layer = rom_img.layers[0]
			
			#rom_imgs.append(rom_img)
			#rom_addrs.append(addr)
			#rom_extra.append(STUFF[addr][2])
			#rom_start_y.append(starty) #(STUFF[img_d[1]][1])
			#rom_end_y.append(endy)
			#rom_compress.append(compress) #(STUFF[img_d[1]][3])
			
			rom_w = rom_layer.width
			rom_h = rom_layer.height
			rom_pr = rom_layer.get_pixel_rgn(0, 0, rom_w, rom_h, False)
			rom_tiles = []
		
			for rom_y in xrange(0, rom_h, 8):
				for rom_x in xrange(0, rom_w, 8):
					#tile_pixels = array("B", sheet_pr[rom_x:rom_x + 8, rom_y : rom_y + 8])
					tile = int(rom_pr[rom_x:rom_x + 8, rom_y : rom_y + 8].encode('hex'), 16)
					rom_tiles.append(tile)

			tiledata = {'2bpp': rom_2bpp, 'addr': addr, 'd': (rom_w, rom_h), 'c': compress, 'tiles': [], 'ms': max_size, 'extra': extra} # + ", 'tiles': ["
			#del rom_used[:]
			

			start = time.clock()

			last_sheet_n = -1
			sheet_n_length = 1
			dest_i = -1
			from_n = -1
			#for i, rom_tile in enumerate(rom_tiles):
			i = 0
			while i < len(rom_tiles):
				#if (rom_tiles[i] != 0): # Skip empty
				try:
					sheet_n = sheet_tiles.index(rom_tiles[i])
					if (sheet_tiles[sheet_n] != 0):
						#if (rom_tiles[i] != 0):
						#	tiledata['tiles'].append([sheet_n, 1, i]) #(sheet_n, i)
						
						sheet_tiles[sheet_n] = -1
						if (i + 1 < len(rom_tiles)):
							sheet_n_next = sheet_tiles.index(rom_tiles[i+1])
						else:
							sheet_n_next = -1 # end
						
						rom_y = int(i / (rom_w / 8.0)) * 8
						rom_y_next = int((i+1) / (rom_w / 8.0)) * 8
						#print str(sheet_n) + " next: " + str(sheet_n_next)
						if (sheet_n + 1 == sheet_n_next and rom_y == rom_y_next):
							sheet_n_length += 1
							if (dest_i == -1):
								dest_i = i
							if (from_n == -1):
								from_n = sheet_n
						else:
							if (dest_i == -1):
								dest_i = i
							if (from_n == -1):
								from_n = sheet_n
							tiledata['tiles'].append([from_n, sheet_n_length, dest_i]) #(sheet_n, i)
							print str(from_n) + " l" + str(sheet_n_length) + " -> " + str(dest_i)
							dest_i = -1
							from_n = -1
							sheet_n_length = 1
							#print str(sheet_n) + " -> " + str(i)
						last_sheet_n = sheet_n
						
				except ValueError:
					a = 1
				i += 1
					
			data.append(tiledata)
			
			end = time.clock()
			print "%.2gs" % (end-start)
			print "Total: %.2gs" % (end-Tostart)
			rom_done_count = rom_done_count + 1;
			gimp.progress_init("Searching... ROMs done: " + str(rom_done_count))
	
	
	with open(kdctools_path + '/tiledata', 'wb') as f:
		pickle.dump(data, f, protocol=2)
		#sys.stdout.write("asd: " + data)
	#with open(home + "/out.txt", "w") as f:
	#	f.write(data)

register(
	"KDCTools-tiledata-new",
	"Tiledata",
	"Tiledata",
	"vltz",
	"vltz",
	"2016",
	"<Image>/Tools/KDC Tools/Tiledata New",
	"INDEXED*",
	[
		(PF_FILE, "rom_location", "ROM Location", "")
	],
	[],
	save)

main()