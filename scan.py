#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#   Region Fixer.
#   Fix your region files with a backup copy of your Minecraft world.
#   Copyright (C) 2011  Alejandro Aguilera (Fenixin)
#   https://github.com/Fenixin/Minecraft-Region-Fixer
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import nbt.chunk as nbt_chunk
import nbt.region as region
import nbt.nbt as nbt
#~ from nbt.region import STATUS_CHUNK_OVERLAPPING, STATUS_CHUNK_MISMATCHED_LENGTHS
        #~ - STATUS_CHUNK_ZERO_LENGTH
        #~ - STATUS_CHUNK_IN_HEADER
        #~ - STATUS_CHUNK_OUT_OF_FILE
        #~ - STATUS_CHUNK_OK
        #~ - STATUS_CHUNK_NOT_CREATED
from os.path import split, join
import progressbar
import multiprocessing
from multiprocessing import queues
import world
import time

import sys
import traceback

import array
# import mysql.connector as mysql

DIAMOND_COUNTS = {
    'DIAMOND': 1,
    'DIAMOND_ORE': 3,
    'DIAMOND_BLOCK': 9,
    'DIAMOND_SWORD': 2,
    'DIAMOND_SPADE': 1,
    'DIAMOND_PICKAXE': 3,
    'DIAMOND_AXE': 3,
    'DIAMOND_HOE': 2,
    'DIAMOND_HELMET': 5,
    'DIAMOND_CHESTPLATE': 8,
    'DIAMOND_LEGGINGS': 7,
    'DIAMOND_BOOTS': 4,
    'JUKEBOX': 1,
    'ENCHANTMENT_TABLE': 2,
  }

