from . import gtfs_realtime_pb2

def decode_binary(binary_data: bytes) -> gtfs_realtime_pb2.FeedMessage:
    """
    Decodes binary data into a FeedMessage object.

    Args:
        binary_data (bytes): The binary data to be decoded.

    Returns:
        gtfs_realtime_pb2.FeedMessage: The decoded FeedMessage object.
    """
    
    # Create an empty FeedMessage object
    feed_message = gtfs_realtime_pb2.FeedMessage()
    
    # Parse the binary data into the FeedMessage object
    feed_message.ParseFromString(binary_data)
    
    return feed_message
