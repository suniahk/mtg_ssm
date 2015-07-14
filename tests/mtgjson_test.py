"""Tests for mtgcdb.mtgjson"""

import datetime

from mtgcdb import models
from mtgcdb import mtgjson

from tests import mtgjson_testcase
from tests import sqlite_testcase


class MtgjsonTest(
        sqlite_testcase.SqliteTestCase, mtgjson_testcase.MtgJsonTestCase):

    def setUp(self):
        super().setUp()
        connection = self.engine.connect()
        models.Base.metadata.create_all(connection)
        connection.close()

    def test_create_set(self):
        # Setup
        set_data = self.mtg_data['ISD']

        # Execute
        mtgjson.update_set(self.session, set_data)
        self.session.commit()

        # Verify
        [card_set] = self.session.query(models.CardSet).all()
        self.assertEqual('ISD', card_set.code)
        self.assertEqual('Innistrad', card_set.name)
        self.assertEqual(datetime.date(2011, 9, 30), card_set.release_date)
        self.assertEqual('expansion', card_set.type)
        self.assertFalse(card_set.online_only)
        self.assertEqual('Innistrad', card_set.block)
        self.assertEqual([], card_set.cards)

    def test_update_set(self):
        # Setup
        self.session.add(models.CardSet(code='ISD', name='Bunk'))
        self.session.commit()
        set_data = self.mtg_data['ISD']

        # Execute
        mtgjson.update_set(self.session, set_data)
        self.session.commit()

        # Verify
        [card_set] = self.session.query(models.CardSet).all()
        self.assertEqual('ISD', card_set.code)
        self.assertEqual('Innistrad', card_set.name)
        self.assertEqual(datetime.date(2011, 9, 30), card_set.release_date)
        self.assertEqual('expansion', card_set.type)
        self.assertFalse(card_set.online_only)
        self.assertEqual('Innistrad', card_set.block)
        self.assertEqual([], card_set.cards)

    def test_online_only(self):
        # Execute
        isd_set = mtgjson.update_set(self.session, self.mtg_data['ISD'])
        vma_set = mtgjson.update_set(self.session, self.mtg_data['VMA'])

        # Verify
        self.assertTrue(vma_set.online_only)
        self.assertFalse(isd_set.online_only)

    def test_create_card(self):
        # Setup
        set_data = self.mtg_data['ISD']
        mtgjson.update_set(self.session, set_data)
        self.session.commit()
        card_data = set_data['cards'][0]

        # Execute
        mtgjson.update_card(self.session, card_data, 'ISD')
        self.session.commit()

        # Verify
        [card] = self.session.query(models.Card).all()
        self.assertEqual('Abattoir Ghoul', card.name)
        self.assertEqual('ISD', card.set_code)
        self.assertEqual('85', card.set_number)
        self.assertEqual(222911, card.multiverseid)
        self.assertEqual('Volkan Baga', card.artist)

    def test_update_card(self):
        # Setup
        set_data = self.mtg_data['ISD']
        mtgjson.update_set(self.session, set_data)
        self.session.add(models.Card(
            name='Abattoir Ghoul', set_code='ISD', set_number='85',
            multiverseid=222911, artist='Hokum'))
        self.session.commit()
        card_data = set_data['cards'][0]

        # Execute
        mtgjson.update_card(self.session, card_data, 'ISD')
        self.session.commit()

        # Verify
        [card] = self.session.query(models.Card).all()
        self.assertEqual('Abattoir Ghoul', card.name)
        self.assertEqual('ISD', card.set_code)
        self.assertEqual('85', card.set_number)
        self.assertEqual(222911, card.multiverseid)
        self.assertEqual('Volkan Baga', card.artist)

    def test_card_properties(self):
        # Setup
        set_data = self.mtg_data['ISD']
        card_data = set_data['cards'][1]
        mtgjson.update_set(self.session, set_data)
        mtgjson.update_card(self.session, card_data, 'ISD')
        self.session.commit()

        # Verify
        [card] = self.session.query(models.Card).all()
        self.assertEqual('Delver of Secrets', card.name)
        self.assertEqual('51a', card.set_number)
        self.assertEqual(51, card.set_integer)
        self.assertEqual('a', card.set_variant)

    def test_card_properties_null(self):
        # Setup
        set_data = self.mtg_data['S00']
        card_data = set_data['cards'][0]
        mtgjson.update_set(self.session, set_data)
        mtgjson.update_card(self.session, card_data, 'S00')
        self.session.commit()

        # Verify
        [card] = self.session.query(models.Card).all()
        self.assertEqual('Rhox', card.name)
        self.assertEqual(None, card.set_number)
        self.assertEqual(None, card.set_integer)
        self.assertEqual(None, card.set_variant)

    def test_update_models(self):
        # Execute
        mtgjson.update_models(self.session, self.mtg_data)
        self.session.commit()

        # Verify
        cards = self.session.query(models.Card).all()
        set_card_mv_number = [
            (c.set_code, c.name, c.multiverseid, c.set_number)
            for c in cards]
        expected = [
            ('LEA', 'Air Elemental', 94, None),
            ('LEA', 'Forest', 288, None),
            ('LEA', 'Forest', 289, None),
            ('ICE', 'Forest', 2746, None),
            ('ICE', 'Forest', 2747, None),
            ('ICE', 'Forest', 2748, None),
            ('ICE', 'Snow-Covered Forest', 2749, None),
            ('HML', 'Cemetery Gate', 2913, None),
            ('HML', 'Cemetery Gate', 2914, None),
            ('S00', 'Rhox', None, None),
            ('pMGD', 'Black Sun\'s Zenith', None, '7'),
            ('HOP', 'Academy at Tolaria West', 198073, '1'),
            ('HOP', 'Akroma\'s Vengeance', 205366, '1'),
            ('ARC', 'All in Good Time', 212648, '1'),
            ('ARC', 'Leonin Abunas', 220527, '1'),
            ('ISD', 'Abattoir Ghoul', 222911, '85'),
            ('ISD', 'Delver of Secrets', 226749, '51a'),
            ('ISD', 'Insectile Aberration', 226755, '51b'),
            ('PC2', 'Akoum', 226512, '9'),
            ('PC2', 'Armored Griffin', 271234, '1'),
            ('PC2', 'Chaotic Æther', 226509, '1'),
            ('PC2', 'Stairs to Infinity', 226521, 'P1'),
            ('VMA', 'Academy Elite', 382835, '55'),
        ]
        self.assertCountEqual(expected, set_card_mv_number)