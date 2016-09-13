#!/usr/bin/env python

from pickle import load
from gimpfu import *
from subprocess import call

DEBUG = 0
SKIP_SPRITES = 0

if (DEBUG):
	import sys
	from os.path import expanduser
	home = expanduser("~")
	sys.stderr = open(home + '/gimpstderr.txt', 'w')
	sys.stdout = open(home + '/gimpstdout.txt', 'w')

CMAP = (0,128,0,31,31,31,47,47,47,63,63,63,79,79,79,95,95,95,111,111,111,127,127,127,143,143,143,159,159,159,175,175,175,191,191,191,207,207,207,223,223,223,239,239,239,255,255,255) + (0,0,0)*240

PALETTES = [
	("0xC0C3E", (87, 83, 116, 0, 0, 0, 0, 0, 0, 248, 248, 248, 0, 0, 0, 8, 16, 72, 0, 0, 0, 240, 120, 40, 248, 144, 40, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 248, 248, 248)), # Title screen BG-tile P1
	("0xC0C5E", (248, 248, 248, 0, 0, 0, 138, 17, 7, 210, 28, 9, 89, 67, 7, 247, 187, 45, 200, 64, 40, 240, 120, 40, 248, 144, 40, 8, 16, 72, 176, 144, 72, 248, 192, 120, 248, 144, 64, 73, 68, 109, 87, 83, 116, 248, 248, 248)), # Title screen BG-tile P2 / Title text part
	("0xC0C7E", (248, 248, 248, 0, 0, 0, 138, 17, 7, 210, 28, 9, 89, 67, 7, 247, 187, 45, 200, 64, 40, 240, 120, 40, 248, 144, 40, 8, 16, 72, 176, 144, 72, 248, 192, 120, 248, 144, 64, 73, 68, 109, 87, 83, 116, 248, 248, 248)), # Title lower part P3
	("0xC0120", (88, 88, 88, 24, 24, 24, 32, 80, 120, 72, 120, 160, 112, 160, 200, 152, 200, 240, 208, 224, 248, 24, 24, 24, 16, 56, 48, 248, 16, 72, 72, 24, 48, 248, 48, 120, 248, 112, 192, 248, 152, 240, 248, 208, 248, 248, 248, 248)), # Keeby 1
	("0xC0784", (24, 24, 24, 16, 56, 48, 32, 80, 120, 72, 120, 160, 112, 160, 200, 152, 200, 240, 208, 224, 248, 24, 24, 24, 16, 56, 48, 120, 72, 96, 160, 112, 136, 176, 152, 184, 192, 184, 224, 208, 232, 248, 80, 80, 80, 16, 56, 48)), # Keeby 2
	("0xC083E", (248, 216, 192, 48, 24, 32, 32, 80, 120, 72, 120, 160, 112, 160, 200, 152, 200, 240, 208, 224, 248, 24, 24, 24, 208, 32, 88, 248, 72, 128, 248, 136, 152, 248, 192, 192, 248, 232, 216, 64, 16, 16, 224, 32, 88, 248, 72, 136)), # Keeby 3
	
	("0xC01C0", (88, 88, 88, 0, 0, 0, 80, 56, 16, 144, 96, 72, 184, 152, 96, 0, 56, 0, 0, 96, 0, 0, 176, 0, 72, 48, 0, 168, 96, 80, 208, 168, 136, 80, 8, 32, 248, 0, 0, 96, 96, 96, 40, 40, 40, 248, 248, 248)), # Whispy Woods
	
	# Whisp Jacques fix
	("0xC01D8", (248, 0, 0, 96, 96, 96)),
	("0xC12B0", (248, 0, 0, 96, 96, 96)),
	("0xC1986", (248, 0, 0, 96, 96, 96)),
	
	("0xC210C", (36, 26, 9, 69, 108, 29, 146, 74, 21, 242, 198, 93, 198, 123, 40, 241, 214, 197)), # Kracko
	# Gordo
	# Golden stars problem.. ("0xC0174", (36, 26, 9, 69, 108, 29, 146, 74, 21, 242, 198, 93, 198, 123, 40, 241, 214, 197)),
	
	("0xC0140", (88, 88, 88, 24, 24, 24, 80, 40, 8, 168, 88, 8, 248, 184, 8, 248, 248, 0, 248, 248, 224, 248, 248, 128, 136, 136, 0, 56, 160, 248, 24, 56, 80, 63, 155, 241, 114, 179, 239, 156, 200, 248, 208, 208, 248, 248, 248, 248)), # P15
	
	("0xC0C34", (80, 40, 8, 168, 88, 8, 248, 184, 8, 248, 248, 0, 248, 248, 224)), # Umbrella (P15)
	("0xC121C", (80, 40, 8, 168, 88, 8, 248, 184, 8, 248, 248, 0, 248, 248, 224, 248, 248, 128)), # Umbrella (P15)
	("0xC18F2", (80, 40, 8, 168, 88, 8, 248, 184, 8, 248, 248, 0, 248, 248, 224, 248, 248, 128)), # Umbrella (P15)
	("0xC301C", (80, 40, 8, 168, 88, 8, 248, 184, 8, 248, 248, 0, 248, 248, 224, 248, 248, 128)), # Umbrella (P15)
	
	("0xC1516", (104, 104, 104, 64, 64, 64, 152, 40, 64, 248, 112, 160, 240, 152, 208, 128, 64, 16, 115, 162, 206, 156, 200, 248, 80, 32, 168, 152, 104, 240, 184, 144, 232, 24, 96, 48, 32, 216, 72, 184, 216, 248, 0, 0, 0, 248, 248, 248)), # Scoreboard
	("0xC16D4", (0, 112, 248)), # In-game no ability card outline
	("0xC1902", (24, 48, 64, 63, 155, 241, 114, 179, 239, 156, 200, 248, 208, 208, 248, 248, 248, 248)), # Course Select Keeby card
	("0xC17AE", (248, 248, 216, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 248, 192, 144, 248, 200, 152, 248, 208, 160, 0, 0, 0, 248, 240, 200, 248, 224, 184, 248, 216, 168, 0, 0, 0, 24, 24, 24, 112, 240, 160, 56, 160, 248)), # Course select scores frame
	("0xC17CE", (104, 104, 104, 24, 24, 24, 112, 240, 160, 248, 104, 184, 0, 0, 0, 24, 24, 24, 152, 80, 248, 56, 160, 248, 0, 0, 0, 24, 24, 24, 152, 80, 248, 248, 104, 184, 0, 0, 0, 24, 24, 24, 152, 80, 248, 112, 240, 160)), # Course select score numbers
	
	# Course select screen background colours
	#("0xC17AE", (136, 248, 96)), # lightest
	#("0xC17B6", (0, 0, 0, 3, 166, 248, 23, 173, 248, 37, 178, 248, 0, 0, 0, 90, 195, 248, 70, 189, 248, 56, 184, 248)),#(0, 0, 0, 248, 121, 3, 248, 132, 23, 248, 143, 37, 0, 0, 0, 248, 182, 90, 248, 162, 70, 248, 154, 56)),
	# Kracko image selected (full colour)
	#("0xC19F2", (26, 33, 8, 242, 198, 93, 75, 95, 30, 153, 80, 23, 117, 144, 40, 200, 128, 52, 233, 208, 193)),
	# Kracko image unselected (light colour)
	#("0xC1870", (77, 84, 54, 255, 231, 174, 130, 145, 96, 204, 156, 119, 176, 194, 127, 250, 206, 160, 255, 242, 234)),
	#("0xC1A52", (77, 84, 54, 255, 231, 174, 130, 145, 96, 204, 156, 119, 176, 194, 127, 250, 206, 160, 255, 242, 234)),
	
	# Course end background stars colours
	("0xC0770", (40, 152, 0, 248, 144, 40, 136, 40, 0, 248, 112, 24)),
	
	("0xC1410", (248, 120, 152, 248, 120, 152, 0, 0, 16, 0, 0, 16)), # Win screen "Arin" text palette
	("0xC1430", (248, 120, 152, 248, 120, 152, 0, 0, 16, 0, 0, 16)), # Win screen "Arin" text palette
	("0xC1450", (248, 120, 152, 248, 120, 152, 0, 0, 16, 0, 0, 16)), # Win screen "Arin" text palette 
	("0xC13B0", (248, 120, 152, 248, 120, 152, 0, 0, 16, 0, 0, 16)), # Win screen "Arin" text palette
	("0xC13D0", (248, 120, 152, 248, 120, 152, 0, 0, 16, 0, 0, 16)), # Win screen "Arin" text palette 
	("0xC13F0", (248, 120, 152, 248, 120, 152, 0, 0, 16, 0, 0, 16)), # Win screen "Arin" text palette
	("0xC1470", (248, 120, 152, 248, 120, 152, 0, 0, 16, 0, 0, 16)), # Win screen "Arin" text palette
	
	("0xC1418", (0, 0, 16, 88, 176, 248, 88, 176, 248, 0, 0, 16)), # Win screen "Danny" text palette
	("0xC1438", (0, 0, 16, 88, 176, 248, 88, 176, 248, 0, 0, 16)), # Win screen "Danny" text palette
	("0xC1458", (0, 0, 16, 88, 176, 248, 88, 176, 248, 0, 0, 16)), # Win screen "Danny" text palette 
	("0xC1478", (0, 0, 16, 88, 176, 248, 88, 176, 248, 0, 0, 16)), # Win screen "Danny" text palette
	("0xC13B8", (0, 0, 16, 88, 176, 248, 88, 176, 248, 0, 0, 16)), # Win screen "Danny" text palette
	("0xC13D8", (0, 0, 16, 88, 176, 248, 88, 176, 248, 0, 0, 16)), # Win screen "Danny" text palette
	("0xC13F8", (0, 0, 16, 88, 176, 248, 88, 176, 248, 0, 0, 16)), # Win screen "Danny" text palette

	("0xC109E", (132, 176, 248)), # Score table Keeby parts and Keeby's stars
	("0xC10BC", (200, 24, 56, 24, 56, 200)), # Meter tomatoes colours 1 (darkest)
	("0xC10B8", (224, 48, 104, 48, 104, 224)), # Meter tomatoes colours 2
	("0xC10B4", (240, 72, 152, 72, 152, 240)), # Meter tomatoes colours 3
	("0xC10B0", (248, 104, 176, 104, 176, 248)), # Meter tomatoes colours 4 (lightest)
	
	# In-game Keeby charging a shot from lightest to darkest colour, last one is the pinnacle blink
	("0xC39E2", (33, 81, 123, 74, 121, 165, 115, 162, 206, 156, 200, 248, 208, 229, 248)),
	("0xC39F0", (27, 67, 102, 65, 107, 145, 104, 146, 186, 143, 183, 227, 190, 210, 227, 8, 64, 104)),
	("0xC39FE", (19, 55, 87, 51, 91, 128, 84, 127, 168, 124, 163, 207, 171, 189, 204)),
	("0xC3A0C", (10, 51, 87, 38, 85, 128, 67, 119, 168, 104, 152, 207, 155, 182, 204, 0, 152, 248)),
	("0xC3A1A", (4, 48, 87, 26, 79, 128, 50, 111, 168, 83, 141, 207, 143, 177, 204)),
	("0xC3A28", (0, 46, 87, 13, 73, 128, 34, 103, 168, 62, 130, 207, 122, 168, 204, 8, 64, 104)),
	("0xC3A36", (0, 46, 87, 6, 70, 128, 17, 95, 168, 41, 119, 207, 112, 164, 204)),
	("0xC3A44", (0, 46, 87, 0, 67, 128, 0, 87, 168, 21, 108, 207, 102, 160, 204, 0, 152, 248)),
	("0xC3A52", (0, 54, 102, 0, 80, 153, 0, 95, 184, 23, 118, 227, 51, 167, 248, 224, 248, 0)), # Blink
	
	# Keeby in the "making a shot" window (Idle position) and curve shot window (index 200)
	("0xC1548", (74, 121, 165, 115, 162, 206, 156, 200, 248)),
	("0xC156C", (74, 121, 165, 115, 162, 206, 156, 200, 248)),
	("0xC1584", (74, 121, 165, 115, 162, 206, 156, 200, 248)),
	# Other positions (lightest to darkest)
	("0xC1590", (86, 102, 137, 126, 141, 177, 165, 179, 224)),
	("0xC159C", (101, 85, 114, 141, 123, 154, 179, 158, 200)),
	("0xC15A8", (116, 68, 91, 156, 105, 131, 193, 138, 176)),
	("0xC15B4", (131, 51, 68, 171, 86, 108, 206, 117, 152)),
	("0xC15C0", (146, 34, 45, 186, 68, 85, 220, 97, 128)),
	("0xC15CC", (161, 17, 22, 201, 50, 62, 234, 76, 104)),
	("0xC15D8", (176, 0, 0, 216, 32, 40, 248, 56, 80)),
	
	# In-game Keeby pulse
	("0xC3228", (0, 80, 160, 32, 116, 200, 96, 160, 224, 160, 196, 232, 208, 228, 248)),
	("0xC3232", (48, 132, 216, 112, 176, 240, 176, 212, 248, 224, 236, 248, 248, 248, 248)),
	
	# Keeby's shoes in curve shot window
	("0xC1556", (80, 48, 136)),

	# Keeby underwater
	("0xC07A4", (55, 91, 123, 104, 135, 165, 152, 180, 206, 201, 223, 248, 241, 245, 248)),
	("0xC3250", (55, 91, 123, 104, 135, 165, 152, 180, 206, 201, 223, 248, 241, 245, 248)),
	("0xC3ADA", (55, 91, 123, 104, 135, 165, 152, 180, 206, 201, 223, 248, 241, 245, 248)),

	# Settings screen background
	("0xC3746", (248, 112, 24, 248, 248, 248, 248, 144, 40)),
	
	# Settings screen Keeby bar [Settings screen: index 25]
	("0xC3720", (156, 200, 248)),
	
	# Settings screen Keeby's cards
	("0xC3770", (96, 152, 184, 192, 80, 24, 128, 16, 24, 80, 24, 96, 64, 96, 144, 192, 192, 248)), # index 65-
	("0xC3790", (156, 200, 248, 240, 128, 16, 184, 8, 16, 120, 40, 128, 104, 144, 200, 224, 224, 248)), # index 81-
	("0xC37B0", (24, 48, 72)), # index 97-
	("0xC37D0", (56, 96, 128)), # index 113-
	
	("0xC3840", (56, 160, 248, 24, 48, 64, 63, 155, 241, 114, 179, 239, 156, 200, 248, 208, 208, 248, 248, 248, 248)), # Settings screen Keeby index 169-
	
	# Story frame
	("0xC3B62", (240, 120, 40, 248, 144, 40)),
	("0xC3B6A", (240, 120, 40, 248, 144, 40)),
	("0xC3B72", (240, 120, 40, 248, 144, 40)),
	("0xC3B7A", (240, 120, 40, 248, 144, 40)),
	("0xC3B82", (240, 120, 40, 248, 144, 40)),
	
	("0xC3D62", (240, 120, 40, 248, 144, 40)),
	("0xC3D6A", (240, 120, 40, 248, 144, 40)),
	("0xC3D72", (240, 120, 40, 248, 144, 40)),
	("0xC3D7A", (240, 120, 40, 248, 144, 40)),
	("0xC3D82", (240, 120, 40, 248, 144, 40)),
	
	("0xC3F62", (240, 120, 40, 248, 144, 40)),
	("0xC3F6A", (240, 120, 40, 248, 144, 40)),
	("0xC3F72", (240, 120, 40, 248, 144, 40)),
	("0xC3F7A", (240, 120, 40, 248, 144, 40)),
	("0xC3F82", (240, 120, 40, 248, 144, 40)),
	
	# King Dedede in story
	# original (?)("0xC40B6", (88, 88, 88, 24, 24, 24, 136, 0, 0, 248, 0, 0, 64, 0, 0, 232, 152, 48, 248, 216, 72, 96, 176, 192, 120, 232, 232, 0, 0, 0, 33, 81, 123, 74, 121, 165, 115, 162, 206, 156, 200, 248, 208, 229, 248, 248, 248, 248)),
	("0xC40B6", (178, 0, 255, 56, 56, 56, 24, 24, 24, 0, 68, 114, 104, 56, 24, 80, 80, 96, 0, 116, 198, 120, 112, 128, 0, 148, 255, 144, 144, 152, 232, 152, 48, 255, 187, 127, 208, 208, 208, 248, 216, 72, 255, 211, 173, 248, 248, 248)),

	# Bronto Burt
	("0xC20C6", (200, 200, 200, 64, 8, 0, 248, 80, 16, 248, 152, 72, 248, 208, 152, 160, 16, 40, 248, 96, 120)),

	# cutscreen logo
	# For Burgie ("0xC0180", (154, 154, 154, 103, 112, 103, 29, 52, 9, 103, 137, 32, 66, 86, 24, 242, 198, 93, 205, 135, 45, 186, 106, 33, 203, 148, 100, 125, 61, 17, 160, 83, 27, 222, 186, 169, 68, 29, 16, 18, 6, 4, 0, 0, 0, 249, 232, 229)),
	# For Dream Tee logo
	("0xC0180", (102, 40, 40, 0, 0, 0, 21, 107, 121, 72, 151, 159, 188, 130, 72, 240, 120, 40, 248, 144, 40, 188, 156, 117, 143, 188, 195, 88, 216, 231, 166, 211, 218, 238, 217, 128, 176, 230, 235, 224, 249, 254, 253, 255, 171, 239, 252, 253)),
	# cutscreen background, frame(?)
	("0xC0040", (104, 104, 104, 0, 0, 0, 48, 0, 0, 80, 54, 16, 200, 108, 32, 240, 120, 40, 248, 144, 40, 128, 112, 96, 88, 72, 56, 136, 120, 104, 96, 80, 64, 64, 72, 120, 216, 216, 192, 112, 120, 168, 248, 248, 240, 248, 248, 248)),

	# Kabu and all others
	("0xC01A0", (88, 88, 88, 0, 0, 0, 70, 40, 40, 248, 0, 0, 248, 72, 112, 248, 136, 48, 0, 96, 0, 0, 176, 0, 82, 76, 55, 248, 200, 0, 248, 216, 176, 88, 248, 72, 0, 0, 120, 0, 0, 248, 136, 136, 248, 248, 248, 248)),

	# Dream: Candy
	#("0xC012E", (24, 24, 24, 16, 56, 48, 248, 0, 0, 68, 45, 45, 204, 173, 83, 229, 208, 105, 226, 177, 154, 240, 208, 176, 248, 248, 248)),
	
	# P19 Gordo (can be used with Dream: Cake)
	("0xC0174", (64, 48, 40, 80, 80, 96, 104, 104, 104, 144, 144, 152, 208, 208, 208, 248, 248, 248)),
	# Orange to yellow for Suzy dream..changes guide balls
	("0xC15EA", (224, 176, 152, 240, 208, 176, 200, 168, 80, 224, 208, 104, 208, 16, 48, 248, 40, 80)),
	# Zombie suzy fix on certain courses
	("0xC0164", (224, 176, 152, 240, 208, 176, 200, 168, 80, 224, 208, 104)),
	# Change city lights colour on night palette
	("0xC3DE8", (248, 248, 248)),
	("0xC3DF4", (248, 0, 248)),
	
	# Course end background leaf fill bg colour to orange
	("0xC0740", (248, 144, 40)),
	
	# Debug menu background colour + yellow -> orange
	("0xC1010", (240, 120, 40, 248, 144, 40)), 
	# Inside bg and stars colours to orange
	("0xC0FEE", (224, 248, 248, 192, 224, 248, 136, 192, 248)), 
]


