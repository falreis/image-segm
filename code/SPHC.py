### Superpixel Hierarchical Clustering algorithm (SPHC)
## Method and Code for merging Superpixels created by Paul Thompson (Please credit if you use this code)
# The algorithm takes image superpixels created by the skimage SLIC function and merges neighors in order of
# color similarity (using euclidean distance).

#References:
#1. http://www.kev-smith.com/papers/SLIC_Superpixels.pdf
#2. http://www.pyimagesearch.com/2014/07/28/a-slic-superpixel-tutorial-using-python/

#####INSTRUCTIONS###################################################################################
### To use:
### 1. Change the parameters below
### 2. Change image path. This was only tested with jpg's.
### 3. Run program

#SLIC Parameters:
#numSegments = 500  # How many superpixels to start with - input for SLIC function
#Sigma = 4 # This parameter controls superpixel shape. Higher values make superpixels more square.

#SPHC Parameters:
#segmentsToMerge = 400 # How many superpixels to merge based on color similarity
#distance_limit = .5 # Limits which segments get merged based on their difference in average color
####################################################################################################

import matplotlib.pyplot as plt, argparse, numpy as np, math, sys, copy
from skimage.segmentation import slic, mark_boundaries
from skimage.util import img_as_float
from skimage import io
from collections import defaultdict
import numpy

def generateDictionary(segm_grid, image):
    '''
    Each segment formed by sklearn's SLIC function is assigned a dictionary of attributes for efficiency.
    :param segm_grid: Each pixel has been identified with a segment identifier by the skimage SLIC function
    :param image: Each pixel has R, B, and G value associated with it
    :return: Dictionary of dictionaries of attributes for each segment
    '''
    def initialSegmAttr():
        '''
        return {'neighbors': set(), 'R': [], 'G': [], 'B': [], 'coord': set(),
                         'R_avg': 0.0, 'G_avg': 0.0, 'B_avg': 0.0}
        '''
        return {'neighbors': set(), 'RGB': [], 'coord': set(), 'RGB_avg': []}
    segm_dict = defaultdict(initialSegmAttr)

    len_line = len(segm_grid) - 1
    len_col = len(segm_grid[0]) -1

    for line in range(len_line):
        line1 = line+1

        for col in range(len_col):
            col1 = col+1

            if segm_grid[line][col] != segm_grid[line][col1]:
                segm_dict[segm_grid[line][col]]['neighbors'].add(segm_grid[line][col1])

            if segm_grid[line][col] != segm_grid[line1][col]:
                segm_dict[segm_grid[line][col]]['neighbors'].add(segm_grid[line1][col])
                
            segm_dict[segm_grid[line][col]]['RGB'].append(image[line][col])
            segm_dict[segm_grid[line][col]]['coord'].add((line,col))

    #adiciona o último item a lista (dev para reduzir comparações)
    segm_dict[segm_grid[len_line][len_col]]['RGB'].append(image[len_line][len_col])
    segm_dict[segm_grid[len_line][len_col]]['coord'].add((len_line,len_col))
    
    for k, v in segm_dict.items():
        v['RGB_avg'] = np.average(v['RGB'], axis=0)
    
    return segm_dict

def toGrid(segm_grid, segm_dicts):
    seg_grids = segm_dicts

    for dicts in segm_dicts:
        newSegmGrid = np.copy(segm_grid)
        
        for k, v in dicts.items():
            for coord in v['coord']:
                newSegmGrid[coord[0], coord[1]] = int(k)
                
        seg_grids.append(newSegmGrid)

    return seg_grids

