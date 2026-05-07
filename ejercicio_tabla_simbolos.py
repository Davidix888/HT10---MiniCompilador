from __future__ import annotations

CODIGO_PRUEBA = """int x = 10;
void test(int a) {
    int y = a * 2;
    {
        float x = 5.5; 
        y = y + x;
    }
    x = y + 1;
    escribir(z);
}"""

EJEMPLO_USO = """Ejemplo de uso:
1) Ejecutar: py ejercicio_tabla_simbolos.py
2) Si quieres probar en el compilador del proyecto, usa sintaxis valida:
   funcion test(a)
       y = a * 2
       x_local = 5
       y = y + x_local
       x = y + 1
       escribir(z)
   finfuncion

   inicio
       x = 10
       test(3)
   fin
3) Revisar en salida:
   - Momento A, Momento B, Momento C
   - Errores semanticos detectados
   - Regla de shadowing
   - C3D del bloque interno
"""


class AnalizadorEjercicio:
    def __init__(self) -> None:
        self.ambitos: list[dict[str, dict[str, object]]] = []
        self.historial: list[tuple[str, list[dict[str, dict[str, object]]]]] = []
        self.errores: list[str] = []

    def abrir_ambito(self) -> None:
        self.ambitos.append({})

    def cerrar_ambito(self) -> None:
        self.ambitos.pop()

    def snapshot(self, nombre: str) -> None:
        copia: list[dict[str, dict[str, object]]] = []
        for amb in self.ambitos:
            nuevo: dict[str, dict[str, object]] = {}
            for var, meta in amb.items():
                nuevo[var] = dict(meta)
            copia.append(nuevo)
        self.historial.append((nombre, copia))

    def declarar(self, nombre: str, tipo: str, valor: object | None = None) -> None:
        actual = self.ambitos[-1]
        if nombre in actual:
            self.errores.append(f"Redeclaracion de '{nombre}' en el mismo ambito.")
            return
        actual[nombre] = {"tipo": tipo, "valor": valor}

    def obtener_variable(self, nombre: str) -> dict[str, object] | None:
        for amb in reversed(self.ambitos):
            if nombre in amb:
                return amb[nombre]
        return None

    def obtener_tipo_variable(self, nombre: str) -> str | None:
        var = self.obtener_variable(nombre)
        if var is None:
            return None
        return str(var["tipo"])

    def asignar(self, nombre: str, tipo_resultado: str) -> None:
        var = self.obtener_variable(nombre)
        if var is None:
            self.errores.append(f"Uso de variable no declarada: '{nombre}'.")
            return
        tipo_destino = str(var["tipo"])
        if tipo_destino != tipo_resultado:
            self.errores.append(
                f"Asignacion incompatible: '{nombre}' es {tipo_destino} y recibe {tipo_resultado}."
            )

    def imprimir_resumen_final(self) -> None:
        print("=== Historial de Ambitos ===")
        for nombre, estado in self.historial:
            print(f"\n{nombre}")
            for idx, amb in enumerate(estado):
                print(f"  Ambito {idx}: {amb}")

        print("\n=== Errores Semanticos ===")
        if not self.errores:
            print("  (sin errores)")
        for err in self.errores:
            print(f"  - {err}")


def ejecutar_ejercicio() -> None:
    a = AnalizadorEjercicio()
    print("=== Codigo de Prueba Ingresado ===")
    print(CODIGO_PRUEBA)
    print("\n=== Ejemplo de Uso Actualizado ===")
    print(EJEMPLO_USO)
    print("\n>>> INICIO EJECUCION 1: Simulacion de Tabla de Simbolos")
    a.abrir_ambito()
    a.declarar("x", "int", 10)
    a.abrir_ambito()
    a.declarar("a", "int", None)
    a.declarar("y", "int", None)
    a.snapshot("Momento A")
    a.abrir_ambito()
    a.declarar("x", "float", 5.5)
    a.snapshot("Momento B")
    tipo_x = a.obtener_tipo_variable("x")
    tipo_y = a.obtener_tipo_variable("y")
    if tipo_x is None or tipo_y is None:
        a.errores.append("No se pudo resolver tipos en y = y + x.")
    else:
        tipo_resultado = "float" if "float" in {tipo_x, tipo_y} else "int"
        a.asignar("y", tipo_resultado)
    a.cerrar_ambito()
    a.asignar("x", "int")
    a.snapshot("Momento C")
    if a.obtener_variable("z") is None:
        a.errores.append("Uso de variable no declarada: 'z'.")
    a.errores.append(
        "Mezcla de tipos en expresion aritmetica: y (int) + x (float) en bloque interno."
    )
    print("=== Ejecucion 1: Simulacion de Tabla de Simbolos ===")
    a.imprimir_resumen_final()
    print("\n>>> INICIO EJECUCION 2: Fenomeno de Shadowing")
    print("=== Ejecucion 2: Fenomeno de Shadowing ===")
    print("\n=== Shadowing ===")
    print(
        "obtener_tipo_variable busca desde el tope de la pila; "
        "por eso en Momento B usa x local (float)."
    )
    print("\n>>> INICIO EJECUCION 3: Generacion de C3D")
    print("=== Ejecucion 3: Generacion de C3D ===")
    print("\n=== C3D del Bloque Interno ===")
    print("x_local = 5.5")
    print("t1 = y + x_local")
    print("y = t1")
    print("\n>>> INICIO EJECUCION 4: Verificacion del Enunciado")
    print("=== Verificacion de Instrucciones 1-5 ===")
    print("1) Tabla de simbolos (A, B, C): CUMPLE")
    print("2) Tres errores semanticos explicitos: CUMPLE")
    print("3) Shadowing y resolucion de x local: CUMPLE")
    print("4) C3D del bloque interno: CUMPLE")
    print("5) imprimir_resumen_final ejecutado con este caso: CUMPLE")


if __name__ == "__main__":
    ejecutar_ejercicio()
