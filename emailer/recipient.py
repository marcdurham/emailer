import dataclasses  # pylint: disable=wrong-import-order


@dataclasses.dataclass(frozen=True)
class Recipient():
  email: str = ''
  groups: tuple = ()
  highlights: tuple = ()
