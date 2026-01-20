import os
import geopandas as gpd
import rasterio
import pandas as pd


def extract_raster_values_to_points(
    vector_file: str,
    raster_folder: str,
    output_csv: str
) -> None:
    """
    Extract raster pixel values at point locations
    """

    vector_gdf = gpd.read_file(vector_file)
    results = []

    for raster_name in os.listdir(raster_folder):
        if not raster_name.lower().endswith(".tif"):
            continue

        raster_path = os.path.join(raster_folder, raster_name)

        with rasterio.open(raster_path) as src:

            if vector_gdf.crs != src.crs:
                vector_gdf = vector_gdf.to_crs(src.crs)

            for _, row in vector_gdf.iterrows():
                geom = row.geometry
                x, y = geom.x, geom.y

                try:
                    value = list(src.sample([(x, y)]))[0][0]
                except Exception:
                    value = None

                results.append({
                    "point_id": row.get("ID"),
                    "x": x,
                    "y": y,
                    "raster": raster_name,
                    "value": value
                })

    df = pd.DataFrame(results)
    df.to_csv(output_csv, index=False)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Extract raster values at point locations"
    )
    parser.add_argument("--vector", required=True)
    parser.add_argument("--raster-folder", required=True)
    parser.add_argument("--output", required=True)

    args = parser.parse_args()

    extract_raster_values_to_points(
        args.vector,
        args.raster_folder,
        args.output
    )
