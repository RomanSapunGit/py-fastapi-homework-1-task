from math import ceil

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func

from src.database import get_db, MovieModel
from src.schemas.movies import MovieListResponseSchema, MovieDetailResponseSchema

router = APIRouter()


# Write your code here
@router.get("/movies/", response_model=MovieListResponseSchema)
async def get_movies_list(page: int = Query(1, ge=1), per_page: int = Query(10, ge=1),
                          db: AsyncSession = Depends(get_db)):
    total_items = await db.execute(select(func.count()).select_from(MovieModel))
    total_items_count = total_items.scalar()
    total_pages = ceil(total_items_count / per_page)

    if page > total_pages:
        HTTPException(status_code=404, detail="No movies found.")

    prev_page = f"/movies?page={page - 1}&per_page={per_page}" if page > 1 else None
    next_page = f"/movies?page={page + 1}&per_page={per_page}" if page < total_pages else None

    start_item_number = (page - 1) * per_page
    result_query = await db.execute(select(MovieModel).slice(start_item_number, start_item_number + per_page))
    result = result_query.scalars().all()

    if not result:
        raise HTTPException(status_code=404, detail="No movies found.")

    movies = [MovieDetailResponseSchema.model_validate(movie) for movie in result]
    return MovieListResponseSchema(
        movies=movies,
        prev_page=prev_page,
        next_page=next_page,
        total_items=total_items_count,
        total_pages=total_pages
    )


@router.get("/movies/{movie_id}/", response_model=MovieDetailResponseSchema)
async def get_movie(movie_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(MovieModel).where(MovieModel.id == movie_id))
    film = result.scalar_one_or_none()
    if not film:
        raise HTTPException(status_code=404, detail="Movie with the given ID was not found.")
    return film
