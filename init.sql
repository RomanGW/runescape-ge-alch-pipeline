-- Create initial table to hold the data.
create table ge_alch (
	item text,
	price numeric,
	high_alch numeric,
	low_alch numeric
);

-- Refresh GE values.
create procedure update_ge_values()
language plpgsql
as $$ 
begin 
	-- Erase previous data in ge_alch.
	truncate ge_alch;
	
	-- Copy the new ge.csv over the old ge.csv.
	copy ge_alch(item, price, high_alch, low_alch)
	from '..\global\path\to\data\ge.csv' -- !!INSERT THE GLOBAL PATH TO data\ge.csv HERE!!
	delimiter ','
	csv header;
end;
$$;

call update_ge_values();

create function get_highest_alch_ratio()
returns table(ItemName text, ItemPrice numeric, HighAlch numeric, AlchRatio numeric) as $$
begin
	return query
	
	-- Select the most profitable 100 rows based on high alchemy to price ratio.
	select item, price, high_alch, round(high_alch / price, 4) as alch_ratio from ge_alch
	-- Check that the item can be alched, and that there's a positive return if so.
	where (price, high_alch) is not null and (high_alch / price) > 1 
	order by alch_ratio desc;
end;
$$ language plpgsql;

create function get_most_coins_on_alch()
returns table (ItemName text, ItemPrice numeric, CoinsEarned numeric) as $$
begin
	return query
	
	-- Select the most profitable rows based on the amount of GP made by alching.
	select item, price, (high_alch - price) as coins_earned from ge_alch
	where (price, high_alch) is not null
	order by coins_earned desc;
end;
$$ language plpgsql;

create function get_alch_value(item_look text)
returns table (GEPrice numeric, AlchValue numeric, NetAmount numeric) as $$
begin
	return query

	-- Find item in table and return the buy price, alchemy return, and the net amount gained from alching.
	select price, high_alch, (high_alch - price) as net_amt from ge_alch
	where item = item_look;
end;
$$ language plpgsql;

-- Finally, call get_most_coins_on_alch to display the top dollar items.
select * from get_most_coins_on_alch()
limit 100