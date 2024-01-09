#!/usr/bin/env python3


import argparse
import glob
import io
import os
import platform
import subprocess
import sys
import tempfile

from vendor.ninja_syntax import Writer


try:
    import json5
    del json5
except ModuleNotFoundError:
    raise SystemExit("Error: pyjson5 not found. Please install it with `python -m pip install json5`")

if sys.version_info < (3, 10):
    raise SystemExit("Error: Python 3.10 or newer is required")

if platform.python_implementation() == "PyPy":
    print("Warning: PyPy may be slower, due to spawning many Python processes")

our_argv = []
ninja_argv = []
found_seperator = False
for arg in sys.argv[1:]:
    if found_seperator:
        ninja_argv.append(arg)
    elif arg == "--":
        found_seperator = True
    else:
        our_argv.append(arg)

parser = argparse.ArgumentParser()
parser.add_argument("--dry", action="store_true")
parser.add_argument("--ci", action="store_true")
args = parser.parse_args(our_argv)

out_buf = io.StringIO()
n = Writer(out_buf)

n.variable('ninja_required_version', '1.3')
n.newline()

n.variable('builddir', 'build')
n.variable('outdir', 'out')
n.newline()

n.variable('merge', os.path.join('.', 'merge.py'))
n.variable('wuj5', os.path.join('vendor', 'wuj5', 'wuj5.py'))
n.newline()

n.rule(
    'merge',
    command = f'{sys.executable} $merge $in -o $out',
    description = 'MERGE $out',
)
n.newline()

n.rule(
    'wuj5',
    command = f'{sys.executable} $wuj5 encode $in -o $out',
    description = 'WUJ5 $out',
)
n.newline()

n.rule(
    'cp',
    command = 'cp $in $out',
    description = 'CP $out',
)
n.newline()

n.rule(
    'arc',
    command = f'{sys.executable} $wuj5 encode $arcin -o $out --retained $in $args',
    description = 'ARC $out',
)
n.newline()

thumbnail_in_files = sorted(glob.glob("thumbnails/*.jpg"))
for in_file in thumbnail_in_files:
    out_file = os.path.join('$builddir', 'contents.arc.d', in_file)
    n.build(
        out_file,
        'cp',
        in_file,
    )

LANGUAGES = [
    'E', # English (PAL)
    'F', # French (PAL)
    'G', # German
    'I', # Italian
    'J', # Japanese
    'K', # Korean
    'M', # Spanish (NTSC)
    'Q', # French (NTSC)
    'S', # Spanish (PAL)
    'U', # English (NTSC)
    'N', # Dutch
]
HUD_LANGUAGES = {
    'E': 'E',
    'F': 'F',
    'G': 'G',
    'I': 'I',
    'J': 'E',
    'K': 'E',
    'M': 'S',
    'Q': 'F',
    'S': 'S',
    'U': 'E',
    'N': 'N',
}

asset_in_files = {}
asset_out_files = {target: [] for target in asset_in_files}
for target in asset_in_files:
    for in_file in asset_in_files[target]:
        base, ext = os.path.splitext(in_file)
        outext = {
            '.bin': '.bin',
            '.breff': '.breff',
            '.breft': '.breft',
            '.brfna': '.brfna',
            '.brfnt': '.brfnt',
            '.brlyt': '.brlyt',
            '.brres': '.brres',
            '.json5': '',
            '.tpl': '.tpl',
        }[ext]
        out_file = os.path.join('$builddir', 'Shared.arc.lzma.d', base + outext)
        basebase, baseext = os.path.splitext(base)
        out_files = [out_file for out_files in asset_out_files.values() for out_file in out_files]
        if baseext == '.bmg':
            merged_file = os.path.join('$builddir', 'merged', in_file)
            if out_file not in out_files:
                n.build(
                    merged_file,
                    'merge',
                    [
                        os.path.join('assets', in_file),
                        os.path.join('assets', basebase.rsplit('_', 1)[0] + 'SP_U.bmg.json5'),
                        os.path.join('assets', basebase.replace('_', 'SP_') + '.bmg.json5'),
                    ],
                    implicit = '$merge',
                )
                in_file = merged_file
        else:
            in_file = os.path.join('assets', in_file)
        if out_file not in out_files:
            rule = {
                '.bin': 'cp',
                '.breff': 'cp',
                '.breft': 'cp',
                '.brfna': 'cp',
                '.brfnt': 'cp',
                '.brlyt': 'cp',
                '.brres': 'cp',
                '.json5': 'wuj5',
                '.tpl': 'cp',
            }[ext]
            n.build(
                out_file,
                rule,
                in_file,
            )
        asset_out_files[target] += [out_file]
