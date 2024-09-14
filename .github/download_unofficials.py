#!/usr/bin/env python3
# Copyright (c) 2022 José Manuel Barroso Galindo <theypsilon@gmail.com>
import csv
import subprocess
from pathlib import Path
try:
    import httpimport
except ImportError as _:
    subprocess.run(['python3', '-m', 'pip', 'install', 'requests', 'httpimport==1.3.1'])
    import httpimport

download_distribution = httpimport.load('download_distribution', 'https://raw.githubusercontent.com/MiSTer-devel/Distribution_MiSTer/develop/.github')

target = download_distribution.read_target_dir()
metadata_props = download_distribution.Metadata.new_props()
delme = subprocess.run(['mktemp', '-d'], shell=False, stderr=subprocess.STDOUT, stdout=subprocess.PIPE).stdout.decode().strip()

def extra_content(url, kind):
    try:
        download_distribution.process_extra_content(url, kind, delme, target)
    except Exception as e:
        print(e)

def core(props):
    try:
        download_distribution.process_core(props, delme, target, metadata_props)
    except Exception as e:
        print(e)

with open('external_mister_repos.csv', "r") as file:
    csv_reader = csv.reader(file)
    for row_number, row in enumerate(csv_reader):
        if row_number == 0: continue
        print('row: ' + str(row_number), row)
        try:
            url, category = row[0].strip(), row[1].strip()
        except ValueError as e:
            print(f"Error processing row {row_number}: {e}")
            continue

        name = Path(url).name

        if category.lower() == '_arcade':
            core({'name': name, 'url': url, 'category': '_Arcade'})
            extra_content(url, 'user-content-mra-alternatives-under-releases')
            continue

        try:
            home = row[2].strip()
        except ValueError as e:
            print(f"No 'home' column on row {row_number}: {e}")
            continue

        core({'name': name, 'url': url, 'home': home, 'category': category})
