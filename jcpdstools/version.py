"""
JCPDSTools version

Todo:

"""
__version__ = "0.1.5"
"""
0.1.5 Add pip packaging (pyproject), package-safe imports, and CLI entrypoint.
0.1.4 Remove local ds_jcpds package; import directly from peakpo.ds_jcpds.
0.1.3 Remove qdarkstyle dependency; use native PyQt5 dark palette.
0.1.2 Enforce peakpo.ds_jcpds backend (no local ds_jcpds fallback).
0.1.1 Use peakpo.ds_jcpds backend by default; legacy fallback is opt-in.
0.1.0 Pip install in PeakPo environment to refer to peakpo module
0.0.8 Strengthen help, disable dioptas JCPDS button.
0.0.7 Block dioptas JCPDS output function due to crash of peakpo.
0.0.6 Add Dioptas JCPDS output.  However, it is less tested than other functions.
0.0.5 Default comment writings and filenames change
0.0.4 Clean up UI.
0.0.3 Add some error checking functions for JCPDS
"""
