import bluetooth

nearby_devices = bluetooth.discover_devices(duration = 10, lookup_names = True, flush_cache = True)

for addr, name in nearby_devices:
    print(f"Name : {name} | Address : {addr}")

