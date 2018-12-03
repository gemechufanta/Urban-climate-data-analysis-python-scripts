import numpy as np
import os
import pandas as pd
import netCDF4 as nc
from netCDF4 import Dataset
import glob
import Ngl
folder="/sf1/escer/blanchet/gemechu/NA_ARCHIVE/NA_ERA_class_teb_new/Samples/"
lst_class=nc.Dataset(folder+"NA_ERA_class_teb_new_monthly_CLASS_2000-2014.nc",'r')
lst_teb=nc.Dataset(folder+"NA_ERA_class_teb_new_monthly_TEB_2000-2014.nc",'r')
lst_class_data_monthly=lst_class.variables['ts'][:]-273.15
lst_teb_data_monthly=lst_teb.variables['ts'][:]-273.15
lat2d=lst_class.variables['lat'][:]
lon2d=lst_class.variables['lon'][:]
time=lst_class.variables['time'][:]
lat=lat2d[0]
lon=lon2d[0]
#Annual mean
lst_class_data=np.mean((lst_class_data_monthly),axis=0)
lst_teb_data=np.mean((lst_teb_data_monthly),axis=0)
#lst_class_annual_mean=np.mean((lst_class_data),axis=0)
#lst_teb_annual_mean=np.mean((lst_teb_data),axis=0)
##################### get stations data ##############
file_loc='/sf1/escer/blanchet/gemechu/MODIS/monthly/'
#f = netcdf.netcdf_file(file_loc+'daymet_v3_tmax_monavg_1980_na.nc4', 'r')
f=nc.Dataset(file_loc+'MODIS-C06__MOD11C3__MONTHLY__LandSurfaceTemperature__0.05deg__UHAM-ICDC__2000-2014__fv0.01_NorthAmerica_regridded.nc4','r')

lst_modis_day=f.variables['lst_day'][:] 
#lst_modis_day_ax=np.swapaxes(lst_modis_day,1,2)
lst_modis_day_mean=np.mean((lst_modis_day),axis=0)

lst_modis_night=f.variables['lst_night'][:] 
#lstmonth_night_ax=np.swapaxes(lstmonth_night,1,2)
lst_modis_night_mean=np.mean((lst_modis_night),axis=0)

#Monthly mean
lst_modis_data_monthly=(lst_modis_day + lst_modis_night)/2


#tmonth_mean=np.nanmean(np.array([lstmonth_day , lstmonth_night]), axis=0)
tannual_mean=np.nanmean(np.array([lst_modis_day_mean, lst_modis_night_mean]), axis=0)
lst_modis_mean=(lst_modis_day_mean + lst_modis_night_mean)/2
#tannual_mean=np.swapaxes(tannual_mean_ax,1,2)


lat_obs=f.variables['lat'][:]

lon_obs=f.variables['lon'][:] 

######################Get bldf #####
filell ='/sf1/escer/blanchet/gemechu/'
me       =nc.Dataset(filell+'MF.nc')
bldf     =nc.Dataset(filell+'BLDF.nc')
pavf     =nc.Dataset(filell+'PAVF.nc')
oro  =me.variables['orog'][:]
bldf_data=bldf.variables['bldfr'][:]
pavf_data=pavf.variables['imp'][:]

urbf=bldf_data+pavf_data

oro_ext = np.ones(lst_teb_data.shape) * oro.squeeze()[np.newaxis,:,:]
urbf_ext = np.ones(lst_teb_data.shape) * urbf.squeeze()[np.newaxis,:,:]

lst_teb_data=lst_teb_data.squeeze()[np.newaxis,:,:]
lst_class_data=lst_class_data.squeeze()[np.newaxis,:,:]

teb_filterd=np.ma.masked_where(oro_ext<=0,lst_teb_data, copy=True)
ann_sea_teb=np.ma.masked_where(urbf_ext<=0.0,teb_filterd, copy=True) 

class_filterd=np.ma.masked_where(oro_ext<=0,lst_class_data, copy=True)
ann_sea_class=np.ma.masked_where(urbf_ext<=0.0,class_filterd, copy=True)  

lst_modis_mean=lst_modis_mean.squeeze()[np.newaxis,:,:]

modis_filterd=np.ma.masked_where(oro_ext<=0,lst_modis_mean, copy=True)
ann_sea_modis=np.ma.masked_where(urbf_ext<=0.0,modis_filterd, copy=True)  

