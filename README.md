# python=3.9
# mamba
# gdal
# geopandas
# rasterio
# numpy

conda create -n gis39 -c conda-forge python=3.9 mamba -y  #Step 1：创建干净环境（只放 Python + mamba）
conda activate gis39
where python
mamba install -c conda-forge --override-channels gdal -y #矢量
mamba install -c conda-forge --override-channels geopandas -y #矢量
mamba install -c conda-forge --override-channels rasterio -y #栅格

