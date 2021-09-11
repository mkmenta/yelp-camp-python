"""Seed MongoDB with data."""
import random

from mongoengine import connect

from models.campground import Campground
from models.review import Review
from models.user import User
from seeds.cities import cities
from seeds.seed_helpers import descriptors, places

if __name__ == "__main__":
    connect("yelpCamp")

    # Remove all campgrounds and reviews
    Campground.drop_collection()
    Review.drop_collection()
    User.drop_collection()

    # Add user
    user = User.register(username="mike", email="mike@gmail.com", password="mike")

    # Add random campgrounds
    K = 200
    campgrounds = []
    for city, descriptor, place in zip(random.choices(cities, k=K),
                                       random.choices(descriptors, k=K),
                                       random.choices(places, k=K)):
        campgrounds.append(
            Campground(
                title=f"{descriptor} {place}",
                author=user.id,
                images=[{'url': 'https://source.unsplash.com/collection/483251', 'public_id': '483251'}],
                geometry={
                    "type": "Point",
                    "coordinates": (city['longitude'], city['latitude'])
                },
                location=f"{city['city']}, {city['state']}",
                description='Lorem ipsum dolor sit amet consectetur adipisicing elit. Quibusdam dolores vero '
                            'perferendis laudantium, consequuntur voluptatibus nulla architecto, sit soluta esse iure '
                            'sed labore ipsam a cum nihil atque molestiae deserunt!',
                price=round((random.random() * 20) + 10, 2)
            )
        )
    Campground.objects.insert(campgrounds)
