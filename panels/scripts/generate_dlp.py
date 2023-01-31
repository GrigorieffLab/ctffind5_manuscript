import mrcfile
from PIL import Image
from pathlib import Path
# Open the mrc file
from pycistem import database

info = database.get_image_info_from_db("/nrs/elferich/DLP/DLP.db",14)

mrc = mrcfile.open(info["FILENAME"])

# Rescale mrc.data to 1200x1200 using fourier space cropping

from scipy.fft import fft2, ifft2, fftshift, ifftshift

# Crop the center 3700x3700
im_data = mrc.data[0][:3700, :3700].copy()
print(im_data.shape)
# Do forward fourier transform
im_data = fft2(im_data)
# Shift the center to the top left
im_data = fftshift(im_data)
# Pad with zeros
#mrc.data = np.pad(mrc.data, ((1850, 1850), (1850, 1850)), mode='constant')
# Crop the center 1200x1200
im_data = im_data[1250:-1250, 1250:-1250]


# Shift back to the center
im_data = ifftshift(im_data)
# Do inverse fourier transform
im_data = ifft2(im_data)

# Rescale the image to 0-255 use 2x std as cutoff

im = im_data.real.copy()
mean = im.mean()
std = im.std()
im[im > mean + 2 * std] = mean + 2 * std
im[im < mean - 2 * std] = mean - 2 * std
im -= im.min()
im /= im.max()
im *= 255

# Save as png using PIL
Image.fromarray(im).convert('RGB').save(Path(__file__).parent.parent / "images/dlp.png")