n.newline()

renamed = {}
for language in LANGUAGES:
    renamed[f'jugemu_lap_{language}.brres'] = 'jugemu_lap.brres'
    renamed[f'jugemu_lapf_{language}.brres'] = 'jugemu_lapf.brres'
    renamed[f'Common_{language}.bmg'] = 'Common.bmg'
    renamed[f'Menu_{language}.bmg'] = 'Menu.bmg'
    renamed[f'Race_{language}.bmg'] = 'Race.bmg'
for hud_language in HUD_LANGUAGES.values():
    renamed[f'tt_lap_{hud_language}.tpl'] = 'tt_lap_E.tpl'
    renamed[f'tt_lap_{hud_language}_lap1.tpl'] = 'tt_lap_E_Lap1.tpl'
    renamed[f'tt_lap_{hud_language}_lap2.tpl'] = 'tt_lap_E_lap2.tpl'
    renamed[f'tt_lap_{hud_language}_lap3.tpl'] = 'tt_lap_E_lap3.tpl'
    renamed[f'tt_speed_{hud_language}.tpl'] = 'tt_speed.tpl'
    renamed[f'tt_time_{hud_language}.tpl'] = 'tt_time_E.tpl'
    for i in range(12):
        for base in ['tt_position_no_st_64x64', 'tt_multi_position_no_st_64x64']:
            renamed[f'{base}_{hud_language}_{i + 1:02d}.tpl'] = f'{base}_{i + 1:02d}.tpl'
for target in asset_out_files:
    target_renamed = {}
    for out_file in asset_out_files[target]:
        out_file = os.path.basename(out_file)
        if out_file in renamed:
            target_renamed[out_file] = renamed[out_file]
    target_renamed = ' '.join([f'--renamed {src} {dst}' for src, dst in target_renamed.items()])
    n.build(
        os.path.join('$builddir', 'contents.arc.d', target),
        'arc',
        asset_out_files[target],
        variables = {
            'arcin': os.path.join('$builddir', 'Shared.arc.lzma.d'),
            'args': target_renamed,
        },
    )
    n.newline()

devkitppc = os.environ.get("DEVKITPPC")
if not devkitppc:
    raise SystemExit("DEVKITPPC environment variable not set")

n.variable('write', os.path.join('tools', 'write.py'))
n.variable('gcc', os.path.join(devkitppc, 'bin', 'powerpc-eabi-gcc'))
n.variable('compiler', os.path.join(devkitppc, 'bin', 'powerpc-eabi-gcc'))
n.variable('postprocess', 'postprocess.py')
n.variable('port', 'port.py')
n.variable('generate_symbol_map', 'generate_symbol_map.py')
n.variable('lzmac', 'lzmac.py')
n.variable('version', 'version.py')
n.variable('elf2dol', 'elf2dol.py')
n.newline()

n.rule(
    'write',
    command = f'{sys.executable} $write "$content" $out',
    description = 'WRITE $out',
)

common_Sflags = [
    '-isystem', 'include',
    '-isystem', 'payload',
    '-isystem', 'vendor',
]
profile_Sflags = {
    'DEBUG': [
        '-DSP_DEBUG'
    ],
    'TEST': [
        '-DSP_TEST'
    ],
    'RELEASE': [
        '-DSP_RELEASE'
    ],
    'CHANNEL': [
        '-DSP_CHANNEL'
    ],
}
common_cflags = [
    '-DREVOLUTION',
    '-ffp-contract=off',
    '-fms-extensions',
    '-fno-asynchronous-unwind-tables',
    '-fshort-wchar',
    '-isystem', '.',
    '-isystem', 'include',
    '-isystem', 'payload',
    '-isystem', 'vendor',
    '-isystem', 'build',
    '-msdata=none',
    '-Wall',
    '-Wextra',
    '-Wno-packed-bitfield-compat',
]
common_ccflags = [
    '-DREVOLUTION',
    '-ffp-contract=off',
    '-fno-asynchronous-unwind-tables',
    '-fno-exceptions',
    '-fno-rtti',
    '-fshort-wchar',
    '-isystem', '.',
    '-isystem', 'include',
    '-isystem', 'payload',
    '-isystem', 'vendor',
    '-isystem', 'build',
    '-msdata=none',
    '-std=c++23',
    '-Wall',
    '-Wextra',
    '-Wno-delete-non-virtual-dtor',
    '-Wno-packed-bitfield-compat',
    '-Wsuggest-override',
]

