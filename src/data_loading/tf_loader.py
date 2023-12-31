from typing import List, Dict
import psycopg2
import logging

def load_trip_updates(trip_updates: List[Dict], conn: psycopg2.extensions.connection) -> None:
    """
    Load trip updates into the database.

    Args:
        trip_updates (list): A list of trip update dictionaries.
        conn (psycopg2.extensions.connection): The database connection object.
    """
    
    with conn.cursor() as cur:
        for trip_update in trip_updates:
            try:
                cur.execute("""
                    INSERT INTO realtime_trip_updates (trip_id, route_id, start_date, schedule_relationship,
                                                       arrival_time, departure_time, stop_id)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                """, (
                    trip_update['trip_id'], trip_update['route_id'], trip_update['start_date'],
                    trip_update['schedule_relationship'], trip_update['arrival_time'],
                    trip_update['departure_time'], trip_update['stop_id']
                ))
            except Exception as e:
                logging.error(f"Failed to insert trip update: {e}")
                conn.rollback()
            else:
                conn.commit()

def load_vehicle_positions(vehicle_positions: List[Dict], conn: psycopg2.extensions.connection) -> None:
    """
    Load vehicle positions into the database.
    
    Args:
        vehicle_positions (list): A list of vehicle position dictionaries.
        conn (psycopg2.extensions.connection): The database connection object.
    """
    
    with conn.cursor() as cur:
        for vehicle_position in vehicle_positions:
            try:
                cur.execute("""
                    INSERT INTO realtime_vehicle_positions (trip_id, route_id, current_stop_sequence,
                                                           stop_id, current_status, timestamp)
                    VALUES (%s, %s, %s, %s, %s, %s)
                """, (
                    vehicle_position['trip_id'], vehicle_position['route_id'],
                    vehicle_position['current_stop_sequence'], vehicle_position['stop_id'],
                    vehicle_position['current_status'], vehicle_position['timestamp']
                ))
            except Exception as e:
                logging.error(f"Failed to insert vehicle position: {e}")
                conn.rollback()
            else:
                conn.commit()

def load_alerts(alerts: List[Dict], conn: psycopg2.extensions.connection) -> None:
    """
    Load alerts into the database.
    
    Args:
        alerts (list): A list of alert dictionaries.
        conn (psycopg2.extensions.connection): The database connection object.
    """
    
    with conn.cursor() as cur:
        for alert in alerts:
            try:
                cur.execute("""
                    INSERT INTO realtime_alerts (alert_id, trip_id, route_id, description_text)
                    VALUES (%s, %s, %s, %s)
                """, (
                    alert['alert_id'], alert['trip_id'], alert['route_id'], alert['description_text']
                ))
            except Exception as e:
                logging.error(f"Failed to insert alert: {e}")
                conn.rollback()
            else:
                conn.commit()

def load_all_data(
        trip_updates: List[Dict],
        vehicle_positions: List[Dict],
        alerts: List[Dict],
        conn: psycopg2.extensions.connection
    ) -> None:
    """
    A wrapper function to load all extracted data into the database.

    Args:
        trip_updates (list): A list of trip update dictionaries.
        vehicle_positions (list): A list of vehicle position dictionaries.
        alerts (list): A list of alert dictionaries.
        conn (psycopg2.extensions.connection): The database connection object.
    """
    
    load_trip_updates(trip_updates, conn)
    load_vehicle_positions(vehicle_positions, conn)
    load_alerts(alerts, conn)
