# data/raw — DO NOT EDIT

`SITE_DASHBOARD.csv` is the original, untouched HRSA site export for all clinic data.

- 129,141 rows x 18 columns (last column is an empty trailing field from the export)
- Includes every site category (FQHC service delivery sites, look-alikes, CMS, NHSC, Rural Health Clinics, VA, Ryan White, etc.), not just FQHCs
- Never modify this file. Anything cleaned, filtered, or enriched goes in `data/processed/` and is produced by a script that reads from here.
- Integrity check: `sha256sum -c SITE_DASHBOARD.csv.sha256`
