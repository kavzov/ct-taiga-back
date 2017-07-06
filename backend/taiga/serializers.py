import serpy


# ---------------------------------------------------------------------------- #
# User ----------------------------------------------------------------------- #
class UserBaseSerializer(serpy.Serializer):
    id = serpy.Field()
    name = serpy.MethodField()

    def get_name(self, obj):
        return obj.get_full_name()


# ---------------------------------------------------------------------------- #
# Issue ---------------------------------------------------------------------- #
class IssueBaseSerializer(serpy.Serializer):
    id = serpy.Field()
    subject = serpy.Field()


# ---------------------------------------------------------------------------- #
# Project -------------------------------------------------------------------- #
class ProjectBaseSerializer(serpy.Serializer):
    id = serpy.Field()
    name = serpy.Field()




