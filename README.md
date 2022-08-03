# MutSpecSerenaOld
This is the old code for processing Serena's archive

The script changes the name of the files in the MutSpecSerena-master \ body \ 1raw \ MtMutectAnnovar folder (adding an agent before the name).

All renamed files go to MutSpecSerena-master \ body \ 1raw \ MtMutectAnnovar \ renamed .

The results are processed by counting single substitutions, where samples with the same agent are summed up.

The result is placed in the root folder MutSpecSerena-master.

The script works only on the downloaded archive, you need to rename the path to the target folder with the archive.

GitHub сontains a modified file treatment_mapped_to_kostya_files.csv, in which the column division format has been changed: instead of "," is used ";" , since the name of the agents contains this sign. This change is necessary to add a column division condition. Added indication of mutagens for empty lines.
