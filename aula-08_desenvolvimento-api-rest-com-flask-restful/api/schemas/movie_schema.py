from api import ma
from marshmallow import schema, fields

class MovieSchema(ma.Schema):
    class Meta:
        fields = ("_id", "title", "description", "year")
        
    _id = fields.Str()
    title = fields.Str(required=True)
    description = fields.Str(required=True)
    year = fields.Int(required=True)