import matplotlib.pyplot as plt
import numpy as np
import copy
from scipy.cluster import hierarchy
from skimage.segmentation import slic, mark_boundaries, felzenszwalb
from skimage import io

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

def generate_ultrametric_map(blank_image, colors, segments, n_seg):
    Z = hierarchy.linkage(colors)
    
    it = 5
    step = int(n_seg/it)
    cutz_images = []
    cutz_nsegs = []
    
    cutz_images.append(mark_boundaries(blank_image, segments, color=(0, 0, 0)))
    cutz_nsegs.append(n_seg)

    for ix in range(it-1, 0, -1):
        cluster_size= int(ix * step)

        cutz = hierarchy.cut_tree(Z, n_clusters = cluster_size)
        cutz_segs = copy.deepcopy(segments)

        for i in range(len(segments)):
            for j in range(len(segments[i])):
                index = segments[i][j]
                cutz_segs[i][j] = cutz[index][0]

        cutz_images.append(mark_boundaries(blank_image, cutz_segs, color=(0, 0, 0)))
        cutz_nsegs.append(cluster_size)
    
    return cutz_images, cutz_nsegs


def process_image(image, save=False, filename = '', paths=[]):
    '''
     * image - current image
     * save - save processing results
     * filename - filename with extension (jpg)
     * paths - [0] - segmentation path
               [1] - border path
               [2] - ultrametric map path
    '''
    #process slic
    segs_slic = slic(image, n_segments = 512, slic_zero = True)
    slic_image, _, _ = color_superpixel(image, segs_slic)

    #process felzenszwalb
    segs_fs = felzenszwalb(slic_image, scale = 1536, min_size = 30)
    fs_image, n_segs_fs, colors_fs = color_superpixel(slic_image, segs_fs)
    
    #borders
    img = np.zeros(image.shape,dtype=np.uint8) #create blank image to save
    img.fill(255)
    fs_borders = mark_boundaries(img, segs_fs, color=(0, 0, 0))
    
    #ultrametric
    ultra_images, ultra_nsegs = generate_ultrametric_map(img, colors_fs, segs_fs, n_segs_fs)
    
    if save == True:
        if filename != '' and len(paths) == 3:
            #save segmentation image
            io.imsave((paths[0] + 'seg_' +filename), fs_image)
            
            #save borders
            io.imsave((paths[1] + 'bor_' +filename), fs_borders)

            #save ultrametric
            for u_img, u_nseg in zip(ultra_images, ultra_nsegs):
                io.imsave((paths[2] + 'ult_' + filename[:-4] + '_' + str(u_nseg) + '.jpg'), u_img)
                
    return fs_image, fs_borders, ultra_images
    
print('Done')

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
    