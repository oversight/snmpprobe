import time


async def snmpping(snmp):
    """Note that the current lowest checkInterval may be 30 seconds and based
    on that value we create a global check timeout (.9 * checkInterval).
    This means the the lowest global check timeout is 27 seconds which is lower
    than the longest possible checkPingTime of 5 * 10 (50 seconds).
    This is not an issue, but may result in a "check time out" error instead of
    the normal result of this check.
    """
    n = 5
    oid = (1, 3, 6, 1, 2, 1, 1, 1, 0)
    response_times = []
    jitters = []
    dropped = 0
    timeout = 10
    for _ in range(n):
        t0 = time.time()
        try:
            await snmp.get(oid, timeout=timeout)
        except Exception:
            response_times.append(timeout)
            dropped += 1
        else:
            response_time = time.time() - t0
            if response_times:
                jitters.append(abs(response_time - response_times[-1]))
            response_times.append(response_time)

    itm = {
        'name': 'snmpping',
        'max': max(response_times),
        'min': min(response_times),
        'jitter': sum(jitters) / (n - 1 - dropped) if dropped < n - 1 else 0,
        'responseTime': sum(response_times) / n,
        'droppedCount': dropped
    }
    return {'snmpping': {'snmpping': itm}}
