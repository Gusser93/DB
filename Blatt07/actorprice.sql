create view actorprice as
	select Firstnam, Lastnam, avg(Price)
	from Person 
		natural join acts 
		natural join screening
	group by PersonId