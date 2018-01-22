#!/usr/bin/env bash

# no-output on pushd and popd
pushd () {
    command pushd "$@" > /dev/null
}

popd () {
    command popd "$@" > /dev/null
}

set_locations() {
    # location of this script: extras/scripts/io_regression_test
    SCRIPTS="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
    pushd ${SCRIPTS}
    BASE="$( cd ../../../ && pwd )"
    popd
}

set_locations

echo "SCRIPTS = $SCRIPTS"
echo "BASE = $BASE"

pushd ${BASE}

input=${SCRIPTS}/input.xlsx
output=${SCRIPTS}/workflow.xlsx
metadata=${SCRIPTS}/metadata.json

filename=${SCRIPTS}/Generic\ ETL\ Test\ 1.xlsx
echo "-------------- input file = $filename"
cp "$filename" ${input}

echo "-- input"
python -m materials_commons.etl.input.main --input ${input} --metadata ${metadata}
echo "-- output"
python -m materials_commons.etl.output.extract_spreadsheet --metadata ${metadata} --file ${output}
echo "-- compare"
python -m materials_commons.etl.output.compare_spreadsheets --base ${SCRIPTS}
echo "-- done"

popd