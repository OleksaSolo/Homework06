import sys
from pathlib import Path
import uuid
import shutil

from normalize import normalize


CATEGORIES = {"Audio": [".mp3", ".aiff", ".amr", ".ogg", ".wav"],
              "Documents": [".doc", ".docx", ".rtf", ".xlsx", ".pptx", ".txt", ".pdf"],
              "Images":[".jpeg", ".png", ".jpg", ".svg"],
              "Video":[".avi", ".mp4", ".mov", ".mkv",],
              "Archives":[".zip", ".gz", ".tar"]}


def move_file(file: Path, root_dir: Path, categorie: str) -> None:
    target_dir = root_dir.joinpath(categorie)
    if not target_dir.exists():
        # print(f"Make {target_dir}")
        target_dir.mkdir()
    # print(path.suffix)
    # print(target_dir.joinpath(f"{normalize(path.stem)}{path.suffix}"))
    new_name = target_dir.joinpath(f"{normalize(file.stem)}{file.suffix}")
    if new_name.exists():
       new_name = new_name.with_name(f"{new_name.stem}-{uuid.uuid4()}{file.suffix}")
    file.rename(new_name)
    

def get_categories(file: Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat
    return "Other"


def sort_folder(path: Path) -> None:
    for item in path.glob("**/*"):
        # print(item)
        if item.is_file():
            cat = get_categories(item)
            move_file(item, path, cat)

def delete_emtpy_dirs(path: Path) -> None:
    for item in path.glob("**/*"):
        #print(item)
        if item.is_dir():
            delete_emtpy_dirs(item)
            # print(item)
            # if not any(item.iterdir()):
            if len(list(item.iterdir())) == 0:
                # print(item)
                # print(item.stat())
                # print(any(item.iterdir()))
                item.rmdir()

def upack_archive(path: Path) -> None:
    p = Path(path, "Archives")
    for item in p.glob("*"):
        if item.suffix == ".zip" or item.suffix == ".gz" or item.suffix == ".tar":  
            target_dir = p.joinpath(item.stem)
            # print(target_dir)
            if not target_dir.exists():
                target_dir.mkdir()
            shutil.unpack_archive(item, target_dir)
            item.unlink()



def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"
    
    if not path.exists():
        return f"Folder with path {path} dos`n exists."
    
    sort_folder(path)
    delete_emtpy_dirs(path)
    upack_archive(path)
    
    return "All ok"


if __name__ == "__main__":
    print(main())