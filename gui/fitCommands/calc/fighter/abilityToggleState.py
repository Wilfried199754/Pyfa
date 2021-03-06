import wx
from logbook import Logger

import eos.db
from service.fit import Fit


pyfalog = Logger(__name__)


class CalcToggleFighterAbilityStateCommand(wx.Command):

    def __init__(self, fitID, projected, position, effectID, forceState=None):
        wx.Command.__init__(self, True, 'Toggle Fighter Ability State')
        self.fitID = fitID
        self.projected = projected
        self.position = position
        self.effectID = effectID
        self.forceState = forceState
        self.savedState = None

    def Do(self):
        pyfalog.debug('Doing toggling of fighter ability {} state at position {} for fit {}'.format(self.effectID, self.position, self.fitID))
        fit = Fit.getInstance().getFit(self.fitID)
        container = fit.projectedFighters if self.projected else fit.fighters
        fighter = container[self.position]
        ability = next((fa for fa in fighter.abilities if fa.effectID == self.effectID), None)
        if ability is None:
            pyfalog.warning('Unable to find fighter ability')
            return False
        self.savedState = ability.active
        ability.active = not ability.active if self.forceState is None else self.forceState
        eos.db.commit()
        return True

    def Undo(self):
        pyfalog.debug('Unoing toggling of fighter ability {} state at position {} for fit {}'.format(self.effectID, self.position, self.fitID))
        cmd = CalcToggleFighterAbilityStateCommand(
            fitID=self.fitID,
            projected=self.projected,
            position=self.position,
            effectID=self.effectID,
            forceState=self.savedState)
        return cmd.Do()
