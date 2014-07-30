import json
import unittest

import api
import models


class CardBulkExportTest(unittest.TestCase):
    def _to_json(self, card):
        return api._JSONCardArchive(cards=[card]).to_json()

    def assert_json(self, first, second):
        """Assert JSON matches, ignoring key order."""
        first_json = json.dumps(json.loads(first), sort_keys=True, indent=2)
        second_json = json.dumps(json.loads(second), sort_keys=True, indent=2)
        self.assertMultiLineEqual(first_json, second_json)

    def assert_card_json(self, card, front='', back='',
                         input_format='text', tags=None):
        """Assert that card serializes to JSON with the given properties."""
        card_obj = {'front': front,
                    'back': back,
                    'input_format': input_format,
                    }
        if tags is not None:
            card_obj['tags'] = tags

        expected = json.dumps({'format': 'JSONCardArchive',
                               'version': 'v1',
                               'cards': [card_obj],
                               })
        self.assert_json(expected, self._to_json(card))

    def test_empty_properties(self):
        # Default values.
        self.assert_card_json(models.Card(), front='', back='',
                              input_format='text', tags=None)

        # Null handling. Setting "tags" to None is an error in NDB, though.
        card = models.Card(front=None, back=None, input_format=None, tags=[])
        self.assert_card_json(card, front='', back='',
                              input_format='text', tags=None)

    def test_no_cards(self):
        self.assert_json(
            api._JSONCardArchive().to_json(),
            '{"cards": [], "version": "v1", "format": "JSONCardArchive"}')

    def test_simple_card(self):
        kwargs = {'front': 'Hello', 'back': 'World', 'tags': ['in-text']}
        self.assert_card_json(models.Card(**kwargs), **kwargs)

        # Now again but with markdown.
        kwargs = {'front': 'Hello\n====', 'back': '* World',
                  'tags': ['in-text'], 'input_format': 'markdown'}
        self.assert_card_json(models.Card(**kwargs), **kwargs)
