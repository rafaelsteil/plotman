import csv
import sys
from plotman.log_parser import PlotLogParser

def export(logfilenames, save_to = None):
    if save_to is None:
        __send_to_stdout(logfilenames)
    else:
        __save_to_file(logfilenames, save_to)

def __save_to_file(logfilenames, filename: str):
    with open(filename, 'w') as file:
        __generate(logfilenames, file)

def __send_to_stdout(logfilenames):
    __generate(logfilenames, sys.stdout)

def __generate(logfilenames, out):
    writer = csv.writer(out)
    writer.writerow([
        'Plot ID', 
        'Start date',
        'Size',
        'Buffer',
        'Buckets',
        'Threads',
        'Tmp dir 1',
        'Tmp dir 2',
        'Phase 1 duration (raw)',
        'Phase 1 duration',
        'Phase 1 duration (minutes)',
        'Phase 1 duration (hours)',
        'Phase 2 duration (raw)',
        'Phase 2 duration',
        'Phase 2 duration (minutes)',
        'Phase 2 duration (hours)',
        'Phase 3 duration (raw)',
        'Phase 3 duration',
        'Phase 3 duration (minutes)',
        'Phase 3 duration (hours)',
        'Phase 4 duration (raw)',
        'Phase 4 duration',
        'Phase 4 duration (minutes)',
        'Phase 4 duration (hours)',
        'Total time (raw)',
        'Total time',
        'Total time (minutes)',
        'Total time (hours)',
        'Copy time (raw)',
        'Copy time',
        'Copy time (minutes)',
        'Copy time (hours)',
        'Filename'
    ])

    parser = PlotLogParser()

    for filename in logfilenames:
        info = parser.parse(filename)
        
        if info.is_empty():
            continue

        writer.writerow([
            info.plot_id,
            info.started_at,
            info.plot_size,
            info.buffer,
            info.buckets,
            info.threads,
            info.tmp_dir1,
            info.tmp_dir2,
            info.phase1_duration_raw,
            info.phase1_duration,
            info.phase1_duration_minutes,
            info.phase1_duration_hours,
            info.phase2_duration_raw,
            info.phase2_duration,
            info.phase2_duration_minutes,
            info.phase2_duration_hours,
            info.phase3_duration_raw,
            info.phase3_duration,
            info.phase3_duration_minutes,
            info.phase3_duration_hours,
            info.phase4_duration_raw,
            info.phase4_duration,
            info.phase4_duration_minutes,
            info.phase4_duration_hours,
            info.total_time_raw,
            info.total_time,
            info.total_time_minutes,
            info.total_time_hours,
            info.copy_time_raw,
            info.copy_time,
            info.copy_time_minutes,
            info.copy_time_hours,
            info.filename
        ])