BLOCK_MAP = {
    0: 'AIR',
    1: 'STONE',
    2: 'GRASS',
    3: 'DIRT',
    4: 'COBBLESTONE',
    5: 'WOOD',
    6: 'SAPLING',
    7: 'BEDROCK',
    8: 'WATER',
    9: 'STATIONARY_WATER',
    10: 'LAVA',
    11: 'STATIONARY_LAVA',
    12: 'SAND',
    13: 'GRAVEL',
    14: 'GOLD_ORE',
    15: 'IRON_ORE',
    16: 'COAL_ORE',
    17: 'LOG',
    18: 'LEAVES',
    19: 'SPONGE',
    20: 'GLASS',
    21: 'LAPIS_ORE',
    22: 'LAPIS_BLOCK',
    23: 'DISPENSER',
    24: 'SANDSTONE',
    25: 'NOTE_BLOCK',
    26: 'BED_BLOCK',
    27: 'POWERED_RAIL',
    28: 'DETECTOR_RAIL',
    29: 'PISTON_STICKY_BASE',
    30: 'WEB',
    31: 'LONG_GRASS',
    32: 'DEAD_BUSH',
    33: 'PISTON_BASE',
    34: 'PISTON_EXTENSION',
    35: 'WOOL',
    36: 'PISTON_MOVING_PIECE',
    37: 'YELLOW_FLOWER',
    38: 'RED_ROSE',
    39: 'BROWN_MUSHROOM',
    40: 'RED_MUSHROOM',
    41: 'GOLD_BLOCK',
    42: 'IRON_BLOCK',
    43: 'DOUBLE_STEP',
    44: 'STEP',
    45: 'BRICK',
    46: 'TNT',
    47: 'BOOKSHELF',
    48: 'MOSSY_COBBLESTONE',
    49: 'OBSIDIAN',
    50: 'TORCH',
    51: 'FIRE',
    52: 'MOB_SPAWNER',
    53: 'WOOD_STAIRS',
    54: 'CHEST',
    55: 'REDSTONE_WIRE',
    56: 'DIAMOND_ORE',
    57: 'DIAMOND_BLOCK',
    58: 'WORKBENCH',
    59: 'CROPS',
    60: 'SOIL',
    61: 'FURNACE',
    62: 'BURNING_FURNACE',
    63: 'SIGN_POST',
    64: 'WOODEN_DOOR',
    65: 'LADDER',
    66: 'RAILS',
    67: 'COBBLESTONE_STAIRS',
    68: 'WALL_SIGN',
    69: 'LEVER',
    70: 'STONE_PLATE',
    71: 'IRON_DOOR_BLOCK',
    72: 'WOOD_PLATE',
    73: 'REDSTONE_ORE',
    74: 'GLOWING_REDSTONE_ORE',
    75: 'REDSTONE_TORCH_OFF',
    76: 'REDSTONE_TORCH_ON',
    77: 'STONE_BUTTON',
    78: 'SNOW',
    79: 'ICE',
    80: 'SNOW_BLOCK',
    81: 'CACTUS',
    82: 'CLAY',
    83: 'SUGAR_CANE_BLOCK',
    84: 'JUKEBOX',
    85: 'FENCE',
    86: 'PUMPKIN',
    87: 'NETHERRACK',
    88: 'SOUL_SAND',
    89: 'GLOWSTONE',
    90: 'PORTAL',
    91: 'JACK_O_LANTERN',
    92: 'CAKE_BLOCK',
    93: 'DIODE_BLOCK_OFF',
    94: 'DIODE_BLOCK_ON',
    95: 'LOCKED_CHEST',
    96: 'TRAP_DOOR',
    97: 'MONSTER_EGGS',
    98: 'SMOOTH_BRICK',
    99: 'HUGE_MUSHROOM_1',
    100: 'HUGE_MUSHROOM_2',
    101: 'IRON_FENCE',
    102: 'THIN_GLASS',
    103: 'MELON_BLOCK',
    104: 'PUMPKIN_STEM',
    105: 'MELON_STEM',
    106: 'VINE',
    107: 'FENCE_GATE',
    108: 'BRICK_STAIRS',
    109: 'SMOOTH_STAIRS',
    110: 'MYCEL',
    111: 'WATER_LILY',
    112: 'NETHER_BRICK',
    113: 'NETHER_FENCE',
    114: 'NETHER_BRICK_STAIRS',
    115: 'NETHER_WARTS',
    116: 'ENCHANTMENT_TABLE',
    117: 'BREWING_STAND',
    118: 'CAULDRON',
    119: 'ENDER_PORTAL',
    120: 'ENDER_PORTAL_FRAME',
    121: 'ENDER_STONE',
    122: 'DRAGON_EGG',
    123: 'REDSTONE_LAMP_OFF',
    124: 'REDSTONE_LAMP_ON',
    125: 'WOOD_DOUBLE_STEP',
    126: 'WOOD_STEP',
    127: 'COCOA',
    128: 'SANDSTONE_STAIRS',
    129: 'EMERALD_ORE',
    130: 'ENDER_CHEST',
    131: 'TRIPWIRE_HOOK',
    132: 'TRIPWIRE',
    133: 'EMERALD_BLOCK',
    134: 'SPRUCE_WOOD_STAIRS',
    135: 'BIRCH_WOOD_STAIRS',
    136: 'JUNGLE_WOOD_STAIRS',
    137: 'COMMAND',
    138: 'BEACON',
    139: 'COBBLE_WALL',
    140: 'FLOWER_POT',
    141: 'CARROT',
    142: 'POTATO',
    143: 'WOOD_BUTTON',
    144: 'SKULL',
    145: 'ANVIL',
    146: 'TRAPPED_CHEST',
    147: 'GOLD_PLATE',
    148: 'IRON_PLATE',
    149: 'REDSTONE_COMPARATOR_OFF',
    150: 'REDSTONE_COMPARATOR_ON',
    151: 'DAYLIGHT_DETECTOR',
    152: 'REDSTONE_BLOCK',
    153: 'QUARTZ_ORE',
    154: 'HOPPER',
    155: 'QUARTZ_BLOCK',
    156: 'QUARTZ_STAIRS',
    157: 'ACTIVATOR_RAIL',
    158: 'DROPPER',
    159: 'STAINED_CLAY',
    160: 'STAINED_GLASS_PANE',
    161: 'LEAVES_2',
    162: 'LOG_2',
    163: 'ACACIA_STAIRS',
    164: 'DARK_OAK_STAIRS',
    170: 'HAY_BLOCK',
    171: 'CARPET',
    172: 'HARD_CLAY',
    173: 'COAL_BLOCK',
    174: 'PACKED_ICE',
    175: 'DOUBLE_PLANT',
    256: 'IRON_SPADE',
    257: 'IRON_PICKAXE',
    258: 'IRON_AXE',
    259: 'FLINT_AND_STEEL',
    260: 'APPLE',
    261: 'BOW',
    262: 'ARROW',
    263: 'COAL',
    264: 'DIAMOND',
    265: 'IRON_INGOT',
    266: 'GOLD_INGOT',
    267: 'IRON_SWORD',
    268: 'WOOD_SWORD',
    269: 'WOOD_SPADE',
    270: 'WOOD_PICKAXE',
    271: 'WOOD_AXE',
    272: 'STONE_SWORD',
    273: 'STONE_SPADE',
    274: 'STONE_PICKAXE',
    275: 'STONE_AXE',
    276: 'DIAMOND_SWORD',
    277: 'DIAMOND_SPADE',
    278: 'DIAMOND_PICKAXE',
    279: 'DIAMOND_AXE',
    280: 'STICK',
    281: 'BOWL',
    282: 'MUSHROOM_SOUP',
    283: 'GOLD_SWORD',
    284: 'GOLD_SPADE',
    285: 'GOLD_PICKAXE',
    286: 'GOLD_AXE',
    287: 'STRING',
    288: 'FEATHER',
    289: 'SULPHUR',
    290: 'WOOD_HOE',
    291: 'STONE_HOE',
    292: 'IRON_HOE',
    293: 'DIAMOND_HOE',
    294: 'GOLD_HOE',
    295: 'SEEDS',
    296: 'WHEAT',
    297: 'BREAD',
    298: 'LEATHER_HELMET',
    299: 'LEATHER_CHESTPLATE',
    300: 'LEATHER_LEGGINGS',
    301: 'LEATHER_BOOTS',
    302: 'CHAINMAIL_HELMET',
    303: 'CHAINMAIL_CHESTPLATE',
    304: 'CHAINMAIL_LEGGINGS',
    305: 'CHAINMAIL_BOOTS',
    306: 'IRON_HELMET',
    307: 'IRON_CHESTPLATE',
    308: 'IRON_LEGGINGS',
    309: 'IRON_BOOTS',
    310: 'DIAMOND_HELMET',
    311: 'DIAMOND_CHESTPLATE',
    312: 'DIAMOND_LEGGINGS',
    313: 'DIAMOND_BOOTS',
    314: 'GOLD_HELMET',
    315: 'GOLD_CHESTPLATE',
    316: 'GOLD_LEGGINGS',
    317: 'GOLD_BOOTS',
    318: 'FLINT',
    319: 'PORK',
    320: 'GRILLED_PORK',
    321: 'PAINTING',
    322: 'GOLDEN_APPLE',
    323: 'SIGN',
    324: 'WOOD_DOOR',
    325: 'BUCKET',
    326: 'WATER_BUCKET',
    327: 'LAVA_BUCKET',
    328: 'MINECART',
    329: 'SADDLE',
    330: 'IRON_DOOR',
    331: 'REDSTONE',
    332: 'SNOW_BALL',
    333: 'BOAT',
    334: 'LEATHER',
    335: 'MILK_BUCKET',
    336: 'CLAY_BRICK',
    337: 'CLAY_BALL',
    338: 'SUGAR_CANE',
    339: 'PAPER',
    340: 'BOOK',
    341: 'SLIME_BALL',
    342: 'STORAGE_MINECART',
    343: 'POWERED_MINECART',
    344: 'EGG',
    345: 'COMPASS',
    346: 'FISHING_ROD',
    347: 'WATCH',
    348: 'GLOWSTONE_DUST',
    349: 'RAW_FISH',
    350: 'COOKED_FISH',
    351: 'INK_SACK',
    352: 'BONE',
    353: 'SUGAR',
    354: 'CAKE',
    355: 'BED',
    356: 'DIODE',
    357: 'COOKIE',
    358: 'MAP',
    359: 'SHEARS',
    360: 'MELON',
    361: 'PUMPKIN_SEEDS',
    362: 'MELON_SEEDS',
    363: 'RAW_BEEF',
    364: 'COOKED_BEEF',
    365: 'RAW_CHICKEN',
    366: 'COOKED_CHICKEN',
    367: 'ROTTEN_FLESH',
    368: 'ENDER_PEARL',
    369: 'BLAZE_ROD',
    370: 'GHAST_TEAR',
    371: 'GOLD_NUGGET',
    372: 'NETHER_STALK',
    373: 'POTION',
    374: 'GLASS_BOTTLE',
    375: 'SPIDER_EYE',
    376: 'FERMENTED_SPIDER_EYE',
    377: 'BLAZE_POWDER',
    378: 'MAGMA_CREAM',
    379: 'BREWING_STAND_ITEM',
    380: 'CAULDRON_ITEM',
    381: 'EYE_OF_ENDER',
    382: 'SPECKLED_MELON',
    383: 'MONSTER_EGG',
    384: 'EXP_BOTTLE',
    385: 'FIREBALL',
    386: 'BOOK_AND_QUILL',
    387: 'WRITTEN_BOOK',
    388: 'EMERALD',
    389: 'ITEM_FRAME',
    390: 'FLOWER_POT_ITEM',
    391: 'CARROT_ITEM',
    392: 'POTATO_ITEM',
    393: 'BAKED_POTATO',
    394: 'POISONOUS_POTATO',
    395: 'EMPTY_MAP',
    396: 'GOLDEN_CARROT',
    397: 'SKULL_ITEM',
    398: 'CARROT_STICK',
    399: 'NETHER_STAR',
    400: 'PUMPKIN_PIE',
    401: 'FIREWORK',
    402: 'FIREWORK_CHARGE',
    403: 'ENCHANTED_BOOK',
    404: 'REDSTONE_COMPARATOR',
    405: 'NETHER_BRICK_ITEM',
    406: 'QUARTZ',
    407: 'EXPLOSIVE_MINECART',
    408: 'HOPPER_MINECART',
    2256: 'GOLD_RECORD',
    2257: 'GREEN_RECORD',
    2258: 'RECORD_3',
    2259: 'RECORD_4',
    2260: 'RECORD_5',
    2261: 'RECORD_6',
    2262: 'RECORD_7',
    2263: 'RECORD_8',
    2264: 'RECORD_9',
    2265: 'RECORD_10',
    2266: 'RECORD_11',
    2267: 'RECORD_12',
    6900: 'CIVCRAFT_INTRO'}


