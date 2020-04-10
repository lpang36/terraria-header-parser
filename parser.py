from collections import OrderedDict
import math

from utils import *


class Element:
    def load(self, f):
        pass

    def store(self, f):
        pass


class Primitive(Element):
    def __init__(self, value=None):
        self.value = value

    def load(self, f):
        self.value = self._load(f)
        return f.tell()

    def store(self, f):
        f.write(self._store())
        return f.tell()

    def _load(self, f):
        pass

    def _store(self):
        pass

    def __repr__(self):
        return repr(self.value)


def primitive_factory(name, _load, _store, insert_self=True, __init__=None):
    _loadf = (lambda self, f: _load(f)) if insert_self else _load
    _storef = (lambda self: _store(self.value)) if insert_self else _store
    attr = {'_load': _loadf, '_store': _storef}
    if __init__ is not None:
        attr['__init__'] = __init__
    return type(name, (Primitive,), attr)


Bool = primitive_factory('Bool', get_bool, set_bool)
Byte = primitive_factory('Byte', get_byte, set_byte)
Short = primitive_factory('Short', get_short, set_short)
Int = primitive_factory('Int', get_int, set_int)
UInt = primitive_factory('UInt', get_uint, set_uint)
Long = primitive_factory('Long', get_long, set_long)
Float = primitive_factory('Float', get_float, set_float)
Double = primitive_factory('Double', get_double, set_double)
String = primitive_factory('String', get_string, set_string)


class Bytes(Primitive):
    def __init__(self, *, length=None, value=None):
        if length is not None:
            super().__init__()
            self.length = length
        elif value is not None:
            super().__init__(value)

    def _load(self, f):
        return f.read(self.length)

    def _store(self):
        return self.value

    def __repr__(self):
        if len(self.value) < 20:
            return repr(self.value)
        return 'Bytes(...)'


class Nested(Element):
    def __init__(self):
        self._fields = OrderedDict()
        self._load_positions = {}
        self._store_positions = {}

    def _generate_fields(self):
        pass

    def load(self, f):
        for field_list in self._generate_fields():
            for field, item in field_list:
                tell = item.load(f)
                self._fields[field] = item
                self._load_positions[field] = tell
        return f.tell()

    def store(self, f):
        for field, item in self._fields.items():
            tell = item.store(f)
            self._store_positions[field] = tell
        self._post_store(f)
        return f.tell()

    def _post_store(self, f):
        pass

    def __getitem__(self, key):
        item = self._fields[key]
        if isinstance(item, Primitive):
            return item.value
        return item

    def __setitem__(self, key, value):
        item = self._fields[key]
        if isinstance(item, Primitive) and not isinstance(value, Primitive):
            self._fields[key].value = value
        else:
            self._fields[key] = value

    def __repr__(self):
        return repr(self._fields)


class Array(Nested):
    def __init__(self, length_class, type_class, *type_args, **type_kwargs):
        super().__init__()
        self.length_class = length_class
        self.type_class = type_class
        self.type_args = type_args
        self.type_kwargs = type_kwargs

    def _generate_fields(self):
        yield [('length', self.length_class())]
        for i in range(self['length']):
            yield [(i, self.type_class(*self.type_args, **self.type_kwargs))]

    def __repr__(self):
        items = []
        for i in range(self['length']):
            items.append(self[i])
        return repr(items)


