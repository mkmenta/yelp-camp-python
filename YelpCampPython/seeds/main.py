"""Seed MongoDB with data."""
import random

from mongoengine import connect

from models.campground import Campground
from models.review import Review
from seeds.cities import cities
from seeds.seed_helpers import descriptors, places

if __name__ == "__main__":
    connect("yelpCamp")

    # Remove all campgrounds and reviews
    Campground.drop_collection()
    Review.drop_collection()

    # Add random campgrounds
    K = 1000
    campgrounds = []
    for city, descriptor, place in zip(random.choices(cities, k=K),
                                       random.choices(descriptors, k=K),
                                       random.choices(places, k=K)):
        campgrounds.append(
            Campground(
                title=f"{descriptor} {place}",
                image='https://source.unsplash.com/collection/483251',
                location=f"{city['city']}, {city['state']}",
                description='Lorem ipsum dolor sit amet consectetur adipisicing elit. Quibusdam dolores vero '
                            'perferendis laudantium, consequuntur voluptatibus nulla architecto, sit soluta esse iure '
                            'sed labore ipsam a cum nihil atque molestiae deserunt!',
                price=round((random.random() * 20) + 10, 2)
            )
        )
    Campground.objects.insert(campgrounds)