if args.ci:
    common_ccflags.append("-Werror")
    common_cflags.append("-Werror")
else:
    common_ccflags.append("-Werror=vla")
    common_cflags.extend((
        '-Werror=implicit-function-declaration',
        '-Werror=incompatible-pointer-types',
        '-Werror=vla',
    ))

target_cflags = {
    'stub': [
        '-DSP_STUB',
    ],
    'loader': [
        '-DSP_LOADER',
    ],
    'payload': [
        '-DSP_PAYLOAD',
    ],
}
profile_cflags = {
    'DEBUG': [
        '-O0',
        '-g',
        '-DSP_DEBUG'
    ],
    'TEST': [
        '-O2',
        '-DSP_TEST'
    ],
    'RELEASE': [
        '-O2',
        '-DSP_RELEASE'
    ],
    'CHANNEL': [
        '-O2',
        '-DSP_CHANNEL'
    ],
}
common_ldflags = [
    '-nostdlib',
    '-Wl,-n',
]
if args.ci:
    common_ldflags.append('-Wl,--fatal-warnings')

n.rule(
    'S',
    command = '$gcc -MD -MT $out -MF $out.d $Sflags -c $in -o $out',
    depfile = '$out.d',
    deps = 'gcc',
    description = 'S $out',
)
n.newline()

n.rule(
    'incbin',
    command = '$gcc -DNAME=$name -DPATH=$path -c Incbin.S -o $out',
    description = 'INCBIN $out',
)
n.newline()

n.rule(
    'c',
    command = '$compiler -MD -MT $out -MF $out.d $cflags -c $in -o $out',
    depfile = '$out.d',
    deps = 'gcc',
    description = 'C $out',
)
n.newline()

n.rule(
    'cc',
    command = '$compiler -MD -MT $out -MF $out.d $ccflags -c $in -o $out',
    depfile = '$out.d',
    deps = 'gcc',
    description = 'CC $out',
)
n.newline()

n.rule(
    'postprocess',
    command = f'{sys.executable} $postprocess $region $in $out',
    description = 'POSTPROCESS $out'
)
n.newline()

n.rule(
    'port',
    command = f'{sys.executable} $port $region $in $out',
    description = 'PORT $out'
)
n.newline()

n.rule(
    'ld',
    command = '$gcc $ldflags $in -o $out',
    description = 'LD $out',
)
n.newline()

n.rule(
    'generate_symbol_map',
    command = f'{sys.executable} $generate_symbol_map $in $out',
    description = 'SMAP $out',
)
n.newline()

n.rule(
    'lzmac',
    command = f'{sys.executable} $lzmac $in $out',
    description = 'LZMA $out',
)
n.newline()

n.rule(
    'version',
    command = f'{sys.executable} $version $type $out',
    description = 'VERSION $out',
)
n.newline()

n.rule(
    'elf2dol',
    command = f'{sys.executable} $elf2dol $in $out',
    description = 'DOL $out',
)
n.newline()