def saveBlockStats(table_name, coords, block_aggregation):
    stmt = 'insert into {0} (x,z,mat,count) VALUES (%s,%s,%s,%s)'.format(table_name)
    # cnx opened in scan_region_file
    if not cnx:
      return
    cur = cnx.cursor()
    try:
        rows = []
        for i, count in enumerate(block_aggregation):
            if count <= 0:
                continue
            if i in BLOCK_MAP:
                mat = BLOCK_MAP[i]
            else:
                mat = str(i)
            rows.append((coords[0], coords[1], mat, count))
        if rows:
            cur.executemany(stmt, rows)
            cnx.commit()
    finally:
        cur.close()


def findTag(compoundTag, keyName):
    for item in compoundTag.tags:
        if item.name == keyName:
            return item
    return None

def recordInventory(inv_id, inventory):
    if not inventory:
        return None
    inv = [inv_id, ' ']
    contents = {}
    for item in inventory.tags:
#        block_id = findTag(item, 'id').value
#        count = findTag(item, 'Count').value
#        if block_id in BLOCK_MAP:
#            block_id = BLOCK_MAP[block_id]
#        if block_id not in contents:
#            contents[block_id] = 0
#        contents[block_id] += count
        block_id = findTag(item, 'id').value
        if block_id == 403:
            enchant_parent = findTag(item, 'tag')
            if enchant_parent:
                if findTag(enchant_parent, 'StoredEnchantments'):
                    block_id = 6900
        count = findTag(item, 'Count').value
        if block_id in BLOCK_MAP:
            block_id = BLOCK_MAP[block_id]
        if block_id not in contents:
            contents[block_id] = 0
        contents[block_id] += count
    for block_id, count in contents.iteritems():
        inv.append('{0}({1}) '.format(block_id, count))
    inv.append('\n')
    return ''.join(inv)

