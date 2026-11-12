
from pathlib import Path
from PIL import Image

# Locate the original scanned invoice image.
project_root = Path(__file__).resolve().parents[1]

input_path = (
    project_root
    / "experiments"
    / "pdf_images"
    / "invoice_scan-1.png"
)

output_path = (
    project_root
    / "experiments"
    / "pdf_images"
    / "invoice_scan_small.png"
)

# Open the original image.
image = Image.open(input_path)

print("Original dimensions:", image.size)

# Resize while preserving the aspect ratio.
image.thumbnail((1000, 1000))

# Save the resized image.
image.save(output_path, format="PNG", optimize=True)

print("Resized dimensions:", image.size)
print("Saved to:", output_path)
