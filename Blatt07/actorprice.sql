create view actorprice as
	select Person.Firstname, Person.Lastname, avg(screening.Price)
	from Person natural join acts natural join screening
	group by Person.PersonId