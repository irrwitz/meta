import sqlite3
from collections import namedtuple
from datetime import datetime
from typing import Dict

DATE_FORMAT = '%Y-%m-%d %H:%M:%S.%f'
DownloadTask = namedtuple('DownloadTasks',
                          ['patient_id',
                           'accession_number',
                           'series_number',
                           'series_instance_uid',
                           'creation_time',
                           'execution_time',
                           'running_time',
                           'dir_name',
                           'status',
                           'exception'])

TransferTask = namedtuple('TransferTask',
                          ['study_id',
                           'creation_time',
                           'execution_time',
                           'running_time',
                           'status',
                           'exception'])


def download_task(conn, entry: Dict[str, str], dir_name: str) -> DownloadTask:
    """
    Creates a new download task with all the necessary fields set.
    """
    patient_id = entry['patient_id']
    accession_number = entry['accession_number']
    series_number = entry['series_number']
    series_instance_uid = entry['series_id']
    task = DownloadTask(patient_id=patient_id,
                        accession_number=accession_number,
                        series_instance_uid=series_instance_uid,
                        series_number=series_number,
                        dir_name=dir_name,
                        creation_time=datetime.now(),
                        execution_time=datetime.now(),
                        running_time=0.0,
                        status=None,
                        exception=None)
    _insert_download(conn, task)
    return task


def finish_task(conn, future):
    """
    Updates db with calculated execution times.
    """
    end = datetime.now()
    task = future.task._replace(
        execution_time=end,
        running_time=(end - future.task.creation_time).total_seconds(),
        exception=future.exception(),
        status='Successful' if future.exception() is None else 'Error')
    if isinstance(task, DownloadTask):
        update_download(conn, task)
    elif isinstance(task, TransferTask):
        update_transfer(conn, task)
    else:
        raise ValueError('Unknown task type {}'.format(type(task)))


def transfer_task(conn, study_id) -> TransferTask:
    """
    Creates a new transfer task with all the necessary fields set.
    """
    task = TransferTask(study_id=study_id,
                        creation_time=datetime.now(),
                        execution_time=datetime.now(),
                        running_time="0",
                        status=None,
                        exception=None)
    _insert_transfer(conn, task)
    return task


def select_download(conn):
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    result = []
    for row in cursor.execute('SELECT * FROM DOWNLOAD_TASKS LIMIT 1000'):
        result.append(row)
    return result


def _insert_download(conn, download):
    cursor = conn.cursor()
    # Cursor, Task -> None
    cursor.execute('INSERT INTO DOWNLOAD_TASKS VALUES (NULL,?,?,?,?,?,?,?,?,?)',
                   (download.patient_id,
                    download.accession_number,
                    download.series_number,
                    download.dir_name,
                    download.creation_time,
                    download.execution_time,
                    download.running_time,
                    download.status,
                    download.exception))
    conn.commit()
    return None


def select_transfer(conn):
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    result = []
    for row in cursor.execute('SELECT * FROM TRANSFER_TASKS LIMIT 1000'):
        result.append(row)
    return result


def _insert_transfer(conn, transfer):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO TRANSFER_TASKS VALUES (NULL,?,?,?,?,?,?)',
                   (transfer.study_id,
                    transfer.creation_time,
                    transfer.execution_time,
                    transfer.running_time,
                    transfer.status,
                    transfer.exception))
    conn.commit()
    return None


def update_download(conn, download):
    cursor = conn.cursor()
    cursor.execute('''
                    UPDATE DOWNLOAD_TASKS SET
                      execution_time=?,
                      running_time=?,
                      exception=?,
                      status=?
                    WHERE
                      study_instance_uid = ?
                    ''',
                   (download.execution_time,
                    download.running_time,
                    download.exception,
                    download.status,
                    download.study_instance_uid))
    conn.commit()
    return None


def update_transfer(conn, transfer):
    cursor = conn.cursor()
    cursor.execute('''
                   UPDATE TRANSFER_TASKS SET
                     execution_time=?,
                     running_time=?,
                     exception=?,
                     status=?
                    WHERE
                      study_id = ?''',
                   (transfer.execution_time,
                    transfer.running_time,
                    str(transfer.exception),
                    transfer.status,
                    transfer.study_id))
    conn.commit()
    return None
