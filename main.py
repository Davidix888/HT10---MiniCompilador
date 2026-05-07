from __future__ import annotations

import json
from pathlib import Path

from generador import MIPSGenerator
from lexico import lex, tokens_by_line
from sintactico_ast import Parser


ROOT = Path(__file__).resolve().parent
BASE_PROGRAM = ROOT / "programa_ejercicio.pseudo"


def read_source(path: Path) -> str:
    return path.read_text(encoding="utf-8").strip() + "\n"


def print_title(title: str) -> None:
    print(f"\n{'=' * 18} {title} {'=' * 18}")


def analyze_program(source: str) -> dict:
    tokens = lex(source)
    parser = Parser(tokens)
    ast = parser.parse()

    mips_generator = MIPSGenerator()
    mips = mips_generator.generate(ast)

    return {
        "tokens": tokens,
        "ast": ast,
        "mips": mips,
    }


def detect_syntax_hints(source: str) -> list[str]:
    hints: list[str] = []
    for idx, raw in enumerate(source.splitlines(), start=1):
        line = raw.strip()
        if not line:
            continue
        if ";" in line:
            hints.append(f"Linea {idx}: ';' no es valido en este lenguaje.")
        if "{" in line or "}" in line:
            hints.append(f"Linea {idx}: '{{' y '}}' no son validos; usa bloques por indentacion con inicio/fin o funcion/finfuncion.")
        if line.startswith("void "):
            hints.append(f"Linea {idx}: 'void' no es valido; usa 'funcion nombre(parametros)'.")
        if line.startswith(("int ", "float ", "double ", "char ", "bool ")):
            hints.append(f"Linea {idx}: no se declaran tipos explicitos; usa asignaciones directas (ej. x = 10).")
    return hints


def show_base_program_report(source: str) -> None:
    try:
        result = analyze_program(source)
    except SyntaxError as error:
        print("=== Error de Sintaxis ===")
        print(str(error))
        hints = detect_syntax_hints(source)
        if hints:
            print("\n=== Detalle de Errores Detectados ===")
            for hint in hints:
                print(f"- {hint}")
        print(
            "\nSugerencia general: este compilador usa sintaxis Pseudo-C++ "
            "(inicio/fin, funcion/finfuncion, sin ';' ni llaves)."
        )
        return

    #print_title("Programa Fuente")
    print(source.rstrip())

    #print_title("1. Analisis Lexico")
    for line, items in tokens_by_line(result["tokens"]).items():
        print(f"Linea {line}: {items}")

    #print_title("2. AST en JSON")
    print(json.dumps(result["ast"].to_dict(), indent=4, ensure_ascii=False))
    #print("\nPuedes pegar este JSON directamente en jsoncrack.com para visualizar el arbol.")

   # print_title("5. Ensamblador MIPS Simplificado")
    print(result["mips"])


def main() -> None:
    base_source = read_source(BASE_PROGRAM)
    show_base_program_report(base_source)


if __name__ == "__main__":
    main()
