from modules.units.meters import Meters
from modules.yarn.domain import Skein, Yarn, YarnId, SkeinId
from modules.yarn.repository import YarnRepository, SkeinRepository


class YarnNotFoundError(Exception):
    pass


class SkeinNotFoundError(Exception):
    pass


class YarnService:
    def __init__(self):
        self._yarn_repo = YarnRepository()
        self._skein_repo = SkeinRepository()

    # --- Yarn operations ---

    def get_all_yarns(self) -> list[Yarn]:
        return self._yarn_repo.get_all()

    def get_yarn(self, yarn_id: YarnId) -> Yarn:
        yarn = self._yarn_repo.get_by_id(yarn_id)
        if yarn is None:
            raise YarnNotFoundError(f"Yarn id {yarn_id} doesn't exist.")
        return yarn

    def add_yarn(self, yarn: Yarn) -> Yarn:
        yarn.validate()
        return self._yarn_repo.add(yarn)

    def update_yarn(self, yarn: Yarn) -> None:
        yarn.validate()
        self._yarn_repo.update(yarn)

    def delete_yarn(self, yarn_id: YarnId) -> None:
        self.get_yarn(yarn_id)
        skeins = self._skein_repo.get_by_yarn_id(yarn_id)
        for skein in skeins:
            self._skein_repo.delete(skein.id)
        self._yarn_repo.delete(yarn_id)

    # --- Skein operations ---

    def get_skein(self, skein_id: SkeinId) -> Skein:
        skein = self._skein_repo.get_by_id(skein_id)
        if skein is None:
            raise SkeinNotFoundError(f"Skein id {skein_id} doesn't exist.")
        return skein

    def get_skeins_for_yarn(self, yarn_id: YarnId) -> list[Skein]:
        return self._skein_repo.get_by_yarn_id(yarn_id)

    def add_skein(self, skein: Skein) -> Skein:
        yarn = self.get_yarn(skein.yarn_id)
        skein.validate(yarn)
        return self._skein_repo.add(skein)

    def update_skein(self, skein: Skein) -> None:
        yarn = self.get_yarn(skein.yarn_id)
        skein.validate(yarn)
        self._skein_repo.update(skein)

    def delete_skein(self, skein_id: SkeinId) -> YarnId:
        skein = self.get_skein(skein_id)
        self._skein_repo.delete(skein_id)
        return skein.yarn_id
