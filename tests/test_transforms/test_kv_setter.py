"""Test the comp_kv_setter."""
import pytest

from hammeraddons.bsp_transform import Context
from . import blank_ctx, get_transform_func, TransFunc


@pytest.fixture(scope='module')
def function() -> TransFunc:
    """Get the transform function"""
    return get_transform_func('comp_kv_setter', 'comp_kv_setter')


async def test_basic_kv(blank_ctx: Context, function: TransFunc) -> None:
    """Test basic keyvalues."""
    vmf = blank_ctx.vmf
    target = vmf.create_ent('info_target', targetname='an_ent')
    vmf.create_ent(
        'comp_kv_setter',
        target='an_ent',
        mode='kv',
        kv_name='some_keyvalue',
        kv_value_global='482',
    )
    await function(blank_ctx)
    assert not vmf.by_class['comp_kv_setter']  # Is removed from the map.
    assert target['some_keyvalue'] == '482'


async def test_basic_flags(blank_ctx: Context, function: TransFunc) -> None:
    """Test basic flags."""
    vmf = blank_ctx.vmf
    target = vmf.create_ent('ambient_generic', targetname='snd_music', spawnflags=32)

    # 1 sets it, do it twice to ensure it's idempotent.
    for i in range(2):
        vmf.create_ent(
            'comp_kv_setter',
            target='snd_music',
            mode='flags',
            kv_name='16',
            kv_value_local='1',
        )
        await function(blank_ctx)
        assert not vmf.by_class['comp_kv_setter']  # Is removed from the map.

        assert target['spawnflags'] == '48'

    # Zero unsets it!
    for i in range(2):
        vmf.create_ent(
            'comp_kv_setter',
            target='snd_music',
            mode='flags',
            kv_name='16',
            kv_value_local='0',
        )
        await function(blank_ctx)
        assert not vmf.by_class['comp_kv_setter']  # Is removed from the map.
        assert target['spawnflags'] == '32'
