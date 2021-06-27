"""
WARNING: the original images will be overwritten!
"""

from pathlib import Path
from PIL import Image

inputPath = Path("./close")
inputFiles = inputPath.glob("**/*.png")
outputPath = Path("./jpeg")
for f in inputFiles:
    outputFile = outputPath / Path(f.stem + ".jpg")
    im = Image.open(f)
    im.save(outputFile)

