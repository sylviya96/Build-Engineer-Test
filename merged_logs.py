import argparse
import json
from pathlib import Path

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Tool to merge test logs')
    parser.add_argument('loga_file', metavar='<path/to/log1>', type=str, help='Path to dir with generated loga')
    parser.add_argument('logb_file', metavar='<path/to/log2>', type=str, help='Path to dir with generated logb')
    parser.add_argument('-o', type=str, default='merged_log.jsonl', help='Path to dir with merged logs', dest='merged_log_file')

    return parser.parse_args()

def merge_logs(log_a: Path, log_b: Path, merged_logs: Path) -> None:
    print('merging logs...')
    with open(log_a, 'r') as log_a_file:
        with open(log_b, 'r') as log_b_file:
            with open(merged_logs, 'w') as merged_logs_file:
                line_from_a = log_a_file.readline()
                line_from_b = log_b_file.readline()
                while 1:
                    #есть обе строки
                    if line_from_a and line_from_b:
                        if json.loads(line_from_a).get('timestamp') <= json.loads(line_from_b).get('timestamp'):
                            merged_logs_file.write(line_from_a)
                            line_from_a = log_a_file.readline()
                        else:
                            merged_logs_file.write(line_from_b)
                            line_from_b = log_b_file.readline()
                    #есть строки только в первом файле
                    elif line_from_a and not line_from_b:
                        merged_logs_file.write(line_from_a)
                        line_from_a = log_a_file.readline()
                    #есть строки только во втором файле
                    elif not line_from_a and line_from_b:
                        merged_logs_file.write(line_from_b)
                        line_from_b = log_b_file.readline()
                    #строки закончились
                    else:
                        break


args = parse_args()
loga_path = Path(args.loga_file)
logb_path = Path(args.logb_file)
merged_log_path = Path(args.merged_log_file)

merge_logs(loga_path, logb_path, merged_log_path)

print('logs merged')