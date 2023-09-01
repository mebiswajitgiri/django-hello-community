bind = "0.0.0.0:8000"  # Use 0.0.0.0 to listen on all available network interfaces
workers = 4  # Number of worker processes
threads = 2  # Number of threads per worker
worker_class = "sync"  # Use sync worker type for simplicity
