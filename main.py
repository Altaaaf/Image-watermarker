from PIL import Image, ImageOps
import argparse
import os

IMAGE_FILE_EXTENSIONS = (
    ".jpg",
    ".jpeg",
    ".png",
    ".gif",
    ".bmp",
)


def offset(original_image, watermark, position):
    """
    Calculates the offset position for the watermark on the original image.

    Args:
    - original_image (PIL.Image): The original image to add the watermark to.
    - watermark (PIL.Image): The watermark image.
    - position (str): The desired position of the watermark on the original image.
                      Possible values: "top-left", "bottom-left", "top-right", "bottom-right", "center".

    Returns:
    - A tuple containing the x and y offset positions for the watermark on the original image.

    Raises:
    - ValueError: If an invalid position is provided.

    """
    try:
        if position == "top-left":
            return (0, 0)
        elif position == "bottom-left":
            return (0, original_image.size[1] - watermark.size[1])
        elif position == "top-right":
            return (original_image.size[0] - watermark.size[0], 0)
        elif position == "bottom-right":
            return (original_image.size[0] - watermark.size[0], original_image.size[1] - watermark.size[1])
        elif position == "center":
            return ((original_image.size[0] - watermark.size[0]) // 2, (original_image.size[1] - watermark.size[1]) // 2)
        else:
            raise ValueError(
                "Invalid position provided. Possible values: 'top-left', 'bottom-left', 'top-right', 'bottom-right', 'center'")
    except Exception as e:
        print(f"Error: {e}")


def resize(original_image_size: tuple, scale_factor: float) -> tuple:
    """
    Resizes an image by a given value.

    Args:
    - original_image_size (tuple): A tuple containing the original image's width and height.
    - scale_factor (float): The value to resize the image by.

    Returns:
    - A tuple containing the resized image's width and height.

    Raises:
    - TypeError: If original_image_size is not a tuple, or if scale_factor is not a float.
    - ValueError: If scale_factor is less than or equal to 0.

    """
    try:
        if not isinstance(original_image_size, tuple):
            raise TypeError("original_image_size must be a tuple.")
        if not isinstance(scale_factor, float):
            raise TypeError("scale_factor must be a float.")
        if scale_factor <= 0:
            raise ValueError("scale_factor must be greater than 0.")

        width, height = original_image_size
        resized_width = int(width * scale_factor)
        resized_height = int(height * scale_factor)
        resized_values = (resized_width, resized_height)
        return resized_values

    except TypeError as te:
        print(f"TypeError: {te}")
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except Exception as e:
        print(f"Error: {e}")


def build_output_path(file_name: str, output_path: str) -> str:
    """
    Builds the output path for the watermarked image.

    Args:
    - file_name (str): The name of the original image file.
    - output_path (str): The path to save the watermarked image file.

    Returns:
    - A string representing the output path for the watermarked image.

    Raises:
    - TypeError: If either file_name or output_path is not a string.
    - ValueError: If file_name or output_path is an empty string.

    """
    try:
        if not isinstance(file_name, str):
            raise TypeError("file_name must be a string.")
        if not isinstance(output_path, str):
            raise TypeError("output_path must be a string.")
        if file_name == "" or output_path == "":
            raise ValueError(
                "file_name and output_path cannot be empty strings.")

        output_file_name = "watermarked_" + file_name
        output_file_path = os.path.join(output_path, output_file_name)
        return output_file_path

    except TypeError as te:
        print(f"TypeError: {te}")
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except Exception as e:
        print(f"Error: {e}")


def add_watermark(image_path: str, watermark_path: str, output_path: str, position: str, scale_factor: float, file_name: str) -> None:
    """
    Adds a watermark to an image.

    Args:
    - image_path (str): The path to the original image file.
    - watermark_path (str): The path to the watermark image file.
    - output_path (str): The path to save the watermarked image file.
    - position (str): The position of the watermark on the image. Valid options are: "top-left", "bottom-left", "top-right", "bottom-right", and "center".
    - scale_factor (float): The value to resize the watermark by.
    - file_name (str): The name of the output watermarked image file.

    Returns:
    - None

    Raises:
    - TypeError: If any of the input arguments are not the expected type.
    - ValueError: If the position argument is not one of the valid options.

    """
    try:
        # check input types
        if not isinstance(image_path, str):
            raise TypeError("image_path must be a string.")
        if not isinstance(watermark_path, str):
            raise TypeError("watermark_path must be a string.")
        if not isinstance(output_path, str):
            raise TypeError("output_path must be a string.")
        if not isinstance(position, str):
            raise TypeError("position must be a string.")
        if not isinstance(scale_factor, float):
            raise TypeError("scale_factor must be a float.")
        if not isinstance(file_name, str):
            raise TypeError("file_name must be a string.")

        # check if position is valid
        valid_positions = ["top-left", "bottom-left",
                           "top-right", "bottom-right", "center"]
        if position not in valid_positions:
            raise ValueError(f"position must be one of {valid_positions}.")

        # open images and resize watermark
        with Image.open(image_path) as image, Image.open(watermark_path) as watermark:
            watermark = watermark.resize(resize(image.size, scale_factor))

            # create watermark mask and paste onto image
            watermark_mask = ImageOps.invert(ImageOps.grayscale(watermark))
            image.paste(watermark, offset(
                image, watermark, position), watermark_mask)

            # save watermarked image
            output_file_path = build_output_path(file_name, output_path)
            image.save(output_file_path)
            print(
                f"Saved watermark ({watermark_path}) to image ({file_name}) at ({position}) position")

    except TypeError as te:
        print(f"TypeError: {te}")
    except ValueError as ve:
        print(f"ValueError: {ve}")
    except Exception as e:
        print(f"Error: {e}")


def add_watermarks_to_directory(directory: str, watermark_path: str, output_path: str, position: str, scale_factor: float):
    """
    Adds a watermark image to all image files in the specified directory that match a certain set of extensions.

    Args:
        directory (str): The path of the directory containing the image files to which the watermark should be added.
        watermark_path (str): The path of the watermark image file.
        output_path (str): The path where the watermarked images should be saved.
        position (str): The position of the watermark on the image, one of "top-left", "bottom-left", "top-right", "bottom-right", and "center".
        scale_factor (float): A scaling factor for the watermark image, which determines its size relative to the size of the image files.

    Raises:
        TypeError: If the `directory` argument is not a string.

    Returns:
        None
    """
    try:
        # check input types
        if not isinstance(directory, str):
            raise TypeError("directory must be a string.")

        for filename in os.listdir(directory):
            filepath = os.path.join(directory, filename)
            if filepath.lower().endswith(IMAGE_FILE_EXTENSIONS):
                add_watermark(
                    image_path=filepath,
                    watermark_path=watermark_path,
                    output_path=output_path,
                    position=position,
                    scale_factor=scale_factor,
                    file_name=os.path.basename(filepath))
    except TypeError as te:
        print(f"TypeError: {te}")
    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add watermark to images')
    parser.add_argument('--input',
                        '-i',
                        help='Image file path or directory path which contains images')
    parser.add_argument('--watermark',
                        '-w',
                        help='Watermark image path to apply to inputted images'
                        )
    parser.add_argument('--watermark_position',
                        '-wp',
                        help='Position to place watermark. Possible values: "top-left", "bottom-left", "top-right", "bottom-right", "center" (default: %(default)s)',
                        default='center')
    parser.add_argument('--scale_watermark',
                        '-sw',
                        help='Scale factor to resize watermark (default: %(default)s)',
                        default=0.5)
    parser.add_argument('--output_directory',
                        '-o',
                        help='Output directory to save watermarked images (default: %(default)s)',
                        default=os.getcwd() + "/watermarked_images")
    args = parser.parse_args()

    if not args.input:
        args.input = input(
            "Enter path to image file or directory of images that you want to watermark: ")
    if not args.watermark:
        args.watermark = input("Enter path to watermark file: ")

    os.makedirs(args.output_directory, exist_ok=True)

    if os.path.isfile(args.input):
        add_watermark(
            image_path=args.input,
            watermark_path=args.watermark,
            output_path=args.output_directory,
            position=args.watermark_position,
            scale_factor=args.scale_watermark,
            file_name=os.path.basename(args.input))
    elif os.path.isdir(args.input):
        add_watermarks_to_directory(
            directory=args.input,
            watermark_path=args.watermark,
            output_path=args.output_directory,
            position=args.watermark_position,
            scale_factor=args.scale_watermark)
    else:
        print(f'Error: {args.input} does not exist')
        exit()
