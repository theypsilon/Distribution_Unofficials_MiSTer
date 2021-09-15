#!/usr/bin/env bash
# Copyright (c) 2021 José Manuel Barroso Galindo <theypsilon@gmail.com>

set -euo pipefail

curl -o /tmp/update_distribution.source "https://raw.githubusercontent.com/MiSTer-devel/Distribution_MiSTermain/.github/update_distribution.sh"

source /tmp/update_distribution.source
rm /tmp/update_distribution.source

update_distribution() {
    local OUTPUT_FOLDER="${1}"
    local PUSH_COMMAND="${2:-}"

    process_url "https://github.com/Kyp069/zx48-MiSTer" _Computer "${OUTPUT_FOLDER}"
    process_url "https://github.com/MrX-8B/MiSTer-Arcade-PenguinKunWars" _Arcade "${OUTPUT_FOLDER}"

    if [[ "${PUSH_COMMAND}" == "--push" ]] ; then
        git checkout -f develop -b main 
        git add "${OUTPUT_FOLDER}"
        git commit -m "-"
        git fetch origin main || true
        if ! git diff --exit-code main origin/main^ ; then
            export DB_ID="${DB_ID}"
            export DB_URL="${DB_URL}"
            export BASE_FILES_URL="${BASE_FILES_URL}"
            export LATEST_ZIP_URL="${LATEST_ZIP_URL}"

            echo
            echo "There are changes to push."
            echo

            ./.github/calculate_db.py
        else
            echo "Nothing to be updated."
        fi
    fi
}

if [[ "${BASH_SOURCE[0]}" == "${0}" ]] ; then
    update_distribution "${1}" "${2:-}"
fi
