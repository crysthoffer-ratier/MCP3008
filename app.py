import time
import spidev
import logging

# Logger setup
logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)

# SPI setup for communication with MCP3008
spi = spidev.SpiDev()
spi.open(0, 0)  # Open SPI bus 0, chip select 0
spi.max_speed_hz = 1000000  # Max speed for SPI (can be adjusted based on your needs)

# Constants
VREF = 3.3  # Reference voltage for the ADC (could be 5V if using a 5V system)

def analog_read(channel):
    """
    Read from the specified channel (0-7) of the MCP3008 ADC.
    """
    if channel < 0 or channel > 7:
        raise ValueError("MCP3008 has 8 channels (0-7). Invalid channel number.")
    
    # MCP3008 SPI transfer
    r = spi.xfer2([1, (8 + channel) << 4, 0])  # Sending the 3-byte command to MCP3008
    
    # Extract the ADC value from the returned list
    adc_out = ((r[1] & 3) << 8) + r[2]  # Combining the 2nd and 3rd byte to form a 10-bit result
    print(f"Raw SPI Response: {r}, ADC Output: {adc_out}")
    
    return adc_out

def main():
    try:
        while True:
            reading = analog_read(0)  # Read from channel 0 (you can change this as needed)
            voltage = reading * VREF / 1023  # Calculate the voltage from the ADC value
            
            # Log the results
            logger.debug(f"Reading: {reading}")
            logger.debug(f"Voltage: {voltage:.2f} V")
            print(f"")
            
            time.sleep(1)  # Sleep for 1 second before the next reading

    except KeyboardInterrupt:
        print("Exiting gracefully...")

    except Exception as e:
        logger.exception(f"Unexpected error: {e}")

    finally:
        spi.close()  # Ensure the SPI connection is properly closed
        print("SPI closed.")

if __name__ == "__main__":
    main()
