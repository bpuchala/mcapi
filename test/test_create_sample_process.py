# add a sample to the experiment with a create sample process (*)
# http://mctest.localhost/api/v2/projects/80f7991c-df55-4eee-b2c0-e455e26bd34a/experiments/4e170b90-069f-4205-a4bb-dc02d3f00654/processes/templates/global_Create%20Samples?apikey=949045af40e942b69f5b32d15b0fb8e5
# POST with data {id: "global_Create Samples"}
# --> returns process
# http://mctest.localhost/api/v2/projects/80f7991c-df55-4eee-b2c0-e455e26bd34a/samples?apikey=949045af40e942b69f5b32d15b0fb8e5
# POST with data {process_id: "d12be2fb-cb04-4948-9031-3817c344e956", samples: [{name: "Sample Name"}]}
# --> returns samples
# http://mctest.localhost/api/v2/projects/80f7991c-df55-4eee-b2c0-e455e26bd34a/experiments/a831c0b1-6185-4a63-a6c4-89caaec83a57/samples?apikey=949045af40e942b69f5b32d15b0fb8e5
# PUT with data {process_id: "d12be2fb-cb04-4948-9031-3817c344e956", samples: [{id: "d9be4d95-27db-4024-9523-95d8fd12473b", name: "Sample"}]
### need to expand steps for creating process properties !!!
# template_id = "global_Create Samples"
# process = create_process_from_template(project_id, experiment_id,template_id)
# process_id = process["id"]
# sample_names = ["Sample A"]
# samples = create_samples(project_id,process_id,sample_names)
# sample_ids = [sample["id"] for sample in samples["samples"] ]
# ids_list = add_samples_to_process(project_id,experiment_id,process_id,sample_ids)
# ids = ids_list[0]
# experiment_id = ids['experiment_id']
# sample_id = ids['sample_id']
# print "experiment_id", experiment_id
# print "sample_id", sample_id
# sys.stdout.flush()
