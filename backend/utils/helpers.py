from datetime import datetime

def add_timestamp_to_report(report: dict) -> dict:
    """添加时间戳到报告"""
    report['timestamp'] = datetime.now().isoformat()
    return report
