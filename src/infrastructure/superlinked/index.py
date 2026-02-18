from superlinked import framework as sl
from ...config import settings


class Property(sl.Schema):
    """real state schema"""
    id: sl.IdField
    description: sl.String
    baths: sl.Integer
    rooms: sl.Integer
    sqm: sl.Integer
    location: sl.String
    price: sl.Integer

property_schema = Property()


description_space = sl.TextSimilaritySpace(
    text=property_schema.description,
    model=settings.superlinked.embedding_model
)

size_space = sl.NumberSpace(
    number=property_schema.sqft,
    min_value=settings.superlinked.sqm_min_value,
    max_value=settings.superlinked.sqm_max_value,
    mode=sl.Mode.MAXIMUM
)

price_space = sl.NumberSpace(
    number=property_schema.price,
    min_value=settings.superlinked.price_min_value,
    max_value=settings.superlinked.price_max_value,
    mode=sl.Mode.MINIMUM
)

property_index = sl.Index(
    spaces=[description_space, size_space, price_space],
    fields=[
        property_schema.rooms,
        property_schema.baths,
        property_schema.sqm,
        property_schema.price,
        property_schema.location,
    ]
)