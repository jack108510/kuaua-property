-- Keep confirmed requests and public availability in sync.
-- Run on Supabase project xacehhtgvubcqdoltazg after the admin auth migration.

begin;

-- The guest form stores a display string. Parse both the calendar format
-- ("Dec 27 – Jan 5, 2027") and the suggested typed format
-- ("Aug 10 – 20, 2026"). End dates are inclusive on the site.
create or replace function public.wilde_maui_booking_range(raw_dates text)
returns daterange
language plpgsql
immutable
as $$
declare
  parts text[];
  months text[] := array['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  start_month integer;
  end_month integer;
  start_day integer;
  end_day integer;
  start_year integer;
  end_year integer;
  start_date date;
  end_date date;
begin
  parts := regexp_match(trim(raw_dates),
    '^([A-Za-z]{3})[[:space:]]+([0-9]{1,2})[[:space:]]*[–-][[:space:]]*([A-Za-z]{3})[[:space:]]+([0-9]{1,2}),[[:space:]]*([0-9]{4})$');
  if parts is not null then
    start_month := array_position(months, initcap(lower(parts[1])));
    start_day := parts[2]::integer;
    end_month := array_position(months, initcap(lower(parts[3])));
    end_day := parts[4]::integer;
    end_year := parts[5]::integer;
  else
    parts := regexp_match(trim(raw_dates),
      '^([A-Za-z]{3})[[:space:]]+([0-9]{1,2})[[:space:]]*[–-][[:space:]]*([0-9]{1,2}),[[:space:]]*([0-9]{4})$');
    if parts is null then
      raise exception 'Choose a date range on the calendar before confirming this request.';
    end if;
    start_month := array_position(months, initcap(lower(parts[1])));
    start_day := parts[2]::integer;
    end_month := start_month;
    end_day := parts[3]::integer;
    end_year := parts[4]::integer;
  end if;

  if start_month is null or end_month is null then
    raise exception 'Unrecognized month in booking dates: %', raw_dates;
  end if;
  start_year := end_year;
  if start_month > end_month or (start_month = end_month and start_day > end_day) then
    start_year := end_year - 1;
  end if;
  start_date := make_date(start_year, start_month, start_day);
  end_date := make_date(end_year, end_month, end_day);
  if start_date > end_date then
    raise exception 'Invalid booking date range: %', raw_dates;
  end if;
  return daterange(start_date, end_date + 1, '[)');
end;
$$;

create or replace function public.wilde_maui_sync_confirmed_booking()
returns trigger
language plpgsql
security definer
set search_path = public, pg_temp
as $$
declare
  booked daterange;
begin
  if tg_op = 'DELETE' then
    delete from public.blocked_ranges
      where id = old.id and label = 'Confirmed booking';
    return old;
  end if;

  if new.status = 'confirmed' then
    booked := public.wilde_maui_booking_range(new.dates);
    insert into public.blocked_ranges (id, from_date, to_date, label)
      values (new.id, lower(booked), upper(booked) - 1, 'Confirmed booking')
      on conflict (id) do update
      set from_date = excluded.from_date,
          to_date = excluded.to_date,
          label = excluded.label;
  else
    delete from public.blocked_ranges
      where id = new.id and label = 'Confirmed booking';
  end if;
  return new;
end;
$$;

revoke execute on function public.wilde_maui_sync_confirmed_booking() from public, anon, authenticated;

drop trigger if exists wilde_maui_sync_confirmed_booking on public.stay_requests;
create trigger wilde_maui_sync_confirmed_booking
after insert or update or delete on public.stay_requests
for each row execute function public.wilde_maui_sync_confirmed_booking();

-- Guests may create requests, while only the designated admin can directly
-- record a confirmed booking.
drop policy if exists wilde_maui_public_request_insert on public.stay_requests;
create policy wilde_maui_public_request_insert on public.stay_requests
  for insert to anon, authenticated
  with check (status = 'new' or auth.uid() = '45717c8c-08f9-469f-bf7d-2fa2ef5ad441'::uuid);

-- Existing confirmed requests need reservations too. The generated ranges
-- share their request IDs, so future status changes clean them up atomically.
insert into public.blocked_ranges (id, from_date, to_date, label)
select id,
       lower(public.wilde_maui_booking_range(dates)),
       upper(public.wilde_maui_booking_range(dates)) - 1,
       'Confirmed booking'
from public.stay_requests
where status = 'confirmed'
on conflict (id) do update
set from_date = excluded.from_date,
    to_date = excluded.to_date,
    label = excluded.label;

commit;
