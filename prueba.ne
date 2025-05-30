WorldName Dirt:
Inventory
    Stack dirtblocks = 0;
SpawnPoint
    spawner
        dropperSpider("I need some dirt");
        soulsand dirtblocks;
    exhausted dirtblocks >= 64;
worldSave