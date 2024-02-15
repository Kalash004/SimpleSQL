import inspect

from SimpleSql.Models.SimpleTableObjects.SimpleTable import SimpleBaseTable


class Base:
    # TODO: Check if all of the attributes are set after init
    table_name: str = None

    def __init__(self, **kwargs):
        # Create table object and (Send table object to the controller singleton) - done in init of table object
        self.__tablename_exists()
        SimpleBaseTable(self)
        # Set values of this ojbect
        try:
            skip_setup = kwargs["skip_setup"]
        except KeyError:
            skip_setup = False
        if not skip_setup is True:
            self.__setup(kwargs)

    def __setup(self, kwargs):
        child_fields = type(self).__dict__
        for attribute, value in kwargs.items():
            if attribute in child_fields.keys():
                # TODO: Check if value is a same type as the SimpleParams
                setattr(self, attribute, value)
            else:
                raise Exception(f"Attribute {attribute} is not a part of this object {type(self)}")
        if self.__get_count_of_atrs(self) > len(kwargs):
            raise Exception(f"The amount of **kwargs is not same as the atributes defined in the table")

    # TODO: if count of inputs not same as atributes of class raise error

    def __tablename_exists(self):
        if self.table_name is None:
            raise Exception(f"{type(self)} : (table_name = {self.table_name}) cant be None. Please set the name of "
                            f"the table")

    @staticmethod
    def __get_count_of_atrs(pre_struct):
        struct = []
        for i in inspect.getmembers(pre_struct):
            if i[0].startswith('_'):
                continue
            if inspect.ismethod(i[1]):
                continue
            if i[0] == 'table_name':
                continue
            struct.append(i)
        return len(struct)

    def map(self, data):
        try:
            for attr, item in data.items():
                self.__dict__[attr] = item
        except Exception as ex:
            raise Exception(f"Error while mapping data from database to object : {ex}") from ex