#----------- Begin first plot -----------------------------------------
wkres = Ngl.Resources()
#wkres.wkColorMap=colors
rlist               = Ngl.Resources()

wks_type = "png"
if(wks_type == "ps" or wks_type == "pdf"):
  rlist.wkOrientation = "Portrait"      # For PS or PDF output only.
wks = Ngl.open_wks(wks_type,"J8_teb_current_validation_urban_mean_teb_class",wkres)
#wks2 = Ngl.open_wks(wks_type,"J8_teb_current_all_3h_validation3",wkres)
colors=["White","Black","SkyBlue","Turquoise","Blue","Green","Yellow","Orange","tomato","Magenta","PaleVioletRed","Maroon","red4","Red"]
#colors=["White","Black","SkyBlue","Turquoise","PaleVioletRed","Red"]
Ngl.define_colormap(wks,colors)
#Ngl.define_colormap(wks,"BlGrYeOrReVi200")
#Ngl.define_colormap(wks,"hotres")
#Ngl.define_colormap(wks2,colors)

#Ngl.define_colormap(wks,"GHRSST_anomaly")
resources = Ngl.Resources()

Ngl.set_values(wks,resources)
resources.pmLabelBarDisplayMode = "Never" # Turn on label bar.
resources.pmLabelBarDisplayMode = "Never" # Turn on label bar.
#resources.pmLabelBarWidthF = 0.50

resources.nglDraw             = False           # dont draw
resources.nglFrame            =  False          # dont advance frame
#resources.nglAddCyclic        = False 


#resources.cnFillOn = True
resources.cnLinesOn = False
#resources.cnMonoFillPattern  = True 
#resources.cnFillPalette     = cmap[:-3,:]
#resources.cnFillPalette          = "BlGrYeOrReVi200"
#  resources.mpCenterLatF =  90 - north_pole_lat
#  resources.mpCenterLonF =  180 + north_pole_lon

#  resources.mpCenterLonF           = lon@Longitude_of_southern_pole 
#  resources.mpCenterLatF           = lon@Latitude_of_southern_pole + 90

#resources.nglSpreadColors = True
resources.mpDataBaseVersion = "MediumRes"
resources.mpOutlineBoundarySets  = "National"

resources.mpDataSetName   = "Earth..4"         # choose most resent boundaries
#---Turn on nicer tickmarks. 'conditional' prevents more than one tickmark object.
resources.pmTickMarkDisplayMode  = "conditional"

  #
# Since the Y-Axis of these data goes from north to south, the Y-Axis
# needs to be reversed to plot it correctly in a "native" projection.
# 
resources.trYReverse             = True#
# Setting tfDoNDCOverlay to True means you have specified the
# exact projection that your data is on, and thus no data
# transformation takes place when the contours are overlaid
# on the map.
# 
resources.tfDoNDCOverlay         = False 
 # resources.mpProjection = "CylindricalEquidistant"
 # resources.mpCenterLonF = 180.0+pollon
 # resources.mpCenterLatF = 90.0-pollat


resources.mpLimitMode = "LatLon"    # Limit the map view.
resources.mpMinLonF   = float(min(lon2d[0,:]))# - 5.0
resources.mpMaxLonF   = float(max(lon2d[144,:])) - 15.0
resources.mpMinLatF   = float(min(lat2d[0,:])) + 8.0
resources.mpMaxLatF   = float(max(lat2d[144,:])) - 5.0
resources.mpGridAndLimbOn      = False               # turn on grid lines


resources.sfXCStartV = float(min(lon2d[0,:]))
resources.sfXCEndV   = float(max(lon2d[0,:]))
resources.sfYCStartV = float(min(lat2d[0,:]))
resources.sfYCEndV   = float(max(lat2d[0,:]))
resources.sfXArray            = lon_obs[:]
resources.sfYArray            = lat_obs[:]
resources.nglMaximize         = True      # Maximize plot in frame  
resources.cnFillOn            = True                  # color fill
resources.cnMonoFillColor     = False

#resources.mpFillOn              =  True         # Turn on map fill.
#resources.mpFillAreaSpecifiers  = ["Water","Land"]
#resources.mpSpecifiedFillColors = np.array([[255,255,255],[255,255,255]])
#resources.mpSpecifiedFillColors =[0,0]           # np.array([[10,10.,10.],[10.,10.,10.]])
#resources.mpAreaMaskingOn       = True            # Indicate we want to
#resources.mpMaskAreaSpecifiers = ["Land"] 
#resources.mpMaskAreaSpecifiers  = "USStatesLand"  # mask land.
resources.mpPerimOn             = True            # Turn on a perimeter.
resources.mpGridMaskMode        = "MaskOcean"      # Mask grid over land.
#resources.mpAreaMaskingOn = True 
resources.cnFillDrawOrder       = "PreDraw"       # Draw contours first.


