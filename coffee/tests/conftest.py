import uuid
from typing import Optional

import aiofiles
import pytest


@pytest.fixture(scope='function')
async def save_images(list_of_images: Optional[list]):
    files = []
    if list_of_images:
        for image in list_of_images:
            async with aiofiles.open(image, mode='rb') as f:
                img = ('images', (str(uuid.uuid4()), await f.read()))
                files.append(img)
    return files
