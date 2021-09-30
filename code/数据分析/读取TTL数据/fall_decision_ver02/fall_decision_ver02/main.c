/*
 *
 */

// 直接在 setting->组件->设备驱动程序中的uart中更改了rx的缓存为256
// 256还是不够，改为512， 512还是不够

// 传感器的传输率不能过高， 否则内存会爆


#include <rtthread.h>
#include <rtdevice.h>
#include <rtconfig.h>
#include <stdio.h>

#include "drv_common.h"
#include "handle.h"

#define TIME_DIFF 10

// 记得先配置settings， 然后在rtconfig.h中BSP之下注册uart1
#define UART_ONE_NAME    "uart1"    // UART名字
#define BUZZ_PIN GET_PIN(A, 8)

static rt_device_t sensor;
struct serial_configure sensor_config = RT_SERIAL_CONFIG_DEFAULT; /* 初始化配置参数 */
static struct rt_semaphore rx_sem; /* 用于接收消息的信号量 */


static time_t cur_seconds;


/* 接收数据回调函数 */
static rt_err_t uart_input(rt_device_t dev, rt_size_t size) {
    /* 串口接收到数据后产生中断，调用此回调函数，然后发送接收信号量 */
    rt_sem_release(&rx_sem);
    return RT_EOK;
}

static void read_from_sensor(void) {
    unsigned char ch;
    time_t now_second = time((time_t *)NULL);

    // 真实情况下应使用 while (1) 来一直轮询

    while (now_second < cur_seconds) {
    // while (1) {
        while (rt_device_read(sensor, -1, &ch, 1) != 1) {
            rt_sem_take(&rx_sem, RT_WAITING_FOREVER);
        }
        handle_data(ch);
        // printf("%x\t", ch);

        now_second = time((time_t *)NULL);
    }
}

int main(void) {
    printf("Now in main.c\n");


    rt_pin_mode(BUZZ_PIN, PIN_MODE_OUTPUT);

    rt_pin_write(BUZZ_PIN, PIN_LOW);
    rt_thread_mdelay(1000);
    rt_pin_write(BUZZ_PIN, PIN_HIGH);

    sensor_config.bufsz = 512;

    sensor = rt_device_find(UART_ONE_NAME);
    rt_device_control(sensor, RT_DEVICE_CTRL_CONFIG, &sensor_config);
    rt_device_open(sensor, RT_DEVICE_FLAG_INT_RX);
    rt_sem_init(&rx_sem, "rx_sem", 0, RT_IPC_FLAG_FIFO);
    rt_device_set_rx_indicate(sensor, uart_input);

    // printf("Test Where Is the Termial.\n");
    // 此行在terminal之后，记得补一个换行

    cur_seconds = time((time_t *)NULL);
    cur_seconds += TIME_DIFF;

    const char * message = "AT+ENTM\r\n"; // ATK-BLE01 透传指令
    rt_device_write(sensor, 0, message, 10);

    printf("\nstart\n");

    read_from_sensor();

    printf("end\n");


    rt_pin_write(BUZZ_PIN, PIN_LOW);
    rt_thread_mdelay(1000);
    rt_pin_write(BUZZ_PIN, PIN_HIGH);


    return RT_EOK;
}

#include "stm32h7xx.h"
static int vtor_config(void)
{
    /* Vector Table Relocation in Internal QSPI_FLASH */
    SCB->VTOR = QSPI_BASE;
    return 0;
}
INIT_BOARD_EXPORT(vtor_config);
