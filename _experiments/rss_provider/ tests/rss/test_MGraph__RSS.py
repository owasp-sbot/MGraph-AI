from unittest                                      import TestCase
from typing                                        import Dict, Any
from datetime                                      import datetime, timezone

from mgraph_ai.providers.rss.MGraph__RSS__Test_Data import MGraph__RSS__Test_Data
from osbot_utils.utils.Dev import pprint

from osbot_utils.helpers.xml.rss.RSS__Feed__Parser import RSS__Feed__Parser

from mgraph_ai.providers.rss.MGraph__RSS           import MGraph__RSS
from mgraph_ai.providers.json.MGraph__Json         import MGraph__Json

from osbot_utils.testing.Duration                   import Duration

class test_MGraph_RSS(TestCase):

    def setUp(self):
        self.test_data  = MGraph__RSS__Test_Data().test_rss_data()
        self.rss_feed   = RSS__Feed__Parser().from_dict(self.test_data)
        self.mgraph_json = MGraph__Json()
        self.mgraph_rss  = MGraph__RSS()

        self.mgraph_rss.load_rss(self.rss_feed)

    def test__setUp(self):
        with self.mgraph_rss as _:
            assert type(_) is MGraph__RSS
            pprint(self.test_data)
            pprint(_.rss_feed.json())

    def test_init(self):                                                  # Test initialization
        self.assertIsInstance(self.mgraph_rss         , MGraph_RSS  )
        self.assertIsInstance(self.mgraph_rss.rss_feed, RSS__Feed)
        self.assertIsInstance(self.mgraph_rss.graph   , MGraph__Json)

    def test_properties(self):                                            # Test property access
        self.assertEqual(self.mgraph_rss.title      , 'Test RSS Feed')
        self.assertEqual(self.mgraph_rss.description, 'Test RSS Feed')
        self.assertEqual(len(self.mgraph_rss.items) , 2              )

    def test_find_items_by_category(self):                               # Test category search
        security_items = self.mgraph_rss.find_items_by_category('security')
        self.assertEqual(len(security_items), 2)

        identity_items = self.mgraph_rss.find_items_by_category('identity')
        self.assertEqual(len(identity_items), 1)
        self.assertEqual(identity_items[0]['guid'], 'test-guid-001')

    def test_find_items_by_date_range(self):                             # Test date range search
        start_date = datetime.fromtimestamp(1737627800, tz=timezone.utc)
        end_date   = datetime.fromtimestamp(1737631300, tz=timezone.utc)

        items = self.mgraph_rss.find_items_by_date_range(start_date, end_date)
        self.assertEqual(len(items), 2)

    def test_find_items_by_author(self):                                 # Test author search
        items = self.mgraph_rss.find_items_by_author('test_author')
        self.assertEqual(len(items), 2)

        items = self.mgraph_rss.find_items_by_author('non_existent')
        self.assertEqual(len(items), 0)

    def test_get_all_categories(self):                                   # Test category listing
        categories = self.mgraph_rss.get_all_categories()
        self.assertEqual(set(categories), {'security', 'identity', 'vulnerability'})

    def test_get_item_by_guid(self):                                     # Test GUID lookup
        item = self.mgraph_rss.get_item_by_guid('test-guid-001')
        self.assertIsNotNone(item)
        self.assertEqual(item['title'], 'Test Article 1')

        item = self.mgraph_rss.get_item_by_guid('non-existent')
        self.assertIsNone(item)

    def test_to_json(self):                                              # Test JSON export
        json_str = self.mgraph_rss.to_json()
        self.assertIsInstance(json_str, str)
        self.assertIn('Test RSS Feed', json_str)
        self.assertIn('test-guid-001', json_str)

    def test_to_rss(self):                                               # Test RSS export
        with self.assertRaises(NotImplementedError):
            self.mgraph_rss.to_rss()

    def test_performance(self):                                          # Test performance
        with Duration(max_seconds=1) as duration:                        # Operations should complete in < 1s
            self.mgraph_rss.get_all_categories()
            self.mgraph_rss.find_items_by_category('security')
            self.mgraph_rss.find_items_by_author('test_author')
            self.mgraph_rss.to_json()