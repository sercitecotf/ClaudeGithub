# Flujo de inflado en `/usr/bin/gzip`

Análisis hecho con REA (`rea-agents` 6.5.0) y Ghidra 12.1.4 sobre el `gzip` del sistema
(ELF x86-64 PIE, 93 KB, sin símbolos, SHA-256 `afea077ce127d4fa9ad410d3066ba2b54dea19c0b44f04adf56c72d5f7b7a9bb`).
Los nombres de función son interpretación por comportamiento, no símbolos del binario.
El pseudocódigo crudo está en `decompiled/`.

## Vista general

```
FUN_00109540  lee la cabecera gzip (1F 8B, método 8)
   └─ PTR_FUN_00117410 = FUN_0010c4c0   manejador del método 8
        └─ bucle de bloques (3 bits de cabecera por bloque)
             ├─ tipo 0 → bloque almacenado (copia directa)
             ├─ tipo 1 → FUN_0010a9e0   Huffman fijo
             ├─ tipo 2 → FUN_0010abe0   Huffman dinámico
             └─ tipo 3 → "invalid compressed data--format violated"
         tipos 1 y 2 usan:
             FUN_00105680   construye tablas Huffman
             FUN_0010a3a0   decodifica literales y copias
             FUN_001092e0   vuelca la ventana de 32 KB
             FUN_00109360   rellena el búfer de entrada
```

## Funciones

| Dirección | Nombre interpretado | Archivo |
|---|---|---|
| `0x10c4c0` | manejador método 8 / bucle de bloques | `decompiled/FUN_0010c4c0_unzip.c` |
| `0x10a9e0` | `inflate_fixed` | `decompiled/FUN_0010a9e0_inflate_fixed.c` |
| `0x10abe0` | `inflate_dynamic` | `decompiled/FUN_0010abe0_inflate_dynamic.c` |
| `0x10a3a0` | `inflate_codes` | `decompiled/FUN_0010a3a0_inflate_codes.c` |
| `0x105680` | `huft_build` | `decompiled/FUN_00105680_huft_build.c` |

- **Bloque fijo:** longitudes fijas de RFC 1951 (288 símbolos: 144×8, 112×9, 24×7, 8×8); tablas de 7 y 5 bits.
- **Bloque dinámico:** lee HLIT/HDIST/HCLEN, el alfabeto de longitudes (3 bits c/u, orden permutado en `DAT_00112aa0`),
  y decodifica longitudes con repeticiones: 16 (2 bits extra, 3–6 copias de la anterior), 17 (3 bits, 3–10 ceros),
  18 (7 bits, 11–138 ceros). Valida desbordes del arreglo. Tablas literal (9 bits) y distancia (6 bits).
- **`huft_build`:** cuenta longitudes, detecta códigos sobresuscritos/incompletos, genera entradas de 16 bytes con
  subtablas enlazadas. Tipo `e`: 16 literal, 15 fin de bloque, 99 inválido, >16 subtabla, <16 longitud/distancia con `e` bits extra.
- **`inflate_codes`:** flujo de bits de 64 bits, ventana circular de 32 KB (`DAT_0018e000`, máscara `0x7fff`),
  copia byte a byte si hay solape, volcado con `FUN_001092e0` al llegar a `0x8000`.

## Códigos de retorno

| Valor | Significado |
|---|---|
| 0 | Bloque correcto |
| 1 | Datos corruptos o código incompleto |
| 2 | Código sobresuscrito o símbolo inválido |
| 3 | Fallo de `malloc` |

## Límites del análisis

No se leyeron `inflate_stored` (dentro de `FUN_0010c4c0`), `FUN_00109360` ni `FUN_001092e0`.
La correspondencia con el `inflate.c` clásico de gzip es una comparación por estructura, no verificada contra el código fuente.
