"""
Fild optin usage.
"""

from dataclasses import dataclass, field


@dataclass
class ClubMember:
    name: str
    # guests: list = [] # ValueError: mutable default <class 'list'> for field guests is not allowed:use default_factory
    guests: list = field(default_factory=list) # use filed and default_factory as default
    athlete: bool = field(default=False, repr=False)

"""
Post-init processing
"""
@dataclass
class HackClubMember(ClubMember):
    all_handles = set()
    handle: str = ''

    def __post_init__(self):
        cls = self.__class__
        if self.handle == '':
            self.handle = self.name.split()[0]
        if self.handle in cls.all_handles:
            msg = f'handle {self.handle} already exists.'
            raise ValueError(msg)
        cls.all_handles.add(self.handle)

anno = HackClubMember('Anna Ravenscroft', handle='AnnaRaven')
print(anno)

leo = HackClubMember('Leo Rochael')
print(leo)

# leo2 = HackClubMember('Leo DaVinci') # 默认操作导致handle重复，报错
leo2 = HackClubMember('Leo DaVinci', handle='Neo')
print(leo2)

print(HackClubMember.__doc__)
