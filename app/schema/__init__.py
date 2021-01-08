import abc

import graphene


class ISchema(abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_schema(cls) -> graphene.Schema:
        """
        GraphQL schema fabric
        :return: schema for GraphQL server
        """
        pass


class HelloSchema(ISchema):
    @classmethod
    def get_schema(cls) -> graphene.Schema:
        class Query(graphene.ObjectType):
            hello = graphene.String()

            async def resolve_hello(self, info: graphene.ResolveInfo) -> str:
                return 'Hello world'

        return graphene.Schema(query=Query)


class DefaultSchema(ISchema):
    @classmethod
    def get_schema(cls) -> graphene.Schema:
        return graphene.Schema()
