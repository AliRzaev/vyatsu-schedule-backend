import click
from flask import Flask
from flask.cli import with_appcontext

import utils.university
from utils.extractors import *
from utils.repository import get_repository


def prefetch(force=False):
    groups = extract_groups(utils.university.get_groups_page())
    groups_date_ranges = extract_date_ranges(utils.university.get_groups_page())

    get_repository().update_groups_info(groups, groups_date_ranges, force)

    departments = extract_departments(utils.university.get_departments_page())
    departments_date_ranges = extract_departments_date_ranges(
        utils.university.get_departments_page()
    )

    get_repository().update_departments_info(
        departments, departments_date_ranges, force
    )

    return len(groups), len(departments)


def init_app(app: Flask):
    @click.command('prefetch')
    @click.option(
        '--force',
        is_flag=True,
        flag_value=True,
        help='Prefetch information even if it already exists'
    )
    @with_appcontext
    def prefetch_command(force):
        prefetch(force)

    app.cli.add_command(prefetch_command)
