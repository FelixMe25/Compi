WorldName OperacionesEnteras:

Inventory
    Stack a = 10;
    Stack b = 4;
    Stack suma, resta, multiplicacion, division, modulo;

SpawnPoint
    suma = a + b;
    resta = a - b;
    multiplicacion = a * b;
    division = a / b;
    modulo = a % b;

    dropperStack(suma);
    dropperStack(resta);
    dropperStack(multiplicacion);
    dropperStack(division);
    dropperStack(modulo);
worldSave
