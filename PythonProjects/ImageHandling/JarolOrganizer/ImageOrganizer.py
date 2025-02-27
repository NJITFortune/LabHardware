#!//Users/efortune/NotCloudy/JarolTest/Jarolsplayground/bin/python3

import os
import shutil
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import folium

def get_exif_data(image):
    try:
        exif_data = image._getexif()
        if not exif_data:
            return {}
        return {TAGS.get(tag, tag): value for tag, value in exif_data.items()}
    except Exception:
        return {}

def get_photo_date(photo_path):
    try:
        with Image.open(photo_path) as img:
            exif_data = get_exif_data(img)
            if "DateTimeOriginal" in exif_data:
                return datetime.strptime(exif_data["DateTimeOriginal"], "%Y:%m:%d %H:%M:%S").date()
    except Exception:
        pass
    
    return datetime.fromtimestamp(os.path.getmtime(photo_path)).date()

def get_gps_coordinates(photo_path):
    try:
        with Image.open(photo_path) as img:
            exif_data = get_exif_data(img)
            if "GPSInfo" in exif_data:
                gps_info = exif_data["GPSInfo"]
                gps_data = {GPSTAGS.get(tag, tag): value for tag, value in gps_info.items()}
                
                if "GPSLatitude" in gps_data and "GPSLongitude" in gps_data:
                    lat = gps_data["GPSLatitude"]
                    lon = gps_data["GPSLongitude"]
                    lat_ref = gps_data.get("GPSLatitudeRef", "N")
                    lon_ref = gps_data.get("GPSLongitudeRef", "E")
                    
                    lat = (lat[0] + lat[1] / 60.0 + lat[2] / 3600.0) * (-1 if lat_ref == "S" else 1)
                    lon = (lon[0] + lon[1] / 60.0 + lon[2] / 3600.0) * (-1 if lon_ref == "W" else 1)
                    return lat, lon
    except Exception:
        pass
    return None

def organize_photos_by_date(source_directory):
    if not os.path.exists(source_directory):
        print("Source directory does not exist.")
        return
    
    map_data = []
    
    for filename in os.listdir(source_directory):
        file_path = os.path.join(source_directory, filename)
        if not os.path.isfile(file_path):
            continue
        
        photo_date = get_photo_date(file_path)
        date_directory = os.path.join(source_directory, photo_date.strftime("%Y-%m-%d"))
        os.makedirs(date_directory, exist_ok=True)
        
        new_file_path = os.path.join(date_directory, filename)
        shutil.move(file_path, new_file_path)
        print(f"Moved {filename} to {date_directory}")
        
        gps_coords = get_gps_coordinates(new_file_path)
        if gps_coords:
            map_data.append((gps_coords, photo_date, filename))
    
    if map_data:
        map_center = map_data[0][0]
        photo_map = folium.Map(location=map_center, zoom_start=10)
        for coords, date, filename in map_data:
            folium.Marker(
                location=coords,
                popup=f"{date} - {filename}"
            ).add_to(photo_map)
        
        map_path = os.path.join(source_directory, "photo_map.html")
        photo_map.save(map_path)
        print(f"Map saved to {map_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 2:
        print("Usage: python script.py <source_directory>")
    else:
        source_directory = sys.argv[1]
        organize_photos_by_date(source_directory)

