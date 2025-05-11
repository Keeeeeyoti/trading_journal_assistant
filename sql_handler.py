from sql_setup import Trade, SessionLocal
from sqlalchemy.orm import Session
import pandas as pd
from datetime import datetime, timedelta


def write_trade(trade_data: dict):
    session: Session = SessionLocal()
    try:
        if trade_data["date_delta"] == 0:
            trade_data["date"] = datetime.now()
        else:
            trade_data["date"] = datetime.now().date - timedelta(
                days=trade_data["date_delta"]
            )
            # Remove "time_delta" from the dictionary as it's no longer needed
        del trade_data["time_delta"]
        trade = Trade(**trade_data)
        session.add(trade)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()


def read_trades() -> pd.DataFrame:
    session: Session = SessionLocal()
    try:
        trades = session.query(Trade).all()
        df = pd.DataFrame([t.__dict__ for t in trades])
        df.drop(columns=["_sa_instance_state"], inplace=True)
        return df
    finally:
        session.close()