def logContainer(container_nbt):
    tagName = findTag(container_nbt, 'id')
    if not tagName:
        return None
    if tagName.value in ('ItemFrame', 'MinecartHopper', 'MinecartChest', 'Chest', 'Dropper', 'Trap', 'Hopper', 'Furnace'):
        pos = findTag(container_nbt, 'Pos')
        if pos:
            x = int(pos[0].value)
            y = int(pos[1].value)
            z = int(pos[2].value)
        else:
            x = findTag(container_nbt, 'x').value
            y = findTag(container_nbt, 'y').value
            z = findTag(container_nbt, 'z').value
        inventory = findTag(container_nbt, 'Items')
        if not inventory and findTag(container_nbt, 'Item'):
            inventory = nbt.TAG_Compound()
            inventory.name = 'Items'
            inventory.tags.append(findTag(container_nbt, 'Item'))
        return recordInventory('({0},{1},{2})'.format(x, y, z), inventory)
    else:
        return None


class ChildProcessException(Exception):
    """Takes the child process traceback text and prints it as a
    real traceback with asterisks everywhere."""
    def __init__(self, error):
        # Helps to see wich one is the child process traceback
        traceback = error[2]
        print "*"*10
        print "*** Error while scanning:"
        print "*** ", error[0]
        print "*"*10
        print "*** Printing the child's Traceback:"
        print "*** Exception:", traceback[0], traceback[1]
        for tb in traceback[2]:
            print "*"*10
            print "*** File {0}, line {1}, in {2} \n***   {3}".format(*tb)
        print "*"*10

class FractionWidget(progressbar.ProgressBarWidget):
    """ Convenience class to use the progressbar.py """
    def __init__(self, sep=' / '):
        self.sep = sep

    def update(self, pbar):
        return '%2d%s%2d' % (pbar.currval, self.sep, pbar.maxval)

