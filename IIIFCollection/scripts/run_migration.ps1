cd c:\Users\Floyd\IIIFCollection
python tgm_migration.py | Tee-Object -FilePath migration_output.txt
Get-Content migration_output.txt
