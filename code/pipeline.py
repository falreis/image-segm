import superpixels as sp
from skimage.segmentation import slic, mark_boundaries, felzenszwalb

def generate_boundaries(image, blank_image, method='sgb'):
    border = None
    
    if(method == 'sgb'):
        #1664;1920 | 1664;1280 | 1536;1024 | 1536;1152 | *1408;1536 | 1408;1408
        
        _, border, _ = sp.process_image(image
                                        , slic_segments = 1408
                                        , felz_scale = 1408
                                        , felz_min_size = 20
                                        , ultrametric = False
                                        , save=False)
    elif(method=='egb'):
        f_segs = felzenszwalb(image, scale=300, sigma=0.8, min_size=20)
        border = mark_boundaries(blank_image, f_segs, color=(0, 0, 0))
        
    elif(method == 'slic'):
        s_segs = slic(image, n_segments = 300, slic_zero = True) #300 ou 100
        border = mark_boundaries(blank_image, s_segs, color=(0, 0, 0))
        
    else:
        return None

    return border[:, :, 0:1]