

# Materials Commons class hierarchy

# Any, specializes: Agents, Object, Collection, Selection
# Agent, specializes: User
# Object, specializes: Activity, Entity
#   Activity, specializes: Process
#   Entity, specializes: Sample, SampleState, File, Attribute, AttributeValue
# Collection, specializes: Project, Experiment, Directory, AttributeSet, Dataset
# Selection, specializes: FileSelection, ObjectSelection

# Collection membership:
#   Project hasMembers of type: User, Object, Collection (excluding Projects)
#   Project hasViewers of type: User
#   Experiment hasMembers of type: Sample, Process
#   Directory hasMembers of type: File, Directory
#   DataSet hasMembers of type: FileSelection, Sample, Process
#   AttributeSet hasMembers of type: Attribute

# Selection:
#   FileSelection: return iterables of Files
#   ObjectSelection: return iterables of Objects


# class Process(Base):  (Example class)
#
#   ### class static attributes ###
#
#   otype = 'process'
#
#   # list of all instance metadata members with name, type, and if user can update them directly
#   model = {
#     'name': { 'otype': 'string', 'can_update': True },
#     'description': { 'otype': 'string', 'can_update': True },
#     'ptype': { 'otype': 'string', 'can_update': True },
#
#     'id': { 'otype': 'string', 'can_update': False },
#     ....
#   }
#
#
#   ### class instance attributes ###
#
#   ## metadata, defined for this class ##
#
#   # has owners
#   user_owner
#   proj_owner
#
#   # single-valued attributes, pre-defined for each otype
#   metadata:
#     (can update): name, description, ptype
#     (cannot update): id, otype, birthtime, mtime, n_relationships
#
#   # relationships: describe relationships
#   # - whether a particular relationship is allowed
#   #   is determined from RELATIONSHIPS master schema (see below)
#   # - get summary list with object data? or just n_relationships?
#   # - includes attributes & attribute sets with 'hasAttribute' and 'hasAttributeSet'
#   relationships: [
#     {'type': 'used', 'object_id': <id>, 'object_otype': 'sample', 'object_name': <name>},
#     {'type': 'has', 'object_id': <id>, 'object_otype': 'attribute_set', 'object_name': <name>},
#     {'type': 'isAssociatedWithFile', 'object_id': <id>, 'object_otype': 'file', 'object_name': <name>}
#     ...
#   ]


# ** Any **

class Any(object):
    def __init__(self, data={}):
        super(Process, self).__init__(data)

        if data.get('otype', None) is not self.otype:
            raise MCConstructionException("Could not construct '" + self._type() + "', wrong otype: '" + data.get('otype', None) + "', expected '" + self.otype + "'", data)

        self.input_data = data

        for key, value in self.model.items():
            setattr(self, key, data.get(key, None))

    def _type(self):
        return self.__class__.__name__

    def data(self):
        """Return dict containing all object metadata"""
        return {key: getattr(self, key) for key in self.model}

    def update_data(self):
        """Return dict used for updating object metadata"""
        result = {
            "id": self.id,
            "otype": self.otype,
        }
        for key in self.model:
             if self.model[key].get('can_update', None):
                 result[key] = getattr(self, key)
        return result

# ** Any specializes to: Agent, Object, Collection, Selection **

class Agent(object):
    def __init__(self):
        pass

class Object(Any):
    def __init__(self):
        pass

class Collection(Any):
    def __init__(self):
        pass

class Selection(Any):
    def __init__(self):
        pass

# ** Object specializes to: Activity, Entity **

class Activity(Object):
    def __init__(self):
        pass

class Entity(Object):
    def __init__(self):
        pass

# ** Activity specializes to Process **

