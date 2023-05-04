from src.engine.services.font_service import FontService
from src.engine.services.images_service import ImageService
from src.engine.services.sounds_service import SoundsService


class ServiceLocator:
    images_service = ImageService()
    sounds_service = SoundsService()
    font_service = FontService()
