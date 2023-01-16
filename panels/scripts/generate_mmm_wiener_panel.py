import mrcfile
from PIL import Image
from pathlib import Path
# Open the mrc file
mrc = mrcfile.open(Path(__file__).parent.parent.parent / "data/mmm/mmm_wiener.mrc")

print(mrc.data.shape)
im = mrc.data[0,300:600,700:1100].copy()
im /= im.mean()
im /= 1.5
im *= 128
# Save as png using PIL
Image.fromarray(im).convert('RGB').save(Path(__file__).parent.parent / "images/mmm_wiener.png")