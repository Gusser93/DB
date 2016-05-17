select Name
from Professoren
where PersNr not in ( 	select gelesenVon
										from Vorlesungen);