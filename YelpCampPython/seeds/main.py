"""Seed MongoDB with data."""
import random

from pymodm import connect

from models.campground import Campground
from seeds.cities import cities
from seeds.seed_helpers import descriptors, places

if __name__ == "__main__":
    connect("mongodb://localhost:27017/yelpCamp", alias="yelp-camp")

    # Remove all campgrounds
    Campground.objects.delete()
    # QuerySet(model=Campground).delete()

    # Add random campgrounds
    K = 1000
    campgrounds = []
    for city, descriptor, place in zip(random.choices(cities, k=K),
                                       random.choices(descriptors, k=K),
                                       random.choices(places, k=K)):
        campgrounds.append(
            Campground(
                title=f"{descriptor} {place}",
                location=f"{city['city']}, {city['state']}"
            )
        )
    Campground.objects.bulk_create(campgrounds)
