import os
import random
from math import floor

from app import create_app
from app.models.objects.post import Post
from app.models.objects.support import Support
from app.models.objects.user import User
from database import db

from faker import Faker

print('Removing old avatars...')
if os.path.exists("./app/static/images/avatars"):
    for file in os.listdir("./app/static/images/avatars"):
        os.remove(os.path.join("./app/static/images/avatars", file))
else:
    os.makedirs("./app/static/images/avatars")
fake = Faker()
numUsers = 100
numPosts = numUsers * 8


app = create_app()
with app.app_context(), app.test_request_context():
    print('Dropping and creating new database...')
    db.drop_all()
    db.create_all()
    print('Creating new users...')
    shuffledUsers = list(range(numUsers))
    random.shuffle(shuffledUsers)
    for i in range(len(shuffledUsers)):
        profile = fake.simple_profile()
        if profile["sex"] == "M":
            gender = "men"
        else:
            gender = "women"
        if "." in profile["name"]:
            profile["name"] = profile["name"].split('.')[1]
            profile["name"] = profile["name"].strip()
        user = User(
            firstName=profile['name'].split(' ')[0],
            lastName=profile['name'].split(' ')[1],
            username=profile['username'],
            email=profile['mail'],
            password=fake.password(),
            isAdmin=False,
            image=f"https://randomuser.me/api/portraits/{gender}/{shuffledUsers[i]}.jpg",
            is_active=True,
            postCount=0,
            joined=fake.date_time_this_decade()
        )
        db.session.add(user)
    db.session.commit()

    print('Creating new posts...')
    for i in range(numPosts):
        total = random.randint(1, 5000)
        numSentences = random.randint(1, 20)
        post = Post(
            title=fake.sentence(),
            content=fake.paragraph(nb_sentences=numSentences, variable_nb_sentences=True),
            date=fake.date_time_this_decade(),
            intensity=random.randint(1, 5),
            type=random.choice(['duel', 'gab']),
        )
        db.session.add(post)
    db.session.commit()

    print('Linking authors to posts...')
    for i in range(numPosts):
        post = db.session.get(Post, i + 1)
        author1 = db.session.get(User, random.randint(1, numUsers))
        while True:
            author2 = db.session.get(User, random.randint(1, numUsers))
            if author1 != author2:
                break
        postedDate = max(author1.joined, author2.joined)
        post.date = fake.date_time_between_dates(datetime_start=postedDate)
        post.authors.append(author1)
        post.authors.append(author2)
        author1.postCount += 1
        author2.postCount += 1
    db.session.commit()

    print('Supporting authors...')
    for userId in range(1, numUsers+1):
        shuffledPostIds = list(range(1, numPosts+1))
        random.shuffle(shuffledPostIds)
        numPostsSupported = random.randint(1, numPosts+1)
        postIds = shuffledPostIds[:numPostsSupported] if numPostsSupported != 100 else shuffledPostIds
        for postId in postIds:
            post = db.session.get(Post, postId)
            authors = post.authors
            support = Support(postId=postId,
                              authorId=random.choice([authors[0].id, authors[1].id]),
                              supporterId=userId)

            db.session.add(support)
    db.session.commit()
    db.session.close()
print("Database updated successfully!")
exit()
