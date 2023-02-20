# Diverse Part Discovery: Occluded Person Re-Identification With Part-Aware Transformer[[pdf]](https://openaccess.thecvf.com/content/CVPR2021/supplemental/Li_Diverse_Part_Discovery_CVPR_2021_supplemental.pdf)   

Unofficial PAT code

## Model   
![fig](https://user-images.githubusercontent.com/33828383/220055963-8c5ee05e-3429-4d1e-98df-9b2af8aa9d0f.png)

## Cfg example   
```
from easydict import EasyDict
cfg = EasyDict({
        "out_channels": 2048,
        "k_parts": 14,
        "d_model": 512,
        "num_head": 8,
        "dropout": 0.1,
        "layer_norm_eps": 1e-6,
        "device": "cuda"
})
```

## Getting start  
- used Colab
- pip install easydict TBC..
 
## Training   
TBC