from fpioa_manager import fm
from machine import UART
from board import board_info
from fpioa_manager import fm


def get_int(shortL, shortH):
    extend_num = 0
    if len(bin(struct.unpack("B", shortH)[0])) == 10:
        extend_num = 255
    return struct.unpack("i", shortL + shortH + struct.pack("B", extend_num) + struct.pack("B", extend_num))[0]


# maixduino board_info PIN10/PIN11/PIN12/PIN13 or other hardware IO 10/11/4/3
fm.register(10, fm.fpioa.UART1_TX, force=True)
fm.register(11, fm.fpioa.UART1_RX, force=True)

uart_A = UART(UART.UART1, 115200, 8, None, 1, timeout=1000, read_buf_len=4096)

TRASH_BIN = None

while True:
    print(uart_A.read(1))
uart_A.deinit()
del uart_A