
'''
Forked from https://github.com/RobinDavid/pyADS/blob/master/pyads.py
This program does significantly less, however, it lists the files within a
specified directory and any alternative data streams
'''

# Specify the directory to look in here:
directory = "dummy"
# Specify the maximum length of the filename to show
maxlength = 64

# Import ctypes, sys, os
from ctypes import *
import os
kernel32 = windll.kernel32

# Constants to be used
LPSTR     = c_wchar_p
DWORD     = c_ulong
LONG      = c_ulong
WCHAR     = c_wchar * 296
LONGLONG  = c_longlong

class LARGE_INTEGER_UNION(Structure):
    _fields_ = [
        ("LowPart", DWORD),
        ("HighPart", LONG),]


class LARGE_INTEGER(Union):
    _fields_ = [
        ("large1", LARGE_INTEGER_UNION),
        ("large2", LARGE_INTEGER_UNION),
        ("QuadPart",    LONGLONG),
    ]

class WIN32_FIND_STREAM_DATA(Structure):
    _fields_ = [
        ("StreamSize", LARGE_INTEGER),
        ("cStreamName", WCHAR),
    ]

class ADS():
    # Constructor for class ADS sets up the filename field and the streams field
    def __init__(self, filename):
        self.filename = filename
        self.streams = self.init_streams()

    # Sets up the streams
    def init_streams(self):
        file_infos = WIN32_FIND_STREAM_DATA()
        streamlist = list()
        myhandler = kernel32.FindFirstStreamW (LPSTR(self.filename), 0, byref(file_infos), 0)

        if file_infos.cStreamName:
            # Add the stream name to the list if it exists
            streamname = file_infos.cStreamName.split(":")[1]
            if streamname: streamlist.append(streamname)
            # Add additional streams
            while kernel32.FindNextStreamW(myhandler, byref(file_infos)):
                streamlist.append(file_infos.cStreamName.split(":")[1])
        kernel32.FindClose(myhandler)
        return streamlist

    # Allow for iteration through each stream
    def __iter__(self):
        return iter(self.streams)

    # returns true if the file has ADS, false if not
    def has_streams(self):
        return len(self.streams) > 0

# Only read files in directory
#files = [file for file in os.listdir(directory) if os.path.isfile(os.path.join(directory, file))]

# Read everything in directory
files = [file for file in os.listdir(directory)]

# Iterate through each file
for file in files:
    handler = ADS(directory+ "\\" + file)
    print("Reading " + ( file[:maxlength] + "..." ) if (len(file)>maxlength)  else file)
    # Print ADS stream if applicable "No ADS found" if not
    if handler.has_streams():
        # Iterate through each stream
        for stream in handler:
            print("\tADS found: " + stream)
    else:
        print("\tNo ADS found")
    print()




