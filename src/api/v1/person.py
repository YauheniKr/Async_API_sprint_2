from http import HTTPStatus

from fastapi import APIRouter, Depends, HTTPException
from pydantic import UUID4

from services.film import FilmService
from src.api.v1.base_params import CommonPaginationParams
from src.models.film import BaseFilm
from src.models.person import Person
from src.services.person import PersonService

router = APIRouter()


@router.get("/search", response_model=list[Person])
async def search_persons(
    query: str,
    pagination: CommonPaginationParams = Depends(),
    service: PersonService = Depends(),
    movies_service: FilmService = Depends(),
):
    person = await service.search_person(
        query=query,
        page_number=pagination.page_number,
        page_size=pagination.page_size,
        movies_service=movies_service,
    )
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="persons not found for this query")
    return person


@router.get("/{id:uuid}", response_model=Person)
async def get_persons_by_id(
    id: UUID4,
    service: PersonService = Depends(),
    movies_service: FilmService = Depends(),
):
    person = await service.get_person_by_id(id, movies_service)
    if not person:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="person not found")
    return person


@router.get("/{id:uuid}/film", response_model=list[BaseFilm])
async def get_person_films(
    id: UUID4,
    film_service: FilmService = Depends(),
):
    person_films = await film_service.get_person_films_by_person_id(id)
    if not person_films:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="person not found")
    return person_films
