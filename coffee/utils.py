from typing import Optional
from fastapi import UploadFile
from image_service.interfaces import ImageServiceInterface


class Utils:
    @staticmethod
    async def save_images(images: Optional[list[UploadFile]],
                          img_service: ImageServiceInterface):
        if images:
            return [
                str(await img_service.write_image(image, image.filename))
                for image in images
            ]
