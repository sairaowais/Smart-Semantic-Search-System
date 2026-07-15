import chromadb
from docx import Document

# -----------------------------
# Create ChromaDB database
# -----------------------------
client = chromadb.PersistentClient(path="school_db")

collection = client.get_or_create_collection(
    name="school_documents"
)

# -----------------------------
# Function to read DOCX
# -----------------------------
def read_docx(file_path):
    doc = Document(file_path)

    text = ""

    for para in doc.paragraphs:
        if para.text.strip():
            text += para.text + "\n"

    return text

# -----------------------------
# Read documents
# -----------------------------
text1 = read_docx("documents/AI_ML_Guide.docx")
text2 = read_docx("documents/subjects_guide.docx")

# -----------------------------
# Create chunks
# -----------------------------
documents = []
ids = []

# Chunks from AI_ML_Guide
for i, paragraph in enumerate(text1.split("\n")):

    paragraph = paragraph.strip()

    if paragraph:
        documents.append(paragraph)
        ids.append(f"AI_chunk_{i}")

# Chunks from subjects_guide
for i, paragraph in enumerate(text2.split("\n")):

    paragraph = paragraph.strip()

    if paragraph:
        documents.append(paragraph)
        ids.append(f"Subjects_chunk_{i}")

# -----------------------------
# Store chunks in ChromaDB
# -----------------------------
collection.upsert(
    documents=documents,
    ids=ids
)


print(f"{len(documents)} chunks stored successfully!")

# -----------------------------
# User Query
# -----------------------------
query = input("\nEnter your question: ")

results = collection.query(
    query_texts=[query],
    n_results=3
)

# -----------------------------
# Display Results
# -----------------------------
print("\n===== SEARCH RESULTS =====\n")

for i in range(len(results["documents"][0])):

    print(f"Result #{i+1}")

    print(f"Chunk ID: {results['ids'][0][i]}")

    if "distances" in results:
        print(f"Distance: {results['distances'][0][i]}")

    print("\nContent:")
    print(results["documents"][0][i])

    print("\n" + "-" * 60 + "\n")
