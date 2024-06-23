from vectordb import Memory

# Erstelle ein Memory-Objekt mit spezifischen Einstellungen
memory = Memory(memory_file="./memory.txt",
                chunking_strategy={'mode': 'sliding_window', 'window_size': 80, 'overlap': 20},
                embeddings="normal")

# Dokumente laden und speichern
path = "training-data/beispiel.txt"
with open(path, "r", encoding="utf-8") as file:
    text = file.read()
    memory.save(texts=text, memory_file="./memory.txt")

# Vektordatenbank speichern
memory.dump()
