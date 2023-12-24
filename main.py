from toPDF import *
import time
start_time = time.time()

create_certificate("Чувилко Илья Романович", "64524293", "30.03.2023", "24.12.2023")






end_time = time.time()
execution_time = end_time - start_time
print(f"Программа выполнена за {execution_time} секунд")
