# Marketing Attribution & ROI — Data Dictionary

## 1. Project information

- Random seed: `20261022`
- Primary currency: INR
- Attribution lookback window: 180 days
- Data format: CSV
- Additional exports: JSON and SQLite

This document describes the fields present in the generated CSV datasets.

## 2. Source datasets

### Campaigns — `campaigns.csv`

| Column | Description |
|---|---|
| campaign_id (PK) | Unique campaign identifier |
| campaign_name | Campaign name |
| channel | Marketing channel |
| budget | Campaign budget |
| currency | Campaign budget currency |

### Channels — `channels.csv`

| Column | Description |
|---|---|
| channel_id (PK) | Unique channel identifier |
| channel_name | Channel name |

### Creatives — `creatives.csv`

| Column | Description |
|---|---|
| creative_id (PK) | Unique creative identifier |
| creative_name | Creative name |
| creative_type | Type of marketing creative |
| status | Creative status |

### Audiences — `audiences.csv`

| Column | Description |
|---|---|
| audience_id (PK) | Unique audience identifier |
| audience_name | Audience name |
| segment_type | Audience segment classification |

### Campaign-Creative Bridge — `campaign_creatives.csv`

| Column | Description |
|---|---|
| campaign_id (FK) | Related campaign |
| creative_id (FK) | Related creative |

Composite key: campaign_id + creative_id.

### Campaign-Audience Bridge — `campaign_audiences.csv`

| Column | Description |
|---|---|
| campaign_id (FK) | Related campaign |
| audience_id (FK) | Related audience |

Composite key: campaign_id + audience_id.

### Contacts — `contacts.csv`

| Column | Description |
|---|---|
| contact_id (PK) | Unique contact identifier |
| contact_name | Contact name |
| email | Contact email |
| created_date | Contact creation date |

### Touchpoints — `touchpoints.csv`

| Column | Description |
|---|---|
| touchpoint_id (PK) | Unique touchpoint identifier |
| contact_id (FK) | Related contact |
|