#resources.tmXBMode      = "Explicit"   # Define your own tick mark labels.
resources.tmXBLabelFont = "times-roman"      # Change font of labels.
resources.tmXBLabelFontHeightF = 0.035 # Change font height of labels.
resources.tiXAxisFontHeightF = 0.035 # Change font height of labels.
resources.tiYAxisFontHeightF = 0.035 # Change font height of labels.

#resources.tmYBLabelFont = "times-roman"      # Change font of labels.
#resources.tmYBLabelFontHeightF = 0.025 # Change font height of labels.

#resources.cnMonoFillPattern = True 
#resources.cnFillOn          = True                  # color fill

#resources.cnFillColors      =  [2,3,4,5,6,7,8]
resources.cnLevelSelectionMode = "ExplicitLevels"
#resources.cnMinLevelValF  = 0.0                    #    set the minimum contour level
#resources.cnMaxLevelValF  =  4.0                     # set the maximum contour level
#resources.cnLevelSpacingF = 0.5                      # set the interval between contours

#resources.cnLevelSelectionMode = "AutomaticLevels"
#  resources.cnLevels        = (/ 0/)
# # resources.cnLevelSpacingF   = 1.                    # interval spacing
resources.nglSpreadColors     = True                # use full colormap
#resources.nglSpreadColorStart = 2 
#resources.nglSpreadColorEnd   = -3  
#if hasattr(lon,"long_name"):
#  resources.tiXAxisString = lon.long_name
#if hasattr(lat,"long_name"):
#  resources.tiYAxisString = lat.long_name
#if hasattr(tt_3d,"long_name"):
#  resources.tiMainString = temp.long_name 
resources.tiYAxisString = "latitude"
resources.tiXAxisString = "longitude"
resources.tiMainString  = ""
#resources.nglLeftString  = "2m-T" 
#resources.nglRightString  = "K " 
#resources.nglCenterString = ""
resources.lbLabelBarOn        = False           # turn off individual cb

#resources.lbLabelAlignment  = "BoxCenters"
#resources.cnConstFEnableFill  = True   
#resources.lbOrientation     ="Vertical"
resources.cnConstFLabelOn     = True
#For the plot2
#resources2 = Ngl.Resources()
#resources2.sfXCStartV = min(lon2)
#resources2.sfXCEndV   = max(lon2)

#resources2.gsnMaximize     = True

#resources.gsnFrame        = False        #; Don't draw or advance
#resources.gsnDraw         = False        # frame yet.

#resources2.sfYCStartV = min(lat2)
#resources2.sfYCEndV   = max(lat2)
#resources2.cnFillOn   = True
#resources2.cnFillMode   = "RasterFill"
#resources2.cnFillColors = ramp 
#resources2.cnLevelSelectionMode  = "EqualSpacedLevels"
#resources2.cnMaxLevelCount       = 254  

#labels=["DJF","MAM","JJA","SON"] #labels0=["ANN MODIS"]
labels=["MODIS","TEB","CLASS"] #labels0=["ANN MODIS"]
#resources2.tiMainString =labels0[0]+" "+" "+labels[0]
#resources2.tiMainFontHeightF = 0.045 

#plot1=Ngl.contour(wks2,band2,resources2)

resources.nglDraw             = False           # dont draw
resources.nglFrame            =  False          # dont advance frame

resources.cnLevelSelectionMode = "ExplicitLevels"
#resources.cnMinLevelValF  = 0.0                    #    set the minimum contour level
#resources.cnMaxLevelValF  =  4.0                     # set the maximum contour level
#resources.cnLevelSpacingF = 0.5                      # set the interval between contours

#Levels        = [-5,0,5,10,15,20,25]
Levels        = [0,2,4,6,8,10,12,14,16,18,20]
resources.lbLabelStrings   = Levels   # Format the labels
#resources.lbLavelAlignment = "ExternalEdges"
#resources.cnLabelBarEndStyle = "IncludeMinMaxLabels"
resources.cnLabelBarEndStyle = "ExcludeOuterBoxes"
resources.cnLevels         =    resources.lbLabelStrings
resources.lbLabelFontHeightF =.022                 # make labels larger
resources.lbTitleOn        = True                  # turn on title
resources.lbTitleString    = "Temperature (~S~o~N~C)"
resources.lbTitleFontHeightF= .015                 # make title smaller
resources.lbTitleOffsetF            = -0.27
resources.lbBoxMinorExtentF         = 0.15
resources.pmLabelBarOrthogonalPosF  = -0.01
resources.lbOrientation             = "Vertical"

