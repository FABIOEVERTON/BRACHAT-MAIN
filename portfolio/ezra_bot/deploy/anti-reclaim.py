#!/usr/bin/env python3
import os, random, sys, threading, time

MEM_MB = 200
LO_CORE = max(1, (os.cpu_count() or 1) - 1)

def cpu_burn(seconds):
    end = time.monotonic() + seconds
    x = 12345
    while time.monotonic() < end:
        x = (x * 1103515245 + 12345) & 0x7FFFFFFF

def mem_burn(seconds, mb):
    buf = bytearray(mb * 1024 * 1024)
    idx = 0
    end = time.monotonic() + seconds
    while time.monotonic() < end:
        buf[idx] = (buf[idx] + 1) & 0xFF
        idx = (idx + 1) % len(buf)

def main():
    while True:
        time.sleep(random.uniform(60, 240))
        burst = random.uniform(20, 40)
        threads = [threading.Thread(target=cpu_burn, args=(burst,), daemon=True) for _ in range(LO_CORE)]
        threads.append(threading.Thread(target=mem_burn, args=(burst, MEM_MB), daemon=True))
        for t in threads: t.start()
        for t in threads: t.join()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(0)