class Process(Activity):

    otype = 'process'

    model = {
        'name': { 'otype': 'string', 'can_update': True },
        'description': { 'otype': 'string', 'can_update': True },
        'ptype': { 'otype': 'string', 'can_update': True },

        'template_id': { 'otype': 'string', 'can_update': False },
        'template_name': { 'otype': 'string', 'can_update': False },
        'process_type': { 'otype': 'string', 'can_update': False },

        'n_relationships': { 'otype': 'integer', 'can_update': False },
        'n_attributes': { 'otype': 'integer', 'can_update': False },
        'n_attribute_sets': { 'otype': 'integer', 'can_update': False },

        'owner': { 'otype': 'string', 'can_update': False },
        'project_owner': { 'otype': 'string', 'can_update': False },
        'id': { 'otype': 'string', 'can_update': False },
        'mtime': { 'otype': 'time', 'can_update': False },
        'birthtime': { 'otype': 'time', 'can_update': False },
        'project_id': { 'otype': 'string', 'can_update': False }
    }

    def __init__(self, data={}):
        super(Process, self).__init__(data)

# ** Entity specializes to Sample, SampleState, File, Attribute, AttributeValue **

class SampleState(Entity):

    otype = 'sample_state'

    model = {
        'name': { 'otype': 'string', 'can_update': True },
        'description': { 'otype': 'string', 'can_update': True },

        'n_relationships': { 'otype': 'integer', 'can_update': False },
        'n_attributes': { 'otype': 'integer', 'can_update': False },
        'n_attribute_sets': { 'otype': 'integer', 'can_update': False },

        'owner': { 'otype': 'string', 'can_update': False },
        'project_owner': { 'otype': 'string', 'can_update': False },
        'id': { 'otype': 'string', 'can_update': False },
        'mtime': { 'otype': 'time', 'can_update': False },
        'birthtime': { 'otype': 'time', 'can_update': False },
        'project_id': { 'otype': 'string', 'can_update': False }
    }

    def __init__(self, data={}):
        super(SampleState, self).__init__(data)

class Sample(Entity):

    otype = 'sample'

    model = {
        'name': { 'otype': 'string', 'can_update': True },
        'description': { 'otype': 'string', 'can_update': True },

        'n_relationships': { 'otype': 'integer', 'can_update': False },
        'n_attributes': { 'otype': 'integer', 'can_update': False },
        'n_attribute_sets': { 'otype': 'integer', 'can_update': False },

        'owner': { 'otype': 'string', 'can_update': False },
        'project_owner': { 'otype': 'string', 'can_update': False },
        'id': { 'otype': 'string', 'can_update': False },
        'mtime': { 'otype': 'time', 'can_update': False },
        'birthtime': { 'otype': 'time', 'can_update': False },
        'project_id': { 'otype': 'string', 'can_update': False }
    }

    def __init__(self, data={}):
        super(Sample, self).__init__(data)

class File(Entity):
    """

    Notes
    -----
    - If acted on by a process, use 'wasCreatedBy', 'wasUsedBy', 'wasTransformedBy'
    - If associated with any object, use 'isAssociatedWith'
    - Indicate file versions with 'wasTransformedTo'/'wasTransformedFrom'
    - Indicate parent directory with 'isChildOf'
    """

    otype = 'file'

    model = {
        'name': { 'otype': 'string', 'can_update': False },

        'size': { 'otype': 'integer', 'can_update': False },
        'checksum': { 'otype': 'string', 'can_update': False },
        'mediatype': { 'otype': 'object', 'can_update': False },

        'n_relationships': { 'otype': 'integer', 'can_update': False },
        'n_attributes': { 'otype': 'integer', 'can_update': False },
        'n_attribute_sets': { 'otype': 'integer', 'can_update': False },

        'owner': { 'otype': 'string', 'can_update': False },
        'project_owner': { 'otype': 'string', 'can_update': False },
        'id': { 'otype': 'string', 'can_update': False },
        'mtime': { 'otype': 'time', 'can_update': False },
        'birthtime': { 'otype': 'time', 'can_update': False },
        'project_id': { 'otype': 'string', 'can_update': False }
    }

    def __init__(self, data={}):
        super(File, self).__init__(data)

