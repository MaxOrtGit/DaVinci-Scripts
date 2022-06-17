
import warnings
from shapely.errors import ShapelyDeprecationWarning

from shapely.geometry import Point, LineString
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
warnings.filterwarnings("ignore", category=ShapelyDeprecationWarning)

x = 0.5
y = 0.5
size = 0.5

x -= 0.5
y -= 0.5

size = 1 / size

x *= -size
y *= -size

p1 = Point((0,0))
p2 = Point((x,y))

gp1 = gpd.GeoSeries(p1)
gp2 = gpd.GeoSeries(p2)

# Buffer the points using a square cap style
# Note cap_style: round = 1, flat = 2, square = 3
b1 = gp1.buffer(0.5, cap_style = 3)
b2 = gp2.buffer(size/2, cap_style = 3)

print(type(b1))

diff = b2.difference(b1)

outer_points = np.dstack(b2.boundary[0].coords.xy).tolist()[0]
tup_outer_points = [tuple(op) for op in outer_points]
diff_points = []
try:
  for b in diff[0].boundary: # for first feature/row
    coords = np.dstack(b.coords.xy).tolist()
    diff_points.append(*coords) 
except:
  diff_points = np.dstack(diff.boundary[0].coords.xy).tolist()
tup_diff_points = [[tuple(dp) for dp in dpa] for dpa in diff_points]
print(outer_points) 
print(tup_outer_points)
print(diff_points)
print(tup_diff_points)
#tup_all_coords = 
outer_line = LineString(tup_outer_points[:-1])

if len(tup_diff_points) == 1:
  diff_line = LineString(tup_diff_points[0][:-1])
elif len(tup_diff_points) == 2:
  diff_line = LineString(tup_diff_points[0][:3] + tup_diff_points[1] + tup_diff_points[0][2:-1])
else:
  print("more than 2 shapes inside")
  exit()
  
  

# Plot the results
fig, ax1 = plt.subplots()
if False:
  b1.boundary.plot(ax=ax1, color = '#ff050d')
  b2.boundary.plot(ax=ax1, color = '#05b4ff')
  diff.plot(ax = ax1, color = 'green')
  gp1.plot(ax = ax1, color = 'red')
  gp2.plot(ax = ax1, color = 'blue')
else:
  b1.boundary.plot(ax=ax1, color = '#ff050d')
  plt.plot(*outer_line.xy, color = '#05b4ff')
  plt.plot(*diff_line.xy, color = 'green')

# Plot the results
plt.show()