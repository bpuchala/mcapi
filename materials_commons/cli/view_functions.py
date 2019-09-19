

# def view_sample(samp, shift=0, indent=2, out=sys.stdout):
#     PrettyPrint pp(shift=shift, indent=indent, out=out)
#     pp.write("Sample: " + pp.str(samp.name))
#     pp.write("id: " + pp.str(self.id))
#
#     sample
#     sample_states
#     sample_attributes:
#       sort by: initial_state, final_state
#
#     sample = {
#         "name": <name>,
#         "id": <id>,
#         "relationships": [
#             {
#                 "rtype": "hasInitialState"
#             },
#             "
#         ]
#     }
#
#     sample_states = [
#         {
#             "name": <name>,
#             "id": <id>,
#             "relationships": [
#                 {
#                     "rtype": "wasCreatedby",
#                     "subject_otype": "process",
#                     "subject_name": <name>,
#                     "subject_id": <id>
#                 },
#                 {
#                     "rtype": "wasUsedby",
#                     "subject_otype": "process",
#                     "subject_name": <name>,
#                     "subject_id": <id>
#                 },
#                 {
#                     "rtype": "wasTransformedby",
#                     "subject_otype": "process",
#                     "subject_name": <name>,
#                     "subject_id": <id>
#                 },
#                 {
#                     "rtype": "wasTransformedTo",
#                     "subject_otype": "sample_state",
#                     "subject_name": <name>,
#                     "subject_id": <id>
#                 },
#                 {
#                     "rtype": "isInitialStateOf",
#                     "subject_otype": "sample_state",
#                     "subject_name": <name>,
#                     "subject_id": <id>
#                 },
#             ]
#         },
#         ...
#     ]
#
#     sample_attributes = [
#         {
#             "name": <name>,
#             "id": <id>,
#             "relationships": [
#                 {
#                     "rtype": "isAttributeOf",
#                     "subject_otype": "sample_state",
#                     "subject_name": <name>,
#                     "subject_id": <id>
#                 },
#                 {
#                     "rtype": "wasCreatedBy",
#                     "subject_otype": "sample_state",
#                     "subject_name": <name>,
#                     "subject_id": <id>
#                 },
#                 {
#                     "rtype": "wasTransformedBy",
#                     "subject_otype": "sample_state",
#                     "subject_name": <name>,
#                     "subject_id": <id>
#                 },
#             ]
#         }
#     }
