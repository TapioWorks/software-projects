from datetime import datetime

from database import create_tables
from game import Game
from game_library import GameLibrary


def add_game(library: GameLibrary) -> None:
    while True:
        name = input("Game name: ").strip()

        if name:
            break

        print("Game name cannot be empty.")

    while True:
        release_date = input("Release date (YYYY-MM-DD): ").strip()

        try:
            datetime.strptime(release_date, "%Y-%m-%d")
            break
        except ValueError:
            print("Please enter a valid date in YYYY-MM-DD format.")

    while True:
        try:
            rating = int(input("Give rating (1-10): "))

            if 1 <= rating <= 10:
                break

            print("Rating must be between 1 and 10.")
        except ValueError:
            print("Please enter a valid whole number.")

    game = Game(
        name=name,
        release_date=release_date,
        rating=rating,
    )
    library.add_game(game)

    print(f"\nAdded: {game}")


def view_games(library: GameLibrary) -> None:
    games = library.get_all_games()

    if not games:
        print("\nYour library is empty.")
        return

    print("\n========== YOUR GAME LIBRARY ==========")

    for index, game in enumerate(games, start=1):
        print(f"{index}. {game}")


def search_games(library: GameLibrary) -> None:
    search_term = input("Enter a game name to search for: ").strip()

    if not search_term:
        print("Search term cannot be empty.")
        return

    games = library.search_games(search_term)

    if not games:
        print(f"\nNo games found matching '{search_term}'.")
        return

    print(f"\n========== SEARCH RESULTS ({len(games)}) ==========")

    for index, game in enumerate(games, start=1):
        print(f"{index}. {game}")


def main() -> None:
    create_tables()
    library = GameLibrary()

    while True:
        print("\n========== GAME LIBRARY ==========")
        print("1. Add game")
        print("2. View games")
        print("3. Search games")
        print("4. Exit")

        choice = input("Choose an option: ").strip()

        if choice == "1":
            add_game(library)
        elif choice == "2":
            view_games(library)
        elif choice == "3":
            search_games(library)
        elif choice == "4":
            print("Thanks for using Game Library. Goodbye!")
            break
        else:
            print("Invalid option. Please choose 1, 2, 3, or 4.")


if __name__ == "__main__":
    main()