resources.pmLabelBarOrthogonalPosF = .10 

#Modis
#for j in range(0,5):
resources.tiMainFontHeightF = 0.045
resources.tiMainString =labels[0]
plot=[]
plot.append(Ngl.contour_map(wks,ann_sea_modis[0,:,:],resources))
#TEB model
#for i in range(0,5):

resources.sfXArray            = lon2d[:]
resources.sfYArray            = lat2d[:]
resources.tiMainFontHeightF = 0.045
resources.tiMainString =labels[1]#+" "+" "+labels[1]
plot.append(Ngl.contour_map(wks,ann_sea_teb[0,:,:],resources))


#CLASS
#for l in range(0,5):
resources.tiMainString =labels[2]#+" "+" "+labels[2]
plot.append(Ngl.contour_map(wks,ann_sea_class[0,:,:],resources))
panelres                            = Ngl.Resources()
panelres.nglPanelRowSpec            = True 
panelres.nglPanelYWhiteSpacePercent = 5.
panelres.nglPanelXWhiteSpacePercent = 5.
#panelres.lbLabelAlignment           =  "BoxCenters"       #-- where to label
#panelres.txString         = "Current (1981 - 2010)"
panelres.nglPanelLabelBar = True   # Common labelbar
panelres.lbOrientation     ="vertical"
panelres.lbLabelStride = 1
panelres.nglPanelLabelBarHeightF=0.800
panelres.nglPanelLabelBarWidthF=0.0000015
panelres.lbTitleString    = "LST(~S~o~N~C)"
panelres.lbTitleFontHeightF= .015                 # make title smaller
panelres.gsnMaximize    = True                # maximize plots
#panelres.nglPanelLabelBarYF=0.010
#panelres.nglPanelLabelBarXF=0.005
panelres.nglPanelLabelBarLabelFontHeightF=0.020
#panelres.gsnPanelFigureStrings = ["ANN","JJA","SON","DJF","MAM"]
Ngl.panel(wks,plot[0:3],[1,1,1],panelres)    #

del plot
del resources
del wks

#Now plot the time series data
#Get area averages of the data
oro_ext_tseries = np.ones(lst_teb_data_monthly.shape) * oro.squeeze()[np.newaxis,:, :]
ubf_ext_tseries = np.ones(lst_teb_data_monthly.shape) * urbf.squeeze()[np.newaxis,:, :]

oro_ext_tseries2 = np.ones(lst_modis_data_monthly.shape) * oro.squeeze()[np.newaxis,:, :]
ubf_ext_tseries2 = np.ones(lst_modis_data_monthly.shape) * urbf.squeeze()[np.newaxis,:, :]

mon_filterd=np.ma.masked_where(oro_ext_tseries<=0,lst_teb_data_monthly, copy=True)
mon_model=np.ma.masked_where(ubf_ext_tseries<=0.0,mon_filterd, copy=True)
mon_filterd2=np.ma.masked_where(oro_ext_tseries<=0,lst_class_data_monthly, copy=True)
mon_model2=np.ma.masked_where(ubf_ext_tseries<=0.0,mon_filterd2, copy=True)

modis_mon_filterd=np.ma.masked_where(oro_ext_tseries2<=0,lst_modis_data_monthly, copy=True)
modis_mon=np.ma.masked_where(ubf_ext_tseries2<=0.0,modis_mon_filterd, copy=True)


MODIS_Avg_tseries=np.mean(np.mean(modis_mon,axis=2),axis=1)
TEB_Avg_tseries=np.mean(np.mean(mon_model,axis=2),axis=1) 
CLASS_Avg_tseries=np.mean(np.mean(mon_model2,axis=2),axis=1)

print 'MODIS_Avg_tseries ',MODIS_Avg_tseries.shape
print 'TEB_Avg_tseries ',TEB_Avg_tseries.shape
print 'CLASS_Avg_tseries ',CLASS_Avg_tseries.shape

