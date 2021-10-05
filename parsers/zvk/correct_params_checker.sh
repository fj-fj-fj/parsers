#!/bin/bash

# This script reads all files without a digital
# prefix and makes a request using `curl`.
# Page with correct parameters contains
# "bx-filter-param-label disabled" classes.
# Also page with incorrect contains JavaScript
# with "filter/clear" in "SEF_SET_FILTER_URL" key
# (see comments below the code).
# Script uses the second case.
# If "SEF_SET_FILTER_URL" is equivalent to "SEF_DEL_FILTER_URL",
# replace the last `-` with `-is-`
# (e.g., path/param-foo -> path/param-is-foo).
# Links with valid parameters, as well as modified ones,
# are added to the `ALL_PARSED_CHECKED`.

SELF=$(readlink -f "${BASH_SOURCE[0]}")
BASENAME=$(basename "$SELF")
PARENT_PATH=$(dirname "$SELF")
PARSER_DIR="$PARENT_PATH/data/"
ALL_PARSED_CHECKED="$PARSER_DIR/_all_parsed_1"

date
echo "$BASENAME is starting ..."

for file in "$PARSER_DIR"**/*; do
    if [[ $file == *_[0-9] ]]; then
        continue
    fi
    for url in $(cat $file); do

        js_chunk=$(curl $url | egrep -oi '(\{.SEF_SET_FILTER_URL.*\})')
        bad_params=$(python3 -c "print( len( set( dict($js_chunk).values() ) ) != 2 )")

        if [[ $bad_params == 'True' ]]; then
            echo "$url is not correct"
            echo $url | sed 's/\(.*\)-/\1-is-/' >> "$ALL_PARSED_CHECKED"
        else
            echo "$url is correct"
            echo $url >> "$ALL_PARSED_CHECKED"
        fi
    done < $file
done

echo "Program finished."
date

# ---------------------------------------------------------------------------------------------------
# $ curl https://zvk.ru/catalog/orgtekhnika/kopiry-mfu/filter/maksimalnoe_razreshenie_chb_pechati-is-ypotqyld/ > correct
# $ curl https://zvk.ru/catalog/orgtekhnika/kopiry-mfu/filter/maksimalnoe_razreshenie_chb_pechati-ypotqyld/ > incorrect
# $ diff correct incorrect
# ...
# <  <label ... class="bx-filter-param-label disabled" ...
# ---
# >  <label ... class="bx-filter-param-label " ...
# ...
# <  var smartFilter = ... 'SEF_SET_FILTER_URL':'/catalog/orgtekhnika/kopiry-mfu/filter/maksimalnoe_razreshenie_chb_pechati-is-ypotqyld/' ...
# ---
# >  var smartFilter = ... 'SEF_SET_FILTER_URL':'/catalog/orgtekhnika/kopiry-mfu/filter/clear/' ...
# ...
# ---------------------------------------------------------------------------------------------------
