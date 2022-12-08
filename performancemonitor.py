# Import functions from tkinter, psutil, and tabulate
from tkinter import *
import psutil
from psutil import disk_partitions, disk_usage, virtual_memory, cpu_percent
from tabulate import tabulate

# Creating window and setting window size and title
window = Tk()
window.geometry("1280x1024")
window.configure(bg='#000000')
window.title("PC Performance Monitor")
window.resizable(False, False)


# Creating the Title inside of the program
title_performance_monitor = Label(window, text="PC Performance Monitor", font="Helvetica 35 bold underline", fg='#ffffff', bg='#000000')
title_performance_monitor.place(x=350, y=40)

# Creating global variable for cpu status
global cpu_status

# Function to change MHz to GHz
def mhz_to_ghz(mhz_speed):
    ghz_speed = mhz_speed / 1000
    return ghz_speed


# Function to collect, update, format the display CPU usage information
def cpu_info():
    cpu_usage = cpu_percent(interval=1)
    cpu_usage_label.config(text='{} %'.format(cpu_usage))
    cpu_usage_label.after(100, cpu_info)

    cpu_cores = psutil.cpu_count(logical=False)
    core_cpu_label.config(text='{}'.format(cpu_cores))

    logical_cpu_cores = psutil.cpu_count(logical=True)
    logical_core_cpu_label.config(text='{}'.format(logical_cpu_cores))

    frequency_cpu = psutil.cpu_freq()
    frequency_cpu_label.config(text='{} GHz'.format(mhz_to_ghz(frequency_cpu[0])))

    # if statement checking if cpu_usage is over 80% and displaying a warning message that CPU usage is dangerously high.
    if cpu_usage > 80:
        cpu_status_warning = "Your CPU usage is dangerously high!"
    else:
        cpu_status_warning = "Your PC is running well!"

    system_status_label.config(text=cpu_status_warning)


# Function to collect, update, format the display RAM usage information
def ram_info():
    ram_usage = virtual_memory()
    ram_usage=dict(ram_usage._asdict())

    # Converting virtual_memory() output amounts that are in bytes to gigabytes
    for key in ram_usage:
        if key != 'percent':
            ram_usage[key]=bytes_to_gb(ram_usage[key])

    ram_usage_label.config(text='{} %'.format(ram_usage["percent"]))
    ram_usage_label.after(100, ram_info)


# Function to convert RAM Bytes to Gigabytes
def bytes_to_gb(byte):
    one_gigabyte=1073741824
    giga=byte/one_gigabyte
    giga='{0:.2f}'.format(giga)
    return giga


data = disk_partitions(all=False)


def details(device_name):
    for i in data:
        if i.device == device_name:
            return i


# Function to return disk partitions
def get_disk_partitions():
    return [i.device for i in data]


# Function to return all disk info
def all_disk_info():
    return_all = []
    for i in get_disk_partitions():
        return_all.append(disk_info(i))
    return return_all


# Function to display disk information (of C: Drive)
def disk_info(device_name):

    disk_information = {}
    try:
        usage = disk_usage(device_name)
        disk_information['Disk']=device_name
        disk_information['Total']= f"{bytes_to_gb(usage.used + usage.free)} GB"
        disk_information['Used']= f"{bytes_to_gb(usage.used)} GB"
        disk_information['Free']= f"{bytes_to_gb(usage.free)} GB"
        disk_information['Percent']= f"{usage.percent}%"
    except PermissionError:
        pass
    except FileNotFoundError:
        pass
    info=details(device_name)
    disk_information.update({"Device":info.device})
    disk_information["Mount Point"]=info.mountpoint
    disk_information["FS-Type"]=info.fstype
    disk_information["Opts"]=info.opts

    return disk_information


# Creating label for "Quick Information"
quick_information_title = Label(window, text="Quick Information", font="Helvetica 18", fg='#FFFFFF', bg='#333333')
quick_information_title.place(x=10, y=180)

# Creating CPU usage title and placement
cpu_usage_title = Label(window, text="CPU Load", font="Helvetica 20", fg='#FFFFFF', bg='#000000')
cpu_usage_title.place(x=380, y=260)

# Creating label to show percentage of CPU utilization
cpu_usage_label = Label(window, bg='#000000', fg='#1AA7EC', font="Helvetica 22 bold", width=10)
cpu_usage_label.place(x=360, y=220)

# Creating RAM usage title and placement
ram_usage_title = Label(window, text="RAM Usage", font="Helvetica 20", fg='#FFFFFF', bg='#000000')
ram_usage_title.place(x=730, y=260)

# Creating label to show percentage of RAM utilization
ram_usage_label = Label(window, bg='#000000', fg='#1AA7EC', font="Helvetica 22 bold", width=10)
ram_usage_label.place(x=710, y=220)

# Creating label for "System Status"
system_status_title = Label(window, text="System Status", font="Helvetica 18", fg='#FFFFFF', bg='#333333')
system_status_title.place(x=10, y=400)

# Creating label area for the system status
system_status_label = Label(window, bg='#000000', fg='#FFFFFF', font='Helvetica 18', width=40)
system_status_label.place(x=160, y=480)

# Creating label for "Advanced CPU Information"
advanced_cpu_title = Label(window, text="Advanced CPU Information", font="Helvetica 18", fg='#FFFFFF', bg='#333333')
advanced_cpu_title.place(x=10, y=600)

# Creating title for CPU physical core count
core_cpu_title = Label(window, text="Physical Cores", font="Helvetica 18", fg='#FFFFFF', bg='#000000')
core_cpu_title.place(x=180, y=690)

# Creating label area for CPU physical core count
core_cpu_label = Label(window, bg='#000000', fg='#1AA7EC', font="Helvetica 20", width=10)
core_cpu_label.place(x=180, y=650)

# Creating title for CPU logical core count
logical_core_cpu_title = Label(window, text="Logical Cores", font="Helvetica 18", fg='#FFFFFF', bg='#000000')
logical_core_cpu_title.place(x=550, y=690)

# Creating label area for CPU logical core count
logical_core_cpu_label = Label(window, bg='#000000', fg='#1AA7EC', font="Helvetica 20", width=10)
logical_core_cpu_label.place(x=540, y=650)

# Creating title for CPU frequency
frequency_cpu_title = Label(window, text="CPU Speed", font="Helvetica 18", fg='#FFFFFF', bg='#000000')
frequency_cpu_title.place(x=910, y=690)

# Creating label area for CPU frequency
frequency_cpu_label = Label(window, bg='#000000', fg='#1AA7EC', font="Helvetica 20", width=10)
frequency_cpu_label.place(x=895, y=650)

# Creating label for "Advanced Disk Information" table
detailed_disk_title = Label(window, text="Advanced Disk Information", font="Helvetica 18", fg='#FFFFFF', bg='#333333')
detailed_disk_title.place(x=10, y=775)

# Creating the text area for disk information
detailed_disk_text_area = Text(window, bg="green", fg="yellow", width=85, height=6, font=("helvetica", 20))
detailed_disk_text_area.place(x=0, y=825)


if __name__ == '__main__':
    info = all_disk_info()
    _list = [i.values() for i in all_disk_info()]
    info_tabulated = tabulate(_list, headers=info[0].keys(), tablefmt="simple", missingval="-")
    v = 10
    detailed_disk_text_area.insert(END, info_tabulated)

    cpu_info()
    ram_info()
    window.mainloop()
