"""
main.py — Gateway del Pipeline Dashboard MultiTodo
Modos: validate | etl | alerts

Uso:
    python main.py --mode validate
    python main.py --mode etl
    python main.py --mode alerts
"""
import argparse


VALID_MODES = ["validate", "etl", "alerts"]


def main():
    parser = argparse.ArgumentParser(description="Pipeline Dashboard MultiTodo")
    parser.add_argument(
        "--mode",
        choices=VALID_MODES,
        required=True,
        help=f"Modo de ejecución: {', '.join(VALID_MODES)}"
    )
    args = parser.parse_args()

    # Stub: implementación en Fase 2
    print(f"[Pipeline] Modo '{args.mode}' recibido. Implementación pendiente — Fase 2.")


if __name__ == "__main__":
    main()
