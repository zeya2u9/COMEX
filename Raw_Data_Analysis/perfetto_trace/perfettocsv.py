import os
from perfetto.trace_processor import TraceProcessor

def run_query_and_export(tp, table, output_path):
    query_result = tp.query(f'select * from {table};')
    query_result.as_pandas_dataframe().to_csv(output_path)

directory_path = '<Path to perfetto_traces>'

for app_trace_file in os.listdir(directory_path):
    trace_file_path = os.path.join(directory_path, app_trace_file)
    print(trace_file_path)
    # file = trace_file_path[:-5]
    output_folder = os.path.join("<Output folder for csvs>", app_trace_file)
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    with TraceProcessor(trace=trace_file_path) as tp:
        tp.query('INCLUDE PERFETTO MODULE android.dvfs;')
        tp.query('INCLUDE PERFETTO MODULE common.slices;')
        tp.query('INCLUDE PERFETTO MODULE android.anrs;')
        tp.query('INCLUDE PERFETTO MODULE android.battery;')
        tp.query('INCLUDE PERFETTO MODULE android.binder;')
        tp.query('INCLUDE PERFETTO MODULE android.io;')
        tp.query('INCLUDE PERFETTO MODULE android.monitor_contention;')
        tp.query('INCLUDE PERFETTO MODULE android.network_packets;')
        tp.query('INCLUDE PERFETTO MODULE android.process_metadata;')
        tp.query('INCLUDE PERFETTO MODULE android.statsd;')
        tp.query('INCLUDE PERFETTO MODULE linux.cpu_idle;')
        tp.query('INCLUDE PERFETTO MODULE pkvm.hypervisor;')
        tp.query('INCLUDE PERFETTO MODULE sched.thread_level_parallelism;')

        tables = ["android_dvfs_counters", "thread_slice", "process_slice", "android_anrs", 
                  "android_battery_charge","android_binder_metrics_by_process", 
                  "android_sync_binder_thread_state_by_txn", "android_sync_binder_blocked_functions_by_txn", 
                  "android_binder_txns", 
                  "android_monitor_contention", 
                  "android_monitor_contention_chain", "android_monitor_contention_chain_thread_state", 
                  "android_monitor_contention_chain_thread_state_by_txn", "android_monitor_contention_chain_blocked_functions_by_txn", 
                  "android_network_packets", "android_process_metadata", "android_statsd_atoms", "linux_cpu_idle_stats", 
                  "pkvm_hypervisor_events", "sched_runnable_thread_count", "sched_active_cpu_count"]

        for table in tables:
            output_path = os.path.join(output_folder, f'{app_trace_file}.{table}.csv')
            run_query_and_export(tp, table, output_path)

os.system("rm -rf <Path to perfetto_traces>")
print("Queries and exports complete.")
