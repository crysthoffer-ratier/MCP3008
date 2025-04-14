import time
import spidev
import logging


logger = logging.getLogger(__name__)
logging.basicConfig(
    level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s"
)
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000


def analog_read(channel):
    r = spi.xfer2([1, (8 + channel) << 4, 0])
    print(r)
    adc_out = ((r[1] & 3) << 8) + r[2]
    print(adc_out)

    return adc_out


def main():
    try:
        while True:
            reading = analog_read(0)
            voltage = reading * 3.3 / 1024

            logger.debug(f"Reading: {reading}")
            logger.debug(f"Voltage: {voltage:.2f} V")

            time.sleep(1)
    except KeyboardInterrupt:
        print("Exiting gracefully...")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")
    finally:
        spi.close()
        print("SPI closed.")


if __name__ == "__main__":
    main()
