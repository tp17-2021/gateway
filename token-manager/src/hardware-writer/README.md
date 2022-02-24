# Linux wrapper for SL600-NFC Reader

Implemented features:
- Turn off led
- Turn on led
- Read from Mifare 1k tag (4th block)
- Write to Mifare 1k tag (4th block)
- Validate write

Example code writes random 16 bytes to 4th block of Mifare 1k tag, then reads from it to validate the write. If everything is ok, the program will exit.