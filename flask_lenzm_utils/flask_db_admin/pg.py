"""click interface for postgresql commands.

"""
import logging
import os
import subprocess

import click
from flask import current_app

DEFAULT_DB_BACKUP_PATH = 'db.pg_dump'

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

cli = click.Group(help=__doc__, name='pg')


@cli.command()
@click.option('-l', '--location', default=DEFAULT_DB_BACKUP_PATH)
@click.option('--format', default='c')
def dump(location, format):
	'''Run pg_dump.'''
	os.environ['PGPASSWORD'] = current_app.config['PG_PASSWORD']
	# /usr/pgsql-9.3/bin/pg_dump -Fd analytics -f analytics-dump --username=analytics
	pg_dump = current_app.config['PG_BIN_DIR'] + 'pg_dump'
	subprocess.call((
		pg_dump,
		'--host={}'.format(current_app.config['PG_HOST']),
		'--username={}'.format(current_app.config['PG_USERNAME']),
		'--format=%s' % format,
		current_app.config['PG_DB_NAME'],
		'--file=%s' % location,
		))


@cli.command()
@click.option('-l', '--location', default=DEFAULT_DB_BACKUP_PATH)
def restore(location):
	'''Restore pg_dump.'''
	os.environ['PGPASSWORD'] = current_app.config['PG_PASSWORD']
	# pg_restore -h localhost -U analytics -d analytics --clean db-backup/
	pg_restore = current_app.config['PG_BIN_DIR'] + 'pg_restore'
	subprocess.call((
		pg_restore,
		'--host={}'.format(current_app.config['PG_HOST']),
		'--username={}'.format(current_app.config['PG_USERNAME']),
		'--dbname={}'.format(current_app.config['PG_DB_NAME']),
		'--clean',
		location,
		))
