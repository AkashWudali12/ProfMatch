from models import Professor

def embed_text(text: str, resume_embedding: list[float]) -> list[float]:
    # use resume embedding to include resume in prompt as well
    return [0.1, 0.2, 0.3]

def vector_search(query: str, school: str, resume_embedding: list[float]) -> list[Professor]:
    query_vector = embed_text(query, resume_embedding)

    print("query_vector: ", query_vector)

    # list of uuids of professors
    return [
        "123",
        "456",
    ]

def rerank_professors(professor_ids: list[str]) -> list[Professor]:
    print("Got professor ids: ", professor_ids)
    # Only MIT professors with real names and tailored email templates
    return [
        Professor(
            id=1,
            uuid="123",
            name="Regina Barzilay",
            school="MIT",
            description="Professor of Computer Science and AI at MIT, focusing on natural language processing, machine learning, and their applications in healthcare and drug discovery. Her research has pioneered new methods in computational linguistics and interdisciplinary AI, with a strong emphasis on real-world impact and collaboration across fields.",
            gscholar="https://scholar.google.com/citations?user=7LJrA0EAAAAJ",
            email_subject="Prospective Research Opportunity in NLP and AI",
            email_body="Dear Professor Barzilay,\n\nI am a student deeply interested in natural language processing and its applications in healthcare. I have followed your work on machine learning for drug discovery and would love to learn more about research opportunities in your group.\n\nWould you be open to a brief meeting or could you share information about how to get involved?\n\nBest regards,\n[Your Name]",
            email_address="regina@csail.mit.edu"
        ),
        Professor(
            id=2,
            uuid="456",
            name="Antonio Torralba",
            school="MIT",
            description="Professor of Electrical Engineering and Computer Science at MIT, renowned for his expertise in computer vision, deep learning, and scene understanding. His work explores large-scale visual recognition, image representation, and the development of algorithms that bridge perception and artificial intelligence.",
            gscholar="https://scholar.google.com/citations?user=GkA7KZgAAAAJ",
            email_subject="Interest in Computer Vision Research Opportunities",
            email_body="Dear Professor Torralba,\n\nI am writing to express my interest in computer vision and deep learning. Your work on scene understanding and large-scale visual recognition has been very inspiring to me.\n\nAre there any openings for undergraduate research assistants in your lab? I would appreciate any guidance on how to get involved.\n\nThank you for your time,\n[Your Name]",
            email_address="torralba@mit.edu"
        ),
        Professor(
            id=3,
            uuid="789",
            name="Tommi Jaakkola",
            school="MIT",
            description="Professor of Electrical Engineering and Computer Science at MIT, specializing in machine learning, computational biology, and probabilistic modeling. His interdisciplinary research advances the understanding of complex biological systems through innovative machine learning techniques and theoretical foundations.",
            gscholar="https://scholar.google.com/citations?user=QKkK5KcAAAAJ",
            email_subject="Inquiry about Machine Learning Research in Computational Biology",
            email_body="Dear Professor Jaakkola,\n\nI am fascinated by the intersection of machine learning and biology, and your research on probabilistic models has greatly influenced my academic interests.\n\nCould you please let me know if there are opportunities to contribute to your research group?\n\nSincerely,\n[Your Name]",
            email_address="tommi@csail.mit.edu"
        ),
    ]