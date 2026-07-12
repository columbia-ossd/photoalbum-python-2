from photo import Photo
from album import Album
import os
from graphics import *

def get_value_between(prompt, low, high):
    while True:
        try:
            choice = int(input(prompt))
        except ValueError:
            print("Please enter a valid number!")
            continue
        if choice < low or choice > high:
            print("Please enter a value between %d and %d" % (low, high))
            continue
        return choice

def saveAlbum(album, filename):
    fp = open(filename, "w")
    for photo in album.get_photos():
        parts = []
        parts.append(photo.get_filename())
        parts.append(photo.get_creator())
        parts.append(photo.get_description())
        
        for tag in photo.get_tags():
            parts.append(tag)
            
        line = ",".join(parts)
        fp.write(line+"\n")
        
    fp.close()

def initialize(filename, title):
    album = Album(title)

    fp = open(filename, "r")

    for line in fp:
        line = line.strip()
        parts = line.split(",")
        fname = parts[0]
        creator = parts[1]
        description = parts[2]
        tags = []
        for i in range(3, len(parts)):
            tags.append(parts[i])
        album.add_photo(Photo(fname, creator, description, tags))

    fp.close()

    return album

def menu():
    print()
    print("1: List all photos")
    print("2: Add a photo")
    print("3: Search photos by tag")
    print("4: View a photo")
    print("5: Edit a photo")
    print("6: Exit")

    choice = get_value_between("Choose an option: ", 1, 6)
    return choice

def editPhoto(album):
    """
    Function for Menu Option 5
    """
    print("Edit Photo")
    photos = album.get_photos()
    for i in range(len(photos)):
        print("%d: %s | %s | created by %s" % (i+1, photos[i].get_description(), photos[i].get_filename(), photos[i].get_creator()))
    choice = get_value_between("Choose a photo to edit: ", 1, len(photos))
    selected_photo = photos[choice-1]
    print()
    print("1: Filename")
    print("2: Creator")
    print("3: Description")
    field_choice = get_value_between("Choose a field to edit: ", 1, 3)
    if field_choice == 1:
        while True:
            new_filename = get_input("Enter the new filename: ")
            
            if not os.path.isfile(new_filename):
                print("Photo file DNE. Try again.")
                continue
            
            duplicate = False
            for photo in album.get_photos():
                if photo != selected_photo and photo.get_filename() == new_filename:
                    duplicate = True
                    break
            if duplicate:
                print("Filename taken. Try again.")
                continue
            selected_photo.edit_filename(new_filename)
            break
                
    elif field_choice == 2:
        new_creator = get_input("Enter the new creator: ")
        selected_photo.edit_creator(new_creator)
    elif field_choice == 3:
        new_description = get_input("Enter the new description: ")
        selected_photo.edit_description(new_description)
    saveAlbum(album, "dogs.txt")
    print("Photo successfully edited")

def viewPhoto(album):
    """
    Function for Menu Option 4
    """
    print()
    photos = album.get_photos()
    for i in range(len(photos)):
        print("%d: %s"  % (i+1, photos[i].get_description()))
    choice = get_value_between("Choose a photo: ", 1, len(photos))
    
    name = photos[choice-1].get_filename()
    display_image(name)

def display_image(name):
    """
    Helper function that we provide
    """
    try:
        image = Image(Point(250, 250), name)
        win = GraphWin(name, image.getWidth(), image.getHeight())
        win.setCoords(0, 0, 500, 500)
        image.draw(win)
        try:
            win.getMouse()
            win.close()
        except:
            pass
    except:
        print("An error occurred trying to open %s" % name)


def searchByTag(album):
    """
    Function for Menu Option 3
    """
    print()
    tags = " ".join(album.get_tags())
    print("Here are the tags: " + tags)
    term = input("Enter the tag to search for: ").lower()
    found = []
    for photo in album.get_photos():
        if term in photo.get_tags():
            found.append(photo)
    if len(found) > 0:
        print("Here are the photos for that tag:")
        for photo in found:
            print(str(photo))
    else:
        print("No photos found for tag " + term)
    

def get_input(prompt):
    resp = ""
    while len(resp.strip()) == 0:
        resp = input(prompt)  
    return resp      


def addPhoto(album):
    """
    Function for Menu Option 2
    """
    print("Add Photo")
    fname = get_input("Enter the name of the file: ")
    creator = get_input("Enter the name of the creator: ")
    description = get_input("Enter the description: ")
    tagString = input("Enter all the tags, separated by spaces: ")
    tags = tagString.split(" ")
    #print(tags)
    if album.add_photo(Photo(fname, creator, description, tags)):
        print("Photo successfully added")
    else:
        print("Could not add photo to album")


def main():
    album = initialize("dogs.txt", "cartoon dog photos")

    choice = -1

    while choice != 6:
        choice = menu()
        if choice == 1: # list all photos
            for photo in album.get_photos():
              print(str(photo))
        elif choice == 2: # add a photo
            addPhoto(album)
        elif choice == 3: # search by tag
            searchByTag(album)
        elif choice == 4: # view a photo
            viewPhoto(album)
        elif choice == 5: # Edit a photo
            editPhoto(album)
    
    print("Good bye!")


if __name__ == "__main__":
    main()