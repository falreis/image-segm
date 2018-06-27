import matplotlib.pyplot as plt, argparse, numpy as np, math, sys, copy

def merge_superpixels_colors(image, segments):
    n_seg = 0

    #get number of segments
    for segs in segments:
        curr_max = max(segs)
        if(curr_max > n_seg):
            n_seg = curr_max

    n_seg += 1
    
    #initalize variables
    colors = [[.0, .0, .0] for x in range(n_seg)]
    itens = [0 for x in range(n_seg)]
    new_image = copy.deepcopy(image)

    #indexing information
    for i in range(len(segments)):
        for j in range(len(segments[i])):
            index = segments[i][j]
            colors[index] += image[i][j]
            itens[index] += 1

    #define new values
    for i in range(len(itens)):
        if(itens[i] > 0):
            colors[i] = [x / itens[i] for x in colors[i]]

    #generate new image
    for i in range(len(segments)):
        for j in range(len(segments[i])):
            index = segments[i][j]
            new_image[i][j] = colors[index]

    #return image
    return new_image

def plot_compare_5(images = [], labels = [], axis_off = False):
    f, (ax1, ax2, ax3, ax4, ax5) = plt.subplots(1, 5, figsize=(20,20))
    
    #remove axis
    if axis_off == True:
        ax1.set_axis_off()
        ax2.set_axis_off()
        ax3.set_axis_off()
        ax4.set_axis_off()
        ax5.set_axis_off()
    
    ax1.imshow(images[0])
    ax2.imshow(images[1])
    ax3.imshow(images[2])
    ax4.imshow(images[3])
    ax5.imshow(images[4])
    
    if len(labels) > 0:
        ax1.set_title(labels[0])
        ax2.set_title(labels[1])
        ax3.set_title(labels[2])
        ax4.set_title(labels[3])
        ax5.set_title(labels[4])
    plt.show()
    
def plot_compare_4(images = [], labels = [], axis_off = False):
    f, (ax1, ax2, ax3, ax4) = plt.subplots(1, 4, figsize=(20,20))
    
    #remove axis
    if axis_off == True:
        ax1.set_axis_off()
        ax2.set_axis_off()
        ax3.set_axis_off()
        ax4.set_axis_off()
    
    ax1.imshow(images[0])
    ax2.imshow(images[1])
    ax3.imshow(images[2])
    ax4.imshow(images[3])
    
    if len(labels) > 0:
        ax1.set_title(labels[0])
        ax2.set_title(labels[1])
        ax3.set_title(labels[2])
        ax4.set_title(labels[3])
    plt.show()
    
def color_superpixel(image, segments):
    n_seg = 0
    for segs in segments:
        curr_max = max(segs)
        if(curr_max > n_seg):
            n_seg = curr_max

    n_seg += 1
    
    colors = [[.0, .0, .0] for x in range(n_seg)]
    itens = [0 for x in range(n_seg)]
    new_image = copy.deepcopy(image)

    #replace colors
    for i in range(len(segments)):
        for j in range(len(segments[i])):
            index = segments[i][j]
            colors[index] += image[i][j]
            itens[index] += 1

    for i in range(len(itens)):
        if(itens[i] > 0):
            colors[i] = [x / itens[i] for x in colors[i]]

    for i in range(len(segments)):
        for j in range(len(segments[i])):
            index = segments[i][j]
            new_image[i][j] = colors[index]
    
    return new_image, n_seg, colors
    