def scan_world(world_obj, options):
    """ Scans a world folder including players, region folders and
        level.dat. While scanning prints status messages. """
    w = world_obj
    # scan the world dir
    print "Scanning directory..."

    if not w.scanned_level.path:
        print "Warning: No \'level.dat\' file found!"

    if w.players:
        print "There are {0} region files and {1} player files in the world directory.".format(\
            w.get_number_regions(), len(w.players))
    else:
        print "There are {0} region files in the world directory.".format(\
            w.get_number_regions())

    # check the level.dat file and the *.dat files in players directory
    print "\n{0:-^60}".format(' Checking level.dat ')

    if not w.scanned_level.path:
        print "[WARNING!] \'level.dat\' doesn't exist!"
    else:
        if w.scanned_level.readable == True:
            print "\'level.dat\' is readable"
        else:
            print "[WARNING!]: \'level.dat\' is corrupted with the following error/s:"
            print "\t {0}".format(w.scanned_level.status_text)

    print "\n{0:-^60}".format(' Checking player files ')
    # TODO multiprocessing!
    # Probably, create a scanner object with a nice buffer of logger for text and logs and debugs
    if not w.players:
        print "Info: No player files to scan."
    else:
        scan_all_players(w)
        all_ok = True
        for name in w.players:
            if w.players[name].readable == False:
                print "[WARNING]: Player file {0} has problems.\n\tError: {1}".format(w.players[name].filename, w.players[name].status_text)
                all_ok = False
        if all_ok:
            print "All player files are readable."

    # SCAN ALL THE CHUNKS!
    if w.get_number_regions == 0:
        print "No region files to scan!"
    else:
        for r in w.regionsets:
            if r.regions:
                print "\n{0:-^60}".format(' Scanning the {0} '.format(r.get_name()))
                scan_regionset(r, options)
    w.scanned = True

def scan_playerfile(scan_dat_file):
    """ Reads a .dat player file and returns the NBT data as a pretty string """

    s = scan_dat_file
    player_summary = ''
    try:
        player_dat = nbt.NBTFile(filename = s)
        player_summary += player_dat.pretty_tree(0); 
        return player_summary
    except Exception, e:
        return e

def scan_player(player_name, scanned_dat_file):
    """ At the moment only tries to read a .dat player file. It returns
    0 if it's ok and 1 if has some problem """

    s = scanned_dat_file
    inventory_summary = ''
    try:
        player_dat = nbt.NBTFile(filename = s.path)
#        enchanted_book_count = 0
        inventory = findTag(player_dat, 'Inventory')
        if inventory:
            px = findTag(player_dat, 'SpawnX')
            py = findTag(player_dat, 'SpawnY')
            pz = findTag(player_dat, 'SpawnZ')
            qq = [player_name]
            if px:
                qq.append(' [{0},{1},{2}]:'.format(px.value, py.value, pz.value))
            else:
                qq.append(':')
            inventory_summary = recordInventory(''.join(qq), inventory)
#            for item in inventory.tags:
#                enchants = None
#                item_id = findTag(item, 'id')
#                if not item_id:
#                    continue
#                if item_id.value == 403:
#                    enchant_parent = findTag(item, 'tag')
#                    if enchant_parent:
#                        if findTag(enchant_parent, 'StoredEnchantments'):
#                            enchanted_book_count += 1
#                item_name = BLOCK_MAP.get(item_id.value)
#                item_count = findTag(item, 'count')
#                if item_count:
#                    item_count = item_count.value
#                else:
#                    item_count = 1
#                if item_name in DIAMOND_COUNTS:
#                    diamond_counts[item_name] += item_count * DIAMOND_COUNTS[item_name]
        s.readable = True
#        return enchanted_book_count
        return inventory_summary
    except Exception, e:
        s.readable = False
        s.status_text = e
#        return 0
        return inventory_summary


def scan_all_players(world_obj):
    """ Scans all the players using the scan_player function. """

#    book_counts = {}
#    diamond_counts = {
#      'DIAMOND': 0,
#      'DIAMOND_ORE': 0,
#      'DIAMOND_BLOCK': 0,
#      'DIAMOND_SWORD': 0,
#      'DIAMOND_SPADE': 0,
#      'DIAMOND_PICKAXE': 0,
#      'DIAMOND_AXE': 0,
#      'DIAMOND_HOE': 0,
#      'DIAMOND_HELMET': 0,
#      'DIAMOND_CHESTPLATE': 0,
#      'DIAMOND_LEGGINGS': 0,
#      'DIAMOND_BOOTS': 0,
#      'JUKEBOX': 0,
#      'ENCHANTMENT_TABLE': 0,
#    }

# Uncomment to dump player inventories
    with open('player_inventories.txt', 'w') as fout:
        for name in world_obj.players:
            print >>fout, scan_player(name, world_obj.players[name])

