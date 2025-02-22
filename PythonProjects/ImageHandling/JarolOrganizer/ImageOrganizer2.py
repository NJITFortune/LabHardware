#!//Users/efortune/NotCloudy/JarolTest/Jarolsplayground/bin/python3

import os
import shutil
from datetime import datetime
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import folium
import base64

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

def create_thumbnail(image_path, thumbnail_path, size=(150, 150)):
    try:
        with Image.open(image_path) as img:
            img.thumbnail(size)
            img.save(thumbnail_path, "JPEG")
    except Exception as e:
        print(f"Error creating thumbnail for {image_path}: {e}")

def encode_image(image_path):
    try:
        with open(image_path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode("utf-8")
    except Exception as e:
        print(f"Error encoding image {image_path}: {e}")
        return None

def organize_photos_by_date(source_directory, output_directory):
    if not os.path.exists(source_directory):
        print("Source directory does not exist.")
        return
    os.makedirs(output_directory, exist_ok=True)
    
    map_data = []
    
    for filename in os.listdir(source_directory):
        file_path = os.path.join(source_directory, filename)
        if not os.path.isfile(file_path):
            continue
        
        photo_date = get_photo_date(file_path)
        date_directory = os.path.join(output_directory, photo_date.strftime("%Y-%m-%d"))
        os.makedirs(date_directory, exist_ok=True)
        
        new_file_path = os.path.join(date_directory, filename)
        shutil.move(file_path, new_file_path)
        print(f"Moved {filename} to {date_directory}")
        
        gps_coords = get_gps_coordinates(new_file_path)
        if gps_coords:
            thumbnail_path = os.path.join(date_directory, f"thumb_{filename}")
            create_thumbnail(new_file_path, thumbnail_path)
            encoded_thumbnail = encode_image(thumbnail_path)
            if encoded_thumbnail:
                map_data.append((gps_coords, photo_date, filename, encoded_thumbnail))
    
    if map_data:
        map_center = map_data[0][0]
        photo_map = folium.Map(location=map_center, zoom_start=10)
        for coords, date, filename, encoded_thumbnail in map_data:
            popup_html = f'<div><strong>{date} - {filename}</strong><br><img src="data:image/jpeg;base64,{encoded_thumbnail}" width="150"></div>'
            folium.Marker(
                location=coords,
                popup=folium.Popup(popup_html, max_width=300)
            ).add_to(photo_map)
        
        map_path = os.path.join(output_directory, "photo_map.html")
        photo_map.save(map_path)
        print(f"Map saved to {map_path}")

if __name__ == "__main__":
    import sys
    if len(sys.argv) < 3:
        print("Usage: python script.py <source_directory> <output_directory>")
    else:
        source_directory = sys.argv[1]
        output_directory = sys.argv[2]
        organize_photos_by_date(source_directory, output_directory)