print 'max MODIS ',np.amax(MODIS_Avg_tseries)
print 'min MODIS ',np.amin(MODIS_Avg_tseries)
#Average values

MODIS_area_Avg=np.mean(MODIS_Avg_tseries, axis=0)
TEB_area_Avg=np.mean(TEB_Avg_tseries, axis=0)
CLASS_area_Avg=np.mean(CLASS_Avg_tseries, axis=0)

print 'avg MODIS:',MODIS_area_Avg
print 'avg TEB:',TEB_area_Avg
print 'avg CLASS:',CLASS_area_Avg
 
#Collect data into one file
data_tseries=np.stack((MODIS_Avg_tseries[:,],TEB_Avg_tseries[1:180,],CLASS_Avg_tseries[1:180,]),axis=0)

#Now plot

if(wks_type == "ps" or wks_type == "pdf"):
  rlist.wkOrientation = "Portrait"      # For PS or PDF output only.
wks = Ngl.open_wks(wks_type,"J8_teb_current_validation_tseries",wkres)
Tres = Ngl.Resources()
Tres.tiXAxisString          = "Months"
Tres = Ngl.Resources()
Tres.tiYAxisString          = "Temperature (~S~o~N~C)"
Tres.tiXAxisFontHeightF     = 0.025        # Change the font size.
Tres.tiYAxisFontHeightF     = 0.025
Tres.xyLineColors           = ["Blue","Green","Red"]    # Set the line colors.
Tres.xyLineThicknessF       = 5.0         # Double the width.
#res.xyDashPatterns         = [2,5,10,12]
Tres.xyMarkLineModes        = ["MarkLines","MarkLines","MarkLines","MarkLines"]
Tres.xyMarkers              = [2,3,5,12]     # (none, dot, asterisk)
Tres.xyMarkerColors          = ["Blue","Green","Red"]         # Marker color
Tres.xyMarkerSizeF          = 0.01        # Marker size (default
Tres.xyMarkerThicknessF     = 3.0         # Double the width.
Tres.nglDraw                =  True           # dont draw
Tres.nglFrame               = True           # dont advance frame
#res.xyLabelMode            = "Custom"    # Label XY curves.
#res.xyExplicitLabels       = ["W","Sp","Su","Au"]   # Labels for curves
Tres.xyLineLabelFontHeightF = 0.025        # Font size and color
Tres.xyLineLabelFontColor   = 189         # for line labels
x=range(1,13)
Tres.pmLegendDisplayMode = "Always"    # Turn on legend.
Tres.pmLegendSide        = "Top"
Tres.tiXAxisFontHeightF  = 0.035
Tres.tiYAxisFontHeightF     = 0.02
Tres.xyLineColors           = ["Blue","Green","Red"]    # Set the line colors.
Tres.xyLineThicknessF       = 5.0         # Double the width.
#res.xyDashPatterns         = [2,5,10,12]
Tres.xyMarkLineModes        = ["MarkLines","MarkLines","MarkLines","MarkLines"]
Tres.xyMarkers              = [2,3,5,12]     # (none, dot, asterisk)
Tres.xyMarkerColors          = ["Blue","Green","Red"]         # Marker color
Tres.xyMarkerSizeF          = 0.01        # Marker size (default
Tres.xyMarkerThicknessF     = 3.0         # Double the width.
Tres.nglDraw                =  True           # dont draw
Tres.nglFrame               = True           # dont advance frame
#res.xyLabelMode            = "Custom"    # Label XY curves.
#res.xyExplicitLabels       = ["W","Sp","Su","Au"]   # Labels for curves
Tres.xyLineLabelFontHeightF = 0.025        # Font size and color
Tres.xyLineLabelFontColor   = 189         # for line labels
x=range(1,13)
Tres.pmLegendDisplayMode    = "Always"    # Turn on legend.
Tres.pmLegendSide           = "Top"
Tres.tiXAxisFontHeightF     = 0.025
Tres.tiYAxisFontHeightF     = 0.025
Tres.pmLegendParallelPosF   = .41                  # move units right
Tres.pmLegendOrthogonalPosF = -0.9                # move units down
Tres.pmLegendWidthF         = 0.10                # Change width and
Tres.pmLegendHeightF        = 0.25                # height of legend.
Tres.tmXBLabelFontHeightF = 0.0035
Tres.tmYLLabelFontHeightF = 0.035
Tres.lgPerimOn              = False               # turn off box around
Tres.tmXBLabelFont = "times-roman"      # Change font of labels.
Tres.tiXAxisFontHeightF = 0.025 # Change font height of labels.
Tres.tiYAxisFontHeightF = 0.025 # Change font height of labels.
Tres.xyExplicitLegendLabels = ["MODIS","TEB","CLASS"]         # create explicit labels
Tres.lgAutoManage           = False
Tres.lgLabelFontHeightF     = .025                 # label font height
Tres.tmXBMode = "Manual"
Tres.tmXBTickStartF  = 1
Tres.tmXBTickEndF  = 12
Tres.tmXBTickSpacingF= 1
Tres.tmXBMode = "Explicit"
Tres.tmXBValues =[1,2,3,4,5,6,7,8,9,10,11,12]
Tres.tmXBLabels =["JAN","FEB","MAR","APR","MAY","JUN","JUL","AUG","SEP","OCT","NOV","DEC"]
Tres.tmXBLabelAngleF = 45        # tilt the XB labels 45 degrees
Tres.tmXBLabelDeltaF = 0.5     # push the XB labels down from plot
Tres.tmYLMode  = "Explicit"
Tres.tmYLValues = [-4,0,4,8,12,16,20,24]
Tres.tmYLLabels =Tres.tmYLValues

