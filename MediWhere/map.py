import folium
from pandas import *

# 위도 경도 지정
map_osm = folium.Map (location = [37.568477, 126.981611],zoom_start=20
                      ,tiles='Open Street Map')
# 마커 지정
folium.Marker([126.967812251,37.5688670052], popup='Mt. Hood Meadows').add_to(map_osm)

# html 파일로 저장
map_osm.save('osm.html')

