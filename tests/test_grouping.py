import unittest
from meta.grouping import group

TEST_DATA_1 = {'groups': [
        {'groupValue': 'ABC',
        'doclist': {'numFound': 1, 'start': 0,
                    'docs': [
                        {
                            'AccessionNumber': '1',
                            'StudyID': '1',
                        }
                    ]}
        },
        {
            'groupValue': 'DEF',
            'doclist': {'numFound': 1, 'start': 0,
                        'docs': [
                            {
                                'AccessionNumber': '3',
                                'StudyID': '20725498'}
                        ]}
        }
    ]}

TEST_DATA = {'groups': [
    {'groupValue': 'ABC',
     'doclist': {'numFound': 3, 'start': 0,
                 'docs': [
                     {
                         'AccessionNumber': '1',
                         'StudyID': '1',
                     },
                     {
                         'AccessionNumber': '2',
                         'StudyID': '2',
                     },
                     {
                         'AccessionNumber': '2',
                         'StudyID': '2'
                     }
                 ]}
    },
    {
        'groupValue': 'DEF',
        'doclist': {'numFound': 3, 'start': 0,
                    'docs': [
                        {
                            'AccessionNumber': '3',
                            'StudyID': '20725498'},
                        {
                            'AccessionNumber': '3',
                            'StudyID': '20725498'},
                        {
                            'AccessionNumber': '3',
                            'StudyID': '20725498',
                        }
                    ]}
    }]}



class TestGroupingStuff(unittest.TestCase):


    def test_grouping1(self):
        result = group(TEST_DATA_1)
        # same group size as before
        groups = result['groups']
        self.assertEqual(2, len(groups))
        # has grouped docs
        self.assertTrue('by_AccessionNumber' in groups[0])
        self.assertTrue('by_AccessionNumber' in groups[1])


    def test_grouping(self):
        result = group(TEST_DATA)
        # same group size as before
        groups = result['groups']
        self.assertEqual(2, len(groups))
        # has grouped docs
        self.assertTrue('by_AccessionNumber' in groups[0])
        self.assertTrue('by_AccessionNumber' in groups[1])



