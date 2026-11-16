-- Marketing Attribution database schema

CREATE TABLE "attribution_results" (
"order_id" TEXT,
  "campaign_id" TEXT,
  "touchpoint_id" TEXT,
  "touchpoint_date" TEXT,
  "model" TEXT,
  "attributed_revenue" REAL
);

CREATE TABLE "audiences" (
"audience_id" TEXT,
  "audience_name" TEXT,
  "segment_type" TEXT
);

CREATE TABLE "campaign_audiences" (
"campaign_id" TEXT,
  "audience_id" TEXT
);

CREATE TABLE "campaign_creatives" (
"campaign_id" TEXT,
  "creative_id" TEXT
);

CREATE TABLE "campaign_roi_report" (
"campaign_id" TEXT,
  "campaign_name" TEXT,
  "currency_campaign" TEXT,
  "cost_amount" INTEGER,
  "currency_cost" TEXT,
  "attributed_revenue" REAL,
  "cost_status" TEXT,
  "currency_status" TEXT,
  "ROI_percent" REAL,
  "ROAS" REAL,
  "roi_status" TEXT,
  "model" TEXT
);

CREATE TABLE "campaigns" (
"campaign_id" TEXT,
  "campaign_name" TEXT,
  "channel" TEXT,
  "budget" INTEGER,
  "currency" TEXT
);

CREATE TABLE "channels" (
"channel_id" TEXT,
  "channel_name" TEXT
);

CREATE TABLE "contacts" (
"contact_id" TEXT,
  "contact_name" TEXT,
  "email" TEXT,
  "created_date" TEXT
);

CREATE TABLE "cost_records" (
"cost_id" TEXT,
  "campaign_id" TEXT,
  "cost_amount" INTEGER,
  "currency" TEXT,
  "cost_date" TEXT
);

CREATE TABLE "creatives" (
"creative_id" TEXT,
  "creative_name" TEXT,
  "creative_type" TEXT,
  "status" TEXT
);

CREATE TABLE "leads" (
"lead_id" TEXT,
  "contact_id" TEXT,
  "lead_source" TEXT,
  "lead_status" TEXT,
  "created_date" TEXT
);

CREATE TABLE "opportunities" (
"opportunity_id" TEXT,
  "lead_id" TEXT,
  "contact_id" TEXT,
  "opportunity_name" TEXT,
  "stage" TEXT,
  "amount" INTEGER,
  "currency" TEXT,
  "created_date" TEXT
);

CREATE TABLE "orders" (
"order_id" TEXT,
  "opportunity_id" TEXT,
  "contact_id" TEXT,
  "revenue" INTEGER,
  "currency" TEXT,
  "order_status" TEXT,
  "order_date" TEXT
);

CREATE TABLE "touchpoints" (
"touchpoint_id" TEXT,
  "contact_id" TEXT,
  "campaign_id" TEXT,
  "channel" TEXT,
  "interaction_type" TEXT,
  "touchpoint_date" TEXT
);

CREATE TABLE "unattributed_orders" (
"order_id" TEXT,
  "opportunity_id" TEXT,
  "contact_id" TEXT,
  "revenue" TEXT,
  "currency" TEXT,
  "order_status" TEXT,
  "order_date" TEXT,
  "attribution_status" TEXT,
  "reason" TEXT
);

CREATE TABLE "web_sessions" (
"session_id" TEXT,
  "contact_id" TEXT,
  "touchpoint_id" TEXT,
  "session_date" TEXT,
  "consent_status" TEXT,
  "identity_link_evidence" TEXT
);

