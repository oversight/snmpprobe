from collections import Counter


def host_resources_mib(state_data):
    if 'processor' in state_data:
        cpus = [item.get('hrProcessorLoad', 0) for item in state_data['processor'].values()]
        aggr = sum(cpus) / len(cpus) if cpus else 0
        state_data['cpu'] = {'cpuAverage': {'name': 'cpuAverage', 'percentUsed': aggr}}

    if 'process' in state_data:
        procs = {}
        counts = Counter()
        for name, item in state_data['process'].items():
            runName = item.get('hrSWRunName')
            if runName is not None:
                item['idx'] = int(name.split('-')[-1])
                item['name'] = name_with_suffix = '{}#{}'.format(runName, counts[runName]) if counts[runName] > 0 else runName
                counts[runName] += 1
                procs[name_with_suffix] = item
        state_data['process'] = procs
        state_data['processCount'] = {'processCount': {'name': 'processCount', 'count': len(procs)}}
        counts.clear()

    if 'storage' in state_data:
        fs_types = {item.get('hrFSStorageIndex'): item.get('hrFSType') for item in state_data.pop('fs', {}).values()}
        for item in state_data['storage'].values():
            if 'hrStorageIndex' in item:
                item['hrFSType'] = fs_types.get(item['hrStorageIndex'])

            if 'hrStorageAllocationUnits' in item:
                total = item.get('hrStorageSize', 0) * item['hrStorageAllocationUnits']
                used = item.get('hrStorageUsed', 0) * item['hrStorageAllocationUnits']
                free = total - used
                free_percentage = 100 * free / total if total else None
                used_percentage = 100 * used / total if total else None
                item['hrStorageSizeInBytes'] = total
                item['hrStorageFreeInBytes'] = free
                item['hrStorageUsedInBytes'] = used
                item['hrStorageFreePercentage'] = free_percentage
                item['hrStorageUsedPercentage'] = used_percentage

    return state_data
