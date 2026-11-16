from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from database import Base


class Channel(Base):
    __tablename__ = "channels"

    id = Column(Integer, primary_key=True)
    channel_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)


class Campaign(Base):
    __tablename__ = "campaigns"

    id = Column(Integer, primary_key=True)
    campaign_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    channel_id = Column(String, ForeignKey("channels.channel_id"))
    budget = Column(Float, nullable=False)
    currency = Column(String, default="INR")


class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True)
    contact_id = Column(String, unique=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, nullable=True)


class Touchpoint(Base):
    __tablename__ = "touchpoints"

    id = Column(Integer, primary_key=True)
    touchpoint_id = Column(String, unique=True, nullable=False)
    contact_id = Column(String, ForeignKey("contacts.contact_id"))
    campaign_id = Column(String, ForeignKey("campaigns.campaign_id"))
    timestamp = Column(DateTime, nullable=False)
    touch_type = Column(String, nullable=False)


class WebSession(Base):
    __tablename__ = "web_sessions"

    id = Column(Integer, primary_key=True)
    session_id = Column(String, unique=True, nullable=False)
    contact_id = Column(String, ForeignKey("contacts.contact_id"), nullable=True)
    touchpoint_id = Column(
        String,
        ForeignKey("touchpoints.touchpoint_id"),
        nullable=True
    )
    timestamp = Column(DateTime, nullable=False)


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True)
    lead_id = Column(String, unique=True, nullable=False)
    contact_id = Column(String, ForeignKey("contacts.contact_id"))
    created_at = Column(DateTime, nullable=False)
    status = Column(String, nullable=False)


class Opportunity(Base):
    __tablename__ = "opportunities"

    id = Column(Integer, primary_key=True)
    opportunity_id = Column(String, unique=True, nullable=False)
    lead_id = Column(String, ForeignKey("leads.lead_id"))
    contact_id = Column(String, ForeignKey("contacts.contact_id"))
    created_at = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String, nullable=False)


class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    order_id = Column(String, unique=True, nullable=False)
    opportunity_id = Column(
        String,
        ForeignKey("opportunities.opportunity_id")
    )
    contact_id = Column(String, ForeignKey("contacts.contact_id"))
    order_date = Column(DateTime, nullable=False)
    revenue = Column(Float, nullable=False)
    currency = Column(String, default="INR")


class CostRecord(Base):
    __tablename__ = "cost_records"

    id = Column(Integer, primary_key=True)
    cost_id = Column(String, unique=True, nullable=False)
    campaign_id = Column(String, ForeignKey("campaigns.campaign_id"))
    amount = Column(Float, nullable=False)
    currency = Column(String, default="INR")


class AttributionResult(Base):
    __tablename__ = "attribution_results"

    id = Column(Integer, primary_key=True)
    attribution_id = Column(String, unique=True, nullable=False)
    order_id = Column(String, ForeignKey("orders.order_id"))
    campaign_id = Column(String, ForeignKey("campaigns.campaign_id"))
    model = Column(String, nullable=False)
    attributed_revenue = Column(Float, nullable=False)