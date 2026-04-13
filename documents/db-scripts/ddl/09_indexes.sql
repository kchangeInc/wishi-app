-- ============================================================
-- WISHI Database DDL - 09: Performance Indexes
-- ============================================================

-- ======================== public ========================

CREATE INDEX idx_subcategories_cat    ON public.subcategories(category_id);
CREATE INDEX idx_field_defs_subcat    ON public.field_definitions(subcategory_id);
CREATE INDEX idx_cities_name          ON public.cities(name);
CREATE INDEX idx_cities_state         ON public.cities(state_id);
CREATE INDEX idx_cities_country       ON public.cities(country_id);
CREATE INDEX idx_cities_type          ON public.cities(type);
CREATE INDEX idx_cities_population    ON public.cities(population DESC) WHERE population IS NOT NULL;
CREATE INDEX idx_countries_iso2       ON public.countries(iso2);
CREATE INDEX idx_states_country       ON public.states(country_id);
CREATE INDEX idx_states_region        ON public.states(region_id);
CREATE INDEX idx_subregions_state     ON public.subregions(state_id);

-- ======================== core ========================

CREATE INDEX idx_users_email          ON core.users(email);
CREATE INDEX idx_users_google_id      ON core.users(google_id) WHERE google_id IS NOT NULL;
CREATE INDEX idx_users_role           ON core.users(role);
CREATE INDEX idx_users_active         ON core.users(id) WHERE is_active = TRUE AND is_deleted = FALSE;

CREATE INDEX idx_refresh_tokens_user  ON core.refresh_tokens(user_id);
CREATE INDEX idx_refresh_tokens_token ON core.refresh_tokens(token);

CREATE INDEX idx_msc_source           ON core.marketplace_source_categories(marketplace_source_id);
CREATE INDEX idx_msc_category         ON core.marketplace_source_categories(category_id);

CREATE INDEX idx_wishlists_user       ON core.wishlists(user_id);
CREATE INDEX idx_wishlists_category   ON core.wishlists(category_id);
CREATE INDEX idx_wishlists_subcat     ON core.wishlists(subcategory_id);
CREATE INDEX idx_wishlists_status     ON core.wishlists(status) WHERE is_deleted = FALSE;
CREATE INDEX idx_wishlists_expiry     ON core.wishlists(expiry_date) WHERE status = 'active';
CREATE INDEX idx_wishlists_created    ON core.wishlists(created_at DESC);

CREATE INDEX idx_wfv_wishlist         ON core.wishlist_field_values(wishlist_id);
CREATE INDEX idx_wfv_field_def        ON core.wishlist_field_values(field_definition_id);

CREATE INDEX idx_wpm_wishlist         ON core.wishlist_preferred_marketplaces(wishlist_id);

CREATE INDEX idx_favourites_user      ON core.favourites(user_id);
CREATE INDEX idx_favourites_match     ON core.favourites(match_id);
CREATE INDEX idx_favourites_wishlist  ON core.favourites(wishlist_id);

CREATE INDEX idx_removed_user         ON core.removed_matches(user_id);
CREATE INDEX idx_removed_match        ON core.removed_matches(match_id);

CREATE INDEX idx_saved_user           ON core.saved_listings(user_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_saved_date           ON core.saved_listings(saved_at DESC);

CREATE INDEX idx_feedback_user        ON core.feedback(user_id);

CREATE INDEX idx_offers_seller        ON core.offers(seller_user_id) WHERE is_deleted = FALSE;
CREATE INDEX idx_offers_category      ON core.offers(category_id);
CREATE INDEX idx_offers_status        ON core.offers(status) WHERE is_active = TRUE;

-- ======================== ai ========================

CREATE INDEX idx_clusters_filters     ON ai.clusters(normalized_filters);
CREATE INDEX idx_clusters_category    ON ai.clusters(category_id);
CREATE INDEX idx_clusters_active      ON ai.clusters(id) WHERE is_active = TRUE;

CREATE INDEX idx_matches_cluster      ON ai.matches(cluster_id);
CREATE INDEX idx_matches_wishlist     ON ai.matches(wishlist_id);
CREATE INDEX idx_matches_source       ON ai.matches(marketplace_source_id);
CREATE INDEX idx_matches_status       ON ai.matches(status) WHERE is_deleted = FALSE;
CREATE INDEX idx_matches_score        ON ai.matches(score DESC) WHERE status IN ('published', 'auto_publish');
CREATE INDEX idx_matches_created      ON ai.matches(created_at DESC);

-- ======================== company ========================

CREATE INDEX idx_company_users_user   ON company.company_users(user_id);
CREATE INDEX idx_audit_table_record   ON company.audit_log(table_name, record_id);
CREATE INDEX idx_audit_user           ON company.audit_log(user_id);
CREATE INDEX idx_audit_timestamp      ON company.audit_log(timestamp DESC);

-- ======================== analytics ========================

CREATE INDEX idx_mh_user              ON analytics.match_history(user_id);
CREATE INDEX idx_mh_wishlist          ON analytics.match_history(wishlist_id);
CREATE INDEX idx_mh_match             ON analytics.match_history(match_id);
CREATE INDEX idx_mh_action            ON analytics.match_history(action);

CREATE INDEX idx_clicks_match         ON analytics.clicks(match_id);
CREATE INDEX idx_clicks_user          ON analytics.clicks(user_id);
CREATE INDEX idx_clicks_ts            ON analytics.clicks(timestamp DESC);

CREATE INDEX idx_events_type          ON analytics.events(event_type);
CREATE INDEX idx_events_user          ON analytics.events(user_id);
CREATE INDEX idx_events_created       ON analytics.events(created_at DESC);

CREATE INDEX idx_product_demand_cat   ON analytics.product_demand(category_id);
CREATE INDEX idx_product_demand_period ON analytics.product_demand(period_start, period_end);

CREATE INDEX idx_seo_perf_path        ON analytics.seo_performance(page_path);
CREATE INDEX idx_seo_perf_period      ON analytics.seo_performance(period_start, period_end);

-- ======================== automation ========================

CREATE INDEX idx_notif_user           ON automation.notifications(user_id);
CREATE INDEX idx_notif_user_unread    ON automation.notifications(user_id) WHERE is_read = FALSE AND is_deleted = FALSE;
CREATE INDEX idx_notif_type           ON automation.notifications(type);
CREATE INDEX idx_notif_wishlist       ON automation.notifications(wishlist_id);
CREATE INDEX idx_notif_created        ON automation.notifications(created_at DESC);

CREATE INDEX idx_sched_status         ON automation.schedulers(status);
CREATE INDEX idx_sched_next_run       ON automation.schedulers(next_run_at) WHERE status = 'active';

-- ======================== seo ========================

CREATE INDEX idx_seo_pages_slug       ON seo.seo_pages(slug);
CREATE INDEX idx_seo_pages_type       ON seo.seo_pages(page_type);
CREATE INDEX idx_seo_pages_published  ON seo.seo_pages(id) WHERE is_published = TRUE;

CREATE INDEX idx_seo_tracking_page    ON seo.seo_tracking(seo_page_id);
CREATE INDEX idx_seo_tracking_type    ON seo.seo_tracking(event_type);
CREATE INDEX idx_seo_tracking_created ON seo.seo_tracking(created_at DESC);