def save(timg, tdrawable, rom_location):
	kdctools_path = pdb.gimp_gimprc_query("plug-in-path").split(";")[0] + "/../KDCTools"
	tmp_path = pdb.gimp_gimprc_query("temp-path")

	with open(kdctools_path + '/tiledata', 'rb') as f:
		tile_info = load(f)
	
	img = pdb.gimp_image_duplicate(timg)
	img.flatten()
	pdb.gimp_image_set_colormap(img, len(CMAP), CMAP)
	
	if (not SKIP_SPRITES):
		gimp.progress_init("Saving sprites to ROM...")
		
		tiles_info_len = len(tile_info)
		for i1, t1 in enumerate(tile_info): 
			nimg = base_image(t1['d'])

			tiles = t1['tiles']
			tiles_len = len(tiles)
			for i2, t2 in enumerate(tiles):
				copy_tile(img, nimg, t2, img.width, t1['d'][0])
				gimp.progress_update(float(i2 + tiles_len * i1) / float(tiles_len * tiles_info_len))
			
			if (DEBUG):
				gimp.Display(nimg)
			else:
				save_pcx(nimg, tmp_path)
				
				if (t1['2bpp']):
					call([kdctools_path + "/Pcx2Snes.exe", tmp_path + "/kdctools_out", "-c4", "-o4", "-s8", "-n"])
				else:
					call([kdctools_path + "/Pcx2Snes.exe", tmp_path + "/kdctools_out", "-c16", "-o16", "-s8", "-n"])
									
				if (t1['ms'] != 0):
					with open(tmp_path + "/kdctools_out.pic", "r+b") as f:
						f.seek(t1['ms'])
						#f.write("\0")
						f.truncate()
						
				with open(tmp_path + "/kdctools_out.pic", "ab") as f:
					f.write(t1['extra'])
					
				if (t1['c']):
					call([kdctools_path + "/inhal.exe", tmp_path + "/kdctools_out.pic", rom_location, t1['addr']])
				else:
					with open(tmp_path + "/kdctools_out.pic", "rb") as f:
						sprite_data = f.read()
					write(rom_location, sprite_data, int(t1['addr'], 16))
					
				pdb.gimp_image_delete(nimg)
				
			gimp.progress_init("Saving sprites to ROM...")
	
	gimp.progress_init("Saving palettes to ROM...")
	
	with open(rom_location, "r+b") as f:
		for p in PALETTES:		
				values = [x / 8 for x in p[1]]
				f.seek(int(p[0], 16))
				for i in xrange(0, len(values), 3):
					b1 = '{:05b}'.format(values[i+2]) + '{:05b}'.format(values[i+1])[:2]
					b2 = '{:05b}'.format(values[i+1])[2:] + '{:05b}'.format(values[i])
					f.write(chr(int(b2, 2)))
					f.write(chr(int(b1, 2)))
	