#        enchanted_book_count = scan_player(name, world_obj.players[name], diamond_counts)
#        if enchanted_book_count > 0:
#            book_counts[name] = enchanted_book_count
#    for name, count in sorted(book_counts.iteritems(), key=lambda tup: tup[1]):
#        print '{0}: {1}'.format(name, count)
#    for name, count in diamond_counts.iteritems():
#        print '{0}: {1}'.format(name, count)


cnx = None

def scan_region_file(scanned_regionfile_obj, options):
    """ Given a scanned region file object with the information of a 
        region files scans it and returns the same obj filled with the
        results.
        
        If delete_entities is True it will delete entities while
        scanning
        
        entiti_limit is the threshold tof entities to conisder a chunk
        with too much entities problems.
    """

    o = options
    delete_entities = o.delete_entities
    entity_limit = o.entity_limit
    try:
        global cnx
        # cnx = mysql.connect(user='block_stats', password='', host='localhost', port='3306', database='block_stats')
        block_aggregation = [0] * 4096
        containers = []
        r = scanned_regionfile_obj
        # counters of problems
        chunk_count = 0
        corrupted = 0
        wrong = 0
        entities_prob = 0
        shared = 0
        # used to detect chunks sharing headers
        offsets = {}
        filename = r.filename
        # try to open the file and see if we can parse the header
        try:
            region_file = region.RegionFile(r.path)
        except region.NoRegionHeader: # the region has no header
            r.status = world.REGION_TOO_SMALL
            return r
        except IOError, e:
            print "\nWARNING: I can't open the file {0} !\nThe error is \"{1}\".\nTypical causes are file blocked or problems in the file system.\n".format(filename,e)
            r.status = world.REGION_UNREADABLE
            r.scan_time = time.time()
            print "Note: this region file won't be scanned and won't be taken into acount in the summaries"
            # TODO count also this region files
            return r
        except: # whatever else print an error and ignore for the scan
                # not really sure if this is a good solution...
            print "\nWARNING: The region file \'{0}\' had an error and couldn't be parsed as region file!\nError:{1}\n".format(join(split(split(r.path)[0])[1], split(r.path)[1]),sys.exc_info()[0])
            print "Note: this region file won't be scanned and won't be taken into acount."
            print "Also, this may be a bug. Please, report it if you have the time.\n"
            return None

        try:# start the scanning of chunks
            
            for x in range(32):
                for z in range(32):

                    # start the actual chunk scanning
                    g_coords = r.get_global_chunk_coords(x, z)
                    chunk, c = scan_chunk(region_file, (x,z), g_coords, o, block_aggregation, containers)
                    if c != None: # chunk not created
                        r.chunks[(x,z)] = c
                        chunk_count += 1
                    else: continue
                    if c[TUPLE_STATUS] == world.CHUNK_OK:
                        continue
                    elif c[TUPLE_STATUS] == world.CHUNK_TOO_MANY_ENTITIES:
                        # deleting entities is in here because parsing a chunk with thousands of wrong entities
                        # takes a long time, and once detected is better to fix it at once.
                        if delete_entities:
                            world.delete_entities(region_file, x, z)
                            print "Deleted {0} entities in chunk ({1},{2}) of the region file: {3}".format(c[TUPLE_NUM_ENTITIES], x, z, r.filename)
                            # entities removed, change chunk status to OK
                            r.chunks[(x,z)] = (0, world.CHUNK_OK)

                        else:
                            entities_prob += 1
                            # This stores all the entities in a file,
                            # comes handy sometimes.
                            #~ pretty_tree = chunk['Level']['Entities'].pretty_tree()
                            #~ name = "{2}.chunk.{0}.{1}.txt".format(x,z,split(region_file.filename)[1])
                            #~ archivo = open(name,'w')
                            #~ archivo.write(pretty_tree)

                    elif c[TUPLE_STATUS] == world.CHUNK_CORRUPTED:
                        corrupted += 1
                    elif c[TUPLE_STATUS] == world.CHUNK_WRONG_LOCATED:
                        wrong += 1
            
            # Now check for chunks sharing offsets:
            # Please note! region.py will mark both overlapping chunks
            # as bad (the one stepping outside his territory and the
            # good one). Only wrong located chunk with a overlapping
            # flag are really BAD chunks! Use this criterion to 
            # discriminate
            metadata = region_file.metadata
            sharing = [k for k in metadata if (
                metadata[k].status == region.STATUS_CHUNK_OVERLAPPING and
                r[k][TUPLE_STATUS] == world.CHUNK_WRONG_LOCATED)]
            shared_counter = 0
            for k in sharing:
                r[k] = (r[k][TUPLE_NUM_ENTITIES], world.CHUNK_SHARED_OFFSET)
                shared_counter += 1
            saveBlockStats('region', r.get_coords(), block_aggregation)

        except KeyboardInterrupt:
            print "\nInterrupted by user\n"
            # TODO this should't exit
            sys.exit(1)

        r.chunk_count = chunk_count
        r.corrupted_chunks = corrupted
        r.wrong_located_chunks = wrong
        r.entities_prob = entities_prob
        r.shared_offset = shared_counter
        r.scan_time = time.time()
        r.status = world.REGION_OK
        r.block_aggregation = block_aggregation
        r.containers = containers
        return r 

        # Fatal exceptions:
    except:
        # anything else is a ChildProcessException
        except_type, except_class, tb = sys.exc_info()
        r = (r.path, r.coords, (except_type, except_class, traceback.extract_tb(tb)))
        return r
    finally:
        if cnx:
            cnx.close()
            cnx = None

