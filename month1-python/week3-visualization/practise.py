import psutil
import GPUtil

print(psutil.cpu_percent())
print(psutil.virtual_memory().percent)
gpu=GPUtil.getGPUs()
print(gpu[0].load*100)
print(gpu[0].temperature)  