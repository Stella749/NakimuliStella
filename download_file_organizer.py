import os
import shutil
from pathlib import Path

DOWNLOADS_DIR = Path.home() / "Downloads"

FILE_CATEGORIES = {
    "Documents": [".pdf", ".docx", ".doc", ".txt", ".xlsx", ".xls", ".pptx", ".csv"],
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg", ".webp"],
    "Audio_Video": [".mp3", ".wav", ".mp4", ".mkv", ".mov", ".avi"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Installers": [".exe", ".msi", ".dmg", ".pkg"],
    "Code_Files": [".py", ".html", ".css", ".js", ".json"]
}

def organize_downloads():
    print(f"Scanning directory: {DOWNLOADS_DIR}\n")
    
    if not DOWNLOADS_DIR.exists():
        print("Error: Downloads directory not found.")
        return

    moved_count = 0

    for item in DOWNLOADS_DIR.iterdir():
    
        if item.is_dir():
            continue
            
        file_extension = item.suffix.lower()
        file_moved = False

        for category, extensions in FILE_CATEGORIES.items():
            if file_extension in extensions:
                
                category_folder = DOWNLOADS_DIR / category
                category_folder.mkdir(exist_ok=True)
                
                destination = category_folder / item.name
                
                if destination.exists():
                    print(f"[Skipped] {item.name} already exists in {category}.")
                    file_moved = True
                    break

                shutil.move(str(item), str(destination))
                print(f"[Moved] {item.name} -> {category}/")
                moved_count += 1
                file_moved = True
                break
        
        if not file_moved and file_extension != "":
            others_folder = DOWNLOADS_DIR / "Others"
            others_folder.mkdir(exist_ok=True)
            destination = others_folder / item.name
            
            if not destination.exists():
                shutil.move(str(item), str(destination))
                print(f"[Moved] {item.name} -> Others/")
                moved_count += 1

    print(f"\nTask Complete! Total files organized: {moved_count}")

if __name__ == "__main__":
    organize_downloads()