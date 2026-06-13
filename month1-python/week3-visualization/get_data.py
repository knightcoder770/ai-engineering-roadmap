import psutil
import GPUtil as gputil

class Get_Data():
    
    def overall_cpu_data():
        return psutil.cpu_percent(interval=1)
    
    def individual_core_data():
        cores=psutil.cpu_percent(interval=1,percpu=True)
        return cores
    
    def ram_data():
        return psutil.virtual_memory().percent
    
    def gpu_data():
        gpu=gputil.getGPUs()
        return gpu[0].load*100
    
    def gpu_temperature():
        gpu=gputil.getGPUs()   
        return gpu[0].temperature
        