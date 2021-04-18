from pymongo.write_concern import WriteConcern

from pymodm import MongoModel, fields


class Campground(MongoModel):
    title = fields.CharField(required=True)
    image = fields.CharField(required=True)
    price = fields.FloatField(required=True, min_value=0.)
    description = fields.CharField(required=True)
    location = fields.CharField(required=True)

    class Meta:
        write_concern = WriteConcern(j=True)
        connection_alias = 'yelp-camp'
