from qgis.core import (
    QgsProject,
    QgsRasterLayer,
    QgsRasterShader,
    QgsColorRampShader,
    QgsSingleBandPseudoColorRenderer,
    QgsMapSettings,
    QgsMapRendererParallelJob
)
from PyQt5.QtGui import QColor, QImage, QPainter
from PyQt5.QtCore import QSize
import os

# === CONFIGURATION ===
raster_path = '/Users/anto/Desktop/WORX/DATASCIENCE/RIVERREM PROJECTS/kernel-f6991c4a-daf7-49b9-a778-27a1b109941c_hillshade-color.tif'
output_dir = '/Users/anto/Desktop/WORX/DATASCIENCE/RIVERREM PROJECTS/'
layer_name_base = 'REM_Custom'
min_val = -100  # Keep this fixed or modify dynamically

# === EXPORT FUNCTION ===
raster_layer = rlayer

# Get vector layer by name (replace with your actual layer name)
vector_layer = QgsProject.instance().mapLayersByName('MapTiler Planet')[0]

# Output path for image
output_path = "/Users/anto/Desktop/WORX/DATASCIENCE/output_with_vector.png"

# Export image with both layers
export_image(raster_layer, vector_layer, output_path)

def export_image(raster_layer, vector_layer, out_path):
    provider = raster_layer.dataProvider()
    raster_width = provider.xSize()
    raster_height = provider.ySize()
    output_size = QSize(raster_width, raster_height)

    settings = QgsMapSettings()
    # Order: raster first (bottom), vector second (top overlay)
    settings.setLayers([raster_layer, vector_layer])
    settings.setExtent(raster_layer.extent())
    settings.setOutputSize(output_size)
    settings.setOutputDpi(300)

    image = QImage(output_size, QImage.Format_ARGB32_Premultiplied)
    image.fill(0)

    painter = QPainter(image)
    job = QgsMapRendererParallelJob(settings)
    job.start()
    job.waitForFinished()
    painter.drawImage(0, 0, job.renderedImage())
    painter.end()

    image.save(out_path, 'PNG')
    print(f"Image saved with raster + vector: {out_path}")


# === LOOP THROUGH max_val VALUES ===
for max_val in range(100, 501, 25):
    print(f"▶ Processing with max_val = {max_val}")

    # Load raster
    rlayer = QgsRasterLayer(raster_path, f"{layer_name_base}_{max_val}")
    if not rlayer.isValid():
        raise Exception("Raster failed to load!")

    # Apply color ramp
    shader = QgsRasterShader()
    color_ramp = QgsColorRampShader()
    color_ramp.setColorRampType(QgsColorRampShader.Interpolated)
    color_ramp.setColorRampItemList([
        QgsColorRampShader.ColorRampItem(min_val, QColor('#deebf7'), f"{min_val}"),
        QgsColorRampShader.ColorRampItem((min_val + max_val) / 2, QColor('#9ecae1'), "mid"),
        QgsColorRampShader.ColorRampItem(max_val, QColor('#3182bd'), f"{max_val}"),
    ])
    shader.setRasterShaderFunction(color_ramp)
    renderer = QgsSingleBandPseudoColorRenderer(rlayer.dataProvider(), 1, shader)
    rlayer.setRenderer(renderer)
    rlayer.triggerRepaint()

    # Add to project (optional: clear previous layers if needed)
    QgsProject.instance().addMapLayer(rlayer)

    # Export image
    output_path = os.path.join(output_dir, f"{layer_name_base}_blue_ramp_max{max_val}.png")
    export_image(rlayer, output_path)