def multithread_scan_regionfile(region_file):
    """ Does the multithread stuff for scan_region_file """
    r = region_file
    o = multithread_scan_regionfile.options

    # call the normal scan_region_file with this parameters
    r = scan_region_file(r,o)

    # exceptions will be handled in scan_region_file which is in the
    # single thread land
    multithread_scan_regionfile.q.put(r)



def scan_chunk(region_file, coords, global_coords, options, block_aggregation, containers):
    """ Takes a RegionFile obj and the local coordinatesof the chunk as
        inputs, then scans the chunk and returns all the data."""
    try:
        chunk_block_aggregation = [0] * 4096
        chunk = region_file.get_chunk(*coords)
        data_coords = world.get_chunk_data_coords(chunk)
        num_entities = len(chunk["Level"]["Entities"])
        if data_coords != global_coords:
            status = world.CHUNK_WRONG_LOCATED
            status_text = "Mismatched coordinates (wrong located chunk)."
            scan_time = time.time()
        elif num_entities > options.entity_limit:
            status = world.CHUNK_TOO_MANY_ENTITIES
            status_text = "The chunks has too many entities (it has {0}, and it's more than the limit {1})".format(num_entities, options.entity_limit)
            scan_time = time.time()
        else:
            status = world.CHUNK_OK
            status_text = "OK"
            scan_time = time.time()
            # Grab our chunk info
            real_chunk = nbt_chunk.Chunk(chunk)
            # Let's just parse NBT chunk sections to get accurate block counts
            chunk_sections = real_chunk.chunk_data['Sections']
            parsed_sections = [0] * 16
            for section in chunk_sections:
                blocksBytes = section['Blocks'].value
                if isinstance(blocksBytes, (bytearray, array.array)):
                    blocks = blocksBytes
                else:
                    continue  # Assume AIR for all blocks in section
                parsed_sections[section['Y'].value] = 1
                for i, block_id in enumerate(blocks):
                    chunk_block_aggregation[block_id] += 1
                    block_aggregation[block_id] += 1
            for was_parsed in parsed_sections:
                if was_parsed:
                    continue
                # Chunk section was AIR, y16*z16*x16 = 4096 blocks
                chunk_block_aggregation[0] += 4096
                block_aggregation[0] += 4096
            real_chunk_data = real_chunk.chunk_data
            if findTag(real_chunk_data, 'Entities'):
                for entity in findTag(real_chunk_data, 'Entities').tags:
                    container_contents = logContainer(entity)
                    if container_contents:
                        containers.append(container_contents)
            if findTag(real_chunk_data, 'TileEntities'):
                for entity in findTag(real_chunk_data, 'TileEntities').tags:
                    container_contents = logContainer(entity)
                    if container_contents:
                        containers.append(container_contents)
            saveBlockStats('chunk', global_coords, chunk_block_aggregation)

    except region.InconceivedChunk as e:
        chunk = None
        data_coords = None
        num_entities = None
        status = world.CHUNK_NOT_CREATED
        status_text = "The chunk doesn't exist"
        scan_time = time.time()

    except region.RegionHeaderError as e:
        error = "Region header error: " + e.msg
        status = world.CHUNK_CORRUPTED
        status_text = error
        scan_time = time.time()
        chunk = None
        data_coords = None
        global_coords = world.get_global_chunk_coords(split(region_file.filename)[1], coords[0], coords[1])
        num_entities = None

    except region.ChunkDataError as e:
        error = "Chunk data error: " + e.msg
        status = world.CHUNK_CORRUPTED
        status_text = error
        scan_time = time.time()
        chunk = None
        data_coords = None
        global_coords = world.get_global_chunk_coords(split(region_file.filename)[1], coords[0], coords[1])
        num_entities = None

    except region.ChunkHeaderError as e:
        error = "Chunk herader error: " + e.msg
        status = world.CHUNK_CORRUPTED
        status_text = error
        scan_time = time.time()
        chunk = None
        data_coords = None
        global_coords = world.get_global_chunk_coords(split(region_file.filename)[1], coords[0], coords[1])
        num_entities = None

    return chunk, (num_entities, status) if status != world.CHUNK_NOT_CREATED else None