def getNearestNeighbors(segm_dict):
    '''
    Calculates the average R, B, and G values for each segment. Then finds the two neighboring segments with
    the smallest euclidean distance (for the three dimensions of R, B, and G).
    :param segm_dict: dictionary of dictionaries of segment attributes
    :return: segment pair with smallest color euclidean distance; distance value
    '''
    #for k, v in segm_dict.items():
    #    v['RGB_avg'] = np.average(v['RGB'], axis=0)

    neighbor_pairs = set()
    nearest_neighbors = []
    shortest_dist = 100.0

    for k, v in segm_dict.items():
        for neighbor in v['neighbors']:
            neighbor_pair = tuple([k, neighbor])            
            eucl_dist = float(math.sqrt(np.sum((v['RGB_avg'] - segm_dict[neighbor]['RGB_avg']) ** 2)))

            if eucl_dist < shortest_dist:
                shortest_dist = eucl_dist
                nearest_neighbors = neighbor_pair

    return nearest_neighbors, shortest_dist

def mergeSegments(segm_dict, nearest_neighbors):
    '''
    Merges the pair of neighboring segments with the shortest euclidean distance (greatest color similarity)
    :param segm_dict: dictionary of dictionaries of segment attributes
    :param nearest_neighbors: segment pair with smallest color euclidean distance
    :return: segm_dict: updated dictionary of dictionaries of segment attributes
    '''
    to_dict = segm_dict[nearest_neighbors[0]]
    from_dict = copy.deepcopy(segm_dict[nearest_neighbors[1]])

    #fill new neighbors
    to_dict['neighbors'] = to_dict['neighbors'] #| from_dict['neighbors']
    to_dict['neighbors'].discard(nearest_neighbors[0])
    to_dict['neighbors'].discard(nearest_neighbors[1])
    
    #fill new rgb and coord
    to_dict['RGB'] += from_dict['RGB']
    to_dict['coord'] = to_dict['coord'] | from_dict['coord']
    
    #fill new RGB_avg
    len_to = len(to_dict['coord'])
    len_from = len(from_dict['coord'])
    to_dict['RGB_avg'] = ((to_dict['RGB_avg'] * len_to) + (from_dict['RGB_avg'] * len_from)) / (len_from + len_to)

    for neighbor in from_dict['neighbors']:
        to_dict['neighbors'].add(neighbor)
        
    for k, v in segm_dict.items():
        v['neighbors'].discard(nearest_neighbors[1]) #remove reference if exists

    del segm_dict[nearest_neighbors[1]]
    return segm_dict

def getSPHCsegmentsVect(segm_grid, image, numToMerge = [], max_dist = 1.0, verbose_freq = 10):
    '''
    Main function for running SPHC clustering algorithm. Initiates segment attributes. Then
    iteratively finds and merges neighboring segments with most similar color.
    :param segm_grid: Each pixel has been identified with a segment identifier by the skimage SLIC function
    :param image: Each pixel has R, B, and G value associated with it
    :param numToMerge: List of ordered number of inputs
    :param max_dist: Maximum euclidean distance for pair of segments to merge
    :return: segm_grid: Each pixel has been identified with a segment identifier by the SPHC function
    '''
    print("Initiating Segment Attributes...")
    segm_dict = generateDictionary(segm_grid, image)
    shortest_dist = 0.0
    merge_count = 0
    
    maxNumToMerge = numToMerge[-1]
    lenNumToMerge = len(numToMerge)
    dicts = []
    j = 0
    
    print("Merging Segments...")
    while (shortest_dist <= max_dist) and (merge_count < maxNumToMerge):
        nearest_neighbors, shortest_dist = getNearestNeighbors(segm_dict)
        segm_dict = mergeSegments(segm_dict, nearest_neighbors)
        merge_count += 1
        
        if(merge_count == numToMerge[j]):
            dicts.append(segm_dict.copy())
            j += 1

        #verbose mode - print merge information
        if((merge_count % verbose_freq) == 0):
            print((str(merge_count) + '/' + str(maxNumToMerge) + ' segments merged \r'), end='')
    #endwhile

    #if(merge_count < maxNumToMerge):
    #    dicts.append(segm_dict.copy())

    #print merge information
    print(merge_count, "segments merged - final")

    return dicts #toGrid(segm_grid, dicts)
