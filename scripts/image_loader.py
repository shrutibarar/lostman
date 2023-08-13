from PIL import Image


class ImageEditor:

    @classmethod
    def resize_image(cls, path: str, new_size: tuple, replace=False,
                     view_image=False):
        """
        Resize image
        :param view_image: shows image after editing
        :param replace: replace current image with resized image (default to false)
        :param path: local path of the image
        :param new_size: tuple containing (height, width) of the image
        :return: resized image path
        """
        edit_image = Image.open(path).resize(new_size)
        if view_image:
            edit_image.show()
        return cls.save_image(edit_image, replace=replace, loaded_path=path, edited=["resized"])

    @classmethod
    def save_image(cls, img: Image, edited: list, replace, loaded_path=None):
        """
        Save and returns the path of the saved image

        :param img: expects Image
        :param edited:  takes a list of editting done on the image
        :param replace: replace orignal image if set true
        :param loaded_path:
        :return:
        """
        saved_path = loaded_path

        if replace:
            img.save(saved_path)
        else:
            new_path = loaded_path.split(".")
            edits = "_" + "_".join(edited) + "."
            new_path = new_path[0] + edits + new_path[1]
            img.save(new_path)
            saved_path = new_path

        return saved_path
