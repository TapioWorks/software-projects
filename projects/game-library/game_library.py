from sqlalchemy import select

from database import SessionLocal
from game import Game


class GameLibrary:
    def add_game(self, game: Game) -> None:
        with SessionLocal() as session:
            session.add(game)
            session.commit()

    def get_all_games(self) -> list[Game]:
        with SessionLocal() as session:
            statement = select(Game).order_by(Game.id)
            games = session.scalars(statement).all()

            return list(games)

    def search_games(self, search_term: str) -> list[Game]:
        search_term = search_term.strip()

        if not search_term:
            return []

        statement = select(Game).where(
            Game.name.ilike(f"%{search_term}%")
        )

        with SessionLocal() as session:
            games = session.scalars(statement).all()

            return list(games)