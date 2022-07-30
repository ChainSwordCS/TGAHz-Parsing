from PIL import Image
import sys
from traceback import print_exc

class CustomException(Exception): pass # raise custom exception

class colors:
	PURPLE = '\033[95m'
	BLUE = '\033[94m'
	GREEN = '\033[92m'
	YELLOW = '\033[93m'
	RED = '\033[91m'
	ENDC = '\033[0m'
	BOLD = '\033[1m'
	UNDERLINE = '\033[4m'

def printrgb(rgb):
	if(color):
		# Print formatted color as RRRRRGGG GGBBBBBA
		print(f"{colors.RED}"+rgb[0:5]+f"{colors.GREEN}"+rgb[5:10]+f"{colors.BLUE}"+rgb[11:]+f"{colors.PURPLE}"+rgb[16]+f"{colors.ENDC}  ", end='')
	else:
		print(rgb+"  ", end='')

def printrgb24(rgb): # The Sequel
    if(color):
        # Print formatted color as RRRRRRRR GGGGGGGG BBBBBBBB
        print(f"{colors.RED}"+rgb[0:8]+f"{colors.GREEN}"+rgb[8:17]+f"{colors.BLUE}"+rgb[17:]+f"{colors.ENDC}  ", end='')
    else:
        print(rgb+"  ", end='')

def printrgb24hex(rgb): # The Squeakquel
    if(color):
        # Print formatted color as RRGGBB
        print(f"{colors.RED}"+rgb[0:2]+f"{colors.GREEN}"+rgb[2:4]+f"{colors.BLUE}"+rgb[4:]+f"{colors.ENDC}  ", end='')
    else:
        print(rgb+"  ", end='')
	
def torgb(b2, b1):
#	RRRRRGGG GGBBBBBA
	r = int(b2/8)
	g = int((b2%8)*4 + int(b1/64))
	b = int(int(b1/2)%32)
	# Note. For some reason, with Super Mario 3D Land (and maybe other games) this byte receives bad data and must use the following formula instead:
	#b = int(int((b1*8)%256)/8)
	
#	Convert to 24-bit color (simple algorithm)
	ra = (r*8+int(r/4))%256
	ga = (g*8+int(g/4))%256
	ba = (b*8+int(b/4))%256

	return(r,g,b,ra,ga,ba)

# Log each packet
log = ("-log" in sys.argv)
# Create image
image = not ("-noimage" in sys.argv)
# Disable colored logging
color = ("-logcolor" in sys.argv)
# Create animation
animated = False
# force interpretation as a 24-bit encoded Targa (experimental)
bit24 = ("-bit24" in sys.argv)
# ability to log colors in 24-bit hex values instead of binary. only compatible with 24-bit color decoding for now
loghex = ("-loghex" in sys.argv)
# To assist in visual debugging (by looking at color hex values). After reading the RLE or RAW header, go back and render that byte as a shade of red.
forcerenderallheaderbytes = ("-forcerenderhbytes" in sys.argv)

# Input data
if ("-txt" in sys.argv):
	txtfile = open(sys.argv[-1], "r")
	data = bytes.fromhex(txtfile.readline())
	txtfile.close()
elif  ("-txtanim" in sys.argv):
	animated = True
	txtfile = open(sys.argv[-1], "r")
	animdata = [bytes.fromhex(a) for a in txtfile.readlines()]
	txtfile.close()
elif ("-hex" in sys.argv):
	data = bytes.fromhex(sys.argv[-1])
elif ("-tga" in sys.argv or "-bin" in sys.argv):
	binfile = open(sys.argv[-1], "rb")
	data = binfile.read()
	binfile.close()
