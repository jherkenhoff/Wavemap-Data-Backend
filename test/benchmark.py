import sys
import os
import time
import tracemalloc
sys.path.append("../")

from data_backend.dataset import Dataset
import numpy as np

def do_benchmark(name, num_freq_bins, num_samples, dtype):
    print("###################################################")
    print("Starting benchmark '%s' (%d freq bins, %d samples, dtype=%s)" %(name, num_freq_bins, num_samples, dtype))
    print("###################################################")
    ###################################
    # DATASET SETUP
    ###################################
    dataset = Dataset("./", name)

    dataset.device.name = "Benchmark Data Generator"
    dataset.device.version = "1.0"

    freq_bins = np.logspace(3, 9, num_freq_bins)

    if not "test" in dataset:
        dataset.create_subset("test", freq_bins, False, dtype=dtype)

    ###################################
    # WRITE
    ###################################
    print("Start writing %d Samples with %d bins each" %(num_samples, num_freq_bins))
    tracemalloc.start()
    start_time = time.perf_counter()
    for i in range(num_samples):
        dataset["test"].append_sample(
            time     = np.datetime64("now"),
            spectrum = np.random.random(num_freq_bins) * 30 - 80
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
    sum = dataset["test"].spectrum[:].sum(1)
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

    chunk_size = 100
    for i in range(int(dataset["test"].len()/chunk_size)):
        sum = dataset["test"].spectrum[i*chunk_size:i*chunk_size+chunk_size].sum(1)

    stop_time = time.perf_counter()
    (current, peak) = tracemalloc.get_traced_memory()
    print("Peak memory consumption: %.3f MiB" %(peak/1048576))
    print("Done. Took %.3f seconds" %(stop_time - start_time))
    print()
    tracemalloc.stop()

    dataset.close()


if __name__ == '__main__':
    do_benchmark("benchmark1", 10000, 10000, np.float64)
    do_benchmark("benchmark2", 10000, 10000, np.float32)
    do_benchmark("benchmark3", 10000, 10000, np.uint16)
    do_benchmark("benchmark4", 10000, 10000, np.uint8)
