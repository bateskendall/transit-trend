from . import gtfs_realtime_pb2

def decode_binary(binary_data):
    # Create an empty FeedMessage object
    feed_message = gtfs_realtime_pb2.FeedMessage()
    
    # Parse the binary data into the FeedMessage object
    feed_message.ParseFromString(binary_data)
    
    return feed_message
