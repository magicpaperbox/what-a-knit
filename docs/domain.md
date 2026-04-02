```python
from dataclasses import dataclass, field
from typing import Optional, Union
from enum import Enum, auto
from datetime import datetime

# ==========================================
# MODUŁ 0: SHARED KERNEL (Współdzielone)
# ==========================================

@dataclass(frozen=True)
class Mass:
    grams: float

    def __add__(self, other: 'Mass') -> 'Mass':
        return Mass(self.grams + other.grams)
        
    def __sub__(self, other: 'Mass') -> 'Mass':
        if self.grams - other.grams < 0:
            raise ValueError("Mass cannot be negative")
        return Mass(self.grams - other.grams)

@dataclass(frozen=True)
class Meters:
    value: float

@dataclass(frozen=True)
class Centimeters:
    value: float

class YarnWeightCategory(Enum):
    LACE = auto()
    FINGERING = auto()
    SPORT = auto()
    DK = auto()
    WORSTED = auto()
    ARAN = auto()
    BULKY = auto()


# ==========================================
# MODUŁ 1: YARN_INVENTORY (Magazyn Włóczek)
# ==========================================

class FiberType(Enum):
    MERINO = auto()
    ACRYLIC = auto()
    COTTON = auto()
    ALPACA = auto()
    NYLON = auto()
    SILK = auto()
    MOHAIR = auto()
    LINEN = auto()

@dataclass(frozen=True)
class YarnFiber:
    fiber_type: FiberType
    percentage: int

@dataclass(frozen=True)
class YarnDefinitionId:
    value: int

@dataclass
class YarnDefinition:
    id: YarnDefinitionId
    brand: str
    name: str
    color_shade: str
    composition: list[YarnFiber] 
    weight_category: YarnWeightCategory
    full_weight: Mass
    full_length: Meters

@dataclass(frozen=True)
class SkeinId:
    value: int

@dataclass
class Skein:
    id: SkeinId
    yarn_definition_id: YarnDefinitionId
    current_weight: Mass


# ==========================================
# MODUŁ 2: EQUIPMENT (Narzędzia)
# ==========================================

class ToolMaterial(Enum):
    WOOD = auto()
    METAL = auto()
    PLASTIC = auto()
    BAMBOO = auto()
    NYLON_WIRE = auto()

@dataclass(frozen=True)
class ToolId:
    value: int

class Tool:
    id: ToolId
    
# Crochet hooks
@dataclass(frozen=True)
class ShortCrochetHook(Tool):
    id: ToolId
    size_mm: float
    material: ToolMaterial

@dataclass(frozen=True)
class StraightTunisianCrochetHook:
    id: ToolId
    size_mm: float
    material: ToolMaterial

@dataclass(frozen=True)
class FixedCircularTunisianCrochetHook:
    id: ToolId
    size_mm: float
    material: ToolMaterial

# Needles
@dataclass(frozen=True)
class StraightNeedles:
    id: ToolId
    size_mm: float
    length: Centimeters
    material: ToolMaterial

@dataclass(frozen=True)
class FixedCircularNeedles:
    id: ToolId
    size_mm: float
    length: Centimeters
    material: ToolMaterial

@dataclass(frozen=True)
class InterchangeableCircularNeedleTips:
    id: ToolId
    size_mm: float
    material: ToolMaterial

@dataclass(frozen=True)
class DoublePointedNeedles:
    id: ToolId
    size_mm: float
    material: ToolMaterial

# Needles accessories
@dataclass(frozen=True)
class Cable:
    id: ToolId
    length: Centimeters
    material: ToolMaterial

Tool = Union[
    ShortCrochetHook, StraightNeedles, FixedCircularNeedles, 
    InterchangeableCircularNeedleTips, DoublePointedNeedles, Cable
]


# ==========================================
# MODUŁ 3: PATTERNS (Wzory i Schematy)
# ==========================================

class PatternDifficulty(Enum):
    BEGINNER = auto()
    INTERMEDIATE = auto()
    ADVANCED = auto()
    EXPERT = auto()

class ChartSymbol(Enum):
    EMPTY = auto()
    KNIT = auto()
    PURL = auto()
    YARN_OVER = auto()
    K2TOG = auto()
    SSK = auto()

@dataclass(frozen=True)
class Gauge:
    stitches: float
    rows: float
    width: Centimeters = Centimeters(10.0)
    height: Centimeters = Centimeters(10.0)

# --- Tool Requirements (ADT dla wymagań) ---
@dataclass(frozen=True)
class CircularNeedleRequirement:
    size_mm: float
    min_length: Centimeters
    max_length: Centimeters | None

@dataclass(frozen=True)
class StraightNeedleRequirement:
    size_mm: float

@dataclass(frozen=True)
class CrochetHookRequirement:
    size_mm: float

@dataclass(frozen=True)
class TunisianCrochetHookRequirement:
    size_mm: float

@dataclass(frozen=True)
class DoublePointedNeedleRequirement:
    size_mm: float

ToolRequirement = Union[
    CircularNeedleRequirement, StraightNeedleRequirement, 
    CrochetHookRequirement, TunisianCrochetHookRequirement, DoublePointedNeedleRequirement
]

@dataclass(frozen=True)
class PatternRequirements:
    possible_yarn_weights: list[YarnWeightCategory]
    allow_multicolor: bool = False
    total_weight: Optional[Mass] = None
    total_length: Optional[Meters] = None
    tool_requirements: list[ToolRequirement] = field(default_factory=list)

@dataclass(frozen=True)
class ChartId:
    value: int

@dataclass
class Chart:
    id: ChartId
    name: str
    grid_width: int
    grid_height: int
    grid_data: list[list[ChartSymbol]]

@dataclass(frozen=True)
class PatternId:
    value: int

@dataclass
class Pattern:
    id: PatternId
    name: str
    description: str
    requirements: PatternRequirements
    
    author: Optional[str] = None
    difficulty_level: Optional[PatternDifficulty] = None
    target_gauge: Optional[Gauge] = None
    
    charts: list[Chart] = field(default_factory=list)


# ==========================================
# MODUŁ 4: PROJECTS (Zarządzanie Projektami)
# ==========================================

class ProjectStatus(Enum):
    STARTED = auto()
    IN_PROGRESS = auto()
    FINISHED = auto()
    FROGGED = auto()

@dataclass(frozen=True)
class SkeinAllocation:
    skein_id: SkeinId
    allocated_mass: Mass

@dataclass
class ProjectLogEntry:
    date: datetime
    notes: str
    photo_urls: list[str] = field(default_factory=list)

@dataclass(frozen=True)
class ProjectId:
    value: int

@dataclass
class Project:
    id: ProjectId
    name: str
    status: ProjectStatus
    progress_percent: int
    
    pattern_id: Optional[PatternId] = None
    
    allocated_skeins: list[SkeinAllocation] = field(default_factory=list)
    assigned_tool_ids: list[ToolId] = field(default_factory=list)
    
    actual_gauge: Optional[Gauge] = None
    logs: list[ProjectLogEntry] = field(default_factory=list)
    
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None

    def frog(self):
        self.status = ProjectStatus.FROGGED
        self.progress_percent = 0
```