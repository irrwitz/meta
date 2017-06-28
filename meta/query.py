import logging
from datetime import datetime

DEFAULT_PAYLOAD = {'offset': 0, 'limit': 100,
                   'query': '*:*',
                   'params': {'group': 'true', 'group.field': 'PatientID',
                              'group.limit': 1000, 'group.ngroups': 'true'},
                   'facet':
                       {'SeriesDescription':
                            {'type': 'terms', 'field': 'SeriesDescription'},
                        'StudyDescription':
                            {'type': 'terms', 'field': 'StudyDescription'}
                       }
                  }


def query_patient(patient, limit=100):
    """ Query list of patients with birthdate. """
    exact_body = query_patient_body()
    exact_body['query'] = _query_patient(patient, approx=False)
    approx_body = query_patient_body()
    approx_body['query'] = _query_patient(patient, approx=True)
    return (exact_body, approx_body)


def query_patient_body(limit=100):
    body = DEFAULT_PAYLOAD.copy()
    body['limit'] = limit
    body['offset'] = 0
    return body


def _query_patient(patient, approx=False):
    patient_id = _create_patient_id(patient.get('patient_id'))
    birthdate = _create_patient_birthdate(patient.get('birthdate'))
    full_name = patient.get('full_name', '')

    if approx:
        full_name = "PatientName:{}~".format(full_name).replace(' ', r'\^')
    else:
        full_name = "PatientName:{}".format(full_name).replace(' ', r'\^')

    cond = [c for c in [patient_id, birthdate, full_name] if c]
    return " OR ".join(cond)


def query_body(args, limit=100):
    """ Normal html form submit function is using this. """
    body = DEFAULT_PAYLOAD.copy()
    body['limit'] = limit
    body['query'] = args.get('query', '*:*')
    body['offset'] = args.get('offset', '0')

    date_range = _create_date_range(args.get('StartDate'), args.get('EndDate'))
    if date_range is not None:
        body['query'] = body['query'] + ' AND ' + date_range

    body['filter'] = _create_filter_query(args)
    return body


def _create_filter_query(args):
    result = [_filter('StudyDescription', args),
              _filter('SeriesDescription', args),
              _filter('PatientID', args),
              _filter('PatientName', args),
              _filter('AccessionNumber', args),
              _filter('Modality', args),
              _filter('InstitutionName', args)]
    return [x for x in result if x is not None]


def _filter(element, args):
    if args.get(element):
        return '{0}:{1}'.format(element, args.get(element))


def _create_patient_id(patient_id):
    if not patient_id:
        return None
    return 'PatientID:' + patient_id


def _create_patient_birthdate(birthdate):
    if not birthdate:
        return None
    return 'PatientBirthDate:' + _convert(birthdate)


def _create_date_range(start_date, end_date):
    if not (start_date or end_date):
        return None
    _start_date = _convert(start_date)
    _end_date = _convert(end_date)
    return 'StudyDate:[' + _start_date + ' TO ' + _end_date + ']'


def _convert(date):
    """
    Converts a date from the frontend which is passed in the following format
    31.12.2016 to 20161231. This is how it is stored in solr.
    """
    try:
        return datetime.strptime(date, '%d.%m.%Y').strftime('%Y%m%d')
    except ValueError:
        logging.warning('Could not parse date %s, setting it to "*"', date)
        return '*'
