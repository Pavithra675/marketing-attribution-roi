# Marketing Attribution & ROI — Data Dictionary

**Version:** 1.0  
**Random seed:** 20261022  
**Date range:** 2026  
**Currency:** INR unless otherwise specified

This document defines the target data contract for the Marketing Attribution & ROI system. Required fields must not be null. IDs must be immutable and unique. Foreign keys must reference existing records.

## 1. Campaign

| Field | Type | Required | Allowed values / units | Uniqueness and validation |
|---|---|---|---|---|
| campaign_id | String | Yes | CMP-2026-000001 format | Primary key; unique |
| campaign_name | String | Yes | Non-empty text | No blank values |
| channel_id | String | Yes | Existing channel ID | Foreign key |
| budget | Decimal | Yes | INR amount, greater than 0 | Non-negative |
| currency | String | Yes | INR, USD, EUR | ISO currency code |
| start_date | Date | Yes | YYYY-MM-DD | Must be before or equal to end_date |
| end_date | Date | Yes | YYYY-MM-DD | Must be after or equal to start_date |
| status | String | Yes | Planned, Active, Paused, Completed | Allowed enum only |

## 2. Channel

| Field | Type | Required | Allowed values / units | Uniqueness and validation |
|---|---|---|---|---|
| channel_id | String | Yes | CH-001 format | Primary key; unique |
| channel_name | String | Yes | Email, Social Media, Search, Display, Offline | Unique name; allowed enum |

## 3. Creative

| Field | Type | Required | Allowed values / units | Uniqueness and validation |
|---|---|---|---|---|
| creative_id | String | Yes | CRE-0001 format | Primary key; unique |
| creative_name | String | Yes | Non-empty text | No blank values |
| creative_type | String | Yes | Image, Video, Text, Banner | Allowed enum |
| status | String | Yes | Active, Inactive, Archived | Allowed enum |

## 4. Audience

| Field | Type | Required | Allowed values / units | Uniqueness and validation |
|---|---|---|---|---|
| audience_id | String | Yes | AUD-0001 format | Primary key; unique |
| audience_name | String | Yes | Non-empty text | No blank values |
| segment_type | String | Yes | New Customers, Returning Customers, High Intent, General | Allowed enum |

## 5. Contact

| Field | Type | Required | Allowed values / units | Uniqueness and validation |
|---|---|---|---|---|
| contact_id | String | Yes | CON-000001 format | Primary key; unique |
| contact_name | String | Yes | Non-empty text | No blank values |
| email | String | No | Valid email format | Unique when present |
| created_date | Date | Yes | YYYY-MM-DD | Cannot be after current dataset date |

## 6. Touchpoint

| Field | Type | Required | Allowed values / units | Uniqueness and validation |
|---|---|---|---|---|
| touchpoint_id | String | Yes | TOUCH-CON-000001-000001 format | Primary key; unique |
| contact_id | String | Yes | Existing contact ID | Foreign key |
| campaign_id | String | Yes | Existing campaign ID | Foreign key |
| channel | String | Yes | Email, Social Media, Search, Display, Offline | Allowed enum |
| interaction_type | String | Yes | Impression, Click, Website Visit, Form Submission, Call, Event, Store Visit | Allowed enum |
| touchpoint_date | DateTime | Yes | Timestamp | Valid date; checked against conversion date |
| source_type | String | Yes | Online, Offline | Allowed enum |

## 7. WebSession

| Field | Type | Required | Allowed values / units | Uniqueness and validation |
|---|---|---|---|---|
| session_id | String | Yes | SES-2026-000001 format | Primary key; unique |
| contact_id | String | No | Existing contact ID | Foreign key when present |
| touchpoint_id | String | No | Existing touchpoint ID | Foreign key when present |
| session_date | DateTime | Yes | Timestamp | Must be valid |
| consent_status | String | Yes | YES, NO | Allowed enum |
| identity_link_evidence | String | Yes | Authenticated Login, Verified Form, NONE | Must support identity linkage |
| lead_id | String | No | Existing lead ID | Foreign key when present |

**Identity rule:** An anonymous session must not be linked to a contact without valid identity evidence and consent. Missing evidence must result in an unlinked session.

## 8. Lead

| Field | Type | Required | Allowed values / units | Uniqueness and validation |
|---|---|---|---|---|
| lead_id | String | Yes | LEAD-2026-000001 format | Primary key; unique |
| contact_id | String | Yes | Existing contact ID | Foreign key |
| lead_source | String | Yes | Website, Email, Social Media, Search, Offline | Allowed enum |
| lead_status | String | Yes | New, Qualified, Unqualified, Converted | Allowed enum |
| created_date | Date | Yes | YYYY-MM-DD | Valid date |

## 9. Opportunity

| Field | Type | Required | Allowed values / units | Uniqueness and validation |
|---|---|---|---|---|
| opportunity_id | String | Yes | OPP-2026-000001 format | Primary key; unique |
| lead_id | String | Yes | Existing lead ID | Foreign key |
| contact_id | String | Yes | Existing contact ID | Must match the lead's contact |
| opportunity_name | String | Yes | Non-empty text | No blank values |
| stage | String | Yes | Prospecting, Negotiation, Won, Lost | Allowed enum |
| amount | Decimal | Yes | Monetary amount | Greater than or equal to 0 |
| currency | String | Yes | INR, USD, EUR | ISO currency code |
| created_date | Date | Yes | YYYY-MM-DD | Must be valid |

## 10. Order

| Field | Type | Required | Allowed values / units | Uniqueness and validation |
|---|---|---|---|---|
| order_id |