else:
	data = bytes.fromhex("81400D058015200D8015A0158015A01581C01581601502804DE07D60AD8100DD8140DD0320DD20E520DD20E58140E510007BA04103A284CA43BAC3996D218F216F1190199119B219F329A1CCF131AF218E198162F808CACB4BF441104108CDFDFFD779C62CFD03F98120F80F61F061F882F8A2F882F820F821F805F920FDA3F570FF6FFFC7FE20034033808382C0B308A0B380AB209B0093E092E08AC08AA082807A814072018072C07A81E082040083008B2093609B80A381A0AB05C0B3A0B3C0B3E0B3E07B204481600407C004C01DE01DE079E071E079007A208A81408A034092809AC0A2E0B28100BB0AC0A220FCE0FD8059A0692082007AC071007A208A409281609209809A80A2A0A200BBC0A2C0B200F4C0FD8059A06181E07102207AC071E079812082014092408A8180A20CA09AA0A2E0B280DB80FD3B7EFA75BA65594D3945D834B824971C81771C827714015714570C83570C83370C82370493170402C004E0044005816005010005400D81400D05200D000D400DE004200D000581200D02400D200D400D81800D81400D06200D600D400D200D400D200D600D82200D01E00C400D82400D058015800DE01DC015A015C01581601504804DC08560B500E500DD8140DD8320E50160ED40E581007B05E3A9C4E2A2E2C5D260DDA0E581CF2911F02960E5A0E500E5236CE024221CC822E83B0CDC2008E3200008EDFD2D1200008EFDE3F88120F80B00F861F861F882F8A2F820F821F8E5F840FDE0FCA7FE600381200301402BA08382C0B303A0B360A3209BE09281E08A02C08A8082607A814072018072C07A81E08281208B03409B609B80A3A0A383C0B302E0AB005C401481600402C004C01D001E81E07121007AE079208A408A40926092609A809AC0AAA09AC0A2C0B200F4C0FD8059A061E071E0792082207A208A2082208A809AA0AA608A8092A09AC0AA00B320FC40FD8059A06183007A82408210608AC09A8092A09AC0AAE0AA00B3C0DB9C9E5B8EFB75BA65594D193DD82CB824971C81771C827714015714570C83570C83370C82370493170481E004046005800D600D0005400D82200D02000D600D200D81400D01000D600D81400D01200D400D82600D02200D600D800D81400D02000D800D000D81400D03E00C200D600D400D81600D0D400DC015A015C015A0156015601D804DA08560B5E0E400DD40DD60E58140E50220E540E560E58140E51B007BA04183E203FB05E340DD80E5C0ED60E540DD60DDA0E520EDE07CC43BA722072354BDEBE307CBA21800004EFDF4CCA851ACFC0BFC20F88100F81548E2F1FCFEFFA6F900F841F8E4F820FDA8FE90FF70FF0DFF60FD403BA093C0B3A0B3C0B3A0B360A3209BE09281E08A03A08A8082607A407281807201E082008B81008B04208B2093409B80A3A0AB83C0B30100940054816004038004C004C01D001E81007A10E071007A2082208A609A2082609A809A809280A2C0AA00B300F400FD8059A069007A81207A81208281408A0780926092A09AC0A2E0AA00B320BB00E481FFEF01207A408281808A14809AA09AC0A2FFEFDEE7BEE79EDF9ED77ECF5DC71DBFFCB6BCA67C961B7EBA65594D193DD82C981C971C81771C81771481571484570C83370C82370493170403E00420052005800D81400581200D110005200DE004200D400D2005400D800D600D400D200D000D200D400D600D800D200D800D81600D07200D000D600DC00C000D200DE00C000D81400D81600D016015801581A015098015A0158025A055A09540C500E520DD40E560E58340E50B60E540E520E540E5007BA6CAC6D220DD20D580E5A0E560E58140DD0F80E520ED008DA533A71A282BD6CD97EE41106DFC0BEC4DFD70FEB1FE6EFD8FFD8200F80D90DC3AFFEDFBEEFBE6F9A4F820FDE0F490FFD4FFB3FFB2FFC3FD20ED83C0B30480AB60A3209B0093E08A81A08A048082607A40726072A07281E08205008B208B208B2093409B80A384C0B301007C400482600403C004E01D201E007A81207A012082408A81608A078092A09AE0A200AB00B340BB80C300EC86BED781BEDF02DEDFDEE7DEE785FEEF84FFEF83FFF711FFEFDEEFDEE7BEE79EDF9ED77ECF3DC71DBFFCAE9C9E3B86DA6D79553945F834B824981C81971C827714015714570C83570C83370C82370493170401E004400581400582200502E004000DE00481000D01200D000581400D01A00D800D81200D05600D400D200D600D000D200D81400D02200DC00C200D81E00C82000D05600D400D8015400D6015401582A01509C01DC02DC06580A520D5E0E440DD40E560ED20E58140E50760DD60E540E520E540E560DD007BE07A8120DD2060DDA0E560E520DD60DD80E520ED0474A52B852BE62A9BE61BFF39FFAAD32EFD70FE90FE50FDA0C440EDE3F820F841F883F8F2FCCBFAAFFB4AFA05F900FD6DFFF6FF81F7FF02F6FF4BFFE0EC81C0B315E0B3C0B380A340A3209BE092E08AC08AA0828082607A407A8072A07AE0820083E0820083208B409B80A3A0A381A0B382C0B3012074400C82600403E00C001E001E201E82402602201E4026202686DEDF85BEDF81DEDF83DEE701FEE7FEEF84FEEF84FFEF83FFF781FFEF0DDEEFDEE7BEDF9EDF7ED75DCF3DBFFDB6BCA65B8EFB759A5D594D193D81B82401981C971C827714015714570C83570C83370C823704931704832005060005200D600D0005200DE004200D81000D81200D01600D400D81400D04200D400D200D400D800D81000D01400D000D81000D81200D81000D09200D000D60158015400D200D40158015A015801581C01505E035C06D80AD20E5E0E460E58240E50720E540DD60DD60E540E520DD20E560E58160DD2140DD20DD80E5A0E580E520DD60DDA0ED20ED046CA42B852B083C674415D632B50BF4B0FDB1FED0FEAA5480D463E5F5FF21F883F8A3F8F4FF90FF42DD20FDE0FC8DFFD3FF81F7FF14F8FFF9FFB0FFC0E4C09BC0B3C0ABA0AB60A3409B0093E08AC08AA08AA0828082607A40728072A07AC082820083012093409B8180A301C0B3A0B382C0B3080094201C20044004600440152026001E2026814026012026E01D81202688DEDF85DEE701FEE7FEEF88FEEF84FFEF84FFF781FFEF0DDEEFDEE7BEE79EDF7ED75DC73DBFDCAE7C961B7EDA6D7A553945D82C81B82401971C7714817714015714570C83570C86370C931704814005090005E0040005200D800D200DE004C004E00C000D81400D81600D01400D200D81400D81200D81600D81200D02400D000D000D81200D01600D400D81400D0D200D600D8015400D200D400DC01D6015A015C01DA015E035C07D80BD8100E50260E540E540E58120E58140DD0560E540E520E540E560E560DD8160E50C40DD80E5A0E580E540DD60DDA0ED82B40454A42B852BE83B08448148440B2CE46DFD70FE11FF400CA1D467CDF9FF45F9C4F8F7FFF4FF8190FF03A2FD71FF70FFF4FF81F7FF81F9FF0269F6C1D4C0AB82C0B31180A3409B0093E08AE092C08A8082807A4072407A8072C07AE0820083008B208B2093409B8180A383C0B308E0BB009C205C600480046004A015001E201E83402602E01D4026402685DEDF87DEE781FEE789FEEF84FFEF86FFF70CFFEFDEEFBEE7BEDF9ED77ECF3DC7FDB6BCA65B8EFB759A65594D81D82C02B824981C971C817714015714570C82570C8A370C901704012005000581000581200503200D2005200DE00481E00C81400D04600D800D600D000D400D81600D01200D800D81600D03400D");

