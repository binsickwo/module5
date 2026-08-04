from faker import Faker
import random
import string
faker = Faker('en')

VALID_GENRE_IDS = [1, 5, 6, 7, 8, 9, 10]


class DataGenerator:
    def __init__(self):
        pass

    @classmethod
    def generate_random_password(cls):
        allowed = string.ascii_letters + string.digits + "?@#$%^&*_+-=()[]{}><"
        password = [random.choice(string.ascii_letters), random.choice(string.digits)]
        password += [random.choice(allowed) for _ in range(8)]
        random.shuffle(password)
        return ''.join(password)

    @classmethod
    def generate_random_email(cls):
        return faker.email()

    @classmethod
    def generate_random_name(cls):
        return faker.name()

    @classmethod
    def generate_movie_data(cls, genre_id=None, location=None):
        locations = ["MSK", "SPB"]
        image_id = random.randint(1, 1000)
        return {
            "name": f"Test Movie {faker.uuid4()[:8]}",
            "description": faker.text(max_nb_chars=200).replace("\n", " "),
            "price": random.randint(100, 1000),
            "imageUrl": f"https://picsum.photos/id/{image_id}/200/300",
            "location": location or random.choice(locations),
            "published": True,
            "genreId": genre_id or random.choice(VALID_GENRE_IDS)
        }