class Header(Nested):
    def _generate_fields(self):
        yield [
            ('name', String()),
            ('seed', String()),
            ('world_gen_version', Long()),
            ('unique_id', Bytes(length=16)),
            ('world_id', Int()),
            ('left_world', Int()),
            ('right_world', Int()),
            ('top_world', Int()),
            ('bottom_world', Int()),
            ('max_tiles_y', Int()),
            ('max_tiles_x', Int()),
            ('expert_mode', Bool()),
            ('creation_time', Long()),
            ('moon_type', Byte()),
            ('tree_x_0', Int()),
            ('tree_x_1', Int()),
            ('tree_x_2', Int()),
            ('tree_style_0', Int()),
            ('tree_style_1', Int()),
            ('tree_style_2', Int()),
            ('tree_style_3', Int()),
            ('cave_back_x_0', Int()),
            ('cave_back_x_1', Int()),
            ('cave_back_x_2', Int()),
            ('cave_back_style_0', Int()),
            ('cave_back_style_1', Int()),
            ('cave_back_style_2', Int()),
            ('cave_back_style_3', Int()),
            ('ice_back_style', Int()),
            ('jungle_back_style', Int()),
            ('hell_back_style', Int()),
            ('spawn_x', Int()),
            ('spawn_y', Int()),
            ('surface', Double()),
            ('rock', Double()),
            ('time', Double()),
            ('is_day', Bool()),
            ('moon_phase', Int()),
            ('blood_moon', Bool()),
            ('eclipse', Bool()),
            ('dungeon_x', Int()),
            ('dungeon_y', Int()),
            ('crimson', Bool()),
            ('downed_boss_1', Bool()),
            ('downed_boss_2', Bool()),
            ('downed_boss_3', Bool()),
            ('downed_queen_bee', Bool()),
            ('downed_mech_boss_1', Bool()),
            ('downed_mech_boss_2', Bool()),
            ('downed_mech_boss_3', Bool()),
            ('downed_mech_boss_any', Bool()),
            ('downed_plantera', Bool()),
            ('downed_golem', Bool()),
            ('downed_slime_king', Bool()),
            ('saved_goblin', Bool()),
            ('saved_wizard', Bool()),
            ('saved_mech', Bool()),
            ('downed_goblins', Bool()),
            ('downed_clown', Bool()),
            ('downed_frost', Bool()),
            ('downed_pirates', Bool()),
            ('shadow_orb_smashed', Bool()),
            ('spawn_meteor', Bool()),
            ('shadow_orb_count', Byte()),
            ('altar_count', Int()),
            ('hard_mode', Bool()),
            ('invasion_delay', Int()),
            ('invasion_size', Int()),
            ('invasion_type', Int()),
            ('invasion_x', Double()),
            ('slime_rain_time', Double()),
            ('sundial_cooldown', Byte()),
            ('raining', Bool()),
            ('rain_time', Int()),
            ('max_rain', Float()),
            ('ore_tier_1', Int()),
            ('ore_tier_2', Int()),
            ('ore_tier_3', Int()),
            ('bg_0', Byte()),
            ('bg_1', Byte()),
            ('bg_2', Byte()),
            ('bg_3', Byte()),
            ('bg_4', Byte()),
            ('bg_5', Byte()),
            ('bg_6', Byte()),
            ('bg_7', Byte()),
            ('cloud_bg_active', Int()),
            ('num_clouds', Short()),
            ('wind_speed', Float()),
            ('angler_finished_today', Array(Int, String)),
            ('saved_angler', Bool()),
            ('angler_quest', Int()),
            ('saved_stylist', Bool()),
            ('saved_tax_collector', Bool()),
            ('invasion_size_start', Int()),
            ('cultist_delay', Int()),
            ('kill_counts', Array(Short, Int)),
            ('fast_forward', Bool()),
            ('downed_fishron', Bool()),
            ('downed_martians', Bool()),
            ('downed_cultist', Bool()),
            ('downed_moonlord', Bool()),
            ('downed_halloween_king', Bool()),
            ('downed_halloween_tree', Bool()),
            ('downed_christmas_ice_queen', Bool()),
            ('downed_christmas_santank', Bool()),
            ('downed_christmas_tree', Bool()),
            ('downed_solar', Bool()),
            ('downed_vortex', Bool()),
            ('downed_nebula', Bool()),
            ('downed_stardust', Bool()),
            ('active_solar', Bool()),
            ('active_vortex', Bool()),
            ('active_nebula', Bool()),
            ('active_stardust', Bool()),
            ('lunar_apocalypse_up', Bool()),
            ('party_manual', Bool()),
            ('party_genuine', Bool()),
            ('party_cooldown', Int()),
            ('celebrating_npcs', Array(Int, Int)),
            ('sandstorm_happening', Bool()),
            ('sandstorm_time_left', Int()),
            ('sandstorm_severity', Float()),
            ('sandstorm_intended_severity', Float()),
            ('saved_bartender', Bool()),
            ('downed_dd2_invasion_1', Bool()),
            ('downed_dd2_invasion_2', Bool()),
            ('downed_dd2_invasion_3', Bool()),
        ]


class World(Nested):
    sections = [
        'header',
        'tiles',
        'chests',
        'signs',
        'npcs',
        'tile_entities',
        'weighted_pressure_plates',
        'town_manager',
    ]

    def _generate_fields(self):
        yield [
            ('version', Int()),
            ('magic', Long()),
        ]
        if self['magic'] != 172097103742133618:
            raise RuntimeError('invalid magic number')
        yield [
            ('revision', UInt()),
            ('is_favorite', Long()),
            ('positions', Array(Short, Int)),
            ('num_importances', Short()),
        ]
        yield [('importances', Bytes(length=math.ceil(self['num_importances'] / 8)))]
        if self['positions'][0] != self._load_positions['importances']:
            raise RuntimeError('file format header did not end at position 0')
        yield [('header', Header())]
        if self['positions'][1] != self._load_positions['header']:
            raise RuntimeError('header did not end at position 1')
        for i, section in enumerate(World.sections[1:]):
            yield [(section, Bytes(length=self['positions'][i + 2] - self['positions'][i + 1]))]
        yield[
            ('footer_flag', Bool()),
            ('footer_name', String()),
            ('footer_world_id', Int()),
        ]
        if not self['footer_flag'] or self['footer_name'] != self['header']['name'] or \
                self['footer_world_id'] != self['header']['world_id']:
            raise RuntimeError('invalid footer')
        self._fields['footer_name'] = self['header']._fields['name']
        self._fields['footer_world_id'] = self['header']._fields['world_id']

    def _post_store(self, f):
        self['positions'][0] = self._store_positions['importances']
        for i, section in enumerate(World.sections):
            self['positions'][i + 1] = self._store_positions[section]
        self['positions'][len(World.sections) + 1] = 0
        f.seek(24)
        self['positions'].store(f)
