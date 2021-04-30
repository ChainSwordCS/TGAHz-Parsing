# TGAHz Parsing

### What is this?

So, HzMod is a 3DS image capturing system that is entirely software-based. It can stream the 3DS top screen to a PC like NTR CFW. Development is a little strange... Archives of builds are hosted on this website: https://chainswordcs.com/horizon-by-sono.html

So, older builds (February 2018) can stream in a TARGA image format. The capability is available for all games I believe, but for some games it is required (such as Mario Kart 7, Super Smash Bros. for Nintendo 3DS, Yoshi's New Island, and Pokemon Yellow Version)

The TARGA image format streamed by HzMod is non-standard, so this repository is to document our reverse engineering efforts. Eventually we plan to push some changes to Snickerstream to add support to TARGA streams: https://github.com/RattletraPM/Snickerstream

# Running the Script

This script is written in Python 3. It requires the 'pillow' module.

This is not a generic TARGA reader. It is only designed to interpret HzMod TGAs, so certain header information is hard-coded as it is constant for HzMod.

There are several available command-line arguments:

* `-log`: Log each packet and some metadata to the console
* `-logcolor`: Color-code log output as RGB, with purple for the attribute bit
* `-noimage`: Don't output an image
* `-txt`: Take input from a text file containing a hex string on the first line
* `-txtanim`: Create an animated image with input from a text file containing a hex string on each line
* `-tga` or `-bin`: Take input from a binary file
* `-hex`: Take input from a hex string

All input, raw or as a file, is at the end of the command. For example, `python TGAHzParse.py -txt -log input.txt` takes input as a hex string in input.txt.

Output images are saved as TGAHZ.png for single frames or TGAHZ.gif for animations.

# Key

* R = This bit is part of the Red
* G = This bit is part of the Green
* B = This bit is part of the Blue
* A = This bit is the 'Attribute Bit'

# Image Parsing Results

## Commit [139fa60](https://github.com/Eiim/TGAHz-Parsing/commit/139fa601fc96389fba8d3332ca6f058a16d84994)

https://cdn.discordapp.com/attachments/836413155894100050/837059467703091210/TGAHZ.png

Bit order: ARRRRRGG GGGBBBBB

![](https://cdn.discordapp.com/attachments/836413155894100050/837059467703091210/TGAHZ.png)

## Commit [387e216](https://github.com/Eiim/TGAHz-Parsing/commit/387e2164f31f00570f211fb9b1e1fff9c635d218)

https://cdn.discordapp.com/attachments/836413155894100050/837069486389198848/RRRRRRGG_GGGBBBBB.png

Bit order: RRRRRRGG GGGBBBBB

![](https://cdn.discordapp.com/attachments/836413155894100050/837069486389198848/RRRRRRGG_GGGBBBBB.png)

https://cdn.discordapp.com/attachments/836413155894100050/837069485445218364/RRRRRGGG_GGGBBBB.png

Bit order: RRRRRGGG GGGBBBBA

![](https://cdn.discordapp.com/attachments/836413155894100050/837069485445218364/RRRRRGGG_GGGBBBB.png)

https://cdn.discordapp.com/attachments/836413155894100050/837069483596185620/RRRRRGGG_GGBBBBBA.png

Bit order: RRRRRGGG GGBBBBBA

![](https://cdn.discordapp.com/attachments/836413155894100050/837069483596185620/RRRRRGGG_GGBBBBBA.png)

## Commit [4c910bf](https://github.com/Eiim/TGAHz-Parsing/commit/4c910bf2f3f5fc08fdeacda75d5cde884d9f5a98)

https://cdn.discordapp.com/attachments/836413155894100050/837097268192346142/TGAHZ.png

![](https://cdn.discordapp.com/attachments/836413155894100050/837097268192346142/TGAHZ.png)

## Commit [60452bc](https://github.com/Eiim/TGAHz-Parsing/commit/60452bcff908b58125ce49026add7b1556cd39ae)

https://cdn.discordapp.com/attachments/836413155894100050/837153929284157491/TGAHZ.png

![](https://cdn.discordapp.com/attachments/836413155894100050/837153929284157491/TGAHZ.png)

## Commit [39ac5f4](https://github.com/Eiim/TGAHz-Parsing/commit/39ac5f437bed6ea7bf5bab137a8edd4fc5924a01)

Fixed a bug in the byte-grabbing code which was causing weird errors at every RAW packet. This was the only bug remaining in the past two revisions.

Also, colors are pretty darn accurate.

https://cdn.discordapp.com/attachments/836413155894100050/837196767270666310/TGAHZ.png

![](https://cdn.discordapp.com/attachments/836413155894100050/837196767270666310/TGAHZ.png)
