import random

from faker import Faker

from app import create_app
from app.models.objects.post import Post
from app.models.objects.user import User
from database import db

fake = Faker()
num = 20

app = create_app()
with app.app_context():
    for i in range(num):
        user = User(
            firstName=fake.first_name(),
            lastName=fake.last_name(),
            username=fake.user_name(),
            email=fake.free_email(),
            password=fake.password(),
            isAdmin=False
        )
        db.session.add(user)
        db.session.commit()

    for i in range(num * 15):
        randomUser = User.query.get(random.randint(1, num))
        post = Post(
            title=fake.sentence(),
            content=fake.paragraph(nb_sentences=20, variable_nb_sentences=True),
            author=randomUser.id,
            date=fake.date_time_this_decade()
        )
        db.session.add(post)
        db.session.commit()
    db.session.close()
    print("\nDatabase updated successfully!\n")
    exit()
