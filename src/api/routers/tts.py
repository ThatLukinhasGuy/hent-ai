from fastapi import APIRouter, Request, Response, Depends, Body
from ..dependencies import auth, rate_limit
from ..models import TTSBody
from ..utils import AIModel, InvalidRequestException
from ..database import UserManager, LogManager

router = APIRouter()

@router.post("/v1/audio/speech", dependencies=[Depends(auth), Depends(rate_limit)])
async def tts(request: Request, data: TTSBody = Body(...)) -> Response:
    """TTS endpoint request handler"""

    key = request.headers.get("Authorization").replace("Bearer ", "", 1)
    premium_check = await UserManager.get_property(key, "premium")
    is_premium_model = data.model in AIModel.get_all_models("audio.speech", premium=True)

    if not premium_check and is_premium_model:
        raise InvalidRequestException("This model is not available in the free tier.", status=402)

    result = await AIModel.get_provider(data.model)(data.model_dump())

    if isinstance(result, tuple) and len(result) == 2:
        await LogManager.log_api_request(result[1], data.model, request)
        return result[0]

    return result