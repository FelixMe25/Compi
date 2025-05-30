WorldName OperacionesEnterasSpider:

Inventory
    Stack largoSaludo, indexBusqueda;

    Spider saludo = "Hola", nombre = "Steve",completo;
    Spider texto= "Hola Steve",palabra = "Steve",extraido,recortado;
    Rune letra;

SpawnPoint
    $$ Concatenación válida
    completo = saludo bind nombre;

    $$ Longitud de Spider
    largoSaludo = # saludo;

    $$ Acceso por índice
    letra = saludo[1];

    $$ Búsqueda con seek
    indexBusqueda = texto seek palabra;

    $$ Corte con from
    extraido = texto from 5 ## 5;

    $$ Recorte con except
    recortado = texto except 5 ## 5;

    $$ ERROR: tipo destino incorrecto para seek
    letra = texto seek palabra;

    $$ ERROR: tipo incorrecto en bind
    completo = saludo bind a;
worldSave