def processframe(data):
	
	exceptionnum = 0
	exceptionstring = str("Unknown exception")
	
	try: # better catch errors at end of data. obsoleted this -> endoffile = False
		if(bit24): # Time for experimental 24-bit image support baby!!!
			# Note: Don't skip any bytes (for now)
			i = 22
			# Pixel Number. This is important for the initial-prototyping stage, because 24-bit TGAHZ files don't have the same footer as 16-bit TGAHZ files,
			# so we don't actually know where to stop rendering unless we count the pixels manually. This is error-checking.
			pxnum = 0
			
			if(image):
				imgdat = bytearray(b'')
				
			while(i < len(data) and pxnum < 96000): # Will abruptly end after the final pixel :)
				header = data[i] # Top byte indicates RLE/RAW
				
				if(header > 127):
					if(log):
						print("RLE",end='')
					rle = True
				else:
					if(log):
						print("RAW",end='')
					rle = False
				
				packlen = header % 128 + 1 # Length of packet; number of pixels to fill in RLE-context, or number of colors to draw sequentially in RAW-context.(?)
				#pxnum = pxnum + packlen # Increment the pixel number by however long the stupid packet says it is (dummied out why?)
				i = i + 1; # Skip header byte
				
				# Print number of pixels :)
				if(log):
					print(str(packlen).rjust(4)+" ",end='')
					# Log bits of the "Header" byte just in case.
					print("  ", end='')
					print((format(data[i-1], '08b'))+"   ",end='')
				
				# Now... the hard part :(
				
				
				if(rle): # If Run Length Encoded (RLE) Packet
					# Three color bytes: R, G, B
					b1 = data[i]
					b2 = data[i+1]
					b3 = data[i+2]
					
					if(log):
						if(loghex):
							printrgb24hex(format(b1, '02x')+format(b2, '02x')+format(b3, '02x'))
						else:
							printrgb24(format(b1, '08b')+" "+format(b2, '08b')+" "+format(b3, '08b'))
					
					if(image):
						# Note: No need to convert to 24-bit... This is already 24-bit hopefully
						
						for j in range(packlen): # Eiim says J is a dummy variable. I think he's a dummy
							# Note to self: I'm a dummy lmfao. This is a different J, the letter was just chosen by personal preference.
							imgdat.append(b1)
							imgdat.append(b2)
							imgdat.append(b3)
					
					# Skip past three color bytes
					i = i + 3
					
				else: # If Raw Packet (RAW)
					j = 0
					while(j < packlen):
						# Two (You mean three? Thats -2 points) color bytes
						b1 = data[i+j*3]
						b2 = data[i+j*3+1]
						b3 = data[i+j*3+2] # Cam says this might break idk what I'm doing half the time
						
						if(log):
							if(loghex):
								printrgb24hex(format(b1, '02x')+format(b2, '02x')+format(b3, '02x'))
							else:
								printrgb24(format(b1, '08b')+" "+format(b2, '08b')+" "+format(b3, '08b'))
						
						if(image):
							# repeat again
							imgdat.append(b1)
							imgdat.append(b2)
							imgdat.append(b3)
						
						# Next color set
						j = j + 1
					# Skip past raw color data
					i = i + packlen*3
				if(log):
					# Need newline after all those colors
					print()

		# 16-bit TGAHZ (THIS IS THE DEFAULT!!!)
		else:
			# Skip last 26 bytes (footer)
			data = data[:-26]
			# Skip first 22 bytes
			i = 22
			# Pixel Number
			pxnum = 0
			
			# Implied header: 16010A000001002000000000F0009001102000000000
			
			if(image):
				imgdat = bytearray(b'')
			
			while(i < len(data) and pxnum < 96000): #Will abruptly end after the final pixel :)
				header = data[i]
				
				if(forcerenderallheaderbytes): # Note: Very stupid (: Debug feature to forcibly render the header byte (or bytes) as a pixel in the image.
					if(image):
						if(pxnum < 96000):
							imgdat.append(header)
							imgdat.append(0x00)
							imgdat.append(0x00)
							pxnum = pxnum + 1
				
				# Highest bit indicates RLE/RAW
				if(header > 127):
					if(log):
						print("RLE",end='')
					rle = True
				else:
					if(log):
						print("RAW",end='')
					rle = False
				# Length of packet, pixels for RLE or colors for RAW
				packlen = header % 128 + 1
				# Skip header byte
				i = i + 1;
				
				if(log):
					print(str(packlen).rjust(4)+" ",end='')
				
