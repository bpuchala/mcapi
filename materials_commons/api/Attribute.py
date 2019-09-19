

# mc samp --id <id> --create-aset <name>
# mc samp --id <id> --create-state
#
# mc versions <path>
#
# mc state --id <id>
#   --states [<index> [<index> ...]]
#   --diff
#   --create-state
#   --delete-state <index>
#
#   --create-state
#   --delete-state
#
#   sample: s1, with states: [st0, st1, st2]
#
#   create new state st3 by proc1
#     st2 wasTransformedBy proc1 - for transf
#     st2 wasTransformedTo st3   - for transf
#     st3 wasCreatedBy proc1     - for creation
#     st3 isStateOf s1           - for creation
#
#     for each transformed attr:
#       attr.0 wasTransformedBy proc1                     - for transf
#       attr.0 wasTransformedTo attr.1                    - for transf
#       attr.1 wasCreatedBy proc1                         - for creation
#       attr.1 isAttributeOf st3 / isMemberOf st3.aset1   - for creation
#
#     for each ended attr:
#       attr.0 wasTransformedBy proc1    - for transf
#
#     for each new attr:
#       attr.1 wasCreatedBy proc1                         - for creation
#       attr.1 isAttributeOf st3 / isMemberOf st3.aset1   - for creation

class ObjectID(object):
    def __init__(self, id=None, otype=None):
        self.id = id
        self.otype = otype

def create(otype=otype, data=data, project_id=project_id, remote=None):
    """Create an object

    Arguments
    ---------
    otype: str, Object type. One of `model.OTYPE_NAMES`.
    data: dict, Object data. Includes:
        'name': str, Object name
        'description': str, Object description
        'specific_type': str, User level control of 'type', for instance to specialize Activity ->
            'tensile_test'  # TODO: naming: 'stype', 'ptype', etc.?
        'value': any JSON str, For AttributeValue.
        'value_dtype': str, For AttributeValue.
        'uncertainty': any JSON str, For AttributeValue.
        'uncertainty_dtype': str, For AttributeValue.
        'units': str, For AttributeValue.
    project_id: str, Project ID
    remote: mcapi.Remote instance, Remote where object should be created.
    """
    pass

def create_relationship(relationship, project_id=project_id, remote=None):
    """Create a relationship

    Arguments
    ---------
    relationship: tuple, Size three tuple of:
        subject: Subject of the relationship
        type: str, The relationship type. One of `model.RELATIONSHIPS.keys()` or a "reverse".
        object: object of the relationship
    project_id: str, Project ID
    remote: mcapi.Remote instance, Remote where object should be created.

    Notes
    -----
    The `relationship` argument could be implemented in various ways. For now imagine it is a size three tuple of (mcapi class instance, relationship type string, mcapi class instance), so that the 'otype' and 'id' can be obtained for the subject and the object of the relationship. The subject and object could also be tuple of strings: (otype, id).
    """
    pass

def create_object_and_relationships(otype=None, data={}, project_id=None, remote=None,
                                    relationships={}):
    """Create an object and relationships in one call"""
    new_obj = create(otype=otype, data=data, project_id=project_id, remote=None)
    for reltype, relobj in relationships.items():
        create_relationship((new_obj, reltype, relobj), project_id=project_id, remote=None)
    return new_obj

def create_sample(data={}, project_id=None, remote=None,
                  wasCreatedBy=None,
                  **relationships):
    """Create a sample

    Arguments
    ---------
    data: dict, For object creation. See `create` for options.
    project_id: str, Project ID
    remote: mcapi.Remote instance, Remote where object should be created.
    wasCreatedBy: subject, Create a `wasCreatedBy` relationship to a process.
    relationships: dict, Other relationships to create, with key=relationship type, value=relationship object.

    Notes
    -----
    The idea here is that it may be useful to users to list some or all allowed relationships explicitly.
    """"
    relationships['wasCreatedBy'] = wasCreatedBy
    return create_object_and_relationships(otype='sample', data=data, relationships=relationships, project_id=project_id, remote=remote)

def delete_sample():
    # delete states?
    # delete attribute sets?
    # delete attributes?
    # delete attribute values?
    # delete related processes?
    pass

def create_sample_state(data={}, project_id=None, remote=None,
                        isStateOf=None,
                        wasCreatedBy=None,
                        wasTransformedBy=None,
                        wasTransformedFrom=None,
                        **relationships):
    """Create a sample state"""
    # transform or create attributes? attribute sets?
    # set isInitialStateOf?, isFinalStateOf? manually? auto?

    relationships['isStateOf'] = isStateOf
    relationships['wasCreatedBy'] = wasCreatedBy
    relationships['wasTransformedBy'] = wasTransformedBy
    relationships['wasTransformedFrom'] = wasTransformedFrom
    return create_object_and_relationships(otype='sample', data=data, relationships=relationships, project_id=project_id, remote=remote)

