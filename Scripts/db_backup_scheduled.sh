#!/bin/bash
#
# Backup bigdata database into a montly file.
#

BACKUP_DIR=/bigdata/dbbackup/backups
DAYS_TO_KEEP=3
FILE_PREFIX=bigdata
DATABASE=bigdata
USER=postgres

FILE=${FILE_PREFIX}_$(date +"%m%d%Y").sql
OUTPUT_FILE=${BACKUP_DIR}/${FILE}

/usr/pgsql-12/bin/pg_dump -U ${USER} ${DATABASE} -F p -f ${OUTPUT_FILE}

# show the created backup file
echo "${OUTPUT_FILE} is created:"

# remove old backups
find $BACKUP_DIR -maxdepth 1 -mtime +$DAYS_TO_KEEP -name "${FILE_PREFIX}*" -exec rm -rf '{}' ';'
