import sys

import psutil


def resource_lock(maximum_cpu_load=90, minimum_free_memory=0.6, memory_lock_warning_message="",
                  cpu_lock_warning_message="", freezing_seconds=1):
    enable_memory_warning_message = len(memory_lock_warning_message) > 0
    enable_cpu_warning_message = len(cpu_lock_warning_message) > 0

    warning_was_show = False

    overload = psutil.cpu_percent(percpu=False, interval=.5) > maximum_cpu_load

    low_memory = psutil.virtual_memory().free < 100000000 * minimum_free_memory

    while overload or low_memory:
        if (enable_memory_warning_message or enable_cpu_warning_message) and not warning_was_show:
            if overload and enable_cpu_warning_message:
                sys.stdout.write(" [!] " + cpu_lock_warning_message + "\n")

            if low_memory and enable_memory_warning_message:
                sys.stdout.write(" [!] " + memory_lock_warning_message + "\n")

            warning_was_show = True

        overload = psutil.cpu_percent(percpu=False, interval=freezing_seconds) > maximum_cpu_load

        low_memory = psutil.virtual_memory().free < 100000000 * minimum_free_memory
