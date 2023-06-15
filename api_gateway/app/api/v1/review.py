import asyncio
import json
from typing import Annotated, List
from uuid import uuid4
from google.protobuf import json_format
import grpc
import httpx
from app.schemas.review import (
    CreateReview,
    UpdateReviewDto
)
from app.utils.json_encoder import UUIDEncoder
from fastapi import APIRouter, Cookie, Form, UploadFile, status
from fastapi.responses import HTMLResponse, ORJSONResponse, Response
from google.protobuf.json_format import MessageToDict, Parse
from jwt import ExpiredSignatureError, InvalidTokenError
from loguru import logger

from proto import (
    review_pb2,
    review_pb2_grpc,
    reservation_crud_pb2,
    reservation_crud_pb2_grpc,
)

from ...config import get_yaml_config
from ...constants import review_server, reservation_server
from ...utils.get_server import get_server
from ...utils.jwt import get_id_from_token, get_role_from_token

router = APIRouter()


@router.get(
    "/all",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Get all reviews",
)
async def getAll():
    logger.info("Gateway processing getAll reviews")
    async with grpc.aio.insecure_channel(review_server) as channel:
        stub = review_pb2_grpc.ReviewServiceStub(channel)
        logger.info("Gateway processing getAll review data")
        data = await stub.GetAllReviews(review_pb2.Empty())
        json = json_format.MessageToJson(data, preserving_proto_field_name=True)
    return Response(
        status_code=200, media_type="application/json", content=json
    )


@router.get(
    "/id/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Get one review by id",
)
async def getById(item_id):
    logger.info("Gateway processing getById review request")
    async with grpc.aio.insecure_channel(review_server) as channel:
        stub = review_pb2_grpc.ReviewServiceStub(channel)
        data = await stub.GetReviewById(review_pb2.ReviewId(id=item_id))
        if data.id == "":
            return Response(
                status_code=200, media_type="application/json", content="Invalid id"
            )
        json = json_format.MessageToJson(data, preserving_proto_field_name=True)
    return Response(
        status_code=200, media_type="application/json", content=json
    )


@router.get(
    "/host/{host_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Get all reviews by host id",
)
async def getByHost(host_id):
    logger.info("Gateway processing getPendingByHostId Reservation request")

    async with grpc.aio.insecure_channel(review_server) as channel:
        stub = review_pb2_grpc.ReviewServiceStub(channel)
        data = await stub.GetReviewsByHost(review_pb2.HostId(id=host_id))
        json = json_format.MessageToJson(data, preserving_proto_field_name=True)
    return Response(
        status_code=200, media_type="application/json", content=json
    )


@router.post("/", response_class=HTMLResponse)
async def create_review(
        # Add additional data that needs to be here
        access_token: Annotated[str | None, Cookie()],
        host_id: Annotated[str, Form()],
        accommodation_id: Annotated[str, Form()],
        host_rating: Annotated[int, Form()],
        accommodation_rating: Annotated[int, Form()],
):
    """Post method used to save acoommodation

    It saves images with their unique ID and then sends gRPC request to
    accommodation service to save data about accommodation
    """

    try:
        user_id = get_id_from_token(access_token)
        user_role = get_role_from_token(access_token)
    except ExpiredSignatureError:
        return Response(
            status_code=401, media_type="text/html", content="Token expired."
        )
    except InvalidTokenError:
        return Response(
            status_code=401, media_type="text/html", content="Invalid token."
        )
    if user_role != "guest":
        return Response(status_code=401, media_type="text/html", content="Unauthorized")
    async with grpc.aio.insecure_channel(reservation_server) as channel:
        stub = reservation_crud_pb2_grpc.ReservationCrudStub(channel)
        reservations = await stub.GetByGuest(user_id)
        if reservations == None:
            return Response(
                status_code=400, media_type="text/html", content="reservations is null"
            )
        has_reservations_at_accommodation = True
        for reservation in reservations.items:
            if str(reservation.guest.id) == str(user_id):
                has_reservations_at_accommodation = True
                logger.info('found reservation ')

    if has_reservations_at_accommodation:

        async with grpc.aio.insecure_channel(review_server) as channel:
            stub = review_pb2_grpc.ReviewServiceStub(channel)
            review = review_pb2.Review(
                id=str(uuid4()),
                host_id=host_id,
                accommodation_id=accommodation_id,
                host_rating=host_rating,
                accommodation_rating=accommodation_rating,
                poster=user_id
            )

            response = await stub.CreateReview(review)

        return Response(
            status_code=response.code,
            media_type="text/html",
            content="success",
        )
    else:
        return Response(
            status_code=400, media_type="text/html", content="guest hsa no reservation at accommodation"
        )


@router.put(
    "/update",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Update reservation",
)
async def update(item: UpdateReviewDto):
    logger.info("Gateway processing update reservation request")
    async with grpc.aio.insecure_channel(review_server) as channel:
        stub = review_pb2_grpc.ReviewServiceStub(channel)

        review = reservation_crud_pb2.UpdateReviewDto()
        review.id = str(item.id)
        review.accommodation_rating = item.accommodation_rating
        review.host_rating = item.host_rating
        response = await stub.UpdateReview(reservation)
    return Response(
        status_code=200, media_type="application/json", content=response
    )


@router.delete(
    "/delete/{item_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    description="Update reservation",
)
async def delete(item_id, access_token: Annotated[str | None, Cookie()] = None):
    logger.info("Gateway processing delete Reservation request")
    try:
        user_role = get_role_from_token(access_token)
    except ExpiredSignatureError:
        return Response(
            status_code=401, media_type="text/html", content="Token expired."
        )
    except InvalidTokenError:
        return Response(
            status_code=401, media_type="text/html", content="Invalid token."
        )
    if user_role != "guest":
        return Response(status_code=401, media_type="text/html", content="Unauthorized")

    async with grpc.aio.insecure_channel(review_server) as channel:
        stub = review_pb2_grpc.ReviewServiceStub(channel)
        data = await stub.Delete(reservation_crud_pb2.ReservationId(id=item_id))
    return Response(
        status_code=200, media_type="application/json", content=data
    )
