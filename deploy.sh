#!/bin/bash
# Build and deploy scottwillsey.com to production.
# The deploy step is the same rsync script the Astro site used.

set -e
cd "$(dirname "$0")"

./build.sh
~/Scripts/Sites/scottwillsey/update-site/update-site.sh
