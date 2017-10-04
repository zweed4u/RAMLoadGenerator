import sys
import time
import psutil
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

class RAMLoad:
    def __init__(self, desired_load_average_percentage: int):
        """
        :param desired_load_average_percentage: the input from apogee config - ram usage average (0.0 - 100.0)
        """
        self.initial_ram_usage = psutil.virtual_memory().percent
        self.desired_load_average_percentage = desired_load_average_percentage
        self.mem_hog = None
        self.percent_displacement = None

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
        # big loop just for now
        while 1:
            print(self.get_current_memory_utilization().percent)
            # if current ram use is less than desired, find/calculate buffer - store var
            if self.get_current_memory_utilization().percent < self.desired_load_average_percentage:
                del self.mem_hog
                self.percentage_displacement = self.desired_load_average_percentage - self.get_current_memory_utilization().percent
                bytes_to_ram_load = int(self.get_current_memory_utilization().total * (self.percentage_displacement / 100))
                self.mem_hog = 'a' * bytes_to_ram_load
                logging.info('var created')

            # if current ram use is over desired - remove variable and see if we can do anything about it
            elif self.get_current_memory_utilization().percent > self.desired_load_average_percentage:
                logging.info('RAM load is already higher than provided - removing variable')
                self.free()
                # check if we can hit desired use by subtracting our original variable
                if self.get_current_memory_utilization().percent > self.desired_load_average_percentage:
                    logging.info('Even with variable deleted RAM usage is above specification')
                else:
                    logging.info('Resizing variable could result in desire RAM usage - resizing')
                    self.percentage_displacement = self.desired_load_average_percentage - self.get_current_memory_utilization().percent
                    bytes_to_ram_load = int(self.get_current_memory_utilization().total * (self.percentage_displacement / 100))
                    self.mem_hog = 'a' * bytes_to_ram_load

            else:
                logging.info('System memory load conditions have been met')
            time.sleep(5)

    def free(self):
        del self.mem_hog

t=RAMLoad(float(sys.argv[-1])).load()
