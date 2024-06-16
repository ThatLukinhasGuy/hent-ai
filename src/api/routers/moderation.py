from fastapi import APIRouter, Request, Response, Depends, Body
from typing import Union
from ..dependencies import auth, rate_limit
from ..models import ModerationBody
from ..utils import AIModel
from ..database import LogManager

router = APIRouter()

@router.post("/v1/moderations", dependencies=[Depends(auth), Depends(rate_limit)], response_model=None)
async def moderation(request: Request, data: ModerationBody = Body(...)) -> Union[Response, dict]:
    """Moderation endpoint request handler"""

    result = await AIModel.get_provider(data.model)(data.model_dump())

    if isinstance(result, tuple) and len(result) == 2:
        await LogManager.log_api_request(result[1], data.model, request)
        return result[0]

    return result