#!/bin/bash

# Dump data that should be suitable for running a dev environment

DUMP_COMMAND="django-admin dumpdata"
DUMP_SETTINGS="--indent=4 --natural-primary --natural-foreign"
PROJECT_DIR="livinglotsphilly"

mkdir -p $PROJECT_DIR/cms/fixtures
$DUMP_COMMAND elephantblog page medialibrary $DUMP_SETTINGS > $PROJECT_DIR/cms/fixtures/dev_cms.json

mkdir -p $PROJECT_DIR/lots/fixtures
$DUMP_COMMAND lots $DUMP_SETTINGS > $PROJECT_DIR/lots/fixtures/dev_lots.json
$DUMP_COMMAND files $DUMP_SETTINGS > $PROJECT_DIR/lots/fixtures/dev_files.json
$DUMP_COMMAND notes $DUMP_SETTINGS > $PROJECT_DIR/lots/fixtures/dev_notes.json
$DUMP_COMMAND photos $DUMP_SETTINGS > $PROJECT_DIR/lots/fixtures/dev_photos.json
$DUMP_COMMAND actstream $DUMP_SETTINGS > $PROJECT_DIR/lots/fixtures/dev_actstream.json

mkdir -p $PROJECT_DIR/pathways/fixtures
$DUMP_COMMAND pathways $DUMP_SETTINGS > $PROJECT_DIR/pathways/fixtures/dev_pathways.json

mkdir -p $PROJECT_DIR/steward/fixtures
$DUMP_COMMAND steward $DUMP_SETTINGS > $PROJECT_DIR/steward/fixtures/dev_steward.json

mkdir -p $PROJECT_DIR/phillyorganize/fixtures
$DUMP_COMMAND organize phillyorganize $DUMP_SETTINGS > $PROJECT_DIR/phillyorganize/fixtures/dev_phillyorganize.json

# Export django-phillydata fixtures
mkdir -p $PROJECT_DIR/phillydata_local/fixtures
$DUMP_COMMAND opa $DUMP_SETTINGS > $PROJECT_DIR/phillydata_local/fixtures/dev_opa.json
$DUMP_COMMAND owners $DUMP_SETTINGS > $PROJECT_DIR/phillydata_local/fixtures/dev_owners.json
$DUMP_COMMAND violations $DUMP_SETTINGS > $PROJECT_DIR/phillydata_local/fixtures/dev_violations.json
