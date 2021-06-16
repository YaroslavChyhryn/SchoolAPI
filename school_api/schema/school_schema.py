from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from ..models.models import GroupModel, StudentModel, CourseModel


# todo relationship as url
class GroupSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = GroupModel
        load_instance = True
        include_relationships = True


class StudentSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = StudentModel
        load_instance = True
        include_relationships = True


class CourseSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = CourseModel
        load_instance = True
        include_relationships = True
