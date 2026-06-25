import shutil, os
DIR = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(DIR, "disk_report.txt")

def gb(b): return b / 1024**3

def get_usage(p="/"):
    u = shutil.disk_usage(p)
    return {"t": gb(u.total), "u": gb(u.used), "f": gb(u.free), "p": round((u.used/u.total)*100)}

def main():
    d = get_usage()
    for l in [f"Total: {d['t']:.1f} GiB", f"Used:  {d['u']:.1f} GiB", f"Free:  {d['f']:.1f} GiB", f"Usage: {d['p']}%"]:
        print(l)
    with open(REPORT, "w") as f:
        f.write("Disk Usage Report\n")
        for l in [f"Total: {d['t']:.1f} GiB", f"Used:  {d['u']:.1f} GiB", f"Free:  {d['f']:.1f} GiB", f"Usage: {d['p']}%\n"]:
            f.write(l + "\n")

if __name__ == "__main__":
    main()
