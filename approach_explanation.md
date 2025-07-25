# Approach for Persona-Driven Document Intelligence

Our solution for Round 1B addresses the challenge of finding relevant information in a large collection of documents for a specific user. The core of our approach is based on modern semantic search techniques, moving beyond simple keyword matching to understand the underlying meaning and context of both the user's query and the documents.

At the heart of the system is the `all-MiniLM-L6-v2` sentence-transformer model. We chose this model because it offers an excellent balance of performance and size, easily fitting within the hackathon's constraints (under 1GB, CPU-only execution). This model excels at converting text into high-dimensional vector embeddings, where sentences with similar meanings are located closer to each other in vector space.

The process is as follows:

1.  **Query Formulation**: We combine the user's persona description and their "job-to-be-done" into a single, rich query string. This provides the model with the full context of the user's intent.

2.  **Document Chunking**: Each page of every PDF in the collection is treated as a distinct "section." The text from each page is extracted.

3.  **Embedding Generation**: Both the user's query and every extracted document section are passed through the sentence-transformer model. This converts all text into numerical vectors.

4.  **Relevance Ranking**: To determine the relevance of each section, we calculate the cosine similarity between the query's vector and each section's vector. A higher cosine similarity score (closer to 1.0) indicates a stronger semantic relationship.

5.  **Output**: The sections are then ranked in descending order of their similarity scores. The final output is a JSON file that presents this ranked list, with the most relevant section for the user's task at the top.

This method allows the system to find sections that are contextually relevant even if they don't share exact keywords with the query. For example, a search for "corporate financial health" could correctly identify a section discussing "revenue, profit margins, and debt-to-equity ratio," demonstrating a true understanding of the user's need.