
# Superpixel Clustering for Image Segmentation

Code started with [Superpixel Hierarchical Clustering algorithm (SPHC) For Image Segmentation](https://github.com/thompspe/image-segm) repository, but changed a lot, became much more faster.

### Superpixel Segmentation

<p align="center">
  <img src="https://raw.githubusercontent.com/falreis/image-segm/master/paper/images/superpixels.png" >
  <span>Superpixel segmentation methods</span>
</p>

### Hierarchical Methods for Superpixel Segmentation

<p align="center">
  <img src="https://raw.githubusercontent.com/falreis/image-segm/master/paper/images/slic_hierarquia_particoes.png" >
  <span>Partition hierarchy of segmentation methods</span>
</p>

## Goals

- New hierarchical superpixel clustering method;
- Superpixels comparison;
- Results tested on BSDS500 dataset;
- Jupyter notebook codes, with images and examples;

## Prerequisites

### Conda Environment

You can use Conda to configure your environment. Conda file with all prerequisites are available here

```shell
conda env create -f i2dl.yml
```
## Code

### Detailed Notebooks

* [fmeasure-segb.ipynb](https://github.com/falreis/image-segm/blob/master/code/fmeasure-segb.ipynb) - Creates hierarchical segmentation with superpixels algorithms;
* [fmeasure.ipynb](https://github.com/falreis/image-segm/blob/master/code/fmeasure.ipynb) - Creates regular segmentation with superpixels algorithms;
* [segmentation.ipynb](https://github.com/falreis/image-segm/blob/master/code/segmentation.ipynb) - Provides example of the developed method;
* [test_groundtruth.ipynb](https://github.com/falreis/image-segm/blob/master/code/test_groundtruth.ipynb) - Notebook just to test groundthruth evaluation method;
* [plot.ipynb](https://github.com/falreis/image-segm/blob/master/code/plot.ipynb) - Plot results of hierarchical and regular segmentation methods;

## Paper

Contains a [paper](https://github.com/falreis/image-segm/blob/master/paper/sbc-template.pdf) (*unpublished*) showing the results of the superpixels algorithms and comparing them. Available only in portuguese.

## References

Available in [bib folder](https://github.com/falreis/image-segm/tree/master/bib) or inside the [paper](https://github.com/falreis/image-segm/blob/master/paper/sbc-template.pdf).
