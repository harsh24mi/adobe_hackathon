from sentence_transformers import SentenceTransformer

print("Downloading model... This may take a moment.")

# This model is small, fast, and effective for semantic search
model = SentenceTransformer('all-MiniLM-L6-v2')

# Save the model to the 'models' directory
model.save('models/all-MiniLM-L6-v2')

print("Model downloaded and saved to the 'models' folder.")