# obsolete		if(i >= len(data) or i+1 >= len(data)): # End-Of-File Error Checking, this works for all of RLE and the first two bytes of RAW
#					endoffile = True
				
				if(rle):
					# Two color bytes in LE order
					b1 = data[i]
					b2 = data[i+1]
					
					if(log):
						printrgb(format(b2, '08b')+" "+format(b1, '08b'))
					if(image):
						# bytes to 5-bit and 8-bit RGB
						r,g,b,ra,ga,ba = torgb(b2,b1)						
						
						for j in range(packlen):
							if(pxnum < 96000): # End-Of-Pixels Error Checking
								imgdat.append(ra)
								imgdat.append(ga)
								imgdat.append(ba)
								pxnum = pxnum + 1
								
					# Skip past two color bytes
					i = i + 2
				else:
					j = 0
					while(j < packlen):
						
						if(i+j*2 >= len(data) or i+j*2+1 >= len(data)): # More Error Checking
							exceptionnum = 1
							exceptionstring = str("Reached end of input data (this message should not appear)")
							raise CustomException("End of data")
						
						# Two color bytes in LE order
						b1 = data[i+j*2]
						b2 = data[i+j*2+1]
						
						if(log):
							printrgb(format(b2, '08b')+" "+format(b1, '08b'))
						if(image):
							# bytes to 5-bit and 8-bit RGB
							r,g,b,ra,ga,ba = torgb(b2,b1)
							#print(b2,b1,r,g,b)
							if(pxnum < 96000): # End-Of-Pixels Error Checking
								imgdat.append(ra)
								imgdat.append(ga)
								imgdat.append(ba)
								pxnum = pxnum + 1
						
						# Next color pair
						j = j + 1
						if(i+j*2 >= len(data) or i+j*2+1 >= len(data)): # More Error Checking
							exceptionnum = 1
							exceptionstring = str("Reached end of input data (this message should not appear)")
							raise CustomException("End of data")
					
					# Skip past raw color data
					i = i + packlen*2
				if(log):
					# Need newline after all those colors
					print()
			
			if(i < len(data) and pxnum >= 96000):
				print("Warning: The input file contains extra data past the end of the image.")
			if pxnum < 96000:
				exceptionnum = 1
				exceptionstring = str("Reached end of input data (this message should not appear)")
				raise CustomException("End of data")

		return imgdat # Return with the processed image data (both 16bpp and 24bpp modes)

	# Result of Error Checking: Here is where we fill the rest of the space with black pixels.
	except Exception as e:
		print()
		if(exceptionnum == 1):
			print("Error: End of data has been reached. This is common.")
		else:
			print("An unexpected error has occurred.")
			if(image):
				print("Attempting to finalize the image file.")
		if(image):
			print("Now rendering black pixels to fill remaining space...")
			k = 0
			m = len(imgdat)
			while(pxnum < 96000):
				imgdat.append(0x00) # Bug (won't fix): A possible bug in which there are 1 or 2 errant $00 bytes at the end of the data. Nothing bad happens, so I don't care lol. Not rewriting this.
				imgdat.append(0x00)
				imgdat.append(0x00)
				k = k + 1
				pxnum = pxnum + 1 # Bug (won't fix): The reported number of black pixels may be 1 too many. Not at all a big deal, but documenting for completeness.
			print("Finished. Rendered " + str(m) + " bytes and added " + str(k) + " black pixels.")
			if(exceptionnum == 1):
				return(imgdat)

			im = Image.frombytes('RGB', (240, 400), bytes(imgdat))
			im.rotate(90, expand=True).save("TGAHZ.png", "PNG")
			print("File saved.")
		else:
			print("Finished. Processed " + str(m) + " bytes.")

		print("Exception Type is:", e.__class__.__name__)
		print("Error Code " + str(exceptionnum))
		print("Error Description: " + exceptionstring)
		print("Other Info, Part 1:")
		print_exc()
		print("Other Info, Part 2:")
		raise

# among us

if(animated): # Included for theoretical better support, but I think this may never come up.
	if(image):
		frames = []
		for i in range(0, len(animdata)):
			imgdat = processframe(animdata[i])
			if(image):
				# Needs to be immutable, so convert to bytes instead of bytearray
				im = Image.frombytes('RGB', (240, 400), bytes(imgdat))
				frames.append(im.rotate(90, expand=True))
		frames[0].save("TGAHZ.gif", save_all=True, append_images=frames[1:], duration=len(animdata), loop=0)
		print("Saved")
else: # Non-animated.

	# Beginning of regular execution here etc (:

	imgdat = processframe(data)
	if(image):
		# Needs to be immutable, so convert to bytes instead of bytearray
		im = Image.frombytes('RGB', (240, 400), bytes(imgdat))
		im.rotate(90, expand=True).save("TGAHZ.png", "PNG")
		print("Saved.")
	else:
		print("Finished. Processed " + str(m) + " bytes.")