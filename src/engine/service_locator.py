from src.engine.services.fonts_service import FontsService
from src.engine.services.images_service import ImageService
from src.engine.services.sounds_service import SoundsService


class ServiceLocator:
    images_service = ImageService()
    sounds_service = SoundsService()
    fonts_service = FontsService()
