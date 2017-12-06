from materials_commons.api import create_project, get_all_templates


class BuildProjectExperiment:
    def __init__(self):
        self._make_template_table()
        self.description = "Project from excel spreadsheet"
        self.source = self.data_start_row = self.project = self.experiment = None
        self.data_start_row = self.data_path = None
        self.parent_process_list = None
        self.previous_row_key = None
        self.previous_parent_process = None

    def build(self, data_path):

        self.data_path = data_path

        if not self._set_project_and_experiment():
            return

        self._set_row_positions()
        self._set_col_positions()

        self.sweep()

        print("Created project:", self.project.name)
        print("With Experiment", self.experiment.name, self.experiment.id)

    def sweep(self):
        process_list = self._scan_for_process_descriptions()
        if len(process_list) == 0:
            print("No complete processes found in project")
        self.parent_process_list = []
        for index in range(self.data_start_row, len(self.source)):
            self.parent_process_list.append(None)
        self.previous_row_key = None
        self.previous_parent_process = None
        for proc_data in process_list:
            self.sweep_process(proc_data)

    def sweep_process(self, proc_data):
        start_col_index = proc_data['start_col']
        end_col_index = proc_data['end_col']
        template_id = proc_data['template']
        name = proc_data['name']
        start_attribute_row_index = self._determine_start_attribute_row(start_col_index)

        # print(start_col_index, end_col_index, template_id, name)
        # print(start_attribute_row_index, self.header_end_row)

        process_record = None

        for row_index in range(self.data_start_row, len(self.source)):
            row_key = self._row_key(row_index, start_col_index, end_col_index)
            if not row_key:
                self.previous_row_key = None
                print("skipping", row_index, template_id)
                continue
            process_index = row_index - self.data_start_row
            parent_process_record = self.parent_process_list[process_index]
            # print (row_index, "parent_process_record: ", parent_process_record)
            parent_process = None
            if parent_process_record:
                parent_process = parent_process_record['process']
            if self._start_new_process(row_key, parent_process):
                print("==============================================================")
                print("Start new process:", name)
                process = self.experiment.create_process_from_template(template_id)
                output_sample = None
                if process.process_type == 'create':
                    sample_names = [row_key]
                    samples = process.create_samples(sample_names=sample_names)
                    output_sample = samples[0]
                elif process.process_type == 'transform' and parent_process_record:
                    input_sample = parent_process_record['output_sample']
                    process = process.add_input_samples_to_process([input_sample]) \
                        .decorate_with_output_samples()
                    output_sample = process.output_samples[0]
                elif (process.process_type == 'measurement' or process.process_type == 'measurement') \
                        and parent_process_record:
                    input_sample = parent_process_record['output_sample']
                    process.add_input_samples_to_process([input_sample])
                process_record = {
                    'key': row_key,
                    'process': process,
                    'output_sample': output_sample
                }
                self.sweep_for_process_value(
                    row_index, process,
                    start_col_index, end_col_index,
                    start_attribute_row_index, self.header_end_row)

            self.previous_row_key = row_key
            self.previous_parent_process = None
            if parent_process_record:
                self.previous_parent_process = parent_process_record['process']
            self.parent_process_list[process_index] = process_record

    def sweep_for_process_value(self, data_row, process, start_col, end_col, start_attr_row, end_attr_row):
        self.clear_params_and_measurement()
        for col in range(start_col, end_col):
            type = self.source[start_attr_row][col]
            signature = self.source[start_attr_row + 1][col]
            if type == 'PARAM' or type == 'MEAS':
                value = self.source[data_row][col]
                self.collect_params_and_measurement(type, value, process, signature)
        self.set_params_and_measurement()

    def clear_params_and_measurement(self):
        self.process_values = {
            "PARAM": {},
            "MEAS": {}
        }

    def collect_params_and_measurement(self, type, value, process, signature):
        unit = None
        index = signature.find('(')
        if index > -1:
            end = signature.find(')')
            if end > -1 and end > index:
                unit = signature[index + 1:end]
            signature = signature[:index]
        signature = signature.strip()
        parts = signature.split('.')
        print("collect: ", type, parts, value, unit, process.name)
        entry = self.process_values[type]
        attribute = parts[0]
        if not attribute in entry:
            entry[attribute] = {}
        print(self.process_values)

    def set_params_and_measurement(self):
        # parameters
        for entry in self.process_values["PARAM"]:
            print("Set parameters for entry: ", entry)
        # measurements
        for entry in self.process_values["MEAS"]:
            print("Set measurements for entry: ", entry)

    def read_entire_sheet(self, sheet):
        data = []
        for row in sheet.iter_rows():
            empty_row = True
            values = []
            for cell in row:
                empty_row = empty_row and cell.value
            if empty_row:
                print("encountered empty row at row_index = " + str(len(data)) + ".  " +
                      "Assuming end of data at this location")
                break
            for cell in row:
                value = cell.value
                if value and (str(value).strip() == "" or ("n/a" in str(value).strip())):
                    value = None
                values.append(value)
            data.append(values)
        self.source = data

    def set_description(self, description):
        self.description = description

    # helper methods

    def _set_project_and_experiment(self):
        self._set_names()
        if self.project_name:
            print("Project name: ", self.project_name)
        else:
            print("No project name found; check format. Quiting.")
            return False

        if self.experiment_name:
            print("Experiment name:", self.experiment_name)
        else:
            print("No experiment name found; check format. Quiting.")
            return False

        self.project = create_project(self.project_name, self.description)
        self.experiment = self.project.create_experiment(self.experiment_name, "")
        return True

    def _scan_for_process_descriptions(self):
        col_index = self.start_sweep_col
        process_list = []
        previous_process = None
        while col_index < self.end_sweep_col:
            process_entry = self.source[0][col_index]
            if process_entry and str(process_entry).startswith("PROC:"):
                if previous_process:
                    previous_process['end_col'] = col_index
                    process_list.append(previous_process)
                    previous_process = None
                process_entry = self._prune_entry(process_entry, "PROC:")
                template_id = self._get_template_id_for(process_entry)
                if template_id:
                    previous_process = {
                        'name': process_entry,
                        'start_col': col_index,
                        'template': template_id
                    }
                else:
                    print("process entry has not corresponding template:", process_entry)
            col_index += 1
        if previous_process:
            previous_process['end_col'] = col_index
            process_list.append(previous_process)
        return process_list

    def _determine_start_attribute_row(self, start_col_index):
        start_attribute_row_index = 2
        for row in range(1, self.header_end_row):
            entry = str(self.source[row][start_col_index])
            if entry.startswith('DUPLICATES_ARE_IDENTICAL'):
                print("Encountered 'DUPLICATES_ARE_IDENTICAL' - ignored as this is the default behaivor")
            if entry.startswith('ATTR_'):
                print("Encountered '" + entry + "' - ignored, not implemented")
            if entry.startswith("NOTE") \
                    or entry.startswith("NO_UPLOAD") \
                    or entry.startswith("MEAS") \
                    or entry.startswith("PARAM"):
                start_attribute_row_index = row
        return start_attribute_row_index

    def _start_new_process(self, row_key, parent_process):
        if parent_process and self.previous_parent_process \
                and parent_process.id != self.previous_parent_process.id:
            return True
        return (row_key != self.previous_row_key)

    @staticmethod
    def _prune_entry(entry, prefix):
        entry = str(entry)
        if entry.startswith(prefix):
            entry = entry[len(prefix):].strip(" ").strip("'").strip('"')
        else:
            entry = None
        return entry

    def _set_names(self):
        self.project_name = self._prune_entry(self.source[0][0], "PROJ:")
        self.experiment_name = self._prune_entry(self.source[1][0], "EXP:")

    def _set_row_positions(self):
        self.header_end_row = 0
        self.data_start_row = 0
        index = 0
        for row in self.source:
            if len(row) > 0 and row[0] and row[0].startswith("BEGIN_DATA"):
                self.data_start_row = index
                break
            index += 1
        if self.data_start_row == 0:
            return
        index = 0
        for row in self.source:
            if len(row) > 0 and row[0] \
                    and (row[0].startswith("BEGIN_DATA") or row[0].startswith("COL_LABEL")):
                self.header_end_row = index
                break
            index += 1

    def _set_col_positions(self):
        self.start_sweep_col = 1
        self.end_sweep_col = 0
        first_row = self.source[0]
        index = 0
        for col in first_row:
            if str(col).startswith("END"):
                self.end_sweep_col = index
                break
            index += 1

    def _row_key(self, row_index, start_col_index, end_col_index):
        row_key = None
        for col in range(start_col_index, end_col_index):
            probe = self.source[row_index][col]
            if probe and row_key:
                row_key += " -- " + str(probe)
            elif probe:
                row_key = str(probe)
        return row_key

    def _make_template_table(self):
        template_list = get_all_templates()
        table = {}
        for template in template_list:
            table[template.id] = template
        self.template_table = table

    def _get_template_id_for(self, match):
        found_id = None
        for key in self.template_table:
            if match in key:
                found_id = key
        return found_id
