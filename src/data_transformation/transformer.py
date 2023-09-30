from .binary_decoder import decode_binary
import time
import datetime
import psycopg2
import logging

logging.basicConfig(level=logging.DEBUG)

def extract_trip_updates(trip_update):
    trip_updates = []  # list to hold extracted trip updates
    trip = trip_update.trip_update.trip
    for stop_time_update in trip_update.trip_update.stop_time_update:
        values = {
            'trip_id': trip.trip_id,
            'route_id': trip.route_id,
            'start_date': trip.start_date,
            'schedule_relationship': trip.schedule_relationship,
            'arrival_time': epoch_to_time(stop_time_update.arrival.time) if stop_time_update.HasField('arrival') else None,
            'departure_time': epoch_to_time(stop_time_update.departure.time) if stop_time_update.HasField('departure') else None,
            'stop_id': stop_time_update.stop_id
        }
        trip_updates.append(values)  # append extracted values to list
    return trip_updates  # return list of extracted values

# Helper function to convert epoch timestamp to time
def epoch_to_time(epoch):
    return time.strftime('%H:%M:%S', time.gmtime(epoch))


def extract_vehicle_positions(vehicle_position):
    vehicle_positions = []  # List to hold extracted vehicle positions
    vehicle = vehicle_position.vehicle  # Assuming vehicle_position is the correct Protobuf message
    vehicle_stop_status = vehicle.vehicle_stop_status if hasattr(vehicle, 'vehicle_stop_status') else None
    values = {
        'trip_id': vehicle.trip.trip_id,
        'route_id': vehicle.trip.route_id,
        'current_stop_sequence': vehicle.current_stop_sequence,
        'stop_id': vehicle.stop_id,
        'current_status': vehicle.current_status,
        'timestamp': datetime.datetime.utcfromtimestamp(vehicle.timestamp),
    }
    vehicle_positions.append(values)  # Append extracted values to list
    return vehicle_positions  # Return list of extracted values

def extract_alerts(alert):
    alerts = []  # List to hold extracted alerts
    for informed_entity in alert.alert.informed_entity:
        for translation in alert.alert.header_text.translation:
            values = {
                'alert_id': alert.id,
                'trip_id': informed_entity.trip.trip_id if informed_entity.HasField('trip') else None,
                'route_id': informed_entity.trip.route_id if informed_entity.HasField('trip') else None,
                'description_text': translation.text
            }
            alerts.append(values)  # Append extracted values to list
    return alerts  # Return list of extracted values

def process_feed(binary_data, conn):
    # Decode binary data using decode_binary
    feed_message = decode_binary(binary_data)

    # Lists to aggregate extracted data
    trip_updates = []
    vehicle_positions = []
    alerts = []

    try:
        # Iterate through feed_message and send feed_message entities to their respective functions for extraction
        for entity in feed_message.entity:
            if entity.HasField('trip_update'):
                trip_updates.extend(extract_trip_updates(entity))
            elif entity.HasField('vehicle'):
                vehicle_positions.extend(extract_vehicle_positions(entity))
            elif entity.HasField('alert'):
                alerts.extend(extract_alerts(entity))
            else:
                logging.warning(f"Unhandled entity type in entity: {entity}")
    except Exception as e:
        logging.warning(f"Error processing entity: {e}")

    return trip_updates, vehicle_positions, alerts  # Return all extracted data

