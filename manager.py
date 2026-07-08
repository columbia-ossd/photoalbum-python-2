from photo import Photo
from album import Album
from graphics import *

def get_value_between(prompt, low, high):
    choice = int(input(prompt))
    while choice < low or choice > high:
        print("Please enter a value between %d and %d" % (low, high))
        choice = int(input(prompt))
    return choice


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
    print("5: Exit")

    choice = get_value_between("Choose an option: ", 1, 5)
    return choice

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

    search_terms = input("Enter the tag(s) to search for, separated by spaces: ").lower().split()

    # Remove duplicate search terms while keeping the original order.
    unique_terms = []
    for term in search_terms:
        if term not in unique_terms:
            unique_terms.append(term)

    if len(unique_terms) == 0:
        print("No tags entered")
        return

    all_matches = []
    partial_matches = []

    for photo in album.get_photos():
        photo_tags = photo.get_tags()
        matches_all = True
        matches_any = False

        for term in unique_terms:
            if term in photo_tags:
                matches_any = True
            else:
                matches_all = False

        if matches_all:
            all_matches.append(photo)
        elif matches_any:
            partial_matches.append(photo)

    if len(unique_terms) == 1:
        if len(all_matches) > 0:
            print("Here are the photos for that tag:")
            for photo in all_matches:
                print(str(photo))
        else:
            print("No photos found for tag " + unique_terms[0])
    else:
        if len(all_matches) > 0:
            print("Here are the photos with all of those tags:")
            for photo in all_matches:
                print(str(photo))
        else:
            print("No photos found with all of those tags")

        if len(partial_matches) > 0:
            print("Here are the photos with one or more of those tags:")
            for photo in partial_matches:
                print(str(photo))
        else:
            print("No additional photos found with one or more of those tags")

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

    while choice != 5:
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
    
    print("Good bye!")


if __name__ == "__main__":
    main()