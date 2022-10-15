
import cv2

def create_keyboard(mapping = ["QWERTYUIOP", "ASDFGHJKL;'", "ZXCVBNM,.?"], starting_coordinate=(0, 0), size=50, spacing = 5):
    keys = {}

    # First Row
    for index, key in enumerate(list(mapping[0])):
        x, y =(starting_coordinate[0] + (size +spacing) * index, starting_coordinate[1])
        keys[key] = (x + int(size/2), y + int(size/2))
    
    # Second Row    
    for index, key in enumerate(list(mapping[1])):
        x, y =(starting_coordinate[0] + 20 + (size +spacing) * index, starting_coordinate[1] + size + spacing)
        keys[key] = (x + int(size/2), y + int(size/2))

    # Third Row    
    for index, key in enumerate(list(mapping[2])):
        x, y =(starting_coordinate[0] + 40 + (size +spacing) * index, starting_coordinate[1] + (size + spacing) * 2)        
        keys[key] = (x + int(size/2), y + int(size/2))


    # Space
    x, y = (starting_coordinate[0] + 100 + (size +spacing), starting_coordinate[1] + (size + spacing) * 3)
    keys[' '] = (x + 180, y + int(size/2))

    return keys


def show_keyboard (img, keys, mapping = ["QWERTYUIOP", "ASDFGHJKL;'", "ZXCVBNM,.?"], starting_coordinate=(0, 0), size=50, spacing = 5):

    for index, key in enumerate(list(mapping[0])):
        x, y =(starting_coordinate[0] + (size +spacing) * index, starting_coordinate[1])
        img = cv2.rectangle(img, (x, y), (x+ size , y+size), (0, 255, 0), 1)
        img = cv2.circle(img, keys[key], 10, (255, 255, 0), cv2.FILLED) 

    for index, key in enumerate(list(mapping[1])):
        x, y =(starting_coordinate[0] + 20 + (size +spacing) * index, starting_coordinate[1] + size + spacing)
        img = cv2.rectangle(img, (x, y), (x+ size , y+size), (0, 255, 0), 1)
        img = cv2.circle(img, keys[key], 10, (255, 255, 0), cv2.FILLED) 
        

    for index, key in enumerate(list(mapping[2])):
        x, y =(starting_coordinate[0] + 40 + (size +spacing) * index, starting_coordinate[1] + (size + spacing) * 2)
        img = cv2.rectangle(img, (x, y), (x+ size , y+size), (0, 255, 0), 1)
        img = cv2.circle(img, keys[key], 10, (255, 255, 0), cv2.FILLED) 

    x, y = (starting_coordinate[0] + 100 + (size +spacing), starting_coordinate[1] + (size + spacing) * 3)
    img = cv2.rectangle(img, (x, y), (x+ 360 , y+size), (0, 255, 0), 1)
    img = cv2.circle(img, keys[' '], 2, (255, 255, 0), cv2.FILLED) 
    
    return img