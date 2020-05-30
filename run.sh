#!/bin/bash
# Bash stuff
BOLD=$(tput bold)
NORMAL=$(tput sgr0)

HEADLESS=0
CSV="$PWD/TimesRichList2020.csv"

while :; do
  case $1 in
    -h|--help) echo "usage: $0 [-h prints this message] [--headless means Python will hide Selenium]
                               [--csv name of csv to save to]"; exit ;;
    --headless)
      HEADLESS=1 ;;
    --csv)
        if [ "$2" ]; then
          NAME=${2//".csv"}
          CSV="$PWD/$NAME.csv"
          shift
        fi ;;
    --)
        shift
        break
        ;;
    -?*)
        printf 'WARN: Unknown option (ignored): %s\n' "$1" >&2
        ;;
    *)
        break
        ;;
  esac
  shift
done

if [ $HEADLESS -eq 1 ]; then
    echo "${BOLD}Running Selenium in headless mode${NORMAL}"
fi

echo "${BOLD}Saving to csv" $CSV

python3 ScrapeData.py
