from peerplays.instance import BlockchainInstance
from .exceptions import BettingMarketGroupDoesNotExistException
from .blockchainobject import BlockchainObject


class BettingMarketGroup(BlockchainObject):
    """ Read data about a Betting Market Group on the chain

        :param str identifier: Identifier
        :param peerplays blockchain_instance: PeerPlays() instance to use when
            accesing a RPC

    """
    type_id = 20

    def refresh(self):
        data = self.blockchain.rpc.get_object(self.identifier)
        if not data:
            raise BettingMarketGroupDoesNotExistException(self.identifier)
        super(BettingMarketGroup, self).__init__(data)
        self.cached = True

    @property
    def event(self):
        from .event import Event
        return Event(self["event_id"])

    @property
    def bettingmarkets(self):
        from .bettingmarket import BettingMarkets
        return BettingMarkets(self["id"])


class BettingMarketGroups(list):
    """ List of all available BettingMarketGroups

        :param strevent_id: Event ID (``1.18.xxx``)
    """
    def __init__(self, event_id, *args, **kwargs):
        BlockchainInstance.__init__(self, *args, **kwargs)
        self.bettingmarketgroups = self.blockchain.rpc.list_betting_market_groups(
            event_id)

        super(BettingMarketGroups, self).__init__([
            BettingMarketGroup(
                x, lazy=True, blockchain_instance=self.blockchain)
            for x in self.bettingmarketgroups
        ])