class Directory(Entity):

    otype = 'directory'

    model = {
        'name': { 'otype': 'string', 'can_update': False },
        'path': { 'otype': 'string', 'can_update': False },

        'n_relationships': { 'otype': 'integer', 'can_update': False },
        'n_attributes': { 'otype': 'integer', 'can_update': False },
        'n_attribute_sets': { 'otype': 'integer', 'can_update': False },

        'owner': { 'otype': 'string', 'can_update': False },
        'project_owner': { 'otype': 'string', 'can_update': False },
        'id': { 'otype': 'string', 'can_update': False },
        'mtime': { 'otype': 'time', 'can_update': False },
        'birthtime': { 'otype': 'time', 'can_update': False },
        'project_id': { 'otype': 'string', 'can_update': False }
    }

    def __init__(self, data={}):
        super(Directory, self).__init__(data)

class Attribute(Entity):

    otype = 'attribute'

    model = {
        'name': { 'otype': 'string', 'can_update': False },
        'best_measure_id': { 'otype': 'string', 'can_update': False },

        'n_relationships': { 'otype': 'integer', 'can_update': False },

        'owner': { 'otype': 'string', 'can_update': False },
        'project_owner': { 'otype': 'string', 'can_update': False },
        'id': { 'otype': 'string', 'can_update': False },
        'mtime': { 'otype': 'time', 'can_update': False },
        'birthtime': { 'otype': 'time', 'can_update': False },
        'project_id': { 'otype': 'string', 'can_update': False }
    }

    def __init__(self, data={}):
        super(Attribute, self).__init__(data)

class AttributeValue(Entity):

    otype = 'attribute_value'

    model = {
        'name': { 'otype': 'string', 'can_update': False },

        'value': { 'otype': 'any', 'can_update': False },
        'units': { 'otype': 'string', 'can_update': False },
        'value_dtype': { 'otype': 'string', 'can_update': False },
        'uncertainty': { 'otype': 'any', 'can_update': False },
        'uncertainty_dtype': { 'otype': 'string', 'can_update': False },

        'n_relationships': { 'otype': 'integer', 'can_update': False },

        'owner': { 'otype': 'string', 'can_update': False },
        'project_owner': { 'otype': 'string', 'can_update': False },
        'id': { 'otype': 'string', 'can_update': False },
        'mtime': { 'otype': 'time', 'can_update': False },
        'birthtime': { 'otype': 'time', 'can_update': False },
        'project_id': { 'otype': 'string', 'can_update': False }
    }

    def __init__(self, data={}):
        super(AttributeValue, self).__init__(data)


# ** Collection specializes to Project, Dataset, Experiment, Directory, AttributeSet **

class Project(Activity):

    otype = "project"

    model = {
        'name': { 'otype': 'string', 'can_update': False },
        'description': { 'otype': 'string', 'can_update': False },

        'n_processes': { 'otype': 'integer', 'can_update': False },

        'n_samples': { 'otype': 'integer', 'can_update': False },
        'n_sample_states': { 'otype': 'integer', 'can_update': False },
        'n_attribute_values': { 'otype': 'integer', 'can_update': False },

        'n_experiments': { 'otype': 'integer', 'can_update': False },
        'n_directories': { 'otype': 'integer', 'can_update': False },
        'n_files': { 'otype': 'integer', 'can_update': False },
        'n_datasets': { 'otype': 'integer', 'can_update': False },

        'n_file_selections': { 'otype': 'integer', 'can_update': False },
        'n_object_selections': { 'otype': 'integer', 'can_update': False },

        'owner': { 'otype': 'string', 'can_update': False },
        'id': { 'otype': 'string', 'can_update': False },
        'mtime': { 'otype': 'time', 'can_update': False },
        'birthtime': { 'otype': 'time', 'can_update': False }
    }
    def __init__(self, data={}):
        super(Project, self).__init__(data)

class Experiment(Collection):

    otype = 'experiment'

    model = None #TODO

    def __init__(self, data={}):
        super(Experiment, self).__init__(data)

class Directory(Collection):

    otype = 'directory'

    model = None #TODO

    def __init__(self, data={}):
        super(Directory, self).__init__(data)

