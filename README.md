# REM - using QGIS and pyQGIS
#REM- Beautiful Maps based on @klarrieu https://github.com/OpenTopography/RiverREM/blob/main/riverrem/REMMaker.py. forked with QGIS to make it easier and to produce different flood #maps from pyqgis
#The code form @klarrieu is used with changes for updates. But most importantly, QuickOSM from QGIS is obtain the river shape file. Later the REM.tif output is processed with PyQGIS to #draw different levels of water on min max scaler of QGIS. 
#Create geo_env and activate following instructions from @klarrieu.
Use QGIS Open topo to produce DEM or use any public repository to download DEM of area of interest as a .tif file
Use the REM-QGIS+pyQGIS in compiler