def base_image(dimensions):
	w = dimensions[0]
	h = dimensions[1]
	nimg = pdb.gimp_image_new(w, h, 2) # 2 INDEXED
	pdb.gimp_image_set_colormap(nimg, len(CMAP), CMAP)
	gimp.set_foreground(CMAP[:3])
	nlayer = pdb.gimp_layer_new(nimg, w, h, INDEXED_IMAGE, "bg", 100, NORMAL_MODE)
	pdb.gimp_image_insert_layer(nimg, nlayer, None, 0)
	pdb.gimp_drawable_fill(nlayer, 0) # Fill with foreground colour
	return nimg
	
def save_pcx(nimg, filepath):
	try:
		gimp.pdb.file_pcx_save(nimg, nimg.layers[0], filepath + "/kdctools_out.pcx", "")
	except Exception as err:
		gimp.message("Unexpected error when saving: " + str(err))

# Slow
def copy_tile(img, nimg, data, sheet_w, rom_w):
	x1 = int(data[0] % (sheet_w / 8.0)) * 8
	y1 = int(data[0] / (sheet_w / 8.0)) * 8
	
	tx = int(data[2] % (rom_w / 8.0)) * 8
	ty = int(data[2] / (rom_w / 8.0)) * 8
		
	pdb.gimp_rect_select(img, x1, y1, data[1] * 8, 8, 2, 0, 0)
	pdb.gimp_edit_copy(img.layers[0])
	pdb.gimp_selection_none(img)

	if (DEBUG):
		nlayer = pdb.gimp_layer_new(nimg, data[1] * 8, 8, INDEXED_IMAGE, "", 100, NORMAL_MODE)	
		pdb.gimp_image_insert_layer(nimg, nlayer, None, 0)
		pdb.gimp_layer_set_offsets(nlayer, tx, ty)
		float_sel = pdb.gimp_edit_paste(nlayer, 1)
		pdb.gimp_floating_sel_anchor(float_sel)
	else:
		float_sel = pdb.gimp_edit_paste(nimg.layers[0], 1)
		pdb.gimp_layer_set_offsets(float_sel, tx, ty)
		pdb.gimp_floating_sel_anchor(float_sel)	
	
def write(file, data, offset):
	with open(file, "r+b") as f:
		f.seek(offset)
		f.write(data)

register(
	"KDCTools-save",
	"Save all sprites to KDC ROM",
	"Save all sprites to KDC ROM",
	"vltz",
	"vltz",
	"2016",
	"<Image>/Tools/KDC Tools/Save...",
	"INDEXED*",
	[
		(PF_FILE, "rom_location", "Select ROM", "")
	],
	[],
	save)

main()