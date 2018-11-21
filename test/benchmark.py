import sys
import os
import time
import tracemalloc
sys.path.append("../data_backend")

from dataset import Dataset
import numpy as np

NUM_FREQ_BINS = 5000
NUM_SAMPLES = 10000

###################################
# SETUP
###################################
dataset = Dataset("./", "benchmark")

dataset.device.name = "Dummy device"
dataset.device.version = "1.0"

freq_bins = np.logspace(3, 9, NUM_FREQ_BINS)

if not "test" in dataset:
    dataset.create_subset("test", freq_bins, False)

###################################
# WRITE
###################################
print("Start writing %d Samples with %d bins each" %(NUM_SAMPLES, NUM_FREQ_BINS))
tracemalloc.start()
start_time = time.perf_counter()
for i in range(NUM_SAMPLES):
    dataset["test"].append_sample(
        time     = 8,
        spectrum = np.random.randn(NUM_FREQ_BINS)
    )
stop_time = time.perf_counter()
(current, peak) = tracemalloc.get_traced_memory()
print("Peak memory consumption: %.3f MiB" %(peak/1048576))
print("Done. Took %.3f seconds" %(stop_time - start_time))
print()
tracemalloc.stop()


###################################
# READ AND SUM
###################################
print("Start reading all samples (%d) and summing up the spectrum" % dataset["test"].len())
tracemalloc.start()
start_time = time.perf_counter()
sum = dataset["test"][:]["spectrum"].mean(1)
stop_time = time.perf_counter()
(current, peak) = tracemalloc.get_traced_memory()
print("Peak memory consumption: %.3f MiB" %(peak/1048576))
print("Done. Took %.3f seconds" %(stop_time - start_time))
print()
tracemalloc.stop()


###################################
# READ AND SUM (Chunked)
###################################
print("Start reading all (chunked) samples (%d) and summing up the spectrum" % dataset["test"].len())
tracemalloc.start()
start_time = time.perf_counter()

chunk_size = 1000
for i in range(int(dataset["test"].len()/chunk_size)):
    sum = dataset["test"][i*chunk_size:i*chunk_size+chunk_size]["spectrum"].mean(1)

stop_time = time.perf_counter()
(current, peak) = tracemalloc.get_traced_memory()
print("Peak memory consumption: %.3f MiB" %(peak/1048576))
print("Done. Took %.3f seconds" %(stop_time - start_time))
print()
tracemalloc.stop()

dataset.close()
