import psutil
import sys
import logging


class RAMLoad:
    def __init__(self, desired_load_average_percentage: int):
        """
        :param desired_load_average_percentage: the input from apogee config - ram usage average (0.0 - 100.0)
        """
        self.desired_load_average_percentage = desired_load_average_percentage
        self.mem_hog = None

    def get_current_memory_utilization(self):
        """
        Returns the average utilization of system memory in bytes
        :return: tuple with various attr
        """
        return psutil.virtual_memory()

    def load(self):
        """
        Declare long string to chew up memory - calculated
        :return:
        """
        if self.get_current_memory_utilization().percent < self.desired_load_average_percentage:
            percentage_displacement = self.desired_load_average_percentage - self.get_current_memory_utilization().percent
            bytes_to_ram_load = int(self.get_current_memory_utilization().total * (percentage_displacement / 100))
            self.mem_hog = 'a' * bytes_to_ram_load

        elif self.get_current_memory_utilization().percent > self.desired_load_average_percentage:
            # free mem here somehow
            print('System is already under higher load than provided')

        else:
            print('System memory load conditions have been met')

    def free(self):
        del self.mem_hog

test = RAMLoad(float(sys.argv[-1]))
print(test.get_current_memory_utilization().percent)
test.load()
print(test.get_current_memory_utilization().percent)
while 1:
    # this is to just keep the script running so that the var is held in mem
    pass
