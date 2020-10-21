from obspy.imaging.beachball import beachball
from obspy import read

mt=[0.0, -1.0, 1.0, 0.0, 0.0, -0.4]
fig = beachball(mt, width=600)
fig.savefig('focalmech.png')