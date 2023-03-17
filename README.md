# Image-watermarker
Adds a watermark to an image or many images in a directory using the Python Imaging Library (PIL)

## Get started
To get started, follow these steps:

1. Clone the repository to your local machine.
``` {.sourceCode}
git clone https://github.com/Altaaaf/Image-watermarker.git
```
2. Install the required packages by running the following command:
``` {.sourceCode}
pip install -r requirements.txt
```
3. After installing the required packages, run main.py to start the application.

## Usage
``` {.sourceCode}
main.py [-h] [--input INPUT] [--watermark WATERMARK] [--watermark_position WATERMARK_POSITION] [--scale_watermark SCALE_WATERMARK] [--output OUTPUT]
```


| Argument | Description |
| --- | --- |
| `-h` or `--help` | Show help message |
| `--input <path>` or `-i <path>` | Image file path or directory path which contains images |
| `--watermark <path>` or `--w <path>` | Watermark image path to apply to inputted images |
| `--watermark_position <path>` or `-wp <path>` | Position to place watermark. Possible values: "top-left", "bottom-left", "top-right", "bottom-right", "center" (default: center) |
| `--scale_watermark <path>` or `-sw <path>` | Scale factor to resize watermark (default: 0.5) |
| `--output_directory <path>` or `-o <path>` | Output directory to save watermarked images (default: /watermarked_images) |


## Example
``` {.sourceCode}
python main.py --input example.jpg --watermark watermark.png --watermark_position "center" --scale_watermark 0.5 --output_directory "/watermarked_images"

python main.py -i example.jpg -w watermark.png -wp "center" -sw 0.5 -o "/watermarked_images"
```
