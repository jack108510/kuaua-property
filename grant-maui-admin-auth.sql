-- Wilde Maui /admin. Apply to Supabase project xacehhtgvubcqdoltazg.
-- Keep public requests and availability reads working; restrict private
-- request records and all management writes to the designated Auth user.

begin;

grant select, insert, update, delete on public.stay_requests to anon, authenticated;
grant select, insert, update, delete on public.blocked_ranges to anon, authenticated;

drop policy if exists allow_all_anon_requests on public.stay_requests;
drop policy if exists wilde_maui_public_request_insert on public.stay_requests;
create policy wilde_maui_public_request_insert on public.stay_requests
  for insert to anon, authenticated with check (true);

drop policy if exists wilde_maui_admin_request_read on public.stay_requests;
create policy wilde_maui_admin_request_read on public.stay_requests
  for select to authenticated
  using (auth.uid() = '45717c8c-08f9-469f-bf7d-2fa2ef5ad441'::uuid);

drop policy if exists wilde_maui_admin_request_update on public.stay_requests;
create policy wilde_maui_admin_request_update on public.stay_requests
  for update to authenticated
  using (auth.uid() = '45717c8c-08f9-469f-bf7d-2fa2ef5ad441'::uuid)
  with check (auth.uid() = '45717c8c-08f9-469f-bf7d-2fa2ef5ad441'::uuid);

drop policy if exists wilde_maui_admin_request_delete on public.stay_requests;
create policy wilde_maui_admin_request_delete on public.stay_requests
  for delete to authenticated
  using (auth.uid() = '45717c8c-08f9-469f-bf7d-2fa2ef5ad441'::uuid);

drop policy if exists allow_all_anon_blocked on public.blocked_ranges;
drop policy if exists wilde_maui_public_availability_read on public.blocked_ranges;
create policy wilde_maui_public_availability_read on public.blocked_ranges
  for select to anon, authenticated using (true);

drop policy if exists wilde_maui_admin_blocked_insert on public.blocked_ranges;
create policy wilde_maui_admin_blocked_insert on public.blocked_ranges
  for insert to authenticated
  with check (auth.uid() = '45717c8c-08f9-469f-bf7d-2fa2ef5ad441'::uuid);

drop policy if exists wilde_maui_admin_blocked_update on public.blocked_ranges;
create policy wilde_maui_admin_blocked_update on public.blocked_ranges
  for update to authenticated
  using (auth.uid() = '45717c8c-08f9-469f-bf7d-2fa2ef5ad441'::uuid)
  with check (auth.uid() = '45717c8c-08f9-469f-bf7d-2fa2ef5ad441'::uuid);

drop policy if exists wilde_maui_admin_blocked_delete on public.blocked_ranges;
create policy wilde_maui_admin_blocked_delete on public.blocked_ranges
  for delete to authenticated
  using (auth.uid() = '45717c8c-08f9-469f-bf7d-2fa2ef5ad441'::uuid);

commit;