#~ TUPLE_COORDS = 0
#~ TUPLE_DATA_COORDS = 0
#~ TUPLE_GLOBAL_COORDS = 2
TUPLE_NUM_ENTITIES = 0
TUPLE_STATUS = 1

#~ def scan_and_fill_chunk(region_file, scanned_chunk_obj, options):
    #~ """ Takes a RegionFile obj and a ScannedChunk obj as inputs,
        #~ scans the chunk, fills the ScannedChunk obj and returns the chunk
        #~ as a NBT object."""
#~
    #~ c = scanned_chunk_obj
    #~ chunk, region_file, c.h_coords, c.d_coords, c.g_coords, c.num_entities, c.status, c.status_text, c.scan_time, c.region_path = scan_chunk(region_file, c.h_coords, options)
    #~ return chunk

def _mp_pool_init(regionset,options,q):
    """ Function to initialize the multiprocessing in scan_regionset.
    Is used to pass values to the child process. """
    multithread_scan_regionfile.regionset = regionset
    multithread_scan_regionfile.q = q
    multithread_scan_regionfile.options = options


def scan_regionset(regionset, options):
    """ This function scans all te region files in a regionset object
    and fills the ScannedRegionFile obj with the results
    """

    total_regions = len(regionset.regions)
    total_chunks = 0
    corrupted_total = 0
    wrong_total = 0
    entities_total = 0
    too_small_total = 0
    unreadable = 0

    # init progress bar
    if not options.verbose:
        pbar = progressbar.ProgressBar(
            widgets=['Scanning: ', FractionWidget(), ' ', progressbar.Percentage(), ' ', progressbar.Bar(left='[',right=']'), ' ', progressbar.ETA()],
            maxval=total_regions)

    # queue used by processes to pass finished stuff
    q = queues.SimpleQueue()
    pool = multiprocessing.Pool(processes=options.processes,
            initializer=_mp_pool_init,initargs=(regionset,options,q))

    if not options.verbose:
        pbar.start()

    # start the pool
    # Note to self: every child process has his own memory space,
    # that means every obj recived by them will be a copy of the
    # main obj
    result = pool.map_async(multithread_scan_regionfile, regionset.list_regions(None), max(1,total_regions//options.processes))

    # printing status
    region_counter = 0
    total_block_aggregation = [0] * 4096
    container_log_file = open('containers.txt', 'w')

    while not result.ready() or not q.empty():
        time.sleep(0.01)
        if not q.empty():
            r = q.get()
            if r == None: # something went wrong scanning this region file
                          # probably a bug... don't know if it's a good
                          # idea to skip it
                continue
            if not isinstance(r,world.ScannedRegionFile):
                raise ChildProcessException(r)
            else:
                corrupted, wrong, entities_prob, shared_offset, num_chunks = r.get_counters()
                filename = r.filename

                block_aggregation, containers = r.get_info_containers()
                for block_id, count in enumerate(block_aggregation):
                    total_block_aggregation[block_id] += count
                for line in containers:
                    container_log_file.write(line)

                # the obj returned is a copy, overwrite it in regionset
                regionset[r.get_coords()] = r
                corrupted_total += corrupted
                wrong_total += wrong
                total_chunks += num_chunks
                entities_total += entities_prob
                if r.status == world.REGION_TOO_SMALL:
                    too_small_total += 1
                elif r.status == world.REGION_UNREADABLE:
                    unreadable += 1
                region_counter += 1
                if options.verbose:
                  if r.status == world.REGION_OK:
                    stats = "(c: {0}, w: {1}, tme: {2}, so: {3}, t: {4})".format( corrupted, wrong, entities_prob, shared_offset, num_chunks)
                  elif r.status == world.REGION_TOO_SMALL:
                    stats = "(Error: not a region file)"
                  elif r.status == world.REGION_UNREADABLE:
                    stats = "(Error: unreadable region file)"
                  print "Scanned {0: <12} {1:.<43} {2}/{3}".format(filename, stats, region_counter, total_regions)
                else:
                    pbar.update(region_counter)
    container_log_file.close()

    # saveBlockStats('world', (0, 0), total_block_aggregation)
    for block_id, count in enumerate(total_block_aggregation):
        if count:
            if block_id in BLOCK_MAP:
                print '{0}: {1}'.format(BLOCK_MAP[block_id], count)
            else:
                print '{0}: {1}'.format(block_id, count)
    if not options.verbose: pbar.finish()

    regionset.scanned = True
