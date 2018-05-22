from nbtlib import nbt

BLOCK_NAME_TO_ID_MAP = {
}

DV_FACING = {'north': 3, 'south': 2, 'west': 1, 'east': 0}
DV_CHEST_FACING = {'north': 2, 'south': 3, 'west': 4, 'east': 5}
DV_HALF = {'bottom': 0, 'top': 1}
DV_DIRT_VARIANT = {'dirt': 0, 'coarse_dirt': 1, 'podzol': 2}
DV_TALLGRASS_TYPE = {'dead_bush': 0, 'tall_grass': 1, 'fern': 2}
DV_STONE_VARIANT = {
    'stone': 0, 'granite': 1, 'smooth_granite': 2, 'diorite': 3, 'smooth_diorite': 4, 'andesite': 5,
    'smooth_andesite': 6}
DV_STONEBRICK_VARIANT = {'stonebrick': 0, 'mossy_stonebrick': 1, 'cracked_stonebrick': 2, 'chiseled_stonebrick': 3}

PROPERTIES_TO_DV_HANDLER_MAP = {
    'minecraft:tallgrass': lambda p: DV_TALLGRASS_TYPE[p['type']],
    'minecraft:dirt': lambda p: DV_DIRT_VARIANT[p['variant']],
    'minecraft:stone': lambda p: DV_STONE_VARIANT[p['variant']],
    'minecraft:stonebrick': lambda p: DV_STONEBRICK_VARIANT[p['variant']],
    'minecraft:stone_brick_stairs': lambda p: DV_FACING[p['facing']] + 4 * DV_HALF[p['half']],
    'minecraft:chest': lambda p: DV_CHEST_FACING[p['facing']]
}


def block_name_to_id(block_name: str):
    parts = block_name.split(':', maxsplit=1)
    if len(parts) > 1:
        block_name = parts[1]
    return BLOCK_NAME_TO_ID_MAP.get(block_name, block_name).upper()


def block_properties_to_data(block_name, block_properties):
    handler = PROPERTIES_TO_DV_HANDLER_MAP.get(block_name)
    return handler(block_properties) if handler else None


def structure_to_bo3_blocks(structure_nbt):
    later_lines = []

    for block_nbt in structure_nbt.root['blocks']:
        x, y, z = block_nbt['pos']
        block_tag = block_nbt.get('nbt')
        p = block_nbt['state']
        palette_nbt = structure_nbt.root['palette'][p]
        block_name = palette_nbt['Name']
        block_id = block_name_to_id(block_name)
        block_properties = palette_nbt.get('Properties')
        block_data = block_properties_to_data(block_name, block_properties) if block_properties else None
        line = ''.join(
            (f'B({x},{y},{z},{block_id}',
             f':{block_data}' if block_data else '',
             f',\'{str(block_tag)}\'' if block_tag else '',
             ')')
        )
        if block_tag:
            later_lines.append(line)
        else:
            yield line

    yield from later_lines

    dx, dy, dz = structure_nbt.root['size']
    yield f'# Size (X*Y*Z): {dx}*{dy}*{dz}'


def structure_file_to_bo3_blocks(structure_file, output_file):
    structure_nbt = nbt.load(structure_file)
    bo3_text = '\n'.join(structure_to_bo3_blocks(structure_nbt))
    with open(output_file, 'w') as fp:
        fp.write(bo3_text)
