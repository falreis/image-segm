import matplotlib.pyplot as plt

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
 