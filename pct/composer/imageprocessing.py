# -*- coding: utf-8 -*-

import math
import numpy
import cv2

from ..common.configuration import (
    PCT_BORDER_PIXELS,
)

def resize_image_width(image, width):
    current_width = image.shape[1]
    if width == current_width:
        return image.copy()
    
    current_height = image.shape[0]
    height = (width * current_height) // current_width
    
    if width < current_width:
        interp = cv2.INTER_AREA
    else:
        interp = cv2.INTER_LINEAR
    return cv2.resize(image, (width, height), interpolation=interp)

def resize_image_height(image, height):
    current_height = image.shape[0]
    if height == current_height:
        return image.copy()
    
    current_width = image.shape[1]
    width = (height * current_width) // current_height
    
    if height < current_height:
        interp = cv2.INTER_AREA
    else:
        interp = cv2.INTER_LINEAR
    return cv2.resize(image, (width, height), interpolation=interp)

def rotate_image(image, angle):
    rows, cols, _ = image.shape
    M = cv2.getRotationMatrix2D((cols // 2, rows // 2), -angle, 1)
    return cv2.warpAffine(image, M, (cols,rows))

def add_image_border(image, noleft=False):
    if noleft:
        left_pixels = 0
    else:
        left_pixels = PCT_BORDER_PIXELS
    return cv2.copyMakeBorder(
        image,
        PCT_BORDER_PIXELS,
        PCT_BORDER_PIXELS,
        left_pixels,
        PCT_BORDER_PIXELS,
        cv2.BORDER_CONSTANT,
    )

def compose_images(images, height):
    resized_images = [resize_image_height(img, height) for img in images]
    
    # Image borders are a little hacky
    bordered_images = []
    for index, img in enumerate(resized_images):
        if index == 0:
            bordered_images.append(add_image_border(img))
        else:
            bordered_images.append(add_image_border(img, True))
            
    return numpy.concatenate(bordered_images, axis=1)

# A lot of this code was based off of https://goo.gl/Rnpyvx
def find_dominant_contours(image, strength):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur_str = 1 + 2 * strength
    blurred = cv2.GaussianBlur(gray, (blur_str, blur_str), 0)
    edge_str = 250 // math.sqrt(strength)
    edged = cv2.Canny(blurred, 0, edge_str)
    _, contours, _ = cv2.findContours(edged, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)
 
    contours = sorted(contours, key=cv2.contourArea, reverse=True)
    return contours
    for cnt in contours:
        return cnt
        print(cv2.contourArea(cnt))
        epsilon = 0.1 * cv2.arcLength(cnt, True)
        approx = cv2.approxPolyDP(cnt, epsilon, True)
        print(len(approx))
        print(cv2.contourArea(approx))
        if len(approx) == 4:
            return approx
        
    return None

def draw_contours(image, contours):
    new_image = image.copy()
    cv2.drawContours(new_image, contours, -1, (0, 255, 0), 10)
    return new_image