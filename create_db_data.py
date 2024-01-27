import random

from faker import Faker

from app import create_app
from app.models.objects.post import Post
from app.models.objects.user import User
from database import db

fake = Faker()
numUsers = 100
numPosts = numUsers * 8

app = create_app()
with app.app_context():
    db.drop_all()
    db.create_all()
    shuffledUsers = list(range(numUsers))
    random.shuffle(shuffledUsers)
    for i in range(len(shuffledUsers)):
        profile = fake.simple_profile()
        if profile["sex"] == "M":
            gender = "men"
        else:
            gender = "women"
        user = User(
            firstName=profile['name'].split(' ')[0],
            lastName=profile['name'].split(' ')[1],
            username=profile['username'],
            email=profile['mail'],
            password=fake.password(),
            isAdmin=False,
            image=f"https://randomuser.me/api/portraits/{gender}/{shuffledUsers[i]}.jpg"
        )
        db.session.add(user)
        db.session.commit()

    for i in range(numPosts):
        post = Post(
            title=fake.sentence(),
            content=fake.paragraph(nb_sentences=20, variable_nb_sentences=True),
            date=fake.date_time_this_decade()
        )
        db.session.add(post)
        db.session.commit()

    for i in range(numPosts):
        post = Post.query.get(i + 1)
        author1 = User.query.get(random.randint(1, numUsers))
        while True:
            author2 = User.query.get(random.randint(1, numUsers))
            if author1 != author2:
                break
        post.authors.append(author1)
        post.authors.append(author2)
        db.session.commit()

    db.session.close()
    print("\nDatabase updated successfully!\n")
    exit()
