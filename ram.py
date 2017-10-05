import psutil
import logging
import threading

class RAMLoad(threading.Thread):
    def __init__(self, desired_load_average_percentage: int):
        """
        :param desired_load_average_percentage: the input from apogee config - ram usage average (0.0 - 100.0)
        """
        super().__init__()
        self.daemon = True
        self.running = True
        self.initial_ram_usage = psutil.virtual_memory().percent
        self.desired_load_average_percentage = desired_load_average_percentage
        self.mem_hog = ''
        self.percent_displacement = None
        self.start()

    def get_current_memory_utilization(self):
        """
        Returns the average utilization of system memory in bytes
        :return: tuple with various attr
        """
        return psutil.virtual_memory()

    def calculate_buffer_bytes(self):
        """
        Used to calculate the needed number of bytes to fill RAM to specifications
        :return: int - number of bytes
        """
        self.percentage_displacement = self.desired_load_average_percentage - self.get_current_memory_utilization().percent
        bytes_to_ram_load = int(self.get_current_memory_utilization().total * (self.percentage_displacement / 100))
        return bytes_to_ram_load

    def run(self):
        """
        Declare long string to chew up memory - calculated
        :return:
        """
        while self.running:
            if self.get_current_memory_utilization().percent < self.desired_load_average_percentage:
                logging.info('RAM usage is below desired load - adjusting variable')
                self.mem_hog += 'a' * self.calculate_buffer_bytes()

            elif self.get_current_memory_utilization().percent > self.desired_load_average_percentage:
                logging.info('RAM load is higher than desired - removing variable')
                self.free()
                if self.get_current_memory_utilization().percent > self.desired_load_average_percentage:
                    logging.info('Even with variable deleted RAM usage is above specification')
                else:
                    logging.info('Resizing variable could result in desire RAM usage - resizing')
                    self.mem_hog = 'a' * self.calculate_buffer_bytes()

            else:
                logging.info('System memory load conditions have been met')

    def free(self):
        """
        Delete the variable that is used to take up space
        :return:
        """
        del self.mem_hog

RAMLoad(33.3)
