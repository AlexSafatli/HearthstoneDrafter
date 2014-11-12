import hearthstone

h = hearthstone.HearthstoneCollection()
for cardtype in h.cards:
    print cardtype
    for card in h.cards[cardtype]:
        print '\t' + card.toDebugString()
