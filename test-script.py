import sys
import os
import contextlib
import logging
import time

import pygeoprocessing.routing
from osgeo import gdal

gdal.SetCacheMax(2048)  # MB
logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

DEM = sys.argv[1]

@contextlib.contextmanager
def _time(message):
    start_time = time.time()
    yield
    LOGGER.info(f"{message} - elapsed time: {round(time.time() - start_time, 2)}")


def _process(input_dem, workspace, codec, predictor):
    creation_tuple = ('GTiff', [
            'TILED=YES', 'BIGTIFF=YES', f'COMPRESS={codec}',
            f'PREDICTOR={predictor}', 'BLOCKXSIZE=256', 'BLOCKYSIZE=256'])
    suffix = f'{codec}_{predictor}'
    # pitfilling
    filled_dem = os.path.join(workspace, f'filled_{suffix}.tif')
    with _time(f"Pitfilling {workspace} - {codec} {predictor}"):
        pygeoprocessing.routing.fill_pits(
            (input_dem, 1), filled_dem, working_dir=workspace,
            raster_driver_creation_tuple=creation_tuple)

    # flow direction
    flow_dir = os.path.join(workspace, f'flow_dir_d8_{suffix}.tif')
    with _time(f"Flow dir {workspace} - {codec} {predictor}"):
        pygeoprocessing.routing.flow_dir_d8(
            (filled_dem, 1), flow_dir, working_dir=workspace,
            raster_driver_creation_tuple=creation_tuple
        )

    # Flow accumulation
    flow_accum = os.path.join(workspace, f'flow_accum_d8_{suffix}.tif')
    with _time(f"Flow Accumulation {workspace} - {codec} {predictor}"):
        pygeoprocessing.routing.flow_accumulation_d8(
            (flow_dir, 1), flow_accum, raster_driver_creation_tuple=creation_tuple
        )

# predictor 3, which can be used with LZW and ZSTD codecs, can only be used on float rasters.
for CODEC, PREDICTORS in [['ZSTD', [1, 3]], ['LZW', [1, 3]], ['NONE', [1]]]:
    for PREDICTOR in PREDICTORS:
        WORKSPACE = f'workspace-dem-codec-test-{CODEC}-{PREDICTOR}'
        start_time = time.time()
        with _time(f"Processing {CODEC} {PREDICTOR} - {WORKSPACE}"):
            _process(DEM, WORKSPACE, CODEC, PREDICTOR)