#res.lgLabelFontAspectF     = 2.0                 # label font height
Tres.lgOrientation          = "Vertical"
#llabels=["Zone I","Zone II","Zone III"]
#res.tiMainString = llabels[0]
Tres.tiMainFontHeightF=0.040

plot = []
x=range(1,13)
plot.append(Ngl.xy(wks,x,data_tseries,Tres))

plres                            = Ngl.Resources()
plres.nglPanelRowSpec            = True
plres.nglPanelYWhiteSpacePercent = 5.
plres.nglPanelXWhiteSpacePercent = 5.
#plres.txString         = "Current (1981 - 2010)"
#plres.nglPanelLabelBar = True   # Common labelbar
#plres.lbOrientation     ="Vertical"
#plres.gsnPanelFigureStrings = ["ANN","JJA","SON","DJF","MAM"]

Ngl.panel(wks,plot,[3],plres)    # Draw 2 rows/2 columns of plots.
print 'python annual climatology output  and '+lst_teb.history

#Write outputs to netcdf file 
dataset=nc.Dataset('./TEB_CLASS_MODIS_AnnualClim_LST.nc', 'w', format='NETCDF4_CLASSIC') 

nlat=len(lat2d[:,0])
nlon=len(lon2d[0,:])



lat = dataset.createDimension('lat', nlat)
lon = dataset.createDimension('lon', nlon) 
time = dataset.createDimension('time', 1 ) 
#Create coordinate variables
latitude=dataset.createVariable('latitude', np.float32, ('lat','lon'))
longitude=dataset.createVariable('longitude', np.float32, ('lon','lat'))
times=dataset.createVariable('time',np.float32, ('time',))
#Create the variable
MODIS_LST=dataset.createVariable('MODIS_LST',np.float32, ('time','lat','lon',))
CLASS_LST=dataset.createVariable('CLASS_LST',np.float32, ('time','lat','lon',))
TEB_LST=dataset.createVariable('TEB_LST',np.float32, ('time','lat','lon',))

# Global Attributes
dataset.description = 'LST MODIS CLASS  and TEB'
dataset.history='python annual climatology output  and '+lst_teb.history

# Variable Attributes
latitude.units = 'degree_north'  
longitude.units = 'degree_east'  
MODIS_LST.units = 'deg C' 
CLASS_LST.units = 'deg C' 
TEB_LST.units = 'deg C' 
times.units="hours since 2000-01-01 00:00:00"
times.calendar = "proleptic_gregorian" 
MODIS_LST.standard_name = "surface_temperature"
MODIS_LST.long_name = "Surface Temperature" 
MODIS_LST.coordinates = "longitude latitude"
#MODIS_LST._FillValue = lst_teb_data_monthly._FillValue 
#MODIS_LST.missing_value = lst_teb_data_monthly.missing_value
MODIS_LST.grid_desc = "rotated_pole" 
#Writing data
print latitude.shape
print longitude.shape
print lat2d.shape
print lon2d.shape
latitude[:]=lat2d
longitude[:]=lon2d
times[:]=1

MODIS_LST[:,:,:]=ann_sea_modis
TEB_LST[:,:,:]=ann_sea_teb
CLASS_LST[:,:,:]=ann_sea_class
dataset.close
Ngl.end()