class AttributeSet(Collection):

    otype = 'attribute_set'

    model = None #TODO

    def __init__(self, data={}):
        super(AttributeSet, self).__init__(data)

class Dataset(Collection):

    otype = 'dataset'

    model = None #TODO

    def __init__(self, data={}):
        super(Dataset, self).__init__(data)


# ** Selection, specializes: FileSelection, ObjectSelection **

class FileSelection(Collection):

    otype = 'file_selection'

    model = None #TODO

    def __init__(self, data={}):
        super(FileSelection, self).__init__(data)

class ObjectSelection(Collection):

    otype = 'object_selection'

    model = None #TODO

    def __init__(self, data={}):
        super(ObjectSelection, self).__init__(data)


# list of otypes, otype_names

OTYPES = [User, Process, Sample, SampleState, File, Attribute, AttributeValue, Project, Experiment, Directory, AttributeSet, Dataset, FileSelection, ObjectSelection]

OTYPE_NAMES = [cls.__name__ for cls in OTYPES]


# list of relationships

RELATIONSHIPS = {
        'owns': {
            'reverse': 'isOwnedBy',
            'allowed': [
                {'type': [['user'], ['object', 'collection', 'selection']], 'n': ['*', 1]},
                {'type': [['project'], ['object', 'experiment', 'dataset', 'directory', 'attribute_set', 'selection']], 'n': ['*', 1]},
            ]
        },
        'isViewerOf': {
            'reverse': 'isViewerOf',
            'allowed': [{'type': [['user'], ['project']], 'n': ['*', '*']}]
        },
        'hasMember': {
            'reverse': 'isMemberOf',
            'allowed': [
                {'type': [['dataset'], ['sample', 'process', 'file_selection', 'object_selection']], 'n': ['*', '*']}
                {'type': [['experiment'], ['sample', 'process']], 'n': ['*', '*']}
                {'type': [['attribute_set'], ['attribute'], 'n': ['*', '*']]}
            ]
        },
        'used': {
            'reverse': 'wasUsedBy',
            'allowed': [{'type': [['process'], ['entity']], 'n': ['*', '*']}]
        },
        'created': {
            'reverse': 'wasCreatedBy',
            'allowed': [
                {'type': [['process'], ['sample', 'sample_state']], 'n': ['*', 1]},
                {'type': [['process'], ['file', 'attribute_value']], 'n': ['*', [0, 1]]}
            ]
        },
        'transformed': {
            'reverse': 'wasTransformedBy',
            'allowed': [{'type': [['process'], ['entity']], 'n': ['*', [0, 1]]}]
        },
        'wasTransformedTo': {
            'reverse': 'wasTransformedFrom',
            'allowed': [
                {'type': [['sample_state'], ['sample_state']], 'n':[[0, 1],[0, 1]]},
                {'type': [['attribute'], ['attribute']], 'n':[[0, 1], [0, 1]]},
                {'type': [['file'], ['file']], 'n':[[0, 1], [0, 1]]},
            ]
        },
        'hasInitialState': {
            'reverse': 'isInitialStateOf',
            'allowed': [{'type': [['sample'], ['sample_state']], 'n': [1, [0, 1]]}]
        },
        'hasFinalState': {
            'reverse': 'isFinalStateOf',
            'allowed': [{'type': [['sample'], ['sample_state']], 'n': [1, [0, 1]]}]
        },
        'hasState': {
            'reverse': 'isStateOf',
            'allowed': [{'type': [['sample'], ['sample_state']], 'n': ["*", 1]}]
        },
        'isAssociatedWithFile': {
            'reverse': 'isAssociatedWith',
            'allowed': [{'type': [['entity'], ['file']], 'n': ['*', '*']}]
        },
        'hasAttribute': {
            'reverse': 'isAttributeOf',
            'allowed': [
                {'type': [['process', 'sample', 'sample_state', 'file'], ['attribute']], 'n': ['*', "*"]}
            ]
        },
        'hasAttributeSet': {
            'reverse': 'isAttributeSetOf',
            'allowed': [
                {'type': [['process', 'sample', 'sample_state', 'file'], ['attribute']], 'n': ['*', "*"]}
            ]
        },
        'hasValue': {
            'reverse': 'isValueOf',
            'allowed': [{'type': [['attribute'], ['attribute_value']], 'n': ['*', 1]}]
        },
        'hasBestValue': {
            'reverse': 'isBestValueOf',
            'allowed': [{'type': [['attribute'], ['attribute_value']], 'n': [[0, 1], [0, 1]]}]
        },
        'hasChild': {
            'reverse': 'isChildOf',
            'allowed': [
                {'type': [['directory'], ['directory']], 'n': ['*', [0, 1]]},
                {'type': [['directory'], ['file']], 'n': ['*', 1]}
            ]
        }
    }


