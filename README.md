1. Install osmium tool to extract the file for specific location and time-filtered OSM data. 
2. Download latest OSM data from geofabrik in .osm.pbf format.
3. Open terminal and run the following command to get your specific data.
```
#OSM data of initial date
osmium time-filter -o data1.osm.pbf history-planet.osm.pbf 2008-01-01T00:00:00Z 

#OSM data of final date
osmium time-filter -o data2.osm.pbf history-planet.osm.pbf 2023-01-01T00:00:00Z

#now extracting data of specific location of initial date
osmium extract -b 11.35,48.05,11.73,48.25 data1.osm.pbf -o initial.osm.pbf

#extracting data of specific location of final date
osmium extract -b 11.35,48.05,11.73,48.25 data2.osm.pbf -o final.osm.pbf
```

These initial.osm.pbf and final.osm.pbf are now compared by the python file OSMmodification.py 

In JSON file, store the desired tags as key in the list. 

Open terminal in the file directory and run the following command for the output. 

```
python OSMmodification.py 
```

The output of the program will be the tags as keys and the count of it being added, removed or modified. #morestats
