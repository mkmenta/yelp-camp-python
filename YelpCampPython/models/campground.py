from pymongo.write_concern import WriteConcern

from pymodm import MongoModel, fields


class Campground(MongoModel):
    title = fields.CharField()
    image = fields.CharField()
    price = fields.FloatField()
    description = fields.CharField()
    location = fields.CharField()

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'yelp-camp'