# ### Sketch of most essential functions ###

### API calls ###

#
# # users
# get_all_users(remote=None)
# get_apikey(user_id, password, remote=None)
#
# # projects
# get_all_projects(remote)
#
# # files & directories
#
# get_file_or_directory_by_path(path, project_id=None, remote=None)
# download_file_by_id(file_id, local_path, project_id=None, remote=None)
# download_file_by_path(remote_path, local_path, project_id=None, remote=None)
# upload_file(local_path, remote_path, project_id=None, remote=None)
# <globus requests>
#
#
# # objects
#
# get_object_models(remote=None)
# create(otype, data={}, project_id=None, experiment_id=None, remote=None)
# create_many(data=[<list of objects with otype and data>], project_id=None, experiment_id=None, remote=None)
# chown_user(object_id, new_user_owner_id, otype=None, project_id=None, experiment_id=None, remote=None)
# chown_project(object_id, new_project_owner_id, otype=None, project_id=None, experiment_id=None, remote=None)
# get(object_id=None, object_type=None, project_id=None, experiment_id=None, remote=None) -> return all matching objects
# delete(object_id=None, otype=None, project_id=None, experiment_id=None, remote=None) -> delete all matching
# update(object_id, data={}, otype=None, project_id=None, experiment_id=None, remote=None)
# update_many(data=[<list of objects with id and data>], otype=None, project_id=None, experiment_id=None, remote=None)
#
#
# relationships
#
# get_relationship_models(remote=None)
# create_relationship(subject_id, relationship_type, object_id, subject_otype=None, object_otype=None, project_id=None, experiment_id=None, remote=None)
# delete_relationships(
#   relationship_type=None,
#   subject_id=None,
#   subject_type=None,
#   object_id=None,
#   object_type=None,
#   project_id=None, experiment_id=None, remote=None) -> delete all matching
# get_relationships(
#   relationship_type=None,
#   subject_id=None,
#   subject_type=None,
#   object_id=None,
#   object_type=None,
#   project_id=None, experiment_id=None, remote=None) -> return all matching
#
#
# # selections: also uses object 'create', 'get', etc.
#
# select(selection_id, stype=None, project_id=None, experiment_id=None, remote=None)
#   -> returns an iterable of objects that were selected
#
# # datasets
#
# get_all_datasets_from_remote(remote=None)
# get_all_datasets_from_project(project_id, remote=None)
# download_dataset_zipfile(dataset_id, output_file_path, remote=None)
# unpublish_dataset(dataset_id, project_id=None, remote=None)
# publish_dataset(dataset_id, project_id=None, remote=None)
# publish_private_dataset(dataset_id, project_id=None, remote=None)


### Not API calls ###

#
# # config
# config = Config(path=None)
#
# # remotes
# print_known_remotes()
# add_remote(username, mcurl, config)
#
# remote = Remote(remote_config=None)
#
# # local projects
# init_project(name, description, prefix=None, remote=None)
# clone_project(id, prefix=None, remote=None)
# project_path(path=None)
# project_exists(path=None)
# pconfig = ProjectConfig(project_path)
# read_project_config(path=None)
# make_local_project_remote(path=None)
# make_local_project(path=None)
# make_local_expt(proj)
#
# # files & directories
# #   standard_download, globus_download
# #   standard_upload, globus_upload
# #   treecompare, mkdir, remove, move,
