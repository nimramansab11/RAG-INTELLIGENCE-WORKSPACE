import argparse
import json

from app.ingest_service import IngestionService


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Create FREE local embeddings and store them in ChromaDB."
        )
    )

    parser.add_argument(
        "--data-dir",
        default="./data",
        help="Directory containing PDF/TXT/MD files.",
    )

    parser.add_argument(
        "--reset",
        action="store_true",
        help="Rebuild the ChromaDB collection.",
    )

    args = parser.parse_args()

    result = IngestionService().ingest(
        directory=args.data_dir,
        reset=args.reset,
    )

    print(
        json.dumps(
            result,
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
