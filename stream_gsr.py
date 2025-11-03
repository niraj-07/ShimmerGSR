import time
from serial import Serial
from pyshimmer import ShimmerBluetooth, DEFAULT_BAUDRATE, DataPacket, EChannelType
from pylsl import StreamInfo, StreamOutlet

stream_name = 'ShimmerGSR'
stream_type = 'GSR'
channel_count = 1
# sample rate must match in shimmer -> set using consenys software
sample_rate = 51.2
channel_format = 'float32'
source_id = 'my-shimmer-1234'

info = StreamInfo(stream_name, stream_type, channel_count, sample_rate, channel_format, source_id)

outlet = StreamOutlet(info)


def shimmer_callback(pkt: DataPacket) -> None:
    """
    Receives a DataPacket from pyshimmer and pushes
    the GSR data to the LSL outlet.
    """
    try:
        gsr_data = pkt[EChannelType.INTERNAL_ADC_13]
        sample = [gsr_data]
        outlet.push_sample(sample)
        print(f"Streaming GSR: {gsr_data:.2f} kOhms")
    except Exception as e:
        print(f"Error in callback: {e}")


if __name__ == '__main__':
    serial_port = 'COM10'

    print(f"Connecting to Shimmer on {serial_port}...")

    try:
        serial = Serial(serial_port, DEFAULT_BAUDRATE)
        shim_dev = ShimmerBluetooth(serial)
        shim_dev.initialize()

        print(f"Connected to device: {shim_dev.get_device_name()}")

        shim_dev.add_stream_callback(shimmer_callback)

        print("\nStarting LSL stream. Open LabRecorder now.")
        print("Stream name: 'ShimmerGSR'")

        shim_dev.start_streaming()

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nStopping stream...")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'shim_dev' in locals():
            shim_dev.stop_streaming()
            shim_dev.shutdown()
        if 'serial' in locals() and serial.is_open:
            serial.close()
        print("Stream stopped.")
    
