WorldName TriangleArea:
$*

Este es un comentario de bloque

Claro que sí
*$

Bedrock 
    Obsidian Stack maxDiamonds 5; 
    Obsidian Torch hasEnchantedGoldenApple On; 
    Obsidian Chest lootContents {: 's', 'a' :};

$$ Sección de Variables
Inventory 
    Shelf Ghast loteria = [10.35, 11.64, 43.75];
    Stack numero;
    Stack base = 5, altura = 10, area;
    Spider nombre;
    Spider apellido = "Pérez";
    
SpawnPoint
    soulsand numero;
    area = (base * altura) / 2;
    dropperStack(area);
worldSave