def create_attribute_set(data={}, project_id=None, remote=None,
                        isAttributeSetOf=None,
                        wasCreatedBy=None,
                        wasTransformedBy=None,
                        wasTransformedFrom=None,
                        **relationships):
    """Create an attribute set"""

    relationships['isAttributeSetOf'] = isAttributeSetOf
    relationships['wasCreatedBy'] = wasCreatedBy
    relationships['wasTransformedBy'] = wasTransformedBy
    relationships['wasTransformedFrom'] = wasTransformedFrom
    return create_object_and_relationships(otype='attribute_set', data=data, relationships=relationships, project_id=project_id, remote=remote)

def create_attribute(data={}, project_id=None, remote=None,
                        isAttributeOf=None,
                        isMemberOf=None,
                        wasCreatedBy=None,
                        wasTransformedBy=None,
                        wasTransformedFrom=None,
                        **relationships):
    """Create an attribute"""

    relationships['isAttributeOf'] = isAttributeOf
    relationships['isMemberOf'] = isMemberOf
    relationships['wasCreatedBy'] = wasCreatedBy
    relationships['wasTransformedBy'] = wasTransformedBy
    relationships['wasTransformedFrom'] = wasTransformedFrom
    return create_object_and_relationships(otype='attribute', data=data, relationships=relationships, project_id=project_id, remote=remote)

def create_attribute_value(data={}, project_id=None, remote=None,
                            isValueOf=None,
                            isBestValueOf=None,
                            wasCreatedBy=None,
                            **relationships):
    """Create an attribute value"""
    relationships['isValueOf'] = isValueOf
    relationships['isBestValueOf'] = isBestValueOf
    relationships['wasCreatedBy'] = wasCreatedBy
    return create_object_and_relationships(otype='attribute_value', data=data, relationships=relationships, project_id=project_id, remote=remote)

# attr = create_attribute(data={"name":"color"}, isAttributeOf=state)
# value = create_attribute_value(data={"value":"blue", "value_dtype":"str"}, isValueOf=attr)
create_attribute_with_value(object, name="color", value="blue", wasCreatedBy=None, **relationships)

class AttributeSetData(object):
    """Data structure to help creating/deleting/updating AttributeSet objects

    Attributes
    ----------
    name: str
    id: str
    create_attributes: list AttributeData instance
        Attributes to be created. May create attribute values also. Cannot create any other related objects (files, processes, etc.)
    delete_attributes: dict of id:AttributeData instance
        Attributes to be deleted. May delete attribute values also (default does not delete). Cannot delete any other related objects (files, processes, etc.)
    update_attributes: dict of id:AttributeData instance
        Values to be updated. May also create/delete/update attributes and attributes values.
    add_member_attributes: set of Attribute ID
        Set of IDs of Attributes to be added to the set (not created, they must already exist).
    remove_member_attributes: set of Attribute ID
        Set of IDs of Attributes to be removed from the set (not deleted).
    """
    def __init__(self):
        self.name = None
        self.id = None

        self.create_attributes = []
        self.update_attributes = {}
        self.delete_attributes = {}
        self.add_member_attributes = set([])
        self.remove_member_attributes = set([])

    def to_dict(self):
        return {
            "name": self.name,
            "attributes": {name:attr.to_dict() for attr in self.attributes}
        }

class AttributeData(object):
    """Data structure for creating/deleting/updating Attribute objects

    Attributes
    ----------
    name: str
    id: str
    best_measure_id: str
    create_values: list AttributeValueData instance
        Values to be created.
    delete_value_ids: set of str
        Set of IDs of AttributeValue to be deleted
    update_values: dict of id:AttributeValueData instance
        Values to be updated.
    """
    def __init__(self):
        self.name = None
        self.id = None
        self.best_measure_id = None

        self.create_values = []
        self.update_values = {}
        self.delete_values = set([])

    def update_value(self, avaldata):
        self.update_values[avaldata.id] = avaldata

    def create_value(self, avaldata):
        self.create_values.append(avaldata)

    def delete_value_id(self, aval_id):
        self.delete_value_ids.add(aval_id)


    def to_dict(self):
        return {
            "name": self.name,
            "best_measure_id": self.best_measure_id,
            "update_values": {value.id:value.to_dict() for value in self.values},
            "create_values": [value.to_dict() for value in self.create_values],
            "delete_value_ids": list(self.delete_value_ids)
        }

class AttributeValueData(object):
    """Data structure for creating/deleting/updating AttributeValue objects

    For update, we'll assume that all AttributeValue attributes are updated. So for instance, if 'units'==None, it will be set to null.

    Attributes
    ----------
    id: str, Materials Commons ID
    units: str, Describes the units of the value
    value: str, Any valid JSON value
    value_dtype: str, Describes the format of the value.
    uncertainty: str, Any valid JSON value. For the future.
    uncertainty_dtype: str, Describes the format of the uncertainty. For the future.

    """
    def __init__(self):
        self.id = None
        self.units = None
        self.value = None
        self.value_dtype = None
        self.uncertainty = None
        self.uncertainty_dtype = None

    def to_dict(self):
        return {
            "unit": self.units,
            "value": self.value,
            "value_dtype": self.value_dtype,
            "uncertainty": self.uncertainty,
            "uncertainty_dtype": self.uncertainty_dtype,
            "id": self.id
        }
