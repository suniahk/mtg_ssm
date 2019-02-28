"""Card and set index container."""

import collections
from typing import Dict
from typing import List
from typing import Tuple
from uuid import UUID

from mtg_ssm.containers.bundles import ScryfallDataSet
from mtg_ssm.mtg import util
from mtg_ssm.scryfall.models import ScryCard
from mtg_ssm.scryfall.models import ScrySet


def name_card_sort_key(card: ScryCard) -> Tuple[str, int, str]:
    """Key function for sorting cards in a by-name list."""
    card_num, card_var = util.collector_int_var(card)
    return (card.set, card_num or 0, card_var or "")  # TODO: sort by set release date


def set_card_sort_key(card: ScryCard) -> Tuple[int, str]:
    """Key function for sorting cards in a by-set list."""
    card_num, card_var = util.collector_int_var(card)
    return (card_num or 0, card_var or "")


class ScryfallDataIndex:
    """Card and set indexes for scryfall data."""

    def __init__(self) -> None:
        self.id_to_card: Dict[UUID, ScryCard] = {}
        self.name_to_cards: Dict[str, List[ScryCard]] = {}
        self.setcode_to_cards: Dict[str, List[ScryCard]] = {}
        self.setcode_to_id_to_index: Dict[str, Dict[UUID, int]] = {}
        self.setcode_to_set: Dict[str, ScrySet] = {}

    def load_data(self, scrydata: ScryfallDataSet) -> None:
        """Load all cards and sets from a Scryfall data set."""
        self.id_to_card = {}
        self.setcode_to_id_to_index = {}
        self.setcode_to_set = {}

        name_to_unsorted_cards: Dict[str, List[ScryCard]] = collections.defaultdict(
            list
        )
        setcode_to_unsorted_cards: Dict[str, List[ScryCard]] = collections.defaultdict(
            list
        )

        for card in scrydata.cards:
            self.id_to_card[card.id] = card
            name_to_unsorted_cards[card.name].append(card)
            setcode_to_unsorted_cards[card.set].append(card)
        for set_ in scrydata.sets:
            self.setcode_to_set[set_.code] = set_

        for cards_list in name_to_unsorted_cards.values():
            cards_list.sort(key=name_card_sort_key)
        self.name_to_cards = dict(name_to_unsorted_cards)

        for setcode, cards_list in setcode_to_unsorted_cards.items():
            cards_list.sort(key=set_card_sort_key)
            self.setcode_to_id_to_index[setcode] = {
                c.id: i for i, c in enumerate(cards_list)
            }
        self.setcode_to_cards = dict(setcode_to_unsorted_cards)
