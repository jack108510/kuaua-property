# Maui shared admin password

The `/admin/` page uses a Maui-specific shared password, with no email or Reachr login. Visitor access uses its existing separate code. The visitor-code settings tab is labelled accordingly.

`assets/maui-admin-client-20261122.js` talks to the hosted password service. It keeps an eight-hour Maui session token in tab session storage, never the typed password. `MauiData()` directs admin reads/writes through that restricted service; public availability and guest-request submission keep the existing public Supabase path. Supabase Auth persistence is disabled in the new frontend because Maui admin no longer uses the Reachr account.

The service allows only `stay_requests`, `blocked_ranges`, and the `site_password` setting, with specific-record mutations and allowed field checks. It has no generic SQL or proxy endpoint. Runtime secrets stay server-side; no password, database admin key, or session-signing secret is stored in this public repository.

Service source is maintained at `/Users/jackserver/maui-password-service`. Hosted project: `appgprj_6b0371ea1a14819188d3701df6e91ef3`. Service URL: `https://wildemaui-admin-api.wildejack1010.chatgpt.site`. The service accepts unauthenticated password submissions, but all administrative data routes require a Maui session. CORS permits only wildemaui.com and www.wildemaui.com.

The owner's protected initial password file is `~/.config/wildemaui/admin-password.txt`. To rotate the password, update the service's secret `MAUI_ADMIN_PASSWORD` through the hosting configuration and deploy that environment revision. Existing sessions become invalid after rotation. Do not change the Reachr/Supabase account password for Maui access. The password-help page only directs people to the owner; it no longer resets the Reachr account.

Tests: `node --test tests/shared-admin.test.cjs`. Service tests live with its source. A temporary past-date calendar hold was inserted, read, deleted, and verified absent to validate deployed write operations. No guest email was sent and no existing booking or visitor password was changed.
