select p.Name
from Professoren p
where not exists (	select *
								from Vorlesungen v
								where v.gelesenVon = p.PersNr);