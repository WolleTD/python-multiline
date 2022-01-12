#!/usr/bin/env python3

import asyncio
import multiline
import signal
import sys


async def system_ml(cmd, ml_stream):
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    async def read_stream(stream, color='\033[0m'):
        # On EOL, stdout.readline() will return an empty string
        while True:
            line = (await stream.readline()).decode('utf-8')
            if len(line) == 0:
                break
            ml_stream.write(f'{color}{line}')

    red = '\033[31m'
    await asyncio.gather(read_stream(proc.stdout), read_stream(proc.stderr, red), proc.wait())
    return proc.returncode


async def do_setup(idx, serl, ml_stream):
    ret = await system_ml(f"./dummy.sh {idx}", ml_stream)
    if ret == 0:
        msg = "Setup complete!"
    else:
        msg = f"Failed with code {ret}!"
        [ml_stream.tail_msg(l) for l in ml_stream.lines]
    ml_stream.close(f"Serial {serl}: {msg}")
    return ret


def read_serials():
    num_cams = 6
    serls = {}
    while len(serls) < num_cams:
        for i in range(1, num_cams + 1):
            ser = 0
            while ser == 0:
                ser = int(input(f"Position {i} Serial: "))
                if not sys.stdin.isatty():
                    print(ser)
                if 0 < ser < 65536 and ser not in serls.values():
                    serls[i] = ser
                else:
                    print("Invalid/duplicate serial!")
                    ser = 0
        confirmation = input("Is this correct? [Y/n] ")
        if not sys.stdin.isatty():
            print(confirmation)
        if confirmation.lower() == "n":
            serls = {}
    return serls


async def system(cmd):
    proc = await asyncio.create_subprocess_shell(cmd)
    _, _ = await proc.communicate()
    return proc.returncode


async def cam_setup():
    # serials = read_serials()
    serials = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6}

    ml = multiline.create(sys.stderr)
    ml.start()

    ml.status("Checking for already configured cameras")
    for cam in serials:
        if await system(f"ping -c1 -w1 192.168.223.{cam} >/dev/null") == 0:
            state = "OK"
            del serials[cam]  # TODO: ERROR
        else:
            state = "Not set"
        ml[f"Position {cam}:"].title(f"Serial {serials[cam]}: {state}")

    current_serial = 0
    last_serial = 0
    setup_error = ""
    i = 1
    setup_tasks = []
    while len(serials) > 0:
        while last_serial == current_serial:
            await asyncio.sleep(1)
            current_serial = i
            i = i + 1

        ids = [i for i in serials if serials[i] == current_serial]
        if len(ids) != 1:
            setup_error = f"Error: {current_serial} is not in the list!"
            break
        idx = ids[0]
        stream = ml[f"Position {idx}:"]

        target_ip = f"192.168.223.{idx}"
        stream.write(f"Setting IP address to {target_ip}...")
        await asyncio.sleep(0.1)
        stream.write("Restarting network...")
        last_serial = current_serial
        del serials[idx]
        await asyncio.sleep(2)
        stream.title(f"Serial: {current_serial} IP OK")
        setup_tasks.append(asyncio.create_task(do_setup(idx, current_serial, stream)))

    ml.status(f"{setup_error}Waiting for unfinished jobs...")
    retcodes = await asyncio.gather(*setup_tasks)
    ml.status(f"Setups completed with: {retcodes}")
    await ml.stop()


async def main():
    """Load configuration and start rsync_forever loops for each parsed host.
    Setup signal handler and run until cancelled by signal.
    """

    def signal_handler():
        main_task.cancel()

    # Setup asyncio signal handler for SIGINT and SIGTERM
    # This is somehow required to make docker-compose gracefully stop
    loop = asyncio.get_running_loop()
    for sig in [signal.SIGINT, signal.SIGTERM]:
        loop.add_signal_handler(sig, signal_handler)

    main_task = asyncio.create_task(cam_setup())
    await main_task


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except asyncio.CancelledError:
        print("Cancelled")
