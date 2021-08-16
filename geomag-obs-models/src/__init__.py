from os.path import dirname, abspath, join

_here = dirname(abspath(__file__))

IGRF13_FILE = join(_here, "igrf13coeffs.txt")
lsfile = join(_here, "land_5deg.csv")
cfile = join(_here, "SwarmVO_IAGASummerSchool.dat")