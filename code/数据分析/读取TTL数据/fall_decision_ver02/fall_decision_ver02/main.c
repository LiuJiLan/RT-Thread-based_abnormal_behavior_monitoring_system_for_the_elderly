/*
 *
 */

// ֱ���� setting->���->�豸���������е�uart�и�����rx�Ļ���Ϊ256
// 256���ǲ�������Ϊ512�� 512���ǲ���

// �������Ĵ����ʲ��ܹ��ߣ� �����ڴ�ᱬ


#include <rtthread.h>
#include <rtdevice.h>
#include <rtconfig.h>
#include <stdio.h>

#include "drv_common.h"
#include "handle.h"

#define TIME_DIFF 10

// �ǵ�������settings�� Ȼ����rtconfig.h��BSP֮��ע��uart1
#define UART_ONE_NAME    "uart1"    // UART����
#define BUZZ_PIN GET_PIN(A, 8)

static rt_device_t sensor;
struct serial_configure sensor_config = RT_SERIAL_CONFIG_DEFAULT; /* ��ʼ�����ò��� */
static struct rt_semaphore rx_sem; /* ���ڽ�����Ϣ���ź��� */


static time_t cur_seconds;


/* �������ݻص����� */
static rt_err_t uart_input(rt_device_t dev, rt_size_t size) {
    /* ���ڽ��յ����ݺ�����жϣ����ô˻ص�������Ȼ���ͽ����ź��� */
    rt_sem_release(&rx_sem);
    return RT_EOK;
}

static void read_from_sensor(void) {
    unsigned char ch;
    time_t now_second = time((time_t *)NULL);

    // ��ʵ�����Ӧʹ�� while (1) ��һֱ��ѯ

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
    // ������terminal֮�󣬼ǵò�һ������

    cur_seconds = time((time_t *)NULL);
    cur_seconds += TIME_DIFF;

    const char * message = "AT+ENTM\r\n"; // ATK-BLE01 ͸��ָ��
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
