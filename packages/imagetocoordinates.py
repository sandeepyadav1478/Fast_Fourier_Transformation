import cv2
import numpy as np
import json

def imgtocord(img_path = 'sample1.jpg'  # image path
            , type = "gray"        # output cordinates of type image
            , threshold_level = 50 # Set threshold level for filter out colors
            , file_loc = 'coordinate.txt'
            , screen_size=(500,500) # pygame window size
            , canny_pass =  [400, #threshold 1
                             430, #threshold 2
                             1 #apertureSize
                             ]):
    image = cv2.imread(img_path)
    #getting size according to screen size
    iwidth = image.shape[1]
    iheight = image.shape[0]
    scale_percent = 100 # percent of original size
    while iwidth > screen_size[1] or iheight > screen_size[0]:
        scale_percent = scale_percent - 1
        iwidth = int(image.shape[1] * scale_percent / 100)
        iheight = int(image.shape[0] * scale_percent / 100)

    dim = (iwidth, iheight)
    #
    # resize image
    image = cv2.resize(image, dim, interpolation = cv2.INTER_AREA)
    #
    #showing original image
    cv2.imshow('original image', image)
    #
    # gray filtered image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #
    # black and white filter
    (thresh, blackAndWhiteImage) = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
    #
    # detection of the edges
    img_edge = cv2.Canny(gray, canny_pass[0], canny_pass[1], canny_pass[2])
    #

    # Find coordinates of all pixels below threshold   
    # Recording number of cordinates in image
    font = cv2.FONT_HERSHEY_SIMPLEX
    img_cord = np.zeros((65,400), np.uint8)

    coords = np.column_stack(np.where(gray < threshold_level))
    cv2.putText(img_cord,"Gray image have "+str(len(coords))+" coordinates.",(1,15), font, 0.5,(255,255,255),1)
    coords = np.column_stack(np.where(blackAndWhiteImage < threshold_level))
    cv2.putText(img_cord,"Black & White image have "+str(len(coords))+" coordinates.",(1,35), font, 0.5,(255,255,255),1)
    coords = np.column_stack(np.where(img_edge == 255))
    cv2.putText(img_cord,"Edge detected image have "+str(len(coords))+" coordinates.",(1,55), font, 0.5,(255,255,255),1)
    #
    # Create mask of all pixels lower than threshold level
    if type == "gray":
        coords = np.column_stack(np.where(gray < threshold_level))
        mask = gray < threshold_level

    elif type == "b&w":
        coords = np.column_stack(np.where(blackAndWhiteImage < threshold_level))        
        mask = blackAndWhiteImage < threshold_level

    elif type == "edge":
        coords = np.column_stack(np.where(img_edge == threshold_level))
        mask = img_edge == threshold_level
    
    coords = coords.tolist()
    #
    #swap cordinates
    new_coords = []
    for i in coords:
        new_coords.append(list([i[1],i[0]]))
    #

    print(len(new_coords),"cords are saved in file.")
    
    # saving to file_path
    file = open(file_loc, "w")
    json.dump(new_coords,file)
    file.close()
    #

    # Color the pixels in the mask
    image[mask] = (204, 119, 0)
    #

    cv2.imshow('black and white image', blackAndWhiteImage)
    cv2.imshow('Masked image | Recorded coordinates', image)
    cv2.imshow('gray image', gray)
    cv2.imshow("Edges detect in Image",img_edge)
    cv2.imshow("Recorded cords are",img_cord)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    if len(new_coords) > 0:
        return str(len(new_coords))+" pixels saved."
    else:
        return "pixels not found check threshold!"
# imgtocord(img_path="sample3.jpg", type = "gray", threshold_level=255)