code_in_files = {
    'payload': [
        os.path.join('common', 'Console.cc'),
        os.path.join('common', 'DCache.cc'),
        os.path.join('common', 'Font.c'),
        os.path.join('common', 'Font.cc'),
        os.path.join('common', 'VI.cc'),
        os.path.join('vendor', 'lzma', 'LzmaDec.c'),
        *sorted(glob.glob("payload/**/*.cc", recursive=True)),
        *sorted(glob.glob("payload/**/*.c", recursive=True)),
        *sorted(glob.glob("payload/**/*.S", recursive=True)),
    ],
    'loader': [
        os.path.join('common', 'Clock.cc'),
        os.path.join('common', 'Console.cc'),
        os.path.join('common', 'DCache.cc'),
        os.path.join('common', 'Font.c'),
        os.path.join('common', 'Font.cc'),
        os.path.join('common', 'FS.cc'),
        os.path.join('common', 'ICache.cc'),
        os.path.join('common', 'IOS.cc'),
        os.path.join('common', 'Memcmp.c'),
        os.path.join('common', 'Memcpy.c'),
        os.path.join('common', 'Memset.c'),
        os.path.join('common', 'Strlcpy.c'),
        os.path.join('common', 'Strlen.c'),
        os.path.join('common', 'VI.cc'),
        os.path.join('vendor', 'sha1', 'sha1.c'),
        *sorted(glob.glob("loader/**/*.cc", recursive=True)),
        *sorted(glob.glob("loader/**/*.c", recursive=True)),
        *sorted(glob.glob("loader/**/*.S", recursive=True)),
    ],
    'stub': [
        os.path.join('common', 'Clock.cc'),
        os.path.join('common', 'Console.cc'),
        os.path.join('common', 'DCache.cc'),
        os.path.join('common', 'Font.c'),
        os.path.join('common', 'Font.cc'),
        os.path.join('common', 'FS.cc'),
        os.path.join('common', 'ICache.cc'),
        os.path.join('common', 'IOS.cc'),
        os.path.join('common', 'Memcpy.c'),
        os.path.join('common', 'Memset.c'),
        os.path.join('common', 'Strlcpy.c'),
        os.path.join('common', 'Strlen.c'),
        os.path.join('common', 'VI.cc'),
        os.path.join('vendor', 'lzma', 'LzmaDec.c'),
        *sorted(glob.glob("stub/**/*.cc", recursive=True)),
        *sorted(glob.glob("stub/**/*.c", recursive=True)),
        *sorted(glob.glob("stub/**/*.S", recursive=True)),
    ],
}
code_out_files = {}
for profile in ['DEBUG', 'TEST', 'RELEASE', 'CHANNEL']:
    code_out_files[profile] = {target: [] for target in code_in_files}

for target in code_in_files:
    for in_file in code_in_files[target]:
        _, ext = os.path.splitext(in_file)
        for profile in ['DEBUG', 'TEST', 'RELEASE', 'CHANNEL']:
            if target == 'stub':
                suffix = profile[0] + '.o'
            elif profile == 'TEST' or profile == 'CHANNEL':
                continue
            else:
                suffix = '.o' if profile == 'RELEASE' else 'D.o'
            out_file = os.path.join('$builddir', target, in_file + suffix)
            code_out_files[profile][target] += [out_file]
            n.build(
                out_file,
                ext[1:],
                in_file,
                variables = {
                    'Sflags': ' '.join([
                        *common_Sflags,
                        *profile_Sflags[profile],
                    ]),
                    'cflags': ' '.join([
                        *common_cflags,
                        *target_cflags[target],
                        *profile_cflags[profile],
                    ]),
                    'ccflags': ' '.join([
                        *common_ccflags,
                        *target_cflags[target],
                        *profile_cflags[profile],
                    ]),
                },
            )
        n.newline()

for profile in ['DEBUG', 'RELEASE']:
    suffix = 'D' if profile == 'DEBUG' else ''
    n.build(
        os.path.join('$builddir', 'bin', f'payload{suffix}.o'),
        'ld',
        code_out_files[profile]['payload'],
        variables = {
            'ldflags': ' '.join([
                *common_ldflags,
                '-r',
            ]),
        },
    )
    n.newline()

for profile in ['DEBUG', 'RELEASE']:
    suffix = 'D' if profile == 'DEBUG' else ''
    n.build(
        [
            os.path.join('$builddir', 'bin', f'symbols{suffix}.txt'),
            os.path.join('$builddir', 'bin', f'Replacements{suffix}.c'),
        ],
        'postprocess',
        [
            os.path.join('$builddir', 'bin', f'payload{suffix}.o'),
            'symbols.txt',
        ],
        implicit = '$postprocess',
    )
    n.newline()

for region in ['P', 'E', 'J', 'K']:
    for profile in ['DEBUG', 'RELEASE']:
        suffix = 'D' if profile == 'DEBUG' else ''
        n.build(
            os.path.join('$builddir', 'scripts', f'RMC{region}{suffix}.ld'),
            'port',
            os.path.join('$builddir', 'bin', f'symbols{suffix}.txt'),
            variables = {
                'region': region,
            },
            implicit = '$port',
        )
        n.newline()

for profile in ['DEBUG', 'RELEASE']:
    suffix = 'D' if profile == 'DEBUG' else ''
    n.build(
        os.path.join('$builddir', 'bin', f'Replacements.c{suffix}.o'),
        'c',
        os.path.join('$builddir', 'bin', f'Replacements{suffix}.c'),
        variables = {
            'cflags': ' '.join([
                *common_cflags,
                *profile_cflags[profile],
            ]),
        },
    )
    n.newline()

for region in ['P', 'E', 'J', 'K']:
    for fmt in ['binary', 'elf32-powerpc']:
        for profile in ['DEBUG', 'RELEASE']:
            suffix = 'D' if profile == 'DEBUG' else ''
            extension = 'bin' if fmt == 'binary' else 'elf'
            base = {
                'P': '0x8076F000',
                'E': '0x8076A000',
                'J': '0x8076E000',
                'K': '0x8075D000',
            }[region]
            n.build(
                os.path.join('$builddir', 'bin', f'payload{region}{suffix}.{extension}'),
                'ld',
                [
                    os.path.join('$builddir', 'bin', f'payload{suffix}.o'),
                    os.path.join('$builddir', 'bin', f'Replacements.c{suffix}.o'),
                ],
                variables = {
                    'ldflags' : ' '.join([
                        *common_ldflags,
                        f'-Wl,--defsym,base={base}',
                        '-Wl,--entry=Payload_Run',
                        f'-Wl,--oformat,{fmt}',
                        '-Wl,-T,' + os.path.join('$builddir', 'scripts', f'RMC{region}{suffix}.ld'),
                    ]),
                },
                implicit = os.path.join('$builddir', 'scripts', f'RMC{region}{suffix}.ld'),
            )
            n.newline()

for region in ['P', 'E', 'J', 'K']:
    for profile in ['DEBUG', 'RELEASE']:
        suffix = 'D' if profile == 'DEBUG' else ''
        out_file = os.path.join('$builddir', 'loader', f'payload{region}{suffix}.o')
        n.build(
            out_file,
            'incbin',
            os.path.join('$builddir', 'bin', f'payload{region}{suffix}.bin'),
            variables = {
                'name': f'payload{region}',
                'path': '/'.join(['$builddir', 'bin', f'payload{region}{suffix}.bin']),
            },
            implicit = 'Incbin.S',
        )
        code_out_files[profile]['loader'] += [out_file]
n.newline()

loader_base = 0x80b00000

for fmt in ['binary', 'elf32-powerpc']:
    for profile in ['DEBUG', 'RELEASE']:
        suffix = 'D' if profile == 'DEBUG' else ''
        extension = 'bin' if fmt == 'binary' else 'elf'
        n.build(
            os.path.join('$builddir', 'bin', f'loader{suffix}.{extension}'),
            'ld',
            code_out_files[profile]['loader'],
            variables = {
                'ldflags' : ' '.join([
                    *common_ldflags,
                    f'-Wl,--defsym,base={loader_base}',
                    '-Wl,--entry=start',
                    f'-Wl,--oformat,{fmt}',
                    '-Wl,-T,' + os.path.join('common', 'RMC.ld'),
                ]),
            },
            implicit = os.path.join('common', 'RMC.ld'),
        )
        n.newline()

for region in ['P', 'E', 'J', 'K']:
    for profile in ['DEBUG', 'RELEASE']:
        suffix = 'D' if profile == 'DEBUG' else ''
        in_file = os.path.join('$builddir', 'bin', f'payload{region}{suffix}.elf')
        out_file = os.path.join('$builddir', 'bin', f'payload{region}{suffix}.SMAP')
        n.build(
            out_file,
            'generate_symbol_map',
            in_file,
        )
        n.newline()

for region in ['P', 'E', 'J', 'K']:
    for profile in ['DEBUG', 'RELEASE']:
        suffix = 'D' if profile == 'DEBUG' else ''
        in_file = os.path.join('$builddir', 'bin', f'payload{region}{suffix}.SMAP')
        out_file = os.path.join(
            '$builddir',
            'contents.arc.d',
            'bin',
            f'payload{region}{suffix}.SMAP.lzma'
        )
        n.build(
            out_file,
            'lzmac',
            in_file,
        )
        n.newline()

for profile in ['DEBUG', 'RELEASE']:
    suffix = 'D' if profile == 'DEBUG' else ''
    n.build(
        os.path.join('$builddir', 'contents.arc.d', 'bin', f'loader{suffix}.bin.lzma'),
        'lzmac',
        os.path.join('$builddir', 'bin', f'loader{suffix}.bin'),
    )

for profile in ['DEBUG', 'TEST', 'RELEASE']:
    suffix = profile[0]
    n.build(
        os.path.join('$builddir', 'contents.arc.d', 'bin', f'version{suffix}.bin'),
        'version',
        '$version',
        variables = {
            'type': profile.lower(),
        },
    )

n.build(
    os.path.join('$builddir', 'contents.arc.d', 'banner.bin'),
    'cp',
    'banner.bin',
)

n.build(
    os.path.join('$builddir', 'contents.arc.d', 'channel', 'opening.bnr.lzma'),
    'lzmac',
    'opening.bnr',
)

n.build(
    os.path.join('$builddir', 'bin', 'stubC.elf'),
    'ld',
    code_out_files['CHANNEL']['stub'],
    variables = {
        'ldflags' : ' '.join([
            *common_ldflags,
            '-Wl,--defsym,base=0x80100000',
            '-Wl,--entry=start',
            '-Wl,-T,' + os.path.join('common', 'RMC.ld'),
        ]),
    },
    implicit = os.path.join('common', 'RMC.ld'),
)
n.newline()

n.build(
    os.path.join('$builddir', 'bin', 'stubC.dol'),
    'elf2dol',
    os.path.join('$builddir', 'bin', 'stubC.elf'),
    implicit = '$elf2dol',
)
n.newline()

n.build(
    os.path.join('$builddir', 'contents.arc.d', 'channel', 'boot.dol.lzma'),
    'lzmac',
    os.path.join('$builddir', 'bin', 'stubC.dol'),
)
n.newline()

for profile in ['DEBUG', 'TEST', 'RELEASE']:
    in_suffix = 'D' if profile == 'DEBUG' else ''
    out_suffix = profile[0]
    in_paths = [
        *[os.path.join('$builddir', 'contents.arc.d', target) for target in thumbnail_in_files],
        *[os.path.join('$builddir', 'contents.arc.d', target) for target in asset_out_files],
        os.path.join('$builddir', 'contents.arc.d', 'bin', f'payloadP{in_suffix}.SMAP.lzma'),
        os.path.join('$builddir', 'contents.arc.d', 'bin', f'payloadE{in_suffix}.SMAP.lzma'),
        os.path.join('$builddir', 'contents.arc.d', 'bin', f'payloadJ{in_suffix}.SMAP.lzma'),
        os.path.join('$builddir', 'contents.arc.d', 'bin', f'payloadK{in_suffix}.SMAP.lzma'),
        os.path.join('$builddir', 'contents.arc.d', 'bin', f'loader{in_suffix}.bin.lzma'),
        os.path.join('$builddir', 'contents.arc.d', 'bin', f'version{out_suffix}.bin'),
        os.path.join('$builddir', 'contents.arc.d', 'banner.bin'),
    ]
    for region in ['P', 'E', 'J', 'K']:
        in_paths += [os.path.join(
            '$builddir',
            'contents.arc.d',
            'bin',
            f'payload{region}{in_suffix}.SMAP.lzma',
        )]
    if profile == 'RELEASE':
        in_paths += [
            os.path.join('$builddir', 'contents.arc.d', 'channel', 'opening.bnr.lzma'),
            os.path.join('$builddir', 'contents.arc.d', 'channel', 'boot.dol.lzma'),
        ]
    n.build(
        os.path.join('$builddir', f'contents{out_suffix}.arc'),
        'arc',
        in_paths,
        variables = {
            'arcin': os.path.join('$builddir', 'contents.arc.d'),
            'args': ' '.join([
                '--renamed payloadPD.SMAP.lzma payloadP.SMAP.lzma',
                '--renamed payloadED.SMAP.lzma payloadE.SMAP.lzma',
                '--renamed payloadJD.SMAP.lzma payloadJ.SMAP.lzma',
                '--renamed payloadKD.SMAP.lzma payloadK.SMAP.lzma',
                '--renamed loaderD.bin.lzma loader.bin.lzma',
                '--renamed versionD.bin version.bin',
                '--renamed versionT.bin version.bin',
                '--renamed versionR.bin version.bin',
            ]),
        },
    )

for profile in ['DEBUG', 'TEST', 'RELEASE']:
    suffix = profile[0]
    out_file = os.path.join('$builddir', 'stub', f'contents{suffix}.o')
    n.build(
        out_file,
        'incbin',
        os.path.join('$builddir', f'contents{suffix}.arc'),
        variables = {
            'name': 'embeddedContents',
            'path': '/'.join(['$builddir', f'contents{suffix}.arc']),
        },
        implicit = 'Incbin.S',
    )
    code_out_files[profile]['stub'] += [out_file]

for profile in ['DEBUG', 'TEST', 'RELEASE']:
    suffix = profile[0]
    n.build(
        os.path.join('$builddir', 'bin', f'stub{suffix}.elf'),
        'ld',
        code_out_files[profile]['stub'],
        variables = {
            'ldflags' : ' '.join([
                *common_ldflags,
                '-Wl,--defsym,base=0x80100000',
                '-Wl,--entry=start',
                '-Wl,-T,' + os.path.join('common', 'RMC.ld'),
            ]),
        },
        implicit = os.path.join('common', 'RMC.ld'),
    )
    n.newline()

for profile in ['DEBUG', 'TEST', 'RELEASE']:
    suffix = profile[0]
    n.build(
        os.path.join('$outdir', profile.lower(), 'boot.dol'),
        'elf2dol',
        os.path.join('$builddir', 'bin', f'stub{suffix}.elf'),
        implicit = '$elf2dol',
    )
n.newline()

for profile in ['DEBUG', 'TEST', 'RELEASE']:
    n.build(
        os.path.join('$outdir', profile.lower(), 'meta.xml'),
        'cp',
        os.path.join('meta', profile.lower() + '.xml'),
    )
n.newline()

for profile in ['DEBUG', 'TEST', 'RELEASE']:
    in_suffix = 'D' if profile == 'DEBUG' else ''
    out_suffix = profile[0]
    n.build(
        profile.lower(),
        'phony',
        [
            os.path.join('$builddir', 'bin', f'payloadP{in_suffix}.elf'),
            os.path.join('$builddir', 'bin', f'payloadE{in_suffix}.elf'),
            os.path.join('$builddir', 'bin', f'payloadJ{in_suffix}.elf'),
            os.path.join('$builddir', 'bin', f'payloadK{in_suffix}.elf'),
            os.path.join('$builddir', 'bin', f'loader{in_suffix}.elf'),
            os.path.join('$outdir', profile.lower(), 'boot.dol'),
            os.path.join('$outdir', profile.lower(), 'meta.xml'),
        ]
    )
n.newline()

n.build(
    'all',
    'phony',
    [
        'debug',
        'test',
        'release',
    ],
)
n.newline()
n.default(["test"])

if args.dry:
    with open('build.ninja', 'w') as out_file:
        out_file.write(out_buf.getvalue())

    raise SystemExit

out_file = tempfile.NamedTemporaryFile("w+", delete=False)
out_file.write(out_buf.getvalue())
out_file.close()
n.close()

try:
    proc = subprocess.run(("ninja", "-f", out_file.name, *ninja_argv))
except KeyboardInterrupt:
    returncode = 130 # 128 + SIGINT
else:
    returncode = proc.returncode

os.remove(out_file.name)
sys.exit(returncode)
