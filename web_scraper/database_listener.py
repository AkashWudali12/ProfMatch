from supabase_client import get_missing_professors, update_description, add_to_pinecone
from pinecone_client import upsert_professor
from gs_links import NAME_TO_ABBR
from description_generation import generate_description
from sentence_transformers import SentenceTransformer
from pprint import pprint

model = SentenceTransformer("all-MiniLM-L6-v2")
BATCH_SIZE = 10


# function should be a pg_cron job that runs either 
# (1) every 12 hours checking for false entries for added_to_pinecone
# (2) as a trigger on the professors table when there is a new insert

# will use emebedding_text to add to pinecone
# will add description to postgres table

def description_and_pinecone_insertion():
    # get all professors where description is NULL or TEST and added_to_pinecone is False
    vectors = []
    professors = get_missing_professors()
    for professor in professors:
        name = professor["first_name"] + " " + professor["middle_name_initial"] + " " + professor["last_name"]
        school = professor["university"]
        uuid = professor["id"]
        embedding_text = professor["embedding_text"]
        new_description = generate_description(name, school)

        if embedding_text is None:
            embedding_text = f"""
            This is Dr. {name}, a researcher at {school}. 
            Here is a short description of the professor:
            {new_description}
            """
        else:
            embedding_text = f"""
            This is Dr. {name}, a researcher at {school}. 
            Here is a short description of the professor:
            {new_description}
            Here is information about his most recent publication:
            {embedding_text}
            """

        # update description in database
        update_description(uuid, new_description)

        embedding = model.encode(embedding_text)
        vectors.append({
            "id": uuid,
            "values": embedding,
            "metadata": {
                "name": name,
                "university": school,
                "uuid": uuid
            }
        })
        add_to_pinecone(uuid)
        if len(vectors) == BATCH_SIZE:
            upsert_professor(vectors, NAME_TO_ABBR[school])
            vectors = []
    if len(vectors) > 0:
        upsert_professor(vectors, NAME_TO_ABBR[school])
        vectors = []

def main():
    description_and_pinecone_insertion()

if __name__ == "